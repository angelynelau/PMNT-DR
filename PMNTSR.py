import streamlit as st
import pandas as pd
from datetime import datetime, time

def format_chainage(value):
    try: 
        value = int(value)
        return f"CH{value // 1000}+{value % 1000:03d}"
    except:
        return ""

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
    route = st.textinput(key=f"route_{team}) if if "Pipe Laying" in activity_list else ""
    route = validate_text_input(route).upper()
    start_ch_raw = st.text_input("Starting Chainage", key=f"startch_{team}") if "Pipe Laying" in activity_list else ""
    end_ch_raw = st.text_input("Ending Chainage", key=f"endch_{team}") if "Pipe Laying" in activity_list else ""
    
    start_ch = format_chainage(start_ch_raw) if start_ch_raw else ""
    end_ch = format_chainage(end_ch_raw) if end_ch_raw else ""
    
    ch_diff = ""
    if start_ch_raw and end_ch_raw:
        try:
            ch_diff = f"({int(end_ch_raw) - int(start_ch_raw)}m)"
        except ValueError:
            ch_diff = "(Invalid)"
    
    # FITTINGS
    fittings = st.multiselect("Fitting(s):", [" ", " ", " "], key=f"fittings_{team}")

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
df = pd.DataFrame(data, columns=["Team", "Pipe Size", "Activity", "Hours Working", "Joints", "Laid Start", "Laid End", "Laid Length(m)", "Fitting"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True)

# GENERATE REPORT
if st.button("Generate Report"):
    pmnt_report = ""

    for _, row in edited_df.iterrows():
        pmnt_report += (
            f"> {row['Team']}\n"
            f"PIPE = {row['Pipe Size']}\n"
            f"DATE = {formatted_date}\n"
            f"WORK ACTIVITY = {row['Activity']}\n"
            f"HOURS WORKING = {row['Hours Working']}\n"
            f"JOINTS = {row['Joints']}\n"
            f"LAID = {row['Laid Start']} to {row['Laid End']} {row['Laid Length(m)']}\n"
            f"FITTING = {row['Fitting']}\n"
            "\n"
        )
    
    # st.text_area("Generated Report:", pmnt_report, height=300)

# DISPLAY REPORTS
    st.subheader("Generated PMNT Report")
    st.text(pmnt_report)
