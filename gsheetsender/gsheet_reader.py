# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient import discovery
from gsheetsender.google_auth import GoogleAuth

__author__ = 'gabor.bereczki'
__all__ = ['GSheetReader', ]


class GSheetReader:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

    def __init__(self):
        self.service = None

    def init_service(self, google_auth: GoogleAuth):
        self.service = discovery.build('sheets', 'v4', credentials=google_auth.get_credential())

    def get_values(self, sheet_id: str, range: str):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=range).execute()
        return result.get('values', [])


