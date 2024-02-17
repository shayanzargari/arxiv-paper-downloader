# Email PDF Downloader 📥📚

This Python script automates the process of downloading PDF attachments from emails sent by `no-reply@arxiv.org`, and storing them in a designated directory. It utilizes the Internet Message Access Protocol (IMAP) to interact with a Gmail account, filters for emails from the specified sender, parses the email content for PDF links and then downloads those documents.

## Requirements 🛠️

- Python 3.x
- `requests` library for making HTTP requests to download PDFs.
- Access to a Gmail account with IMAP enabled. Activate IMAP in your Gmail settings under the "Forwarding and POP/IMAP" section to allow the script to access your emails.


## Setup Instructions 🚀

Clone the script's repository to your local machine and navigate to the directory:

```sh
git clone <repository-url>
cd <repository-directory>
```

##  Configuration ⚙️
Edit the script to include your Gmail credentials (`your_email@gmail.com` and `your_password`). Use App Passwords for added security if 2-Step Verification is enabled.

Specify the directory for saving PDFs by updating the `save_path` variable in the script.

##  Detailed Code Explanation 📖
The script's workflow includes:

- **Logging Setup:** Configures logging for recording operations and errors.
- **Directory Preparation:** Ensures the specified directory for saving PDFs exists.
- **Gmail IMAP Connection:** Securely connects to Gmail's IMAP server for email access.
- **Email Search and Fetch:** Identifies and retrieves emails from no-reply@arxiv.org.
- **Email Processing:** Extracts and downloads PDFs from the email content, using regex to parse for links.
- **Filename Sanitization:** Removes unsafe characters from filenames and ensures OS compatibility.
- **Error Handling and Retries:** Implements robust mechanisms for email fetching and PDF downloading.
