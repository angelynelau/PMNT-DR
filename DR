import streamlit as st
from datetime import datetime

st.title("Work Report Generator")

# User selections
team = st.selectbox("Select TEAM:", ["TEAM A", "TEAM B","TEAM C", "TEAM D", "TEAM E"])
pipe_size = st.selectbox("Select PIPE SIZE:", ["400mm HDPE", "355mm HDPE", "280mm HDPE", "225mm HDPE","160mm HDPE"])
work_activity = st.selectbox("Select WORK ACTIVITY:", ["Pipe Laying", "Pipe Jointing"])
date_selected = st.date_input("Select DATE:", datetime.today())

# Numeric inputs
hours_working = st.number_input("HOURS WORKING", min_value=0, step=1)
manpower = st.number_input("MANPOWER", min_value=0, step=1)
joint = st.number_input("JOINT", min_value=0, step=1)
laid = st.text_input("LAID (leave blank if none)")

# Delivery input
delivery_400 = st.text_input("DELIVERY (400mm HDPE)")
delivery_225 = st.text_input("DELIVERY (225mm HDPE)")

# Generate report button
if st.button("Generate Report"):
    output = f"> {team}\nPIPE = {pipe_size}\nDATE = {date_selected}\n"
    output += f"WORK ACTIVITY = {pipe_size} {work_activity}\n"
    if hours_working:
        output += f"HOURS WORKING = {hours_working}\n"
    if manpower:
        output += f"MANPOWER = {manpower}\n"
    if joint:
        output += f"JOINT = {joint}\n"
    if laid:
        output += f"LAID = {laid}\n"
    if delivery_400:
        output += f"DELIVERY = 400mm HDPE {delivery_400}m\n"
    if delivery_225:
        output += f"DELIVERY = 225mm HDPE {delivery_225}m\n"

    st.text_area("Generated Report:", output, height=200)
