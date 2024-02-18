import os
import re
import imaplib
import requests
import email
import logging
from time import sleep
from getpass import getpass

def sanitize_filename(filename):
    """Remove non-alphanumeric characters and limit length."""
    filename = re.sub(r'[^a-zA-Z0-9 ]', '', filename)
    return filename[:300]

def fetch_email(mail, e_id):
    """Attempt to fetch an email with retries for robustness."""
    max_attempts = 10
    for attempt in range(max_attempts):
        result, msg_data = mail.fetch(e_id, '(RFC822)')
        if result == 'OK':
            return msg_data
        else:
            logging.warning(f"Retry {attempt + 1} for email ID {e_id}.")
            sleep(5)  # Wait for 5 seconds before retrying
    logging.error(f"Failed to fetch email ID {e_id} after {max_attempts} attempts.")
    return None

def download_and_save_pdf(title, link, save_path):
    """Download PDF from the link and save it with the title as filename."""
    try:
        pdf_response = requests.get(link, timeout=10)
        if pdf_response.status_code == 200:
            valid_title = sanitize_filename(title)
            filepath = os.path.join(save_path, f"{valid_title}.pdf")
            with open(filepath, "wb") as f:
                f.write(pdf_response.content)
            logging.info(f"PDF downloaded and saved: {filepath}")
        else:
            logging.error(f"Failed to download PDF for {title}. HTTP Status Code: {pdf_response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {title}. Error: {e}")

def extract_and_download(email_body, save_path):
    """Extract titles and links from email body and download PDFs."""
    pattern = r"Title: (.*?)\nAuthors:.*?\\\\ \( (https://arxiv.org/abs/\d+\.\d+)"
    matches = re.findall(pattern, email_body, re.DOTALL)
    if not matches:
        logging.info("No matches found in the email body.")
    for title, link in matches:
        pdf_link = f"https://arxiv.org/pdf/{link.split('/')[-1]}.pdf"
        download_and_save_pdf(title, pdf_link, save_path)

def main(email, password, file_path):
    # Setup logging
    logging.basicConfig(level=logging.INFO, filename='email_download.log',
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Create the directory if it does not exist
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email, password)
    mail.select('inbox')

    # Search for emails from no-reply@arxiv.org
    result, data = mail.search(None, '(FROM "no-reply@arxiv.org")')
    if result != 'OK':
        logging.error("Failed to search for emails.")
        return

    email_ids = data[0].split()

    for e_id in email_ids:
        msg_data = fetch_email(mail, e_id)
        if msg_data is None:
            continue
        
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        if email_message.get_content_type() == 'text/plain':
            email_body = email_message.get_payload(decode=True).decode('utf-8')
            extract_and_download(email_body, file_path)
            # Move the email to the trash after processing
            mail.store(e_id.decode('utf-8'), '+X-GM-LABELS', '\\Trash') 
            mail.expunge()
        else:
            logging.info("Email content type is not text/plain, skipping.")

if __name__ == "__main__":
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")
    file_path = input("Enter the download path: ")
    main(email, password, file_path)
