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
team = st.multiselect("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

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
  pipe_size = st.selectbox(f"{team} - Pipe Size", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"])
