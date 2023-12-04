import streamlit as st
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
# from google.oauth2.service_account import Credentials as ServiceAccountCredentials


openai.api_key = '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'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
SERVICE_ACCOUNT_FILE = "C:/Users/raman/Downloads/SmartRecruiter/credentials.json"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'chebrolu.prasanna1@gmail.com'
EMAIL_PASSWORD = 'ttni ctmw uldu irev'
SENDER_EMAIL = 'chebrolu.lakshmi.prasanna.lp.147@gmail.com'


def schedule_google_meet_video_call(email,scheduled_time):
    '''st.subheader("Video Call Scheduling")
    scheduled_time = None
    call_date = st.date_input("Select Date", min_value=datetime.now().date())
    call_time = st.time_input("Select Time")
    scheduled_time = datetime.combine(call_date, call_time)
    st.session_state.selected_datetime = scheduled_time'''
    if scheduled_time:
        st.write(f"Video call scheduled for: {scheduled_time}")
        meeting_link = schedule_google_meet_meeting(scheduled_time)
        if meeting_link:
            send_video_call_email(email, scheduled_time, meeting_link)
            st.success("Meeting link sent successfully!")
            

# Function to schedule a Google Meet meeting and return the meeting link
def schedule_google_meet_meeting(scheduled_time):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Scheduled Video Call',
        'description': 'Interview Meeting Link from Societe Generale .',
        'start': {
            'dateTime': scheduled_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (scheduled_time + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {'conferenceSolutionKey': {'type': 'hangoutsMeet'}}}
    }
    try:
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        meeting_link = event.get('hangoutsMeet')
        if not meeting_link:
            meeting_link = event.get('htmlLink') or event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri')
        return meeting_link
    except Exception as e:
        st.error(f"Error scheduling the Google Meet meeting: {str(e)}")
        return None



# Function to send an email with the Teams meeting link
def send_video_call_email(email, scheduled_time, meeting_link):
    subject = "Interview Meeting Link from Societe Generale"
    body = f"Your Google Meet video call is scheduled for {scheduled_time}. Here is the link: {meeting_link}"

    # Create MIMEText object
    message = MIMEMultipart()
    message.attach(MIMEText(body, 'plain'))

    # Set email addresses
    message['From'] = SENDER_EMAIL
    message['To'] = email
    message['Subject'] = subject

    # Connect to SMTP server and send email
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, message.as_string())

    st.write(f"Email sent to {email}. Check your inbox for the Google Meet link.")
    
def interview_meet_link():
    st.title("Google Meet Video Call Scheduling")

    # Get user's email address
    user_email = st.text_input("Enter Your Email Address")
    st.subheader("Video Call Scheduling")
    scheduled_time = None
    call_date = st.date_input("Select Date", min_value=datetime.now().date())
    call_time = st.time_input("Select Time")
    scheduled_time = datetime.combine(call_date, call_time)
    if st.button("Schedule Google Meet Video Call"):
        """if hasattr(st.session_state, 'selected_datetime'):
            scheduled_time = st.session_state.selected_datetime
            st.write(f"Video call scheduled for: {scheduled_time}")"""
        schedule_google_meet_video_call(user_email,scheduled_time)
    

# Streamlit App


# Schedule Google Meet Video Call and Send Email
