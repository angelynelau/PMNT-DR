import streamlit as st
from datetime import datetime

st.title("PMNT P2S1 Site Diary")

# TEAM Selection
team = st.selectbox("TEAM:", ["TEAM A", "TEAM B", "TEAM C", "TEAM D", "TEAM E"])

# DATE Selection
date_selected = st.date_input("DATE:", datetime.today())

# Format Date as DD/MM/YY (DAY)
formatted_date = date_selected.strftime("%d/%m/%y (%A)")

# Weather Selection
morning_weather = st.selectbox("Morning Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])
afternoon_weather = st.selectbox("Afternoon Weather:", ["Sunny", "Drizzling", "Rainy", "Cloudy"])

# Working Hours: Start and End Time
start_time = st.time_input("Start Time:", datetime.strptime("08:00", "%H:%M").time())
end_time = st.time_input("End Time:", datetime.strptime("17:00", "%H:%M").time())

# Calculate Total Working Hours (subtract 1 hour for break)
total_working_hours = ((datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600) - 1
working_time = f"{start_time.strftime('%H%M')}-{end_time.strftime('%H%M')}"

# 🚜 **Machinery Selection**
st.markdown("### Machinery (Select if Applicable)")
machinery_list = ["Excavator", "Piling Rig", "Crane"]
machinery_selected = []
machinery_numbers = {}
for machinery in machinery_list:
    selected = st.checkbox(f"{machinery}")
    if selected:
        number = st.number_input(f"Enter number for {machinery}", min_value=1, step=1, key=machinery)
        machinery_selected.append(machinery)
        machinery_numbers[machinery] = number

# 📜 **Generate Report**
if st.button("Generate Report"):
    output = f"> {team}\n"
    output += f"Date: {formatted_date}\n"
    output += f"Morning: {morning_weather}\n"
    output += f"Afternoon: {afternoon_weather}\n"
    output += f"Total Working Hours: {total_working_hours:.0f} hrs\n"
    output += f"Working Time: {working_time}\n"

    # Machinery Section
    if machinery_selected:
        output += "\n**Machinery**\n"
        for machinery in machinery_selected:
            output += f"- {machinery} - {machinery_numbers[machinery]}\n"

    st.text_area("Generated Report:", output, height=300)