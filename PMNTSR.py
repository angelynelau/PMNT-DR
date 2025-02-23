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

# FORMAT DATE AS DD/MM/YY (DAY)
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# WEATHER SELECTION
weather_am = st.selectbox("Morning Weather", ["Fine","Rainy"])
weather_pm = st.selectbox("Afternoon Weather", ["Fine","Rainy"])
