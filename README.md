# Email PDF Downloader

This Python script automatically downloads PDF attachments from emails sent by `no-reply@arxiv.org` and saves them to a specified directory. It uses IMAP to connect to a Gmail inbox, searches for emails from the specified sender, extracts PDF links from the email content, and downloads them.

## Features

- **Email Searching:** Filters emails in the inbox from `no-reply@arxiv.org`.
- **PDF Extraction and Downloading:** Extracts PDF links from the email content and downloads the PDF files.
- **Filename Sanitization:** Ensures that the filenames for saved PDFs are safe and OS-compatible.
- **Logging:** Logs actions and errors for troubleshooting and monitoring the script's activity.

## Requirements

- Python 3.x
- `requests` library for making HTTP requests to download PDFs.
- Access to a Gmail account with IMAP enabled.

## Setup

Clone the repository:

```sh
git clone <repository-url>
cd <repository-directory>
```

## Install dependencies:

Ensure you have Python 3 installed, then install the required Python packages:

## Enable IMAP in Gmail:

Make sure IMAP is enabled in your Gmail account settings to allow the script to access your emails.


##  Configuration
Update the your_email@gmail.com and your_password in the script with your Gmail credentials. It's highly recommended to use App Passwords if you have 2-Step Verification enabled on your Google account.

Specify the path where PDFs will be saved by updating the save_path variable.

## Usage
Run the script using Python:

```sh
Copy code
python email_pdf_downloader.py
The script will connect to your Gmail account, search for emails from no-reply@arxiv.org, extract PDF links from the emails, download the PDFs, and save them to the specified directory.
```

##  Logging
The script logs its operations and any errors encountered to email_download.log in the current directory. You can monitor this file to check the script's activity and troubleshoot any issues.
