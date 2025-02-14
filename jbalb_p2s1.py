import streamlit as st
from datetime import datetime, time

def format_chainage(value):
    try:
        value = int(value)
        return f"CH{value // 1000}+{value % 1000:03d}"
    except:
        return "Invalid input"

st.title("PMNT P2S1 Site Diary")

# TEAM Selection
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection
selected_date = st.date_input("DATE:", datetime.today())
formatted_date = selected_date.strftime("%d/%m/%y (%A)")

# WEATHER Selection
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])

# WORKING HOURS
start_time = st.time_input("Start Time:", time(8, 0))
end_time = st.time_input("End Time:", time(17, 0))
working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')}"

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

# ACTIVITY CARRIED OUT
st.markdown("**ACTIVITY CARRIED OUT**")
activity_list = []
if st.checkbox("Pipe Laying"):
    start_chainage = format_chainage(st.text_input("Starting Chainage"))
    end_chainage = format_chainage(st.text_input("Ending Chainage"))
    if start_chainage and end_chainage:
        activity_list.append(f"Pipe laying works from {start_chainage} to {end_chainage}")

if st.checkbox("Pipe Jointing"):
    joint_count = st.number_input("Number of Joints", min_value=1, step=1)
    joint_pipe_size = st.selectbox("Pipe Size for Jointing", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"], key="joint_pipe_size")
    joint_route = st.text_input("Insert Route")
    joint_chainage = format_chainage(st.text_input("Jointing Chainage"))
    if joint_count and joint_chainage:
        activity_list.append(f"{joint_count} nos joints ({joint_pipe_size}) // {joint_route}-{joint_chainage}")

# REMARKS
remarks = st.text_area("REMARKS")

# GENERATE REPORT
if st.button("Generate Report"):
    report = f"> {team}\n"
    report += f"Date: {formatted_date}\n"
    report += f"Morning: {morning_weather}\n"
    report += f"Afternoon: {afternoon_weather}\n"
    report += f"Total Working Hours: {working_hours:.2f} hrs\n"
    report += f"{working_time}\n\n"
    
    if machinery_types:
        report += "**MACHINERY**\n" + "\n".join(machinery_types) + "\n\n"
    
    if equipment_list:
        report += "**EQUIPMENT**\n" + "\n".join(equipment_list) + "\n\n"
    
    if team_members:
        report += "**PIPE LAYING TEAM**\n" + "\n".join(team_members) + "\n\n"
    
    if materials:
        report += "**MATERIALS DELIVERED TO SITE**\n" + "\n".join(materials) + "\n\n"
    
    if activity_list:
        report += "**ACTIVITY CARRIED OUT**\n" + "\n".join(activity_list) + "\n\n"
    
    if remarks:
        report += "**REMARKS**\n" + remarks + "\n"
    
    st.text_area("Generated Report:", report, height=400)
