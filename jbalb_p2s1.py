import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

# TEAM Selection (Choose One)
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("DATE:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Weather Selection
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])

# Working Hours: Select Start and End Time
start_time = st.time_input("Start Time:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("End Time:", datetime.strptime("17:00", "%H:%M").time())

total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')} hrs"

# Machinery Selection
st.markdown("**MACHINERY**")
machinery_list = ["Excavator", "Piling Rig", "Crane"]
machinery_selected = {mach: st.number_input(f"{mach} (if applicable, insert number)", min_value=0, step=1) for mach in machinery_list}

# Equipment Selection
st.markdown("**EQUIPMENT**")
equipment_list = ["Genset", "Butt Fusion Welding Machine"]
equipment_selected = [equip for equip in equipment_list if st.checkbox(equip)]

# Pipe Laying Team Selection
st.markdown("**PIPE LAYING TEAM**")
pipeline_roles = {"Supervisor": 1, "Excavator Operator": 1, "General Worker": st.number_input("General Worker (choose number)", min_value=0, step=1)}

# Materials Delivered
st.markdown("**MATERIALS DELIVERED TO SITE**")
materials = []
pipe_size = st.selectbox("Pipe Size:", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])
pipe_count = st.number_input("Insert number of lengths", min_value=0, step=1)
if pipe_count > 0:
    materials.append(f"1. {pipe_size} \n- {pipe_count} lengths")
if st.checkbox("Valves & Fittings"):
    materials.append("2. Valves & Fittings")

# Activity Carried Out
st.markdown("**ACTIVITY CARRIED OUT**")
activity_list = []
if st.checkbox("Pipe Laying"):
    start_chainage = st.text_input("Starting Chainage (Insert number)")
    end_chainage = st.text_input("Ending Chainage (Insert number)")
    if start_chainage and end_chainage:
        chainage_length = f"({int(end_chainage) - int(start_chainage)}m)"
        activity_list.append(f"1. Pipe Laying \n- {pipe_size} pipe laying works from CH{start_chainage}+{end_chainage} {chainage_length}")

if st.checkbox("Pipe Jointing"):
    joint_count = st.number_input("Number of Joints", min_value=0, step=1)
    jointing_chainage = st.text_input("Jointing Chainage (Insert number)")
    if joint_count > 0 and jointing_chainage:
        activity_list.append(f"2. Pipe Jointing \n- {joint_count} nos joints ({pipe_size}) // E-CH{jointing_chainage}")

# Remarks
remarks = st.text_area("REMARKS")

# Generate Report Button
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {total_working_hours:.2f} hrs\n"
    output += f"{working_time}\n\n"
    
    output += "**MACHINERY**\n"
    for mach, count in machinery_selected.items():
        if count > 0:
            output += f"- {mach} - {count}\n"
    
    output += "\n**EQUIPMENT**\n"
    for equip in equipment_selected:
        output += f"- {equip}\n"
    
    output += "\n**PIPE LAYING TEAM**\n"
    for role, count in pipeline_roles.items():
        if count > 0:
            output += f"- {role} - {count}\n"
    
    if materials:
        output += "\n**MATERIALS DELIVERED TO SITE**\n" + "\n".join(materials) + "\n"
    
    if activity_list:
        output += "\n**ACTIVITY CARRIED OUT**\n" + "\n".join(activity_list) + "\n"
    
    output += "\n**REMARKS**\n"
    output += f"{remarks}\n"
    
    st.text_area("Generated Report:", output, height=300)
