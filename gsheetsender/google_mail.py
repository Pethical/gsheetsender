# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient import discovery
from gsheetsender.google_auth import GoogleAuth
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart

import base64
from apiclient import errors


class GMail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send', "https://www.googleapis.com/auth/gmail.compose"]

    def __init__(self):
        self.service = None

    def init_service(self, google_auth: GoogleAuth):
        self.service = discovery.build('gmail', 'v1', credentials=google_auth.get_credential())

    def get_labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded html email object.
        """
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(message_text, 'html'))
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, user_id, message):
        try:
            return self.service.users().messages().send(userId=user_id, body=message).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
        return "Send mail failed!"