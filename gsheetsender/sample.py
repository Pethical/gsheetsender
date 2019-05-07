# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

__author__ = 'gabor.bereczki'
__all__ = ['sample_function', ]


def sample_function(first, second=4):
    """This is a sample function to demonstrate doctests
    of :mod:`gsheetsender.code` and docs.
    It only return the sum of its two arguments.

    Args:
      :param first: (:class:`int`): first value to add
      :param second:  (:class:`int`): second value to add, 4 by default

    Returns:
      * :class:`int`: the sum of `first` and `second`.

    >>> sample_function(6, second=3)
    9
    >>> sample_function(6)
    10
    """
    return first + second
DRIVE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


SHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

# The ID and range of a sample spreadsheet.
RELEASE_SPREADSHEET_ID = '1jyGHvf46TZidQQqPXR5dLCuYWioZsV35B3R_YQXsXas'
DOMAIN_TASKS_SPREADSHEET_ID = '1v1vNLmwb2vSVWNOXLfpGnTZe-OGrmLoYLRGiykhve60'
SAMPLE_RANGE_NAME = 'Projects!A1:R'

def list_drive_files(creds_json):
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(creds_json, DRIVE_SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    files = DRIVE.files().list().execute().get('files', [])
    for f in files:
        print(f['name'], f['mimeType'])

def read_table(creds_json):
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(creds_json, SHEET_SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=RELEASE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    list_drive_files(sys.argv[1])
    read_table(sys.argv[1])


    import doctest
    doctest.testmod()
