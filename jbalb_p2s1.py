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

if st.checkbox("Pipe"):
    pipe_count = st.number_input("Insert number of lengths", min_value=0, step=1)
    if pipe_count > 0:
        materials.append(f"{len(materials)+1}. {pipe_size} \n- {pipe_count} lengths")
if st.checkbox("Valves & Fittings"):
    materials.append(f"{len(materials)+1}. Valves & Fittings")
    
# ACTIVITY CARRIED OUT
st.markdown("**ACTIVITY CARRIED OUT**")
activity_list = []

if st.checkbox("Pipe Laying"):
    start_chainage = st.text_input("Starting Chainage", "")
    end_chainage = st.text_input("Ending Chainage", "")
    if start_chainage and end_chainage:
        start_formatted = format_chainage(start_chainage)
        end_formatted = format_chainage(end_chainage)
        if start_formatted and end_formatted:
            chainage_length = f"({int(end_chainage) - int(start_chainage)}m)"
            activity_list.append(f"{len(activity_list)+1}. Pipe Laying \n- {pipe_size} pipe laying works from {start_formatted} to {end_formatted} {chainage_length}")

if st.checkbox("Pipe Jointing"):
    joint_count = st.number_input("Number of Joints", min_value=1, step=1)
    joint_route = st.text_input("Insert Route")
    joint_chainage = format_chainage(st.text_input("Jointing Chainage"))
    if joint_count and joint_chainage:
        activity_list.append(f"{len(activity_list)+1}. Pipe Jointing \n- {joint_count} nos joints ({pipe_size}) // {joint_route}-{joint_chainage}")
    
# REMARKS
remarks = st.text_area("REMARKS")

# GENERATE REPORT
if st.button("Generate Report"):
    #PMNT FORMAT
    output = f"> {team}\n"
    output += f"PIPE = {pipe_size}\n"
    output += f"DATE = {formatted_date}\n"
    
    # Include work activity if any is selected
    if activity_list:
        output += f"WORK ACTIVITY = {pipe_size} {' & '.join(activity_list)}\n"
    else:
        output += "WORK ACTIVITY = \n"

    # Always include these fields
    output += f"HOURS WORKING = {working_hours}\n" if working_hours else "HOURS WORKING = \n"

    # Manpower
    if team_members:
        output += F" MANPOWER = \n".join(team_members) + f"\nTotal Manpower: {total_people}\n"
    else:
        output += "MANPOWER = \n"

    # JOINT 
    output += f"JOINT = {joint_count}\n" if joint else "JOINT = \n"

    # LAID
    output += f"LAID = {start_chainage} to {end_chainage} {chainage_length}\n" if start_chainage else "LAID = \n"

    # Only include FITTING if it's not blank
    if fitting:
        output += f"FITTING = {fitting}\n"
    else:
        output += "FITTING = \n"

    # Add DELIVERY only if it has a value
    if delivery > 0:
        output += f"DELIVERY = {pipe_size} - {delivery} lengths\n"
    else:
        output += "DELIVERY = \n"
    
    output += f"WEATHER = {weather}\n" if weather else "WEATHER = \n"
    output += f"REMARKS = {remarks}\n" if remarks else "REMARKS = \n"
    
    #JBALB P2S1 FORMAT
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {working_hours:.2f} hrs\n"
    output += f"{working_time}\n\n"
    
    if machinery_types:
        output += "*MACHINERY*\n" + "\n".join(machinery_types) + "\n\n"
    
    if equipment_list:
        output += "*EQUIPMENT*\n" + "\n".join(equipment_list) + "\n\n"
    
    if team_members:
        output += "*PIPE LAYING TEAM*\n" + "\n".join(team_members) + "\n\n"
    
    if materials:
        output += "*MATERIALS DELIVERED TO SITE*\n" + "\n".join(materials) + "\n\n"
    
    if activity_list:
        output += "*ACTIVITY CARRIED OUT*\n" + "\n".join(activity_list) + "\n\n"
    
    if remarks:
        output += "*REMARKS*\n" + remarks + "\n"    

    st.text_area("Generated Report:", output, height=300)


if 'output' in locals() and output:
    encoded_report = urllib.parse.quote(output)
    whatsapp_link = f"https://wa.me/?text={encoded_report}"
    st.markdown(f"[Share on WhatsApp]({whatsapp_link})", unsafe_allow_html=True)
else:
    st.warning("Generate the report first before sharing.")
