from pathlib import Path
import os

from src.defs_google_api import authenticate_google_api
from src.defs_automation import search_emails, download_attachments, unlock_pdf, upload_files
from src.configs import REMETENTE, FILE_TYPE, FILES_PASS, FOLDER_FILES_LOCKED, FOLDER_FILES_UNLOCKED, SCOPES_GMAIL, SCOPES_DRIVE, DRIVE_FOLDER_ID

if __name__ == "__main__":

    main_path = Path(__file__).resolve().parent
    print(f"\nCurrent working directory: {main_path}")
    
    token_path_gmail = os.path.join(main_path, "api", "token_gmail.json")
    token_path_drive = os.path.join(main_path, "api", "token_drive.json")
    credentials_path = os.path.join(main_path, "api", "credentials.json")

    print("\nGmail API authentication...")
    service_gmail = authenticate_google_api(SCOPES_GMAIL, "gmail", token_path_gmail, credentials_path)
    
    print(f"\nFetching e-mail with attachments from: {REMETENTE}...")
    emails = search_emails(service_gmail, REMETENTE)

    if emails:
        print("\nDownloading attachments...")
        for email_id in emails:
            download_attachments(service_gmail, email_id, FOLDER_FILES_LOCKED, FILE_TYPE)

    print("Unlocking PDFs...")
    unlock_pdf(Path.cwd(), FOLDER_FILES_LOCKED, FOLDER_FILES_UNLOCKED, FILES_PASS)

    print("Saving unlocked PDFs to Google Drive...")
    service_drive = authenticate_google_api(SCOPES_DRIVE, "drive", token_path_drive, credentials_path)

    print("Uploading files to Google Drive...")
    upload_files(os.path.join(main_path, "data", "unlocked"), service_drive, DRIVE_FOLDER_ID)