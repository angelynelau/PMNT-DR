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
    return re.sub(r'[^A-Za-z\s]', '', input_value).upper()

st.set_page_config(page_title="PMNT Site Diary", page_icon="🛠️")
st.title("PMNT Site Diary")

# DATA STORAGE
data = []
team_activities = {}
team_working_hours = {}
team_lroutes = {}
team_manpower = {}
team_deliveries = {}  
pipe_count = 0
total_pipe_length = 0 

# TEAM SELECTION
teams = st.multiselect("TEAM(S):", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE SELECTION
date_selected = st.date_input("Date:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# WEATHER SELECTION
weather_am = st.selectbox("Morning Weather:", ["Fine", "Rainy"])
weather_pm = st.selectbox("Afternoon Weather:", ["Fine", "Rainy"])

# WORKING HOURS
start_time = st.time_input("Start Time:", time(8, 0))
end_time = st.time_input("End Time:", time(17, 0))
working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')} hrs"

# LOOP THROUGH EACH SELECTED TEAM
for team in teams:
    st.subheader(f"{team}")

    # PIPE SIZE
    pipe_size = st.selectbox(f"Pipe Size", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"], key=f"pipe_{team}")

    # ACTIVITY
    activity_list = st.multiselect("Activity Carried Out:", ["Pipe Jointing", "Pipe Laying"], key=f"activity_{team}")
    team_activities[team] = " & ".join(activity_list)

    team_working_hours[team] = working_hours

    # PIPE LAYING
    ("**PIPE LAYING**") if "Pipe Laying" in activity_list else ""
    lroute = st.text_input("Route", key=f"lroute_{team}") if "Pipe Laying" in activity_list else ""
    lroute = validate_text_input(lroute)
    if team and lroute:
        team_lroutes[team] = lroute

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
            
    # MACHINERY
    st.markdown("**MACHINERY**")
    machinery_types = []
    if st.checkbox(f"Excavator", key=f"excavator_{team}"):
        machinery_types.append("Excavator - 1")

    # EQUIPMENT
    st.markdown("**EQUIPMENT**")
    equipment_list = []
    if st.checkbox(f"Genset", key=f"genset_{team}"):
        equipment_list.append("Genset - 1")
    if st.checkbox(f"Butt Fusion Welding Machine", key=f"welding_{team}"):
        equipment_list.append("Butt Fusion Welding Machine - 1")
        
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

    team_manpower[team] = {
        "members": team_members,
        "total": total_people
    }

    # FITTINGS
    fittings = st.multiselect("Fitting(s):", ["x", "y", "z"], key=f"fittings_{team}")

    # REMARKS
    remarks = st.text_input("Remarks", key=f"remarks_{team}")

    # APPEND DATA FOR EACH TEAM
    data.append([
        team,
        pipe_size,
        start_ch,
        end_ch,
        ch_diff,
        ", ".join(fittings),
        remarks
    ])

# CONVERT TO DATAFRAME
df = pd.DataFrame(data, columns=["Team", "Pipe Size", "Laid Start", "Laid End", "Laid Length(m)", "Fitting", "Remarks"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True)

if st.button("Generate Report"):
    pmnt_report = ""

    for _, row in edited_df.iterrows():
        lroute_text = team_lroutes.get(row["Team"], "")
        laid_text = f"LAID = {lroute_text}-{row['Laid Start']} to {row['Laid End']} ({row['Laid Length(m)']})" if row["Laid Start"] or row["Laid End"] or row["Laid Length(m)"] else "LAID = "
        weather_text = f"WEATHER = {weather_am}" if weather_am == weather_pm else f"WEATHER = {weather_am} (am) / {weather_pm} (pm)"
        total_people = team_manpower.get(row["Team"], {}).get("total", 0)

        # Generate delivery text
        delivery_text = "DELIVERY = "
        if row["Team"] in team_deliveries and team_deliveries[row["Team"]]:
            deliveries = team_deliveries[row["Team"]]
            delivery_text = "DELIVERY = " + " // ".join(
                [f"{row['Pipe Size']} - {entry['count']} lengths // {entry['route']}-{entry['chainage']}" for entry in deliveries]
            )

        pmnt_report += (
            f"> {row['Team']}\n"
            f"PIPE = {row['Pipe Size']}\n"
            f"DATE = {formatted_date}\n"
            f"WORK ACTIVITY = {team_activities.get(row['Team'])}\n"
            f"HOURS WORKING = {team_working_hours.get(row['Team'])}\n"
            f"MANPOWER = {total_people}\n"
            f"JOINT = {row['Joint']}\n"
            f"{laid_text}\n"
            f"FITTING = {row['Fitting']}\n"
            f"{delivery_text}\n"
            f"{weather_text}\n"
            f"REMARKS = {row['Remarks']}\n"
            "\n"
        )

    # Generate JBALB Report
        jbalb_report = (
            f"Date: {formatted_date}\n"
            f"Morning: {weather_am}\n"  
            f"Afternoon: {weather_pm}\n"
            f"Total Working Hours: {working_hours} hrs\n"   
            f"{working_time}\n"
        )

    # Ensure both reports are displayed
        st.subheader("Generated PMNT Report")
        st.text(pmnt_report)
    
        st.subheader("Generated JBALB Report")
        st.text(jbalb_report)

