import os
import re
import imaplib
import requests
import email
import logging
from time import sleep

# Setup logging
logging.basicConfig(level=logging.INFO, filename='email_download.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Specify the path where PDFs will be saved
save_path = "file_path"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Connect to Gmail IMAP server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your_email@gmail.com', 'your_password')
mail.select('inbox')

def sanitize_filename(filename):
    """Remove non-alphanumeric characters and limit length."""
    filename = re.sub(r'[^a-zA-Z0-9 ]', '', filename)
    return filename[:300]

# Search for emails from no-reply@arxiv.org
result, data = mail.search(None, '(FROM "no-reply@arxiv.org")')
if result != 'OK':
    logging.error("Failed to search for emails.")
    exit()

email_ids = data[0].split()

def fetch_email(e_id):
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

def download_and_save_pdf(title, link):
    """Download PDF from the link and save it with the title as filename."""
    try:
        pdf_response = requests.get(link, timeout=10)
        if pdf_response.status_code == 200:
            valid_title = sanitize_filename(title)
            filepath = os.path.join(save_path, f"{valid_title}.pdf")
            with open(filepath, "wb") as f:
                f.write(pdf_response.content)
            print(f"PDF downloaded and saved: {filepath}")
        else:
            print(f"Failed to download PDF for {title}. HTTP Status Code: {pdf_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {title}. Error: {e}")

def extract_and_download(email_body):
    """Extract titles and links from email body and download PDFs."""
    pattern = r"Title: (.*?)\nAuthors:.*?\\\\ \( (https://arxiv.org/abs/\d+\.\d+)"
    matches = re.findall(pattern, email_body, re.DOTALL)
    if not matches:
        print("No matches found in the email body.")
    for title, link in matches:
        pdf_link = f"https://arxiv.org/pdf/{link.split('/')[-1]}.pdf"
        download_and_save_pdf(title, pdf_link)
        
for e_id in email_ids:
    msg_data = fetch_email(e_id)
    if msg_data is None:
        # If fetching the email fails, log the failure and skip to the next email ID
        logging.error(f"Failed to fetch or parse email ID {e_id}.")
        continue
    
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Check the content type before processing
    if email_message.get_content_type() == 'text/plain':
        email_body = email_message.get_payload(decode=True).decode('utf-8')
        extract_and_download(email_body)
        # Move the email to the trash after processing
        mail.store(e_id.decode('utf-8'), '+X-GM-LABELS', '\\Trash') 
        mail.expunge()
    else:
        logging.info("Email content type is not text/plain, skipping.")