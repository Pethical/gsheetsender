import argparse
import gsheetsender
from oauth2client import file, client, tools
from gsheetsender.gsheet_reader import GSheetReader

class GSMain:

    def __init__(self):
        self.sheet_reader = None

    def parse_args(self):
        parser = argparse.ArgumentParser(prog='Google sheet email sender',
                                         description='Tool to send table details from Google Sheet',
                                         parents=[tools.argparser])
        parser.add_argument('--oauth_store', type=str, help='Google oauth token store json file', required=True)
        parser.add_argument('--credential', type=str, help='Google credential json file for oauth', required=True)
        parser.add_argument('--sheet', type=str, help='Google sheet id')
        parser.add_argument('--range', type=str, help='Range from sheet. example: Sheet1!A1:R.  [sheet]![left]:[right]')
        args = parser.parse_args()
        return args

    def init_google_api(self, oauth_store, oauth_credential):
        self.sheet_reader = GSheetReader(oauth_store)
        self.sheet_reader.oauth(oauth_credential)

    def get_table_content(self, sheet_id: str, range: str):
        self.sheet_reader.init_service()
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

