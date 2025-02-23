import streamlit as st
import pandas as pd
import datetime

# Streamlit page setup
st.set_page_config(page_title="Pipe Laying Report", page_icon="🛠️")
st.title("🛠️ Pipe Laying Report Generator")

# Team selection
teams = st.multiselect("Select Teams", ["Team A", "Team B", "Team C", "Team D", "Team E"], default=["Team A"])

# Weather selection
weather_am = st.selectbox("Morning Weather", ["Sunny", "Rainy", "Cloudy"], index=0)
weather_pm = st.selectbox("Afternoon Weather", ["Sunny", "Rainy", "Cloudy"], index=0)

# Working hours
hours_working = st.number_input("Total Working Hours", min_value=1, max_value=12, value=8)

data = []

for team in teams:
    st.subheader(f"{team} Work Details")
    pipe_size = st.selectbox(f"{team} - Pipe Size", ["400mm HDPE", "350mm HDPE", "280mm HDPE", "225mm HDPE", "160mm HDPE"], key=f"pipe_{team}")
    work_activity = f"{pipe_size} Pipe Jointing & Laying"
    manpower = st.number_input(f"{team} - Manpower", min_value=1, max_value=20, value=5, key=f"manpower_{team}")
    joints = st.number_input(f"{team} - Joints", min_value=1, max_value=50, value=5, key=f"joints_{team}")
    laid_start = st.text_input(f"{team} - Laid Start Chainage", "CH1+000", key=f"laid_start_{team}")
    laid_end = st.text_input(f"{team} - Laid End Chainage", "CH1+500", key=f"laid_end_{team}")
    laid_length = st.number_input(f"{team} - Laid Length (m)", min_value=1, max_value=5000, value=500, key=f"laid_length_{team}")
    fittings = st.multiselect(f"{team} - Fittings", ["Stub End", "Adaptor", "Tee"], default=["Tee"], key=f"fittings_{team}")
    delivery = st.number_input(f"{team} - Delivery (number of lengths)", min_value=1, max_value=100, value=23, key=f"delivery_{team}")
    remarks = st.text_area(f"{team} - Remarks", key=f"remarks_{team}")

    data.append([team, pipe_size, work_activity, hours_working, manpower, joints, laid_start, laid_end, laid_length, fittings, delivery, remarks])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Team", "Pipe Size", "Work Activity", "Hours Working", "Manpower", "Joints", "Laid Start", "Laid End", "Laid Length", "Fittings", "Delivery", "Remarks"])

# Display editable table
st.subheader("Editable Work Data Table")
edited_df = st.data_editor(df, use_container_width=True)

# Generate report button
if st.button("Generate Report"):
    date_today = datetime.datetime.today().strftime('%d/%m/%y (%A)')
    
    pmnt_report = ""
    jbalb_report = f"Date: {date_today}\nMorning: {weather_am}\nAfternoon: {weather_pm}\nTotal Working Hours: {hours_working}.00 hrs\n0800 - 1700 hrs\n\n"
    
    jbalb_report += "MACHINERY\nExcavator - 2\n\nEQUIPMENT\nGenset - 2\nButt Fusion Welding Machine - 2\n\nPIPE LAYING TEAM\nSupervisor - 2\nExcavator Operator - 2\nGeneral Worker - 5\n\nMATERIALS DELIVERED TO SITE\n"
    
    activity_carried_out = ""
    
    for _, row in edited_df.iterrows():
        pmnt_report += f"> {row['Team']}\nPIPE = {row['Pipe Size']}\nDATE = {date_today}\nWORK ACTIVITY = {row['Work Activity']}\nHOURS WORKING = {row['Hours Working']}\nMANPOWER = {row['Manpower']}\n"
        pmnt_report += f"JOINT = {row['Joints']}\nLAID = {row['Laid Start']} to {row['Laid End']} ({row['Laid Length']}m)\n"
        pmnt_report += f"FITTING = {', '.join(row['Fittings'])}\nDELIVERY = {row['Pipe Size']} - {row['Delivery']} lengths\n"
        pmnt_report += f"WEATHER = {weather_am} (AM) / {weather_pm} (PM)\nREMARKS = {row['Remarks']}\n\n"
        
        jbalb_report += f"- {row['Pipe Size']} - {row['Delivery']} lengths (ROUTE {row['Team'][-1]})\n"
        
        activity_carried_out += f"1. Pipe Jointing\n> {row['Team']}\n- {row['Joints']} nos joints ({row['Pipe Size']})\n"
        activity_carried_out += f"2. Pipe Laying\n> {row['Team']}\n- ({row['Pipe Size']}) {row['Laid Start']} to {row['Laid End']} ({row['Laid Length']}m)\n"
    
    jbalb_report += "\nACTIVITY CARRIED OUT\n" + activity_carried_out
    
    # Display reports
    st.subheader("Generated PMNT Format Report")
    st.text(pmnt_report)
    
    st.subheader("Generated JBALB Format Report")
    st.text(jbalb_report)
