import asyncio
import os  # To access environment variables
from datetime import date
from tapo import ApiClient, EnergyDataInterval
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import functions_framework

# Environment variables
TAPO_USERNAME = os.environ.get('TAPO_USERNAME')
TAPO_PASSWORD = os.environ.get('TAPO_PASSWORD')
DEVICE_IP = os.environ.get('DEVICE_IP')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
APP_PASS = os.environ.get('APP_PASS')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

USAGE_THRESHOLD = 2
ENERGY_CONSUMPTION_THRESHOLD = 1

def send_notification_email():
    sender_address = EMAIL_ADDRESS
    sender_pass = APP_PASS
    receiver_address = RECIPIENT_EMAIL

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Device Usage Alert'  # Make sure this is only set once

    mail_content = '''Hello,

Your device has been on for more than the configurable hours today.

Best regards,
Your Python Script
'''
    message.attach(MIMEText(mail_content, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


async def check_energy_usage():
    client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
    plug = await client.p115(DEVICE_IP)

    # Check if the device is turned off
    device_info = await plug.get_device_info()
    if device_info.device_on == False:
        print("Device is turned off, skipping email notification.")
        return

    energy_data = await plug.get_energy_data(interval=EnergyDataInterval.Hourly, start_date=date.today())
    energy_readings = energy_data.data
    
     # Count hours when the device was on (based on ENERGY_CONSUMPTION_THRESHOLD)
    hours_on = sum(1 for reading in energy_readings if reading > ENERGY_CONSUMPTION_THRESHOLD)
    
    # Check if the device has been on for more than the USAGE_THRESHOLD
    if hours_on > USAGE_THRESHOLD:
        print(f"Warning: The device has been on for more than {USAGE_THRESHOLD} hours today.")
        if hours_on > USAGE_THRESHOLD:
            send_notification_email()

@functions_framework.cloud_event
def pubsub_trigger(cloud_event):
    """
    This function is the entry point for Pub/Sub-triggered executions.
    """
    print("it works!")
    asyncio.run(check_energy_usage())
    return 'Function executed via Pub/Sub'
