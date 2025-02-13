import streamlit as st
from datetime import datetime

st.title("PMNT Daily Report Generator")

# TEAM Selection (Choose One)
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("DATE:", datetime.today())

# Format Date as DD/MM/YY (DAY)
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Morning Weather Selection
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# Afternoon Weather Selection
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# Working Hours: Select Start and End Time using Time Input
start_time = st.time_input("Start Time:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("End Time:", datetime.strptime("17:00", "%H:%M").time())

# Calculate Total Working Hours (in hours)
total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1

# Time Working (e.g., 0800-1700)
working_time = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

# Select Machinery (Checkbox)
machinery_list = ("Machinery:", ["Excvator", "Piling Rig", "Crane", "Cloudy"])
selected_machinery = []

for item in machinery_list:
    if st.checkbox(f"{item}"):
        number = st.number_input(f"Enter number for {item}:", min_value=0, step=1)
        selected_machinery.append(f"{item} - {number if number > 0 else 'N/A'}")

# Equipment
welding_genset = st.number_input("Welding/Genset -", min_value=0, step=1)

# Manpower
project_manager = st.number_input("Project Manager -", min_value=0, step=1)
construction_manager = st.number_input("Construction Manager -", min_value=0, step=1)

# Pipe Laying Team
supervisor = st.number_input("Supervisor -", min_value=0, step=1)
operator_excavator = st.number_input("Operator Excavator -", min_value=0, step=1)

# Materials Delivered to Site (Choose pipe size then insert number)
pipe_size = st.selectbox("Pipe Size:", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])
materials_delivered = st.number_input(f"Number of {pipe_size} pipes delivered", min_value=0, step=1)

# Activity Carried Out (Choose activity)
activity = st.multiselect("Activity Carried Out:", ["Pipe Laying", "Pipe Jointing"])

# Chainage Details (for Pipe Laying)
start_chainage_raw = st.text_input("Starting Chainage (e.g., 400)")
end_chainage_raw = st.text_input("Ending Chainage (e.g., 500)")

# Pipe Jointing Details
joint_number = st.number_input("Number of joints (size pipe)", min_value=0, step=1)
jointing_chainage = st.text_input("Jointing Chainage (e.g., CH0+900)")

# Generate Report button
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {total_working_hours:.2f} hrs\n"
    output += f"{working_time}\n"
    
    output += "**Machinery**\n"
    for item in machinery_list:
        if machinery[item] > 0:
            output += f"{item} - {machinery[item]}\n"

    output += "Equipment\n"
    output += f"Welding/Genset - {welding_genset}\n"

    output += "Manpower\n"
    output += f"Project Manager - {project_manager}\n"
    output += f"Construction Manager - {construction_manager}\n"

    output += "Pipe Laying Team\n"
    output += f"Supervisor - {supervisor}\n"
    output += f"Operator Excavator - {operator_excavator}\n"

    output += "Materials Delivered to Site:\n"
    output += f"{pipe_size} - {materials_delivered} lengths\n"

    output += "Activity Carried Out:\n"
    if "Pipe Laying" in activity:
        output += f"Pipe Laying\n"
        if start_chainage_raw and end_chainage_raw:
            output += f"Pipe laying works from {start_chainage_raw} to {end_chainage_raw}\n"
    if "Pipe Jointing" in activity:
        output += f"Pipe Jointing\n"
        if joint_number and jointing_chainage:
            output += f"{joint_number} nos joints ({pipe_size}) // {jointing_chainage}\n"

    st.text_area("Generated Report:", output, height=500)
