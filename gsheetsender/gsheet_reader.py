# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient import discovery
from oauth2client import file, client, tools

__author__ = 'gabor.bereczki'
__all__ = ['GSheetReader', ]


class GSheetReader:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

    def __init__(self, oauth_store_json: str):
        self.store = file.Storage('storage.json')
        self.creds = self.store.get()
        self.service = None

    def oauth(self, credential_json):
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets(credential_json, self.SCOPES)
            creds = tools.run_flow(flow, self.store)

    def init_service(self):
        self.service = discovery.build('sheets', 'v4', credentials=self.creds)

    def get_values(self, sheet_id: str, range: str):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=range).execute()
        return result.get('values', [])


