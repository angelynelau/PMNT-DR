import streamlit as st
import urllib.parse
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

# Materials Delivered
st.markdown("**MATERIALS DELIVERED TO SITE**")
materials = []
pipe_entries = []
total_pipe_length = 0
delivery_entries = []  # Fixing the undefined variable issue

if st.checkbox("Pipe"):
    num_entries = st.number_input("Number of Pipe Entries", min_value=1, step=1, value=1)
    for i in range(num_entries):
        pipe_count = st.number_input(f"Pipe Count (Entry {i+1})", min_value=0, step=1, key=f"pipe_count_{i}")
        route = st.text_input(f"Route (Entry {i+1})", key=f"route_{i}")
        chainage_input = st.text_input(f"Chainage (Entry {i+1})", key=f"chainage_{i}")
        chainage = format_chainage(chainage_input) if chainage_input else ""
        total_pipe_length += pipe_count
        
        if pipe_count > 0 and route and chainage:
            pipe_entries.append(f"- {pipe_count} lengths // {route} {chainage}")
            delivery_entries.append(f"- {pipe_count} lengths // {route} {chainage}")

    if pipe_entries:
        materials.append(f"{len(pipe_size)+1}\n" + "\n".join(pipe_entries))
    else:
        materials.append(f"{len(pipe_size)+1}\n- {total_pipe_length} lengths")

if st.checkbox("Valves & Fittings"):
    materials.append(f"{len(materials)+1}. Valves & Fittings")

# ACTIVITY CARRIED OUT
st.markdown("**ACTIVITY CARRIED OUT**")
activity_list = []
activity_names = []

if st.checkbox("Pipe Laying"):
    start_chainage = st.text_input("Starting Chainage", "")
    end_chainage = st.text_input("Ending Chainage", "")
    if start_chainage and end_chainage:
        start_formatted = format_chainage(start_chainage)
        end_formatted = format_chainage(end_chainage)
        if start_formatted and end_formatted:
            chainage_length = f"({int(end_chainage) - int(start_chainage)}m)"
            activity_list.append(f"{len(activity_list)+1}. Pipe Laying \n- {pipe_size} pipe laying works from {start_formatted} to {end_formatted} {chainage_length}")
            activity_names.append("Pipe Laying")

if st.checkbox("Pipe Jointing"):
    joint_count = st.number_input("Number of Joints", min_value=0, step=1)
    joint_route = st.text_input("Insert Route")
    joint_chainage = format_chainage(st.text_input("Jointing Chainage"))
    if joint_count and joint_chainage:
        activity_list.append(f"{len(activity_list)+1}. Pipe Jointing \n- {joint_count} nos joints ({pipe_size}) // {joint_route}-{joint_chainage}")
        activity_names.append("Pipe Jointing")

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
    
    if machinery_types:
        jbalb_report += "*MACHINERY*\n" + "\n".join(machinery_types) + "\n\n"
    
    if equipment_list:
        jbalb_report += "*EQUIPMENT*\n" + "\n".join(equipment_list) + "\n\n"
    
    if team_members:
        jbalb_report += "*PIPE LAYING TEAM*\n" + "\n".join(team_members) + "\n\n"
    
    if materials:
        jbalb_report += "*MATERIALS DELIVERED TO SITE*\n" + "\n".join(materials) + "\n\n"
    
    if activity_list:
        jbalb_report += "*ACTIVITY CARRIED OUT*\n" + "\n".join(activity_list) + "\n\n"
    
    if remarks:
        jbalb_report += "*REMARKS*\n" + remarks + "\n"    



    st.text_area("JBALB Daily Report:", jbalb_report, height=300)

if 'jbalb_report' in locals() and jbalb_report:
    encoded_report = urllib.parse.quote(jbalb_report)
    whatsapp_link = f"https://wa.me/?text={encoded_report}"
    st.markdown(f"[Share JBALB Daily on WhatsApp]({whatsapp_link})", unsafe_allow_html=True)
else:
    st.warning("Generate the report first before sharing.")
