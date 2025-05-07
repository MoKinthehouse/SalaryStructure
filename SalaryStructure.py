import streamlit as st
import pandas as pd

st.set_page_config(page_title="Doctor Visit Pricing Calculator", layout="centered")

st.title("🩺 Doctor Visit Pricing Calculator")

# Sidebar inputs
st.sidebar.header("Input Parameters")

# Experience Level
level = st.sidebar.selectbox("Select Experience Level:", ["Level A (1-3 years)", "Level B (4-6 years)", "Level C (7-10 years)"])

# Status
status = st.sidebar.radio("Select Status:", ["Exclusive", "Common"])

# Monthly Working Hours
monthly_hours = st.sidebar.number_input("Monthly Working Hours:", min_value=1, max_value=170, value=40)

# Distance from City
distance_km = st.sidebar.number_input("Distance from Main City (in km):", min_value=0, max_value=100, value=0)

# Determine Tier based on hours
if 8 <= monthly_hours <= 24:
    tier = "Part-Time Tier 1"
    rate_range = (275, 325)
elif 25 <= monthly_hours <= 49:
    tier = "Part-Time Tier 2"
    rate_range = (325, 375)
elif 50 <= monthly_hours <= 79:
    tier = "Part-Time Tier 3"
    rate_range = (375, 425)
elif 80 <= monthly_hours <= 120:
    tier = "Full-Time Tier 1"
    rate_range = (300, 350)
elif 121 <= monthly_hours <= 140:
    tier = "Full-Time Tier 2"
    rate_range = (350, 375)
elif 141 <= monthly_hours <= 170:
    tier = "Full-Time Tier 3"
    rate_range = (375, 400)
else:
    tier = "Undefined"
    rate_range = (0, 0)

# Base rate selection
if status == "Exclusive":
    base_rate = rate_range[1]  # max
elif status == "Common":
    if level.startswith("Level A"):
        base_rate = rate_range[0]  # min
    else:
        base_rate = sum(rate_range) / 2  # avg
else:
    base_rate = rate_range[0]

# Remote adjustment
if distance_km >= 21:
    remote_bonus = 0.15
else:
    remote_bonus = 0.0

# Final rate
final_rate = base_rate * (1 + remote_bonus)

# Output Section
st.header("📊 Visit Pricing Summary")
st.write(f"**Experience Level:** {level}")
st.write(f"**Status:** {status}")
st.write(f"**Monthly Hours:** {monthly_hours} hrs")
st.write(f"**Tier:** {tier}")
st.write(f"**Base Visit Rate:** {base_rate:.2f} EGP")
st.write(f"**Remote Area Bonus:** {int(remote_bonus * 100)}%")
st.success(f"**Final Visit Rate: {final_rate:.2f} EGP**")

# Export to Excel
if st.button("Export to Excel"):
    df = pd.DataFrame({
        'Experience Level': [level],
        'Status': [status],
        'Monthly Hours': [monthly_hours],
        'Tier': [tier],
        'Base Rate': [base_rate],
        'Remote Bonus %': [remote_bonus * 100],
        'Final Visit Rate': [final_rate]
    })
    df.to_excel("doctor_visit_pricing.xlsx", index=False)
    st.success("Exported as 'doctor_visit_pricing.xlsx'")

