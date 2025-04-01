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
for role in team_mp.get("Manpower", {}).get("manpower", []):
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

# DELIVERY
jb_del_text = f"*MATERIALS DELIVERED TO SITE:* \n {del_size} - {pipe_count} lengths\n\n" if pipe_count > 0 else ""

# ACTIVITY CARRIED OUT
activity_report = "*ACTIVITY CARRIED OUT:*\n"
for team in teams:
    activity_text = f"> {team} // Route {team_routes.get(team, 'N/A')}\n"
    
    # Get the joints if Pipe Jointing activity is present
    joints = 0
    if "Pipe Jointing" in team_activities.get(team, []):
        joints = st.session_state.get(f"joint_{team}", 0)  # Get the joints input for this team
    
    if joints > 0:
        activity_text += f"- {joints} nos joints\n"
    
    if "Pipe Laying" in team_activities.get(team, []):
        activity_text += f"- Pipe Laying at {laidstartch} to {laidendch}\n"
    
    fitting_list = team_fittings.get(team, "").split(", ")
    fitting_details = []
    for fitting in fitting_list:
        match = re.match(r"(.+?) \((.+?)\)", fitting)
        if match:
            fittings, chainages = match.groups()
            chainage_list = chainages.split(", ")
            if len(chainage_list) == 1:
                fitting_details.append(f"Installation of {fittings} at {chainages}")
            else:
                fitting_details.append(f"Installation of fittings at {chainages}")
        
        if fitting_details:
            for line in fitting_details:
                activity_text += f"- {line}\n"
    
    activity_report += activity_text + "\n"
    
    jbalb_report += (
        f"Date: {formatted_date}\n"
        f"Morning: {weather_am}\n"
        f"Afternoon: {weather_pm}\n"
        f"Total Working Hours: {working_hours} hrs\n"
        f"{working_time}\n\n"
        f"*MACHINERY:*\n"
        f"Excavator - {machinery_summary.get('Excavator', 0)}\n\n"
        f"*EQUIPMENT:*\n"
        f"Genset - {equipment_summary.get('Genset', 0)}\n"
        f"Butt Fusion Welding Machine - {equipment_summary.get('Butt Fusion Welding Machine', 0)}\n\n"
        f"*MANPOWER:*\n"
        f"{mp_summary_text}\n"
        f"*PIPE LAYING TEAM:*\n"
        f"Supervisor - {pipelaying_summary.get('Supervisor', 0)}\n"
        f"Excavator Operator - {pipelaying_summary.get('Excavator Operator', 0)}\n"
        f"General Workers - {pipelaying_summary.get('General Worker', 0)}\n\n"
        f"{jb_del_text}"
        f"{activity_report}\n"
    )

# Show reports
st.subheader("PMNT REPORT")
st.text(pmnt_report)
st.subheader("JBALB REPORT")
st.text(jbalb_report)
