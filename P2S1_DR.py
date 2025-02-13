import streamlit as st
from datetime import datetime

st.title("Work Report Generator")

# TEAM Selection (Choose One)
team = st.selectbox("Select TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("Select DATE:", datetime.today())

# PIPE SIZE Selection (Choose One)
pipe_size = st.selectbox("Select PIPE SIZE:", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])

# WORK ACTIVITY (Multiple Choice)
work_activity = st.multiselect("Select WORK ACTIVITY:", ["Pipe Laying", "Pipe Jointing"])

# Numeric Inputs
hours_working = st.number_input("HOURS WORKING", min_value=0, step=1)
manpower = st.number_input("MANPOWER", min_value=0, step=1)
joint = st.number_input("JOINT", min_value=0, step=1)

# Chainage Formatting Function
def format_chainage(value):
    try:
        value = int(value)
        return f"CH{value // 1000}+{value % 1000:03d}"
    except:
        return "Invalid input"

# Chainage Inputs (Automatically Formats)
starting_chainage_raw = st.text_input("Starting Chainage (Enter as a number)")
ending_chainage_raw = st.text_input("Ending Chainage (Enter as a number)")

starting_chainage = format_chainage(starting_chainage_raw) if starting_chainage_raw else ""
ending_chainage = format_chainage(ending_chainage_raw) if ending_chainage_raw else ""

# Calculate Chainage Difference (if both values are provided)
chainage_diff = ""
if starting_chainage_raw and ending_chainage_raw:
    try:
        start_value = int(starting_chainage_raw)
        end_value = int(ending_chainage_raw)
        chainage_diff = f"({end_value - start_value}m)"
    except:
        chainage_diff = "(Invalid chainage format)"

# FITTING input
fitting = st.text_input("FITTING (Leave blank if not applicable)")

# DELIVERY input
delivery = st.number_input(f"DELIVERY ({pipe_size})", min_value=0, step=1)

# WEATHER Selection (Choose One)
weather = st.selectbox("Select WEATHER:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# REMARKS input
remarks = st.text_area("REMARKS")

# Generate report button
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"PIPE = {pipe_size}\n"
    output += f"DATE = {date_selected}\n"
    output += f"WORK ACTIVITY = {pipe_size} {' & '.join(work_activity)}\n"
    output += f"HOURS WORKING = {hours_working}\n"
    output += f"MANPOWER = {manpower}\n"
    output += f"JOINT = {joint}\n"
    output += f"LAID = {starting_chainage} to {ending_chainage} {chainage_diff}\n"
    output += f"FITTING = {fitting}\n"
    output += f"DELIVERY = {pipe_size} - {delivery} lengths\n"
    output += f"WEATHER = {weather}\n"
    output += f"REMARKS = {remarks}\n"

    st.text_area("Generated Report:", output, height=300)
