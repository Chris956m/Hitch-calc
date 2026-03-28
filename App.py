import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- App Styling ---
st.set_page_config(page_title="Oilfield Hitch Calc", page_icon="🛢️")
st.title("🛢️ Oilfield Hitch Calculator")
st.markdown("Plan your year and see exactly when you'll be home.")

# --- Sidebar Inputs ---
st.sidebar.header("Schedule Settings")
start_date = st.sidebar.date_input("When is your next 'Day 1' of work?", datetime.now())
weeks_on = st.sidebar.number_input("Weeks ON (Hitch)", min_value=1, value=3)
weeks_off = st.sidebar.number_input("Weeks OFF", min_value=1, value=1)
year_to_calc = st.sidebar.selectbox("Select Year", [2026, 2027])

# --- Calculation Logic ---
def get_full_schedule(start, w_on, w_off, year):
    schedule = []
    current = datetime.combine(start, datetime.min.time())
    end_of_year = datetime(year, 12, 31)
    
    while current <= end_of_year:
        work_end = current + timedelta(weeks=w_on, days=-1)
        off_start = work_end + timedelta(days=1)
        off_end = off_start + timedelta(weeks=w_off, days=-1)
        
        schedule.append({
            "Status": "WORK 🛠️",
            "Start": current.strftime("%b %d, %Y"),
            "End": work_end.strftime("%b %d, %Y")
        })
        schedule.append({
            "Status": "OFF 🏠",
            "Start": off_start.strftime("%b %d, %Y"),
            "End": off_end.strftime("%b %d, %Y")
        })
        current = off_end + timedelta(days=1)
    return schedule

# --- Display Results ---
data = get_full_schedule(start_date, weeks_on, weeks_off, year_to_calc)
df = pd.DataFrame(data)

st.table(df)

# --- Download Feature ---
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Schedule as CSV",
    data=csv,
    file_name=f'hitch_schedule_{year_to_calc}.csv',
    mime='text/csv',
)
