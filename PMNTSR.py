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
team_jroutes = {}
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

    # JOINTS
    ("**PIPE JOINTING**") if "Pipe Jointing" in activity_list else ""
    #jroute = st.text_input("Route", key=f"jroute_{team}") if "Pipe Jointing" in activity_list else ""
    #jroute = validate_text_input(jroute)
    #if team and jroute:
    #    team_jroutes[team] = jroute
    joints = st.number_input("Joint", step=1, key=f"joint_{team}") if "Pipe Jointing" in activity_list else ""

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

    
    # DELIVERY
    st.markdown("**MATERIALS DELIVERED TO SITE**")
    delivery = st.checkbox("Pipe", key=f"del_checkbox_{team}")
    if delivery:
        pipe_count = st.number_input(f"Total Number Delivered", min_value=0, step=1, key=f"pipe_count_{team}")
        del_chainage = st.text_input(f"Chainage", key=f"chainage_{team}")
        chainage = format_chainage(del_chainage) if del_chainage else ""
        total_pipe_length += pipe_count

        if team not in team_deliveries:
            team_deliveries[team] = []
        team_deliveries[team].append({"count": pipe_count, "route": lroute, "chainage": chainage})

    # REMARKS
    remarks = st.text_input("Remarks", key=f"remarks_{team}")

    # APPEND DATA FOR EACH TEAM
    data.append([
        team,
        pipe_size,
        joints,
        start_ch,
        end_ch,
        ch_diff,
        ", ".join(fittings),
        pipe_count,
        remarks
    ])

# CONVERT TO DATAFRAME
df = pd.DataFrame(data, columns=["Team", "Pipe Size", "Joint", "Laid Start", "Laid End", "Laid Length(m)", "Fitting","Delivery","Remarks"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True)

# GENERATE REPORT
if st.button("Generate Report"):
    
    pmnt_report = ""
    manpower_summary = {"Supervisor": 0, "Excavator Operator": 0, "General Worker": 0}
    material_summary = {}
    machinery_summary = {"Excavator": 0}
    equipment_summary = {}


    for _, row in edited_df.iterrows():
        #jroute_text = team_jroutes.get(row["Team"], "")
        #if row["Joint"]:
        #    joint_text = f"JOINT = {row['Joint']} // ROUTE {jroute_text}"
        #else:
        #    joint_text = "JOINT = "
        lroute_text = team_lroutes.get(row["Team"], "")
        laid_text = f"LAID = {lroute_text}-{row['Laid Start']} to {row['Laid End']} ({row['Laid Length(m)']})" if row["Laid Start"] or row["Laid End"] or row["Laid Length(m)"] else "LAID = "
        weather_text = f"WEATHER = {weather_am}" if weather_am == weather_pm else f"WEATHER = {weather_am} (am) / {weather_pm} (pm)"
        total_people = team_manpower.get(row["Team"], {}).get("total", 0)

        # MANPOWER SUMMARY
        for role in team_manpower.get(row["Team"], {}).get("members", []):
            if "Supervisor" in role:
                manpower_summary["Supervisor"] += 1
            elif "Excavator Operator" in role:
                manpower_summary["Excavator Operator"] += 1
            elif "General Worker" in role:
                count = int(re.search(r'\d+', role).group()) if re.search(r'\d+', role) else 1
                manpower_summary["General Worker"] += count

        # Machinery
        if st.session_state.get(f"excavator_{team}"):
            machinery_summary["Excavator"] += 1

    # Equipment
        if st.session_state.get(f"genset_{team}"):
            equipment_summary["Genset"] = equipment_summary.get("Genset", 0) + 1
        if st.session_state.get(f"welding_{team}"):
            equipment_summary["Butt Fusion Welding Machine"] = equipment_summary.get("Butt Fusion Welding Machine", 0) + 1

        
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
            #f"{joint_text}\n"
            f"JOINT = {row['Joint']}\n"
            f"{laid_text}\n"
            f"FITTING = {row['Fitting']}\n"
            f"{delivery_text}\n"
            f"{weather_text}\n"
            f"REMARKS = {row['Remarks']}\n"
            "\n"
        )
        
    jbalb_report = (
        f"Date: {formatted_date}\n"
        f"Morning: {weather_am}\n"  
        f"Afternoon: {weather_pm}\n"
        f"Total Working Hours: {working_hours} hrs\n"   
        f"{working_time}\n\n"
        f"*MACHINERY:*\n"
        f"Excavator - {machinery_summary['Excavator']}\n\n"        
        f"*EQUIPMENT:*\n"
        f"Genset - {equipment_summary.get['Genset']}\n"
        f"Welding Machine - {equipment_summary.get['Butt Fusion Welding Machine']}\n\n"
        f"*PIPE LAYING TEAM:*\n"
        f"Supervisor - {manpower_summary['Supervisor']}\n"
        f"Excavator Operator - {manpower_summary['Excavator Operator']}\n"
        f"General Workers - {manpower_summary['General Worker']}\n\n"
        f"*MATERIAL DELIVERED TO SITE:*\n"
    )

    for material, count in material_summary.items():
        jbalb_report += f"- {material}: {count} lengths\n"

    jbalb_report += "\n*ACTIVITY CARRIED OUT:*\n"
    
    if any(row["Joint"] for _, row in edited_df.iterrows()):
        jbalb_report += "Pipe Jointing\n"
        for _, row in edited_df.iterrows():
            if row["Joint"]:
                jbalb_report += f"> {row['Team']}\n- {row['Joint']} nos joints ({row['Pipe Size']})\n"

    if any(row["Laid Length(m)"] for _, row in edited_df.iterrows()):
        jbalb_report += "Pipe Laying\n"
        for _, row in edited_df.iterrows():
            if row["Laid Length(m)"]:
                jbalb_report += f"> {row['Team']}\n- ({row['Pipe Size']}) {row['Laid Start']} to {row['Laid End']} ({row['Laid Length(m)']})\n"

    st.subheader("Generated PMNT Report")
    st.text(pmnt_report)
    st.subheader("Generated JBALB Report")
    st.text(jbalb_report)
