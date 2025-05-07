import os
import base64
from pathlib import Path
import PyPDF2 
from googleapiclient.http import MediaFileUpload

def search_emails(service, remetente, max_results=None):
 
    query = f'from:{remetente} has:attachment'
    results = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    messages = results.get("messages", [])

    if not messages:
        print(f"\nNo email found from {remetente} with attachments. \n")
        return []

    print(f"\nEmails found from {remetente}: \n")

    email_ids = []

    for msg in messages:
        msg_id = msg["id"]
        email = service.users().messages().get(userId="me", id=msg_id).execute()
        headers = email["payload"]["headers"]

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No subject")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "Date unknown")

        print(f"ID: {msg_id}\n   Date: {date}\n   Subject: {subject}\n")
        email_ids.append(msg_id)

    return email_ids

def download_attachments(service, email_id, destiny_folder, file_type):
    
    message = service.users().messages().get(userId="me", id=email_id).execute()
    payload = message.get("payload", {})
    parts = payload.get("parts", [])

    if not os.path.exists(destiny_folder):
        os.makedirs(destiny_folder)

    for part in parts:
        if part.get("filename") and part["filename"].lower().endswith(file_type):
            filename = part["filename"]
            att_id = part["body"].get("attachmentId")
            attachment = service.users().messages().attachments().get(userId="me", messageId=email_id, id=att_id).execute()

            data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
            file_path = os.path.join(destiny_folder, filename)

            with open(file_path, "wb") as f:
                f.write(data)

            print(f"Attachments saved: {file_path}")
        else:
            print(f"Ignored attachment: {part.get('filename', 'Sem nome')}")


def unlock_pdf(path, origin_folder, destiny_folder, files_pass):

    for filename in os.listdir(path / origin_folder):
        print(f"\n {filename}")

        if filename.endswith(('.pdf', '.PDF')):
            input_path = os.path.join(path, origin_folder, filename)
            output_path = os.path.join(path, destiny_folder, f'unlocked_{filename}')

            try:
                with open(input_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)

                    if reader.is_encrypted:
                        reader.decrypt(files_pass)

                    writer = PyPDF2.PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)

                    with open(output_path, 'wb') as out_file:
                        writer.write(out_file)

                print("Unlocked!")
            except Exception as e:
                print(f"Failed to unlock: {e}")


def upload_files(origin_folder, service_drive, pasta_id):
    
    for filename in os.listdir(origin_folder):
        print(f"\n {filename}")

        local_file_path = os.path.join(origin_folder, filename)
        drive_file_name = filename

        file_metadata = {"name": drive_file_name}
        if pasta_id:
            file_metadata["parents"] = [pasta_id]

        media = MediaFileUpload(local_file_path, resumable=True)

        file = service_drive.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink"
        ).execute()

        print(f"File uploaded successfully!")
        print(f"File ID: {file.get('id')}")
        print(f"Acess link: {file.get('webViewLink')}")