# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from gsheetsender.google_auth import GoogleAuth
from apiclient import errors
import io
import warnings

class GDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive.file', "https://www.googleapis.com/auth/drive.metadata"]

    def __init__(self):
        self.service = None

    def init_service(self, google_auth: GoogleAuth):
        self.service = discovery.build('drive', 'v3', credentials=google_auth.get_credential())


    def export_xlsx(self, file_id):
        """Download Google Sheet as MS Excel file (xlsx).

        Args:
        file_id: Google Sheet id.
        output_file: Output file name. Downloaded file
        """
        if not self.service:
            warnings.warn("GDrive service not initialized. Call init_service method!")
            return "GDrive service not initialized. Call init_service method!"
        try:
            request = self.service.files().export_media(fileId=file_id,
                                                        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
        return fh