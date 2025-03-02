import streamlit as st
import pandas as pd
from datetime import datetime, time
import re

def format_chainage (value):
    try:
        value = int(value)
        return f"CH{value // 1000}+{value % 1000:03d}"
    except ValueError:
        return ""

def validate_text_input(input_value):
    return re.sub(r'[A-Za-z\s]','', input_value).upper()

st.set_page_config(page_title="PMNT Site Diary", page_icon="🛠️")
st.title("PMNT Site Diary")

# DATA STORAGE
data = []
team_activities = {}

# TEAM SELECTION
teams = st.multiselect("TEAM(S):", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE SELECTION
date_selected = st.date_input("DATE:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# WEATHER SELECTION
weather_am = st.selectbox ("MORNING WEATHER:", ["Fine", "Rainy"])
weather_pm = st.selectbox ("AFTERNOON WEATHER:", ["Fine", "Rainy"])

# WORKING HOURS
start_time = st.time_input("START TIME:", time(8,0))
end_time = st.time_input("END TIME:", time(17,0))
working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')} hrs"

# LOOP THRU EACH TEAM
for team in teams:
    st.subheader(f"{team}")

    # PIPE SIZE
    pipe_size = st.selectbox(f"PIPE SIZE:", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"], key=f"pipe_{team}")

    # ROUTE
    route = st.text_input("ROUTE:", key=f"route_{team}")
    route = validate_text_input(route)
        
    # ACTIVITY
    activity_list = st.multiselect("ACTIVITY CARRIED OUT:", ["Pipe Jointing", "Pipe Laying", "Road Reinstatement"], key=f"activity_{team}")
    team_activities[team] = ", ".join(activity_list)

    # JOINTS
    ("**PIPE JOINTING**") if "Pipe Jointing" in activity_list else ""
    joints = st.number_input ("JOINT(S):", step=1, key=f"joint_{team}") if "Pipe Jointing" in activity_list else ""
    
