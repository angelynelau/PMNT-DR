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

st.set_page_config(page_title="Site Diary", page_icon="🛠️")
st.title("Site Diary")

# DATA STORAGE
data = []
team_routes = {}
team_activities = {}
team_machinery = {}
team_equip = {}
team_mp = {}
team_pipelaying = {}
team_working_hours = {}
team_delivery = {}
team_fittings = {}
joints = 0
stub_end_qty = 0

# TEAM SELECTION
teams = st.multiselect("TEAM(S):", ["TEAM A", "TEAM B", "TEAM C", "TEAM D"])

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

# MANPOWER
st.markdown("**MANPOWER:**")
mp_list = []
total_mp = 0
if st.checkbox(f"Project Manager"):
    mp_list.append("Project Manager - 1")
    total_mp += 1
if st.checkbox(f"Project Engineer"):
    mp_list.append("Project Engineer - 1")
    total_mp += 1
if st.checkbox(f"Site Safety Supervisor"):
    mp_list.append("Site Safety Supervisor - 1")
    total_mp += 1
team_mp["Manpower"] = {
    "manpower": mp_list,
    "total manpower": total_mp
}

# MATERIALS DELIVERED TO SITE
st.markdown("**MATERIALS DELIVERED TO SITE:**")
delivery = st.checkbox("Pipe", key="delivery_pipe")
if delivery:
    pipe_count = st.number_input("TOTAL NUMBER OF LENGTHS DELIVERED", min_value=0, step=1, key="pipe_count")
    delroute = st.text_input("ROUTE:", key="delroute")
    delroute = validate_text_input(delroute)

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
    activity_list = st.multiselect("ACTIVITY CARRIED OUT:", ["Pipe Jointing", "Pipe Laying", "Fitting(s) Installation", "Road Reinstatement"], key=f"activity_{team}")
    team_activities[team] = ", ".join(activity_list)

    # PIPE JOINTING
    ("**PIPE JOINTING:**") if "Pipe Jointing" in activity_list else ""
    joints = st.number_input("JOINT(S):", step=1, key=f"joint_{team}") if "Pipe Jointing" in activity_list else 0
    if joints > 0:
        stub_end = st.checkbox("Stub End", key=f"stub_end_{team}")
        if stub_end:
            stub_end_qty = st.number_input("Enter number of Stub End(s):", min_value=1, step=1, key=f"stub_end_qty_{team}")

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

    # FITTINGS
    ("**VALVES & FITTINGS:**") if "Fitting(s) Installation" in activity_list else ""
    selected_fittings = st.multiselect(
        "FITTING(S):", 
        ["TEE", "25mm SAV", "80mm DAV", "100mm WO", "100mm FH", "150mm SV", "200mm SV", 
         "250mm SV", "300mm SV", "350mm SV", "150mm CC", "200mm CC", "250mm CC", "300mm CC", "350mm CC"], 
        key=f"fittings_{team}" 
    ) if "Fitting(s) Installation" in activity_list else "" 
    selected_data = {}
    fitting_chainages = []
    if selected_fittings:
        for fitting in selected_fittings:
            if fitting not in selected_data:
                selected_data[fitting] = []
            quantity = st.number_input(f"ENTER QUANTITY FOR {fitting}:", min_value=0, step=1, key=f"fittingsnos_{team}_{fitting}")
            if quantity > 0:
                for i in range(quantity):
                    fitting_ch_raw = st.number_input(f"ENTER CHAINAGE FOR {fitting} (Entry {i+1}):", step=1, key=f"chainage_{team}_{fitting}_{i}")
                    fitting_ch = format_chainage(fitting_ch_raw) if fitting_ch_raw else ""
                    if fitting_ch:
                        selected_data[fitting].append(fitting_ch)
        for fitting, chainages in selected_data.items():
            fitting_chainages.append(f"{fitting} ({', '.join(chainages)})")
        team_fittings[team] = ", ".join(fitting_chainages) if fitting_chainages else ""

    # ROAD REINSTATEMENT
    ("**ROAD REINSTATEMENT:**") if "Road Reinstatement" in activity_list else ""
    rrstartch_raw = st.number_input("STARTING CHAINAGE:", step=1, key=f"rrstartch_{team}") if "Road Reinstatement" in activity_list else ""
    rrendch_raw = st.number_input("ENDING CHAINAGE:", step=1, key=f"rrendch_{team}") if "Road Reinstatement" in activity_list else ""
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

    # PIPE LAYING TEAM
    st.markdown("**PIPE LAYING TEAM:**")
    team_members = []
    total_people = 0
    if st.checkbox(f"Supervisor", key=f"supervisor_{team}"):
        team_members.append("Supervisor - 1")
        total_people += 1
    if st.checkbox(f"Excavator Operator", key=f"excavator operator_{team}"):
        team_members.append("Excavator Operator - 1")
        total_people += 1
    if st.checkbox(f"General Worker", key=f"General Worker_{team}"):
        workers = st.number_input(f"General Worker", min_value=1, step=1, key=f"workers_{team}")
        team_members.append(f"General Worker - {workers}")
        total_people += workers
    team_pipelaying[team] = {
        "members": team_members,
        "total people": total_people
    }

    # REMARKS
    remarks = st.text_input("**REMARKS:**", key=f"remarks{team}")

    # APPEND DATE
    data.append([
    team,
    pipe_size,
    joints,
    stub_end_qty,
    laidstartch,
    laidendch,
    laidch_diff,
    ",".join(selected_fittings),
    remarks
    ])

# CONVERT TO DATAFRAME
df = pd.DataFrame(data, columns= ["Team", "Pipe Size", "Joint(s)", "Stub End(s)", "Laid Start", "Laid End", "Laid Length (m)", "Fitting(s)", "Remarks"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True, disabled=True)

# GENERATE REPORT
if st.button("Generate Report"):
    pmnt_report = ""
    jbalb_report = ""

    for _, row in edited_df.iterrows():
        laid_text = f"{row['Laid Start']} to {row['Laid End']} ({row['Laid Length (m)']})" if row["Laid Start"] or row["Laid End"] or row["Laid Length (m)"] else ""
        del_text = f"{row['Pipe Size']} - {team_delivery.get(row['Team'], 0)} lengths" if team_delivery.get(row['Team'], 0) else ""
        weather_text = f"{weather_am}" if weather_am == weather_pm else f"WEATHER = {weather_am} (am) / {weather_pm} (pm)"
        fitting_text = team_fittings.get(row['Team'], "")
        pmnt_report += (
            f"> {row['Team']} (ROUTE {team_routes.get(row['Team'])})\n"
            f"PIPE = {row['Pipe Size']}\n"
            f"DATE = {formatted_date}\n"
            f"WORK ACTIVITY = {team_activities.get(row['Team'])}\n"
            f"HOURS WORKING = {team_working_hours.get(row['Team'])}\n"
            f"MANPOWER = {team_pipelaying.get(row['Team'], {}).get('total people', 0)}\n"
            f"JOINT = {row['Joint(s)']}" + (f" // Stub End(s) = {row['Stub End(s)']}" if 'Stub End(s)' in row and row['Stub End(s)'] else "") + "\n"
            f"LAID = {laid_text}\n"
            f"FITTING = {fitting_text}\n"
            f"DELIVERY = {del_text}\n"
            f"WEATHER = {weather_text}\n"
            f"REMARKS = {row['Remarks']}\n\n"
        )
    # MACHINERY SUMMARY
    machinery_summary = {"Excavator": 0}
    for team in teams:
        for machinery in team_machinery.get(team, {}).get("machinery",[]):
            if "Excavator" in machinery:
                machinery_summary["Excavator"] += 1

    # EQUIPMENT SUMMARY
    equipment_summary = {"Genset": 0, "Butt Fusion Welding Machine": 0}
    for team in teams:
        for equipment in team_equip.get(team, {}).get("equipment",[]):
            if "Genset" in equipment:
                equipment_summary["Genset"] += 1
            elif "Butt Fusion Welding Machine" in equipment:
                equipment_summary["Butt Fusion Welding Machine"] += 1

    # MANPOWER SUMMARY
    mp_summary_text = ""
    for role in team_mp["Manpower"]["manpower"]:
        mp_summary_text += f"{role}\n"
    
    # PIPE LAYING TEAM SUMMARY
    pipelaying_summary = {"Supervisor": 0, "Excavator Operator": 0, "General Worker": 0}
    for team in teams:
        for member in team_pipelaying.get(team, {}).get("members", []):
            if "Supervisor" in member:
                pipelaying_summary["Supervisor"] += 1
            elif "Excavator Operator" in member:
                pipelaying_summary["Excavator Operator"] += 1
            elif "General Worker" in member:
                count = int(re.search(r'\d+', member).group()) if re.search(r'\d+', member) else 1
                pipelaying_summary["General Worker"] += count

    jbalb_report += (
        f"Date: {formatted_date}\n"
        f"Morning: {weather_am}\n"
        f"Afternoon: {weather_pm}\n"
        f"Total Working Hours: {working_hours} hrs\n"
        f"{working_time}\n\n"
        f"*MACHINERY:*\n"
        f"Excavator - {machinery_summary['Excavator']}\n\n"
        f"*EQUIPMENT:*\n"
        f"Genset - {equipment_summary['Genset']}\n"
        f"Butt Fusion Welding Machine - {equipment_summary['Butt Fusion Welding Machine']}\n\n"
        f"*MANPOWER:*\n"
        f"{mp_summary_text}\n"
        f"*PIPE LAYING TEAM:*\n"
        f"Supervisor - {pipelaying_summary['Supervisor']}\n"
        f"Excavator Operator - {pipelaying_summary['Excavator Operator']}\n"
        f"General Workers - {pipelaying_summary['General Worker']}\n\n"
    )

    st.subheader("PMNT REPORT")
    st.text(pmnt_report)
    st.subheader("JBALB REPORT")
    st.text(jbalb_report)
