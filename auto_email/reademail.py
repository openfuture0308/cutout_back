import imaplib
import email
import os


class MailBox:
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    USER = "tonyandrew0308@gmail.com"  # Replace with your actual email
    PASSWORD = "avue hvpf rqva vkls"  # Replace with your actual password

    def __init__(self):
        # Initialize the IMAP connection
        self.imap = imaplib.IMAP4_SSL(host=self.SMTP_SERVER, port=self.SMTP_PORT)
        self.imap.login(self.USER, self.PASSWORD)

    def __enter__(self):
        # Ensure the mailbox is selected and return the self object for context manager
        self.imap.select("INBOX")
        self.emails = self._get_all_messages()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Close and log out of the IMAP connection
        self.imap.close()
        self.imap.logout()

    def fetch_message(self, num):
        # Fetch the specified email by index
        _, data = self.imap.fetch(num, "(RFC822)")  # Use num directly here
        _, bytes_data = data[0]
        email_message = email.message_from_bytes(bytes_data)
        return email_message

    def get_all_attachments(self):
        attachment_filenames = []  # List to store attachment filenames
        for email_id in self.emails:
            email_message = self.fetch_message(
                email_id.decode("utf-8")
            )  # Decode email ID to str
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue
                filename = part.get_filename()
                if filename:
                    attachment_filenames.append(filename)  # Append filename to the list
                    # Optionally save the attachment
                    file_data = part.get_payload(decode=True)
                    file_path = os.path.join(
                        "./excel", filename
                    )  # Change path as needed
                    with open(file_path, "wb") as f:
                        f.write(file_data)
                    print(f"Attachment saved: {file_path}")
        return attachment_filenames

    def _get_all_messages(self):
        # Search and return all email IDs in the Inbox
        status, data = self.imap.search(None, "ALL")
        return data[0].split()


# Usage
with MailBox() as mb:
    attachment_filenames = mb.get_all_attachments()  # Get all attachment filenames
    print("All attachment filenames:")
    for filename in attachment_filenames:
        print(filename)
