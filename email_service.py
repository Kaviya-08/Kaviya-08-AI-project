import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

class EmailService:
    def __init__(self, groq_service, email_user, email_pass):
        self.groq_service = groq_service
        self.email_user = email_user
        self.email_pass = email_pass

    def fetch_emails(self, max_count=3):
        print("function called..")
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(self.email_user, self.email_pass)
        print("login done")
        imap.select("inbox")
        print("inbox")
        result, data = imap.search(None, "ALL")
        print("data : ",data)
        mail_ids = data[0].split()
        emails = []
        print(emails)
        for num in reversed(mail_ids[-max_count:]):
            result, msg_data = imap.fetch(num, "(RFC822)")
            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)
            parsed = self.parse_email(msg)
            emails.append(parsed)

        imap.logout()
        return emails

    def parse_email(self, msg):
        email_data = {
            'subject': '',
            'from': '',
            'date': '',
            'body': '',
            'summary': None
        }

        # Extract headers
        for header in ['subject', 'from', 'date']:
            raw = msg.get(header, '')
            decoded, charset = decode_header(raw)[0]
            if isinstance(decoded, bytes):
                decoded = decoded.decode(charset or 'utf-8', errors='ignore')
            email_data[header] = decoded

        # Extract body
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition"))
                if ctype == "text/plain" and "attachment" not in disp:
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode(errors='ignore')
                    break
                elif ctype == "text/html" and "attachment" not in disp:
                    html_content = part.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    email_data['body'] = soup.get_text()
                    break
        else:
            body = msg.get_payload(decode=True)
            email_data['body'] = body.decode(errors='ignore')

        return email_data
