import streamlit as st
import pandas as pd
import openpyxl

# Set page config
st.set_page_config(page_title="Doctor Pricing Calculator", layout="centered")

st.title("🩺 Salary Structure ")

# Sidebar inputs
st.sidebar.header("Input Parameters")

# Experience level
level = st.sidebar.selectbox("Select Doctor Level:", ["A (1-3 years)", "B (4-6 years)", "C (7-10 years)"])

# Work type
work_type = st.sidebar.radio("Select Work Type:", ["Part-Time", "Full-Time"])

# Monthly working hours
monthly_hours = st.sidebar.number_input("Monthly Working Hours:", min_value=1, max_value=160, value=40)

# Distance (for remote adjustment)
distance_km = st.sidebar.number_input("Distance from Main City (in km):", min_value=0, max_value=100, value=0)

# Number of active clients
active_clients = st.sidebar.number_input("Number of Active Clients:", min_value=0, max_value=20, value=2)

# Set hourly rate based on level
hourly_rates = {"A": 200, "B": 250, "C": 300}
level_key = level[0]
hourly_rate = hourly_rates[level_key]

# Base salary calculation
base_salary = hourly_rate * monthly_hours

# Remote area adjustment (based on distance)
if distance_km >= 21:
    if distance_km < 30:
        remote_adjustment = 0.15
    elif distance_km < 40:
        remote_adjustment = 0.20
    else:
        remote_adjustment = 0.25
else:
    remote_adjustment = 0.0

# Workload adjustment
workload_adjustment = (active_clients // 2) * 0.05

# Total adjustment
total_adjustment = 1 + remote_adjustment + workload_adjustment
final_salary = base_salary * total_adjustment

# Output Section
st.header("📊 Pricing Summary")
st.write(f"**Doctor Level:** {level}")
st.write(f"**Work Type:** {work_type}")
st.write(f"**Monthly Hours:** {monthly_hours} hrs")
st.write(f"**Hourly Rate:** {hourly_rate} EGP")
st.write(f"**Base Salary:** {base_salary:,.0f} EGP")

st.subheader("💡 Adjustments")
st.write(f"**Remote Area Adjustment:** +{int(remote_adjustment * 100)}%")
st.write(f"**Workload Adjustment (Clients = {active_clients}):** +{int(workload_adjustment * 100)}%")

st.success(f"**Final Adjusted Salary: {final_salary:,.0f} EGP / month**")

# Optional: export result
if st.button("Export to Excel"):
    df = pd.DataFrame({
        'Doctor Level': [level],
        'Work Type': [work_type],
        'Monthly Hours': [monthly_hours],
        'Hourly Rate': [hourly_rate],
        'Base Salary': [base_salary],
        'Remote Adj. %': [remote_adjustment * 100],
        'Workload Adj. %': [workload_adjustment * 100],
        'Final Salary': [final_salary]
    })
    df.to_excel("doctor_pricing_output.xlsx", index=False)
    st.success("File exported as 'doctor_pricing_output.xlsx'")
