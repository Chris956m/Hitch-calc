import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Theme Configuration ---
st.set_page_config(page_title="Hitch Tracker", page_icon="📅")

# Sidebar Theme Selector
st.sidebar.header("App Style")
theme_choice = st.sidebar.radio("Choose Theme:", ["Classic", "Black & Gold"])

# Apply Custom CSS for the Black & Gold Theme
if theme_choice == "Black & Gold":
    primary_color = "#FFD700"  # Gold
    bg_color = "#0E1117"       # Dark Charcoal
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: white; }}
        h1, h2, h3 {{ color: {primary_color} !important; }}
        .stMetric {{ background-color: #1c1c1c; padding: 15px; border-radius: 10px; border: 1px solid {primary_color}; }}
        button {{ background-color: {primary_color} !important; color: black !important; font-weight: bold; }}
        thead tr th {{ background-color: #1c1c1c !important; color: {primary_color} !important; }}
        </style>
    """, unsafe_allow_html=True)
else:
    primary_color = "#FF4B4B" # Default Streamlit Red

st.title("📅 Oilfield Hitch Tracker")

# --- Sidebar Logic ---
st.sidebar.markdown("---")
st.sidebar.header("Schedule Settings")
start_date = st.sidebar.date_input("Next 'Day 1' of work?", datetime(2026, 3, 31))
weeks_on = st.sidebar.number_input("Weeks ON", min_value=1, value=3)
weeks_off = st.sidebar.number_input("Weeks OFF", min_value=1, value=1)

# --- Holiday Data 2026 ---
holidays_2026 = {
    "Easter": datetime(2026, 4, 5), "Mother's Day": datetime(2026, 5, 10),
    "Memorial Day": datetime(2026, 5, 25), "Father's Day": datetime(2026, 6, 21),
    "July 4th": datetime(2026, 7, 4), "Labor Day": datetime(2026, 9, 7),
    "Halloween": datetime(2026, 10, 31), "Thanksgiving": datetime(2026, 11, 26),
    "Christmas": datetime(2026, 12, 25)
}

# --- Calculation Logic ---
def get_hitch_details(start, w_on, w_off):
    schedule, holiday_report = [], []
    current = datetime.combine(start, datetime.min.time())
    today = datetime.now()
    status_now, days_left = "Not Started", 0

    for _ in range(15): # Calculate 15 rotations (~full year)
        work_end = current + timedelta(weeks=w_on, days=-1, hours=23, minutes=59)
        off_start = work_end + timedelta(seconds=1)
        off_end = off_start + timedelta(weeks=w_off, days=-1, hours=23, minutes=59)
        
        if current <= today <= work_end:
            status_now, days_left = "ON HITCH 🛠️", (work_end - today).days + 1
        elif off_start <= today <= off_end:
            status_now, days_left = "OFF DUTY 🏠", (off_end - today).days + 1

        for name, date in holidays_2026.items():
            if current <= date <= work_end: holiday_report.append({"Holiday": name, "Status": "AT WORK 🛠️"})
            elif off_start <= date <= off_end: holiday_report.append({"Holiday": name, "Status": "AT HOME 🏠"})

        schedule.append({"Status": "WORK 🛠️", "Start": current.strftime("%b %d"), "End": work_end.strftime("%b %d")})
        schedule.append({"Status": "OFF 🏠", "Start": off_start.strftime("%b %d"), "End": off_end.strftime("%b %d")})
        current = off_end + timedelta(seconds=1)
        
    return schedule, status_now, days_left, holiday_report

data, current_status, time_remaining, holiday_report = get_hitch_details(start_date, weeks_on, weeks_off)

# --- UI Display ---
st.metric("Current Status", current_status)
st.metric("Days Remaining", f"{time_remaining} Days")

st.markdown("### 🏖️ Holiday Forecast")
st.dataframe(pd.DataFrame(holiday_report).drop_duplicates(subset=['Holiday']), use_container_width=True, hide_index=True)

st.markdown("### 🗓️ Full Schedule")
st.table(pd.DataFrame(data))
