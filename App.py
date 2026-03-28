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
# --- Email Feature ---
st.markdown("---")
st.subheader("📬 Send Schedule")
email_recipient = st.text_input("Recipient Email (e.g., wife@email.com or boss@oilfield.com)")

# Format the schedule into a readable text block for the email
schedule_text = "My 2026 Hitch Schedule:\n\n"
for item in data:
    schedule_text += f"{item['Status']}: {item['Start']} to {item['End']}\n"

# Create a 'Mailto' link
import urllib.parse
subject = urllib.parse.quote("My Work Schedule")
body = urllib.parse.quote(schedule_text)
mailto_link = f"mailto:{email_recipient}?subject={subject}&body={body}"

if email_recipient:
    st.markdown(f'<a href="{mailto_link}" style="text-decoration:none;"><button style="width:100%; border-radius:5px; background-color:#FF4B4B; color:white; padding:10px; border:none; cursor:pointer;">📧 Send Schedule via Email</button></a>', unsafe_allow_html=True)
else:
    st.info("Enter an email address above to enable the send button.")
