import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

def format_chainage(chainage):
    """Function to format chainage as CHX+XXX."""
    if chainage.isdigit():
        chainage = int(chainage)
        return f"CH{chainage // 1000}+{chainage % 1000:03d}"
    return ""

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

# MACHINERY Selection
st.markdown("**MACHINERY**")
machinery_types = []
if st.checkbox("Excavator"):
    machinery_types.append("Excavator - 1")

# EQUIPMENT Selection
st.markdown("**EQUIPMENT**")
equipment_list = []
if st.checkbox("Genset"):
    equipment_list.append("Genset - 1")
if st.checkbox("Butt Fusion Welding Machine"):
    equipment_list.append("Butt Fusion Welding Machine - 1")

# PIPE LAYING TEAM
st.markdown("**PIPE LAYING TEAM**")
team_members = []
if st.checkbox("Supervisor"):
    team_members.append("Supervisor - 1")
if st.checkbox("Excavator Operator"):
    team_members.append("Excavator Operator - 1")
if st.checkbox("General Worker"):
    workers = st.number_input("Enter number of General Workers", min_value=1, step=1)
    team_members.append(f"General Worker - {workers}")

# MATERIALS DELIVERED
st.markdown("**MATERIALS DELIVERED TO SITE**")
materials = []
if st.checkbox("Pipe"):
    pipe_size = st.selectbox("Select Pipe Size", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])
    pipe_length = st.number_input("Enter number of lengths", min_value=1, step=1)
    materials.append(f"{pipe_size} - {pipe_length} lengths")
if st.checkbox("Valves & Fittings"):
    materials.append("Valves & Fittings")

# Activity Carried Out
st.markdown("**ACTIVITY CARRIED OUT**")
activity_list = []
if st.checkbox("Pipe Laying"):
    start_chainage = st.text_input("Starting Chainage (Insert number)")
    end_chainage = st.text_input("Ending Chainage (Insert number)")
    if start_chainage and end_chainage:
        chainage_length = f"({int(end_chainage) - int(start_chainage)}m)"
        activity_list.append(f"{len(activity_list)+1}. Pipe Laying \n- {pipe_size} pipe laying works from CH{start_chainage}+{end_chainage} {chainage_length}")

if st.checkbox("Pipe Jointing"):
    joint_count = st.number_input("Number of Joints", min_value=0, step=1)
    jointing_chainage = st.text_input("Jointing Chainage (Insert number)")
    if joint_count > 0 and jointing_chainage:
        activity_list.append(f"{len(activity_list)+1}. Pipe Jointing \n- {joint_count} nos joints ({pipe_size}) // E-CH{jointing_chainage}")

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
    
    if machinery_types:
        report += "**MACHINERY**\n" + "\n".join(machinery_types) + "\n\n"
    
    if equipment_list:
        report += "**EQUIPMENT**\n" + "\n".join(equipment_list) + "\n\n"
    
    if team_members:
        report += "**PIPE LAYING TEAM**\n" + "\n".join(team_members) + "\n\n"
    
    if materials:
        output += "\n**MATERIALS DELIVERED TO SITE**\n" + "\n".join(materials) + "\n"
    
    if activity_list:
        output += "\n**ACTIVITY CARRIED OUT**\n" + "\n".join(activity_list) + "\n"
    
    output += "\n**REMARKS**\n"
    output += f"{remarks}\n"
    
    st.text_area("Generated Report:", output, height=300)
