import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def generate_report(data):
    pmnt_format = ""
    jbalb_format = ""
    record_table = []
    
    date_today = data.get("date", datetime.datetime.today().strftime('%d/%m/%y'))
    morning_weather = data.get("weather_am", "Sunny")
    afternoon_weather = data.get("weather_pm", "Sunny")
    total_hours = data.get("hours_working", 8)
    
    jbalb_format += f"Date: {date_today}\nMorning: {morning_weather}\nAfternoon: {afternoon_weather}\n"
    jbalb_format += f"Total Working Hours: {total_hours}.00 hrs\n0800 - 1700 hrs\n\n"
    
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
        
        pmnt_format += f">{team['name']}\nPIPE = {pipe_size}\nDATE = {date_today}\n"
        pmnt_format += f"WORK ACTIVITY = {work_activity}\nHOURS WORKING = {total_hours}\nMANPOWER = {manpower}\n"
        pmnt_format += f"JOINT = {joints}\nLAID = {laid_start} to {laid_end} ({laid_length}m)\n"
        pmnt_format += f"FITTING = {fittings}\nDELIVERY = {delivery}\n"
        pmnt_format += f"WEATHER = {morning_weather} (AM) / {afternoon_weather} (PM)\nREMARKS = {remarks}\n\n"
        
        record_table.append([date_today, f"{morning_weather}/{afternoon_weather}", team['name'], laid_start, laid_end, joints, laid_length])
    
    return pmnt_format, jbalb_format, record_table

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            "date": request.form.get("date"),
            "weather_am": request.form.get("weather_am"),
            "weather_pm": request.form.get("weather_pm"),
            "hours_working": int(request.form.get("hours_working")),
            "teams": []
        }
        for i in range(2):  # Assume max 2 teams can be selected
            team_name = request.form.get(f"team_{i}")
            if team_name:
                data["teams"].append({
                    "name": team_name,
                    "pipe_size": request.form.get(f"pipe_size_{i}"),
                    "manpower": int(request.form.get(f"manpower_{i}")),
                    "joints": int(request.form.get(f"joints_{i}")),
                    "laid_start": request.form.get(f"laid_start_{i}"),
                    "laid_end": request.form.get(f"laid_end_{i}"),
                    "laid_length": int(request.form.get(f"laid_length_{i}")),
                    "fittings": request.form.getlist(f"fittings_{i}"),
                    "delivery": int(request.form.get(f"delivery_{i}")),
                    "remarks": request.form.get(f"remarks_{i}")
                })
        
        pmnt_report, jbalb_report, record_table = generate_report(data)
        return render_template("report.html", pmnt_report=pmnt_report, jbalb_report=jbalb_report, record_table=record_table)
    
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)
