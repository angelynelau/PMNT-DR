import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

# TEAM Selection
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection
date_selected = st.date_input("DATE:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Weather Selection
morning_weather = st.selectbox("MORNING WEATHER:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])
afternoon_weather = st.selectbox("AFTERNOON WEATHER:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])

# Working Hours
start_time = st.time_input("START TIME:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("END TIME:", datetime.strptime("17:00", "%H:%M").time())
total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')}"

# Machinery Selection
st.markdown("### MACHINERY")
machinery_list = ["Excavator", "Piling Rig", "Crane"]
machinery_selected = {}
for machinery in machinery_list:
    if st.checkbox(machinery):
        machinery_selected[machinery] = st.number_input(f"Enter number for {machinery}", min_value=1, step=1, key=machinery)

# Equipment Selection
st.markdown("### EQUIPMENT")
equipment_selected = [eq for eq in ["Genset", "Butt Fusion Welding Machine"] if st.checkbox(eq)]

# Pipe Laying Team
st.markdown("### PIPE LAYING TEAM")
team_roles = {"Supervisor": None, "Excavator Operator": None, "General Worker": "general_worker"}
pipeline_team = {}
for role, key in team_roles.items():
    if st.checkbox(role):
        pipeline_team[role] = st.number_input(f"Enter number for {role}", min_value=1, step=1, key=key) if key else 1

# Materials Delivered
st.markdown("### MATERIALS DELIVERED TO SITE")
materials_selected = {}
if st.checkbox("PIPE"):
    pipe_size = st.selectbox("Select Pipe Size:", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])
    pipe_count = st.number_input("Enter number of lengths:", min_value=1, step=1, key="pipe_count")
    materials_selected[pipe_size] = pipe_count
if st.checkbox("VALVES & FITTINGS"):
    materials_selected["Valves & Fittings"] = True

# Activity Carried Out
st.markdown("### ACTIVITY CARRIED OUT")
activity_selected = []
laid_chainage = ""
joint_count = 0

if st.checkbox("PIPE LAYING"):
    start_chainage = st.number_input("Starting Chainage:", min_value=0, step=1)
    end_chainage = st.number_input("Ending Chainage:", min_value=0, step=1)
    laid_chainage = f"CH{start_chainage // 1000}+{start_chainage % 1000:03d} to CH{end_chainage // 1000}+{end_chainage % 1000:03d}"
    activity_selected.append("Pipe Laying")

if st.checkbox("PIPE JOINTING"):
    joint_count = st.number_input("Number of Joints:", min_value=1, step=1)
    activity_selected.append("Pipe Jointing")

# Remarks
remarks = st.text_area("REMARKS")

# Generate Report
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {total_working_hours:.0f} hrs\n"
    output += f"Working Time: {working_time}\n\n"
    
    if machinery_selected:
        output += "**MACHINERY**\n"
        for machinery, number in machinery_selected.items():
            output += f"- {machinery} - {number}\n"
    
    if equipment_selected:
        output += "\n**EQUIPMENT**\n" + "\n".join([f"- {eq}" for eq in equipment_selected]) + "\n"
    
    if pipeline_team:
        output += "\n**PIPE LAYING TEAM**\n"
        for role, number in pipeline_team.items():
            output += f"- {role} - {number}\n"
    
    if materials_selected:
        output += "\n**MATERIALS DELIVERED TO SITE**\n"
        for material, count in materials_selected.items():
            if isinstance(count, int):
                output += f"- {material} - {count} lengths\n"
            else:
                output += f"- {material}\n"
    
    if activity_selected:
        output += "\n**ACTIVITY CARRIED OUT**\n"
        if "Pipe Laying" in activity_selected:
            output += f"Pipe laying works from {laid_chainage}\n"
        if "Pipe Jointing" in activity_selected:
            output += f"{joint_count} nos joints\n"
    
    output += f"\n**REMARKS**\n{remarks}\n"
    
    st.text_area("Generated Report:", output, height=300)
