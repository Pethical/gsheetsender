# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient import discovery
from gsheetsender.google_auth import GoogleAuth
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
import base64
from apiclient import errors
import warnings

class GMail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send', "https://www.googleapis.com/auth/gmail.compose"]

    def __init__(self):
        self.service = None

    def init_service(self, google_auth: GoogleAuth):
        self.service = discovery.build('gmail', 'v1', credentials=google_auth.get_credential())

    @staticmethod
    def create_message(sender, to, subject, message_text):
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
        """Send the message email.

        Args:
        user_id: user_id for GMail api. Special value 'me' when the mail sender is the authenticated user.
        message: Email object, contain raw mail.

        Returns:
        An object containing a base64url encoded html email object.
        """
        if not self.service:
            warnings.warn("GMail service not initialized. Call init_service method!")
            return "GMail service not initialized. Call init_service method!"
        try:
            return self.service.users().messages().send(userId=user_id, body=message).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
        return "Send mail failed!"