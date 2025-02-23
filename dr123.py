import datetime

def generate_report(data):
    pmnt_format = ""
    jbalb_format = ""
    record_table = []
    
    date_today = data.get("date", datetime.datetime.today().strftime('%d/%m/%y'))
    morning_weather = data.get("weather_am", "Sunny")
    afternoon_weather = data.get("weather_pm", "Sunny")
    total_hours = data.get("hours_working", 8)
    machinery = data.get("machinery", "Excavator - 2")
    equipment = data.get("equipment", "Genset - 2\nButt Fusion Welding Machine - 2")
    
    jbalb_format += f"Date: {date_today}\nMorning: {morning_weather}\nAfternoon: {afternoon_weather}\n"
    jbalb_format += f"Total Working Hours: {total_hours}.00 hrs\n0800 - 1700 hrs\n\n"
    jbalb_format += f"MACHINERY\n{machinery}\n\nEQUIPMENT\n{equipment}\n\nPIPE LAYING TEAM\n"
    
    team_summary = ""
    material_delivery = "MATERIALS DELIVERED TO SITE\n"
    activity_summary = "ACTIVITY CARRIED OUT\n"
    
    for team in data.get("teams", []):
        pipe_size = team.get("pipe_size", "400mm HDPE")
        work_activity = f"{pipe_size} Pipe Jointing & Laying"
        manpower = team.get("manpower", 5)
        joints = team.get("joints", 5)
        laid_start = team.get("laid_start", "CH1+000")
        laid_end = team.get("laid_end", "CH1+500")
        laid_length = team.get("laid_length", 500)
        fittings = ", ".join(team.get("fittings", ["TEE"]))
        delivery = f"{pipe_size} - {team.get('delivery', 23)} lengths"
        remarks = team.get("remarks", "")
        route = team.get("route", "A")
        
        pmnt_format += f">{team['name']}\nPIPE = {pipe_size}\nDATE = {date_today}\n"
        pmnt_format += f"WORK ACTIVITY = {work_activity}\nHOURS WORKING = {total_hours}\nMANPOWER = {manpower}\n"
        pmnt_format += f"JOINT = {joints}\nLAID = {laid_start} to {laid_end} ({laid_length}m)\n"
        pmnt_format += f"FITTING = {fittings}\nDELIVERY = {delivery}\n"
        pmnt_format += f"WEATHER = {morning_weather} (AM) / {afternoon_weather} (PM)\nREMARKS = {remarks}\n\n"
        
        material_delivery += f"{pipe_size}\n- {team.get('delivery', 23)} lengths (ROUTE {route})\n"
        
        activity_summary += f"1. Pipe Jointing\n> {team['name']}\n- {joints} nos joints ({pipe_size})\n"
        activity_summary += f"2. Pipe Laying\n> {team['name']}\n- ({pipe_size}) {laid_start} to {laid_end} ({laid_length}m)\n"
        
        record_table.append([date_today, f"{morning_weather}/{afternoon_weather}", team['name'], route, laid_start, laid_end, joints, laid_start, laid_end, laid_length])
    
    jbalb_format += material_delivery + "\n" + activity_summary
    
    return pmnt_format, jbalb_format, record_table

# Example Input Data
data = {
    "date": "23/02/25",
    "weather_am": "Sunny",
    "weather_pm": "Rainy",
    "hours_working": 8,
    "teams": [
        {
            "name": "TEAM A",
            "pipe_size": "400mm HDPE",
            "manpower": 5,
            "joints": 5,
            "laid_start": "CH1+000",
            "laid_end": "CH1+500",
            "laid_length": 500,
            "fittings": ["TEE", "STUB END"],
            "delivery": 23,
            "route": "A",
            "remarks": ""
        },
        {
            "name": "TEAM B",
            "pipe_size": "225mm HDPE",
            "manpower": 4,
            "joints": 9,
            "laid_start": "CH2+000",
            "laid_end": "CH3+500",
            "laid_length": 1500,
            "fittings": ["TEE"],
            "delivery": 60,
            "route": "E",
            "remarks": "Machine Breakdown"
        }
    ]
}

pmnt_report, jbalb_report, record_table = generate_report(data)

print("# PMNT FORMAT\n")
print(pmnt_report)
print("# JBALB FORMAT\n")
print(jbalb_report)
print("# RECORD TABLE\n")
print("No | Date Submit | Weather | Team | Route | Chainage From | Chainage To | No. Of Joint | Chainage From | Chainage To | Laid Length (m)")
for i, record in enumerate(record_table, 1):
    print(f"{i}. | {' | '.join(map(str, record))}")
