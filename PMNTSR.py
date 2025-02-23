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
  pipe_size = st.selectbox(f"Pipe Size", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"])
  
  st.multiselect("Activity Carried Out:", ["Pipe Jointing", "Pipe Laying"])
  activity_list = []
  activity_names = []

  if "Pipe Jointing" in activity_list:
    joint = st.number_input("Joint")
  if "Pipe Laying" in activity_list:
    start_ch_raw = st.text_input ("Starting Chainage")
    end_ch_raw = st.text_inpur ("Ending Chainage")
    start_ch = format_chainage(start_ch_raw) if start_ch_raw else ""
    end_ch = format_chainage(end_ch_raw) if end_ch_raw else ""
    
    # CALCULATE CHAINAGE DIFF
    if start_ch_raw and end_ch_raw:
      try:
        start_value = int(start_ch_raw)
        end_value = int(end_ch_raw)
        ch_diff = f"({end_value - start_value}m)"
    
  fittings = st.multiselect
