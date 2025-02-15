import streamlit as st
import urllib.parse
from datetime import datetime

st.title("P2S1 Daily Report")

# TEAM Selection (Choose One)
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("DATE:", datetime.today())

# Format Date as DD/MM/YY (DAY)
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# PIPE SIZE Selection (Choose One)
pipe_size = st.selectbox("PIPE SIZE:", ["160mm HDPE", "225mm HDPE", "280mm HDPE", "355mm HDPE", "400mm HDPE"])

# WORK ACTIVITY (Multiple Choice)
work_activity = st.multiselect("WORK ACTIVITY:", ["Pipe Laying", "Pipe Jointing"])

# Numeric Inputs
hours_working = st.number_input("HOURS WORKING", min_value=0, step=1)
manpower = st.number_input("MANPOWER", min_value=0, step=1)

# Chainage Formatting Function
def format_chainage(value):
    try:
        value = int(value)
        return f"CH{value // 1000}+{value % 1000:03d}"
    except:
        return "Invalid input"

# Conditional Inputs for LAID and JOINT
joint = 0
starting_chainage = ""
ending_chainage = ""
chainage_diff = ""

if "Pipe Jointing" in work_activity:
    joint = st.number_input("JOINT", min_value=0, step=1)

if "Pipe Laying" in work_activity:
    starting_chainage_raw = st.text_input("Starting Chainage (Enter as a number)")
    ending_chainage_raw = st.text_input("Ending Chainage (Enter as a number)")

    starting_chainage = format_chainage(starting_chainage_raw) if starting_chainage_raw else ""
    ending_chainage = format_chainage(ending_chainage_raw) if ending_chainage_raw else ""

    # Calculate Chainage Difference
    if starting_chainage_raw and ending_chainage_raw:
        try:
            start_value = int(starting_chainage_raw)
            end_value = int(ending_chainage_raw)
            chainage_diff = f"({end_value - start_value}m)"
        except:
            chainage_diff = "(Invalid chainage format)"

# FITTING input
fitting = st.text_input("FITTING")

# DELIVERY input
delivery = st.number_input(f"NUMBER OF PIPES DELIVERED ({pipe_size})", min_value=0, step=1)

# WEATHER Selection (Choose One)
weather = st.selectbox("WEATHER:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# REMARKS input
remarks = st.text_area("REMARKS")

# Generate report button
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"PIPE = {pipe_size}\n"
    output += f"DATE = {formatted_date}\n"
    
    # Include work activity if any is selected
    if work_activity:
        output += f"WORK ACTIVITY = {pipe_size} {' & '.join(work_activity)}\n"
    else:
        output += "WORK ACTIVITY = \n"

    # Always include these fields
    output += f"HOURS WORKING = {hours_working}\n" if hours_working else "HOURS WORKING = \n"
    output += f"MANPOWER = {manpower}\n" if manpower else "MANPOWER = \n"

    # JOINT 
    output += f"JOINT = {joint}\n" if joint else "JOINT = \n"

    # LAID
    output += f"LAID = {starting_chainage} to {ending_chainage} {chainage_diff}\n" if starting_chainage else "LAID = \n"

    # Only include FITTING if it's not blank
    if fitting:
        output += f"FITTING = {fitting}\n"
    else:
        output += "FITTING = \n"

    # Add DELIVERY only if it has a value
    if delivery > 0:
        output += f"DELIVERY = {pipe_size} - {delivery} lengths\n"
    else:
        output += "DELIVERY = \n"
    
    output += f"WEATHER = {weather}\n" if weather else "WEATHER = \n"
    output += f"REMARKS = {remarks}\n" if remarks else "REMARKS = \n"
    
    st.text_area("Generated Report:", output, height=300)

# Encode report for URL
encoded_report = urllib.parse.quote(report_content)

# WhatsApp share link
whatsapp_link = f"https://wa.me/?text={encoded_report}"

st.markdown(f"[Share on WhatsApp]({whatsapp_link})", unsafe_allow_html=True)
