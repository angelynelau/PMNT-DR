import streamlit as st
import pandas as pd
from datetime import datetime, time
import re  # For text validation

def format_chainage(value):
    try:
        value = int(value)
        return f"CH{value // 1000}+{value % 1000:03d}"
    except ValueError:
        return ""

def validate_text_input(input_value):
    """Allow only alphabets and spaces, remove numbers and special characters."""
    return re.sub(r'[^A-Za-z\s]', '', input_value).upper()

st.set_page_config(page_title="PMNT Site Diary", page_icon="🛠️")
st.title("PMNT Site Diary")

# TEAM SELECTION
teams = st.multiselect("TEAM(S):", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE SELECTION
date_selected = st.date_input("Date:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# WEATHER SELECTION
weather_am = st.selectbox("Morning Weather", ["Fine", "Rainy"])
weather_pm = st.selectbox("Afternoon Weather", ["Fine", "Rainy"])

# WORKING HOURS
start_time = st.time_input("Start Time:", time(8, 0))
end_time = st.time_input("End Time:", time(17, 0))
working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')} hrs"

# DATA STORAGE
data = []
team_routes = {}

# LOOP THROUGH EACH SELECTED TEAM
for team in teams:
    st.subheader(f"{team}")

    # PIPE SIZE
    pipe_size = st.selectbox(f"Pipe Size", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"], key=f"pipe_{team}")

    # ACTIVITY
    activity_list = st.multiselect("Activity Carried Out:", ["Pipe Jointing", "Pipe Laying"], key=f"activity_{team}")

    # JOINTS
    joints = st.number_input("Joint", step=1, key=f"joint_{team}") if "Pipe Jointing" in activity_list else ""

    # PIPE LAYING
    route = st.text_input("Route", key=f"route_{team}") if "Pipe Laying" in activity_list else ""
    route = validate_text_input(route)
    if team and route: 
        team_routes[team] = route
            
    start_ch_raw = st.text_input("Starting Chainage", key=f"startch_{team}") if "Pipe Laying" in activity_list else ""
    end_ch_raw = st.text_input("Ending Chainage", key=f"endch_{team}") if "Pipe Laying" in activity_list else ""

    start_ch = format_chainage(start_ch_raw) if start_ch_raw else ""
    end_ch = format_chainage(end_ch_raw) if end_ch_raw else ""

    ch_diff = ""
    if start_ch_raw and end_ch_raw:
        try:
            ch_diff = f"{int(end_ch_raw) - int(start_ch_raw)}m"
        except ValueError:
            ch_diff = "(Invalid)"

    # FITTINGS
    fittings = st.multiselect("Fitting(s):", ["x", "y", "z"], key=f"fittings_{team}")

    # MANPOWER
    st.markdown("**PIPE LAYING TEAM**")
    team_members = []
    total_people = 0

    if st.checkbox(f"Supervisor", key=f"supervisor_{team}"):
        team_members.append("Supervisor - 1")
        total_people += 1

    if st.checkbox(f"Excavator Operator", key=f"ExcavatorOperator_{team}"):
        team_members.append("Excavator Operator - 1")
        total_people += 1

    if st.checkbox(f"General Worker", key=f"General Worker_{team}"):
        workers = st.number_input(f"Enter number of General Workers ({team})", min_value=1, step=1, key=f"workers_{team}")
        team_members.append(f"General Worker - {workers}")
        total_people += workers
    
    # APPEND DATA FOR EACH TEAM
    data.append([
        team,
        pipe_size,
        " & ".join(activity_list),
        working_hours,
        joints,
        start_ch,
        end_ch,
        ch_diff,
        ", ".join(fittings),
    ])

# CONVERT TO DATAFRAME
df = pd.DataFrame(data, columns=["Team", "Pipe Size", "Activity", "Hours Working", "Joint", "Laid Start", "Laid End", "Laid Length(m)", "Fitting"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True)

# GENERATE REPORT
if st.button("Generate Report"):
    pmnt_report = ""

    for _, row in edited_df.iterrows():
        route_text = team_routes.get(row["Team"], "")
        laid_text = f"LAID = {route_text}-{row['Laid Start']} to {row['Laid End']} ({row['Laid Length(m)']})" if row["Laid Start"] or row["Laid End"] or row["Laid Length(m)"] else "LAID = "
        weather_text = f"WEATHER = {weather_am}" if weather_am == weather_pm else f"WEATHER = {weather_am} (am) / {weather_pm} (pm)"
        manpower_details = "\n".join(team_manpower.get(row["Team"], {}).get("members", []))
        total_people = team_manpower.get(row["Team"], {}).get("total", 0)
        
        pmnt_report += (
            f"> {row['Team']}\n"
            f"PIPE = {row['Pipe Size']}\n"
            f"DATE = {formatted_date}\n"
            f"WORK ACTIVITY = {row['Activity']}\n"
            f"HOURS WORKING = {row['Hours Working']}\n"
            f"MANPOWER = {total_people} people\n{manpower_details}\n"
            f"JOINT = {row['Joint']}\n"
            f"{laid_text}\n"
            f"FITTING = {row['Fitting']}\n"
            f"DELIVERY = \n"
            f"{weather_text}\n"
            f"REMARKS = \n"
            "\n"
        )

    # DISPLAY REPORT
    st.subheader("Generated PMNT Report")
    st.text(pmnt_report)
