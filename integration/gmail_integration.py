import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',  # Allows reading, modifying, and deleting emails
    'https://www.googleapis.com/auth/gmail.send'     # Allows sending emails
]

class GmailIntegration:
    def __init__(self):
        self.creds = None
        self.authenticate()

    def authenticate(self):
        """Authenticate the user and build the Gmail service."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)

    def list_messages(self, query=''):
        """List all messages that match the query string."""
        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            return messages
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_message(self, message_id):
        """Retrieve a specific message by its ID."""
        try:
            message = self.service.users().messages().get(userId='me', id=message_id).execute()
            return message
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def archive_message(self, message_id):
        """Archive a specific message by ID."""
        try:
            self.service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['INBOX']}).execute()
        except HttpError as error:
            print(f'An error occurred: {error}')

    def draft_reply(self, message_id, response_text):
        """Draft a reply to a specific message."""
        try:
            original_message = self.service.users().messages().get(userId='me', id=message_id).execute()
            message_payload = original_message['payload']
            headers = message_payload.get('headers', [])
            subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
            sender = [h['value'] for h in headers if h['name'] == 'From'][0]

            message = MIMEMultipart()
            message['to'] = sender
            message['subject'] = f'Re: {subject}'

            msg_text = MIMEText(response_text, 'plain')
            message.attach(msg_text)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()

            return draft
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def get_or_create_label(self, label_name):
        """Get the label ID for the given label name or create it if it doesn't exist."""
        labels = self.service.users().labels().list(userId='me').execute()
        for label in labels['labels']:
            if label['name'] == label_name:
                return label['id']
        
        # If label does not exist, create it
        label = {
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show',
            'name': label_name
        }
        new_label = self.service.users().labels().create(userId='me', body=label).execute()
        return new_label['id']

    def apply_label(self, message_id, label_id):
        """Apply a label to a message."""
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': [label_id]}
        ).execute()

    def mark_as_read(self, message_id):
        """Mark a specific message as read."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f'Marked message {message_id} as read.')
        except HttpError as error:
            print(f'An error occurred while marking message {message_id} as read: {error}')
