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
team_routes = {}
team_activities = {}
team_machinery = {}
team_equip = {}
team_manpower = {}
team_working_hours = {}
team_delivery = {}
pipe_count = 0

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

    # WORKING HOURS
    team_working_hours[team] = working_hours
    
    # PIPE SIZE
    pipe_size = st.selectbox(f"PIPE SIZE:", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"], key=f"pipe_{team}")

    # ROUTE
    route = st.text_input("ROUTE:", key=f"route_{team}")
    route = route.upper()
    if team and route:
        team_routes[team] = route
        
    # ACTIVITY
    activity_list = st.multiselect("ACTIVITY CARRIED OUT:", ["Pipe Jointing", "Pipe Laying", "Road Reinstatement"], key=f"activity_{team}")
    team_activities[team] = ", ".join(activity_list)

    # PIPE JOINTING
    ("**PIPE JOINTING:**") if "Pipe Jointing" in activity_list else ""
    joints = st.number_input ("JOINT(S):", step=1, key=f"joint_{team}") if "Pipe Jointing" in activity_list else ""

    # PIPE LAYING
    ("**PIPE LAYING:**") if "Pipe Laying" in activity_list else ""
    laidstartch_raw = st.number_input("STARTING CHAINAGE:", step=1, key=f"laidstartch_{team}") if "Pipe Laying" in activity_list else ""
    laidendch_raw = st.number_input("ENDING CHAINAGE:", step=1, key=f"laidendch_{team}") if "Pipe Laying" in activity_list else ""
    laidstartch = format_chainage(laidstartch_raw) if laidstartch_raw else ""
    laidendch = format_chainage(laidendch_raw) if laidendch_raw else ""
    laidch_diff = ""
    if laidstartch_raw and laidendch_raw:
        try:
            laidch_diff = f"{int(laidendch_raw) - int(laidstartch_raw)} m"
        except ValueError:
            laidch_diff = "Invalid"

    # ROAD REINSTATEMENT
    ("**ROAD REINSTATEMENT:**") if "Road Reinstatement" in activity_list else ""
    rrstartch_raw = st.number_input("STARTING CHAINAGE:", step=1, key=f"rrstartch_{team}") if "Road Reinstatement" in activity_list else ""
    rrendch_raw = st.number_input("ENDING CHAINAGE:", step=1, key=f"rrendch_{team}") if "Road Reinstatement" in activity_list else ""
    rrstartch = format_chainage(rrstartch_raw) if rrstartch_raw else ""
    rrendch = format_chainage(rrendch_raw) if rrendch_raw else ""
    rrch_diff = ""
    if rrstartch_raw and rrendch_raw:
        try:
            rrch_diff = f"{int(rrendch_raw) - int(rrstartch_raw)} m"
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
    st.markdown("**VALVES & FITTINGS:**")
    selected_fittings = st.multiselect(f"SELECT FITTING(S):",list(fittings.keys()), key=f"fittings_{team}")
    selected_data = {}
    if selected_fittings:
        for fitting in selected_fittings:
            selected_sizes = st.multiselect(f"SELECT SIZE FOR {fitting}:", fittings[fitting], key=f"fittingssize_{team}_{fitting}")
            if selected_sizes:
                selected_data[fitting] = {}  # Store sizes and quantities
                for size in selected_sizes:
                    quantity = st.number_input(f"ENTER QUANTITY FOR {fitting} {size}:", min_value=0, step=1, key=f"fittingsnos_{team}_{fitting}_{size}")
                    if quantity > 0:
                        selected_data[fitting][size] = quantity

    # DELIVERY
    st.markdown("**MATERIALS DELIVERED TO SITE:**")
    delivery = st.checkbox("Pipe", key=f"delivery_{team}")
    if delivery:
        pipe_count = st.number_input(f"TOTAL NUMBER DELIVERED for {team}", min_value=0, step=1, key=f"pipe_count_{team}")
        delroute = st.text_input(f"ROUTE for {team}:", key=f"delroute_{team}")
        delroute = validate_text_input(delroute)
    
    # REMARKS
    remarks = st.text_input("REMARKS:", key=f"remarks{team}")

    # APPEND DATE
    data.append([
    team,
    pipe_size,
    joints,
    laidstartch,
    laidendch,
    laidch_diff,
    ",".join(selected_fittings),
    remarks
    ])

# CONVERT TO DATAFRAME
df = pd.DataFrame(data, columns= ["Team", "Pipe Size", "Joint(s)", "Laid Start", "Laid End", "Laid Length (m)", "Fitting(s)", "Remarks"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True, disabled=True)

# GENERATE REPORT
if st.button("Generate Report"):
    pmnt_report = ""
    jbalb_report = ""

    for _, row in edited_df.iterrows():
        laid_text = f"{row['Laid Start']} to {row['Laid End']} ({row['Laid Length (m)']})" if row["Laid Start"] or row["Laid End"] or row["Laid Length (m)"] else ""
        del_text = f"{row['Pipe Size']} - {row[pipe_count]} lengths" if pipe_count else ""
        weather_text = f"{weather_am}" if weather_am == weather_pm else f"WEATHER = {weather_am} (am) / {weather_pm} (pm)"
        pmnt_report += (
            f"> {row['Team']} (ROUTE {team_routes.get(row['Team'])})\n"
            f"PIPE = {row['Pipe Size']}\n"
            f"DATE = {formatted_date}\n"
            f"WORK ACTIVITY = {team_activities.get(row['Team'])}\n"
            f"HOURS WORKING = {team_working_hours.get(row['Team'])}\n"
            f"MANPOWER = {team_manpower.get(row['Team'], {}).get('total people', 0)}\n"
            f"JOINT = {row['Joint(s)']}\n"
            f"LAID = {laid_text}\n"
            f"FITTING = {row['Fitting(s)']}\n"
            f"DELIVERY = {del_text}\n"
            f"WEATHER = {weather_text}\n"
            f"REMARKS = {row['Remarks']}\n\n"
        )
    
    jbalb_report += (
        f"Date: {formatted_date}\n"
        f"Morning: {weather_am}\n"
        f"Afternoon: {weather_pm}\n"
        f"Total Working Hours: {working_hours} hrs\n"
        f"{working_time}\n\n"
    )

    st.subheader("PMNT REPORT")
    st.text(pmnt_report)
    st.subheader("JBALB REPORT")
    st.text(jbalb_report)
