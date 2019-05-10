# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient import discovery
from gsheetsender.google_auth import GoogleAuth
import warnings

__author__ = 'gabor.bereczki'
__all__ = ['GSheetReader', ]


class GSheetReader:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

    def __init__(self):
        self.service = None

    def init_service(self, google_auth: GoogleAuth):
        self.service = discovery.build('sheets', 'v4', credentials=google_auth.get_credential())

    def get_values(self, sheet_id: str, range: str):
        """Get a table values from google sheet. The table cells is defined by range.

        Args:
        sheet_id: Sheet long id, values read from. This ID is in URL path, when open a Google sheet in browser.
        range: This string parameter specify the data source in sheet. Define the table from where data read.
            [Sheet name]![left/top cell]:[right/bottom cell]. ex: sheet1!A1:D

        Returns:
        Values array [][] matrix.
        """
        if not self.service:
            warnings.warn("GSheetReader service not initialized. Call init_service method!")
            return None
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=range).execute()
        return result.get('values', [])


