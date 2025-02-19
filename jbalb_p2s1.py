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
pipe_size = st.selectbox("Pipe Size:", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])

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
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')} hrs"

# MACHINERY Selection
st.markdown("**MACHINERY**")
machinery_list = []
if st.checkbox("Excavator"):
    machinery_list.append("Excavator - 1")

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
total_people = 0

if st.checkbox("Supervisor"):
    team_members.append("Supervisor - 1")
    total_people += 1
if st.checkbox("Excavator Operator"):
    team_members.append("Excavator Operator - 1")
    total_people += 1
if st.checkbox("General Worker"):
    workers = st.number_input("Enter number of General Workers", min_value=1, step=1)
    team_members.append(f"General Worker - {workers}")
    total_people += workers

# ACTIVITY CARRIED OUT
st.markdown("**ACTIVITY CARRIED OUT**")
activity_list = []

if st.checkbox("Pipe Laying"):
    start_chainage = st.text_input("Starting Chainage", "")
    end_chainage = st.text_input("Ending Chainage", "")
    if start_chainage and end_chainage:
        start_formatted = format_chainage(start_chainage)
        end_formatted = format_chainage(end_chainage)
        chainage_length = f"({int(end_chainage) - int(start_chainage)}m)"
        activity_list.append("Pipe Laying")

if st.checkbox("Pipe Jointing"):
    joint_count = st.number_input("Number of Joints", min_value=0, step=1)
    joint_route = st.text_input("Insert Route")
    joint_chainage = format_chainage(st.text_input("Jointing Chainage"))
    if joint_count and joint_chainage:
        activity_list.append("Pipe Jointing")

# REMARKS
remarks = st.text_area("REMARKS")

# GENERATE REPORT
if st.button("Generate Report"):
    # JBALB FORMAT
    jbalb_report = f"> {team}\n"
    jbalb_report += f"Date: {formatted_date}\n"
    jbalb_report += f"Morning: {morning_weather}\n"
    jbalb_report += f"Afternoon: {afternoon_weather}\n"
    jbalb_report += f"Total Working Hours: {working_hours:.2f} hrs\n"
    jbalb_report += f"{working_time}\n\n"

    if machinery_list:
        jbalb_report += "*MACHINERY*\n" + "\n".join(machinery_list) + "\n\n"

    if equipment_list:
        jbalb_report += "*EQUIPMENT*\n" + "\n".join(equipment_list) + "\n\n"

    if team_members:
        jbalb_report += "*PIPE LAYING TEAM*\n" + "\n".join(team_members) + "\n\n"

    if activity_list:
        jbalb_report += "*ACTIVITY CARRIED OUT*\n"
        if start_chainage and end_chainage:
            jbalb_report += f"- Pipe Laying {pipe_size} from {start_formatted} to {end_formatted} {chainage_length}\n"
        if joint_count:
            jbalb_report += f"- Pipe Jointing {pipe_size}, {joint_count} joints at {joint_chainage}\n"
        jbalb_report += "\n"

    if remarks:
        jbalb_report += "*REMARKS*\n" + remarks + "\n"

    # PMNT FORMAT
    pmnt_report = f"> {team}\n"
    pmnt_report += f"PIPE = {pipe_size}\n"
    pmnt_report += f"DATE = {formatted_date}\n"
    
    # Ensure proper WORK ACTIVITY format
    if activity_list:
        pmnt_report += f"WORK ACTIVITY = {pipe_size} {' & '.join(activity_list)}\n"
    else:
        pmnt_report += "WORK ACTIVITY = \n"

    pmnt_report += f"HOURS WORKING = {working_hours:.2f} hrs ({working_time})\n"
    pmnt_report += f"MANPOWER = {total_people}\n"
    pmnt_report += f"JOINT = {joint_count}\n"

    if start_chainage and end_chainage:
        pmnt_report += f"LAID = {start_chainage} to {end_chainage} {chainage_length}\n"
    else:
        pmnt_report += "LAID = \n"

    pmnt_report += "DELIVERY = " + pipe_size + "\n"

    if morning_weather == afternoon_weather:
        pmnt_report += f"WEATHER = {morning_weather}\n"
    else:
        pmnt_report += f"MORNING WEATHER AM = {morning_weather}\n"
        pmnt_report += f"AFTERNOON WEATHER PM = {afternoon_weather}\n"

    if remarks:
        pmnt_report += f"REMARKS = {remarks}\n"

    # Display Reports
    st.subheader("JBALB Format Report:")
    st.text_area("JBALB Report", jbalb_report, height=300)

    st.subheader("PMNT Format Report:")
    st.text_area("PMNT Report", pmnt_report, height=300)
