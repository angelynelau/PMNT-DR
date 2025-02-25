import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime, time

def format_chainage(value):
  try: 
    value = int(value)
    return f"CH{value // 1000}+{value % 1000:03d}"
  except:
    return "Invalid Input"

st.set_page_config(page_title="PMNT Site Diary", page_icon="🛠️")
st. title("PMNT Site Diary")

# TEAM SELECTION
teams = ""
teams = st.multiselect("TEAM(S):", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE SELECTION
date_selected = st.date_input("Date:", datetime.today())
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# WEATHER SELECTION
weather_am = st.selectbox("Morning Weather", ["Fine","Rainy"])
weather_pm = st.selectbox("Afternoon Weather", ["Fine","Rainy"])

# WORKING HOURS
start_time = st.time_input("Start Time:", time(8, 0))
end_time = st.time_input("End Time:", time(17, 0))
working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')} hrs"

data = []

for team in teams:
  st.subheader(f"{team}")
  pipe_size = st.selectbox(f"Pipe Size", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"], key=f"pipe_{team}")
  
  activity_list = st.multiselect("Activity Carried Out:", ["Pipe Jointing", "Pipe Laying"], key=f"activity_{team}")

  joints = "" 
  
  if "Pipe Jointing" in activity_list:
    joints = st.number_input("Joint",step=1, key=f"joint_{team}")

  start_ch_raw = ""
  end_ch_raw = ""
  ch_diff = ""
  
  if "Pipe Laying" in activity_list:
    start_ch_raw = st.text_input ("Starting Chainage", key=f"startch_{team}")
    end_ch_raw = st.text_input ("Ending Chainage", key=f"endch_{team}")
    start_ch = format_chainage(start_ch_raw) if start_ch_raw else ""
    end_ch = format_chainage(end_ch_raw) if end_ch_raw else ""
    
    # CALCULATE CHAINAGE DIFF
    if start_ch_raw and end_ch_raw:
      try:
        start_value = int(start_ch_raw)
        end_value = int(end_ch_raw)
        ch_diff = f"({end_value - start_value}m)"
      except ValueError:
        ch_diff = "(Invalid)"

  fittings = st.multiselect("Fitting(s):", ["A","B"], key=f"fittings_{team}")

data.append([
    team if team else "", 
    pipe_size if pipe_size else "", 
    activity_list if activity_list else "", 
    working_hours if working_hours else "", 
    joints if joints else "",
    start_ch if start_ch else "",
    end_ch if end_ch else "",
    ch_diff,
    fittings if fittings else ""
])

# CONVERT TO DATAFRAME
df = pd.DataFrame(data, columns=["Team","Pipe Size","Activity","Hours Working","Joints","Laid Start","Laid End","Laid Length(m)", "Fitting"])

# DISPLAY TABLE
edited_df = st.data_editor(df, use_container_width=True)

# GENERATE REPORT
if st.button("Generate Report"):
  pmnt_report = ""

  for _, row in edited_df.iterrows():
    #pmnt_report += f"> {row['Team]}\n"
    #pmnt_report += f"PIPE = = {row['Pipe Size']} \n"
    pmnt_report += f"> {row['Team']}\nPIPE = {row['Pipe Size']}\nDATE = {date_selected.strftime('%d/%m/%y (%A)')}\nWORK ACTIVITY = {row['Activity']}\nHOURS WORKING = {row['Hours Working']}\n"
