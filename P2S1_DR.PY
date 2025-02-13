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

# Chainage Inputs
starting_chainage = st.text_input("Starting Chainage (e.g., CH1+000)")
ending_chainage = st.text_input("Ending Chainage (e.g., CH1+500)")

# Calculate Chainage Difference (if both values are provided)
chainage_diff = ""
if starting_chainage and ending_chainage:
    try:
        start_value = int(starting_chainage.split("+")[1])
        end_value = int(ending_chainage.split("+")[1])
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
