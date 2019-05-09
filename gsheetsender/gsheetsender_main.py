import argparse
from gsheetsender.google_auth import GoogleAuth
from oauth2client import tools
from gsheetsender.gsheet_reader import GSheetReader

class GSMain:

    def __init__(self):
        self.google_auth = None
        self.sheet_reader = None
        self.args = None

    def parse_args(self):
        parser = argparse.ArgumentParser(prog='Google sheet email sender',
                                         description='Tool to send table details from Google Sheet',
                                         parents=[tools.argparser])
        parser.add_argument('--oauth_store', type=str, help='Google oauth token store json file', required=True)
        parser.add_argument('--credential', type=str, help='Google credential json file for oauth', required=True)
        parser.add_argument('--sheet', type=str, help='Google sheet id', required=True)
        parser.add_argument('--range', type=str, help='Range from sheet. example: Sheet1!A1:R.  [sheet]![left]:[right]',
                            required=True)
        self.args = parser.parse_args()
        return self.args

    def init_google_api(self, oauth_store, oauth_credential):
        self.google_auth = GoogleAuth(oauth_store)
        self.google_auth.oauth(oauth_credential, GSheetReader.SCOPES, self.args)
        self.sheet_reader = GSheetReader()

    def get_table_content(self, sheet_id: str, range: str):
        self.sheet_reader.init_service(self.google_auth)
        return self.sheet_reader.get_values(sheet_id, range)

    def generate_mail_from_teplate(self, temaple_file):
        None

    def send_mail(to: str, subject:str, body:str):
        None

if __name__ == '__main__':

    gsmain = GSMain()
    args = gsmain.parse_args()
    gsmain.init_google_api(args.oauth_store, args.credential)
    print(gsmain.get_table_content(args.sheet, args.range))

