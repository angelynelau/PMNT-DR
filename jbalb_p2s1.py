import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

# TEAM Selection (Choose One)
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("DATE:", datetime.today())

# Format Date as DD/MM/YY (DAY)
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Morning & Afternoon Weather
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# Working Hours: Select Start and End Time using Time Input
start_time = st.time_input("Start Time:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("End Time:", datetime.strptime("17:00", "%H:%M").time())

# Calculate Total Working Hours (subtract 1 hour for break)
total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

# 🚜 **Machinery**
st.markdown("### Machinery (Select if Applicable)")
machinery_list = ["Excavator", "Piling Rig", "Crane"]
machinery_selected = []
machinery_numbers = {}
col1, col2 = st.columns([2, 1])
with col1: st.write("**Machinery Type**")
with col2: st.write("**Total Number**")
for machinery in machinery_list:
    with col1:
        selected = st.checkbox(f"{machinery}")
    with col2:
        if selected:
            number = st.number_input(f"Enter number for {machinery}", min_value=1, step=1, key=machinery)
            machinery_selected.append(machinery)
            machinery_numbers[machinery] = number

# 🔧 **Equipment**
st.markdown("### Equipment (Select if Applicable)")
equipment_list = ["Welding/Genset"]
equipment_selected = []
equipment_numbers = {}
col1, col2 = st.columns([2, 1])
with col1: st.write("**Equipment Type**")
with col2: st.write("**Total Number**")
for equipment in equipment_list:
    with col1:
        selected = st.checkbox(f"{equipment}")
    with col2:
        if selected:
            number = st.number_input(f"Enter number for {equipment}", min_value=1, step=1, key=equipment)
            equipment_selected.append(equipment)
            equipment_numbers[equipment] = number

# 👷 **Manpower**
st.markdown("### Manpower (Select if Applicable)")
manpower_list = ["Project Manager", "Construction Manager"]
manpower_selected = []
manpower_numbers = {}
col1, col2 = st.columns([2, 1])
with col1: st.write("**Manpower Type**")
with col2: st.write("**Total Number**")
for manpower in manpower_list:
    with col1:
        selected = st.checkbox(f"{manpower}")
    with col2:
        if selected:
            number = st.number_input(f"Enter number for {manpower}", min_value=1, step=1, key=manpower)
            manpower_selected.append(manpower)
            manpower_numbers[manpower] = number

# 🚧 **Pipe Laying Team**
st.markdown("### Pipe Laying Team (Select if Applicable)")
pipe_team_list = ["Supervisor", "Operator Excavator"]
pipe_team_selected = []
pipe_team_numbers = {}
col1, col2 = st.columns([2, 1])
with col1: st.write("**Role**")
with col2: st.write("**Total Number**")
for role in pipe_team_list:
    with col1:
        selected = st.checkbox(f"{role}")
    with col2:
        if selected:
            number = st.number_input(f"Enter number for {role}", min_value=1, step=1, key=role)
            pipe_team_selected.append(role)
            pipe_team_numbers[role] = number

# 📦 **Materials Delivered**
st.markdown("### Materials Delivered to Site")
pipe_sizes = ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"]
delivered_pipes = {}
for pipe in pipe_sizes:
    quantity = st.number_input(f"{pipe} - Number of Pipes Delivered", min_value=0, step=1, key=pipe)
    if quantity > 0:
        delivered_pipes[pipe] = quantity

# 🏗 **Activities Carried Out**
st.markdown("### Activities Carried Out")
activities = st.multiselect("Select Activities:", ["Pipe Laying", "Pipe Jointing"])

# Pipe Laying Details
pipe_laying_start = ""
pipe_laying_end = ""
if "Pipe Laying" in activities:
    start_raw = st.text_input("Pipe Laying Start Chainage (Enter as a number)")
    end_raw = st.text_input("Pipe Laying End Chainage (Enter as a number)")
    try:
        pipe_laying_start = f"CH{int(start_raw)//1000}+{int(start_raw)%1000:03d}" if start_raw else ""
        pipe_laying_end = f"CH{int(end_raw)//1000}+{int(end_raw)%1000:03d}" if end_raw else ""
    except:
        st.error("Invalid chainage format.")

# Pipe Jointing Details
joint_count = ""
joint_chainage = ""
joint_pipe_size = ""
if "Pipe Jointing" in activities:
    joint_count = st.number_input("Number of Joints", min_value=0, step=1)
    joint_pipe_size = st.selectbox("Joint Pipe Size:", pipe_sizes)
    joint_chainage_raw = st.text_input("Joint Chainage (Enter as a number)")
    try:
        joint_chainage = f"CH{int(joint_chainage_raw)//1000}+{int(joint_chainage_raw)%1000:03d}" if joint_chainage_raw else ""
    except:
        st.error("Invalid chainage format.")

# 📜 **Generate Report**
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {total_working_hours:.2f} hrs\n"
    output += f"{working_time}\n"

    # Machinery
    if machinery_selected:
        output += "\n**Machinery**\n"
        for machinery in machinery_selected:
            output += f"- {machinery} - {machinery_numbers[machinery]}\n"

    # Equipment
    if equipment_selected:
        output += "\n**Equipment**\n"
        for equipment in equipment_selected:
            output += f"- {equipment} - {equipment_numbers[equipment]}\n"

    # Manpower
    if manpower_selected:
        output += "\n**Manpower**\n"
        for manpower in manpower_selected:
            output += f"- {manpower} - {manpower_numbers[manpower]}\n"

    # Pipe Laying Team
    if pipe_team_selected:
        output += "\n**Pipe Laying Team**\n"
        for role in pipe_team_selected:
            output += f"- {role} - {pipe_team_numbers[role]}\n"

    # Materials Delivered
    if delivered_pipes:
        output += "\n**Materials Delivered**\n"
        for pipe, qty in delivered_pipes.items():
            output += f"- {pipe} - {qty} lengths\n"

    # Activities
    if "Pipe Laying" in activities:
        output += f"\nPipe Laying Works from {pipe_laying_start} to {pipe_laying_end}\n"
    if "Pipe Jointing" in activities:
        output += f"\nPipe Jointing: {joint_count} joints ({joint_pipe_size}) // {joint_chainage}\n"

    st.text_area("Generated Report:", output, height=300)