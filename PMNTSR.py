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
team_machinery = {}
team_equip = {}
team_manpower = {}

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

    # PIPE JOINTING
    ("**PIPE JOINTING:**") if "Pipe Jointing" in activity_list else ""
    joints = st.number_input ("JOINT(S):", step=1, key=f"joint_{team}") if "Pipe Jointing" in activity_list else ""

    # PIPE LAYING
    ("**PIPE LAYING:**") if "Pipe Laying" in activity_list else ""
    laidstartch_raw = st.text_input("STARTING CHAINAGE:", key=f"laidstartch_{team}") if "Pipe Laying" in activity_list else ""
    laidendch_raw = st.text_input("ENDING CHAINAGE:", key=f"laidendch_{team}") if "Pipe Laying" in activity_list else ""
    laidstartch = format_chainage(laidstartch_raw) if laidstartch_raw else ""
    laidendch = format_chainage(laidendch_raw) if laidendch_raw else ""
    laidch_diff = ""
    if laidstartch_raw and laidendch_raw:
        try:
            laidch_diff = f"{int(laidendch_raw) - int(laidstartch_raw)}m"
        except ValueError:
            laidch_diff = "Invalid"

    # ROAD REINSTATEMENT
    ("**ROAD REINSTATEMENT:**") if "Road Reinstatement" in activity_list else ""
    rrstartch_raw = st.text_input("STARTING CHAINAGE:", key=f"rrstartch_{team}") if "Road Reinstatement" in activity_list else ""
    rrendch_raw = st.text_input("ENDING CHAINAGE:", key=f"rrendch_{team}") if "Road Reinstatement" in activity_list else ""
    rrstartch = format_chainage(rrstartch_raw) if rrstartch_raw else ""
    rrendch = format_chainage(rrendch_raw) if rrendch_raw else ""
    rrch_diff = ""
    if rrstartch_raw and rrendch_raw:
        try:
            rrch_diff = f"{int(rrendch_raw) - int(rrstartch_raw)}m"
        except ValueError:
            rrch_diff = "Invalid"
    
    # MACHINERY
    st.markdown("**MACHINERY:**")
    mach_list = []
    total_mach = 0
    if st.checkbox(f"Excavator", key=f"excavator_{team}"):
        mach_list.append("Excavator - 1")
        total_mach += 1
    team_machinery[team] = {
        "machinery": mach_list,
        "total machinery": total_mach
    }

    # EQUIPMENT
    st.markdown("**EQUIPMENT:**")
    equip_list = []
    total_equip = 0
    if st.checkbox(f"Genset", key=f"genset_{team}"):
        equip_list.append("Genset - 1")
        total_equip += 1
    if st.checkbox(f"Butt Fusion Welding Machine", key=f"welding_{team}"):
        equip_list.append("Butt Fusion Welding Machine - 1")
        total_equip += 1
    team_equip[team] = {
        "equipment": equip_list,
        "total equipment": total_equip
    }

    # MANPOWER
    st.markdown("**PIPE LAYING TEAM:**")
    team_members = []
    total_people = 0
    if st.checkbox(f"Supervisor", key=f"supervisor_{team}"):
        team_members.append("Supervisor - 1")
        total_people += 1
    if st.checkbox(f"Excavator Operator", key=f"excavator operator_{team}"):
        team_members.append("Excavator Operation - 1")
        total_people += 1
    if st.checkbox(f"General Worker", key=f"General Worker_{team}"):
        workers = st.number_input(f"General Worker", min_value=1, step=1, key=f"workers_{team}")
        team_members.append(f"General Worker - {workers}")
        total_people += workers
    team_manpower[team] = {
        "members": team_members,
        "total people": total_people
    }

    # FITTINGS
    fittings = {
        "Stub Tee": ["a", "b", "c", "d", "e"],
        "Tee": ["j", "k", "l"],
        "C": ["m", "n", "o"]
    }
    ("**VALVES & FITTINGS:**")
    selected_fittings = st.multiselect("SELECT FITTING(S):", list(fittings.keys()), key=f"fittings_{team}")
    selected_data = {}
    if selected_fittings:
        for fitting in selected_fittings:
            selected_sizes = st.multiselect(f"Select size for {fitting}:", fittings[fitting], key=f"fittingssize_{team}_{fitting}")
            if selected_sizes:
                selected_data[fitting] = {}  # Store sizes and quantities
                for size in selected_sizes:
                    quantity = st.number_input(f"Enter quantity for {fitting} {size}:", min_value=0, step=1, key=f"fittingsnos_{team}_{fitting}_{size}")
                    if quantity > 0:  # Only store non-zero quantities
                        selected_data[fitting][size] = quantity
