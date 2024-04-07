# Tapo Smart Plug Email Alert

This project is a Python script that monitors a Tapo smart plug device and sends an email alert when the device has been on for more than a user-specified number of hours.

## Features

- Connects to Tapo smart plug device and tracks the on/off status
- Sends an email notification when the on-time exceeds a configurable threshold
- Supports customizable email settings (recipient, subject, message)
- Designed to be hosted as a Google Cloud Function and triggered by a Pub/Sub event

## Usage

The script is intended to be hosted on Google Cloud as a serverless function, triggered by a Pub/Sub event. To use it, you'll need to:

1. Set up the required environment variables, including your Tapo device credentials and email settings.
2. Deploy the script as a Google Cloud Function.
3. Configure a Pub/Sub trigger to execute the function at regular intervals (e.g., every hour).

The script will then automatically monitor the Tapo smart plug device and send an email alert if the on-time exceeds the specified threshold.

## License

😂
