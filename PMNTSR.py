import streamlit as st
import urllib.parse
from datetime import datetime, time

def format_chainage(value):
  try: 
    value = int(value)
    return f"CH{value // 1000}+{value % 1000:03d}"
  except:
    return "Invalid Input"

st. title("PMNT Site Diary")

# TEAM SELECTION
team = st.multiselect("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])
