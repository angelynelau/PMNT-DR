import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

# TEAM Selection (Choose One)
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("DATE:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Morning & Afternoon Weather Selection
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Cloudy", "Drizzling", "Rainy"])

# Working Hours: Select Start and End Time using Time Input
start_time = st.time_input("Start Time:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("End Time:", datetime.strptime("17:00", "%H:%M").time())

# Calculate Total Working Hours (in hours) with 1-hour break
total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

# Machinery Selection
st.markdown("**Machinery**")
machinery_options = {"Excavator": 0, "Piling Rigs": 0, "Crane": 0}
for role in machinery_options.keys():
    if st.checkbox(machine):
        if role == "General Worker":
            machinery_options[machine] = st.number_input(f"Enter number for {machine}", min_value=1, step=1)
        else:
            machinery_options[machine] = 1


# Equipment Selection
st.markdown("**EQUIPMENT**")
equipment_selected = []
equipment_options = ["Genset", "Butt Fusion Welding Machine"]
for equipment in equipment_options:
    if st.checkbox(equipment):
        equipment_selected.append(equipment)

# Pipe Laying Team
st.markdown("**PIPE LAYING TEAM**")
team_roles = {"Supervisor": 0, "Excavator Operator": 0, "General Worker": 0}
for role in team_roles.keys():
    if st.checkbox(role):
        if role == "General Worker":
            team_roles[role] = st.number_input(f"Enter number for {role}", min_value=1, step=1)
        else:
            team_roles[role] = 1

# Materials Delivered
st.markdown("**MATERIALS DELIVERED TO SITE**")
pipe_sizes = ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"]
pipes_delivered = {}
if st.checkbox("Pipes Delivered"):
    pipe_size_selected = st.selectbox("Select Pipe Size:", pipe_sizes)
    pipes_delivered[pipe_size_selected] = st.number_input("Enter number of lengths", min_value=1, step=1)

valves_fittings = st.checkbox("Valves & Fittings")

# Activity Carried Out
st.markdown("**ACTIVITY CARRIED OUT**")
pipe_laying = st.checkbox("Pipe Laying")
starting_chainage = ""
ending_chainage = ""
if pipe_laying:
    starting_chainage = st.number_input("Starting Chainage", min_value=0, step=1)
    ending_chainage = st.number_input("Ending Chainage", min_value=0, step=1)

pipe_jointing = st.checkbox("Pipe Jointing")
joint_count = 0
joint_route = ""
joint_chainage = ""
if pipe_jointing:
    joint_count = st.number_input("Number of Joints", min_value=1, step=1)
    joint_route = st.text_input("Insert Route")
    joint_chainage = st.number_input("Jointing Chainage", min_value=0, step=1)

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
    
    # Machinery
    if any(machinery_options.values()):
        output += "**MACHINERY**\n"
        for machine, count in machinery_options.items():
            if count > 0:
                output += f"{machine} - {count}\n"
    
    # Equipment
    if equipment_selected:
        output += "\n**EQUIPMENT**\n"
        for eq in equipment_selected:
            output += f"{eq}\n"
    
    # Pipe Laying Team
    if any(team_roles.values()):
        output += "\n**PIPE LAYING TEAM**\n"
        for role, count in team_roles.items():
            if count > 0:
                output += f"{role} - {count}\n"
    
    # Materials Delivered
    if pipes_delivered or valves_fittings:
        output += "\n**MATERIALS DELIVERED TO SITE**\n"
        for size, count in pipes_delivered.items():
            output += f"{size} - {count} lengths\n"
        if valves_fittings:
            output += "Valves & Fittings\n"
    
    # Activity Carried Out
    if pipe_laying or pipe_jointing:
        output += "\n**ACTIVITY CARRIED OUT**\n"
        if pipe_laying:
            output += f"Pipe Laying\n{pipe_size_selected} pipe laying works from CH{starting_chainage:04d} to CH{ending_chainage:04d}\n"
        if pipe_jointing:
            output += f"Pipe Jointing\n{joint_count} nos joints ({pipe_size_selected}) // {joint_route}-CH{joint_chainage:04d}\n"
    
    # Remarks
    if remarks:
        output += "\n**REMARKS**\n" + remarks + "\n"
    
    st.text_area("Generated Report:", output, height=300)
