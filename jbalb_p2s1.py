import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

# TEAM Selection (Choose One)
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection (Calendar)
date_selected = st.date_input("DATE:", datetime.today())

# Format Date as DD/MM/YY (DAY)
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Morning Weather Selection
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# Afternoon Weather Selection
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# Working Hours: Select Start and End Time using Time Input
start_time = st.time_input("Start Time:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("End Time:", datetime.strptime("17:00", "%H:%M").time())

# Calculate Total Working Hours (in hours)
total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1

# Time Working (e.g., 0800-1700)
working_time = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

# Display the "Machinery" title before the checkboxes
st.markdown("Machinery")

# List of Machinery
machinery_list = ["Excavator", "Piling Rig", "Crane"]

# Create columns for selection (Checkbox) and input (Number)
machinery_selected = []
machinery_numbers = {}

# Streamlit Columns for side-by-side layout
col1, col2 = st.columns([2, 1])

with col1:
    st.write("**Machinery Type**")

with col2:
    st.write("**Total Number**")

# Loop through machinery list to create checkboxes and number inputs
for machinery in machinery_list:
    with col1:
        selected = st.checkbox(f"{machinery}")
    with col2:
        if selected:
            number = st.number_input(f"Enter number for {machinery}", min_value=1, step=1, key=machinery)
            machinery_selected.append(machinery)
            machinery_numbers[machinery] = number

# Generate Report button
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {total_working_hours:.2f} hrs\n"
    output += f"{working_time}\n"
    
    # Output machinery only if selected
    if machinery_selected:
        output += "**Machinery**\n"
        for machinery in machinery_selected:
            output += f"- {machinery} - {machinery_numbers[machinery]}\n"

    st.text_area("Generated Report:", output, height=200)