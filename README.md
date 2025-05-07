# Automation Credit Card Bill from Gmail

This project uses Google APIs for Gmail and Google Drive integration.

## Features

- Fetches credit card bill emails from Gmail.
- Downloads and unlocks PDF files with a predefined password.
- Organizes files into locked and unlocked folders.
- Uploads unlocked files to a specific Google Drive folder.

## Requirements

- Python 3.7+
- Google API credentials for Gmail and Drive.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/matthewz5/Automation-Credit-Card-Bill-from-Gmail.git
   cd Automation-Credit-Card-Bill-from-Gmail
2. Install dependecies:
   ```bash
   pip install -r requirements.txt
3. Set up Google API credentials:
- Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
- Enable the Gmail and Drive APIs.
- Download the credentials.json file and place it in the project directory.
4. Configure the project:
- Update the configs.py file with your email, file password, and Google Drive folder ID.

## Folder Structure

- project/
  - api/
    - credentials.json # Google Cloud Credentials
  - data/
    - locked/       # Folder for locked PDF files
    - unlocked/     # Folder for unlocked PDF files
  - src/
    - configs.py    # Configuration file
    - defs_google_api.py  # Google API functions
    - defs_automation.py  # Automation functions
  - main.py           # Main script
  - requirements.txt # Main bibs