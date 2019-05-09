import argparse
from os import terminal_size

from gsheetsender.google_auth import GoogleAuth
from oauth2client import tools
from gsheetsender.gsheet_reader import GSheetReader
from gsheetsender.google_mail import GMail
from jinja2 import Environment, FileSystemLoader, Template


class GSMain:

    def __init__(self):
        self.google_auth = None
        self.sheet_reader:GSheetReader = None
        self.mail:GMail = None
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
        parser.add_argument('--template_dir', type=str, help='E-Mail template directory, contain mail_template.html',
                            required=True)

        self.args = parser.parse_args()
        return self.args

    def init_google_api(self, oauth_store, oauth_credential):
        self.google_auth = GoogleAuth(oauth_store)
        self.google_auth.oauth(oauth_credential, GSheetReader.SCOPES+GMail.SCOPES, self.args)
        self.sheet_reader = GSheetReader()
        self.mail = GMail()

    def get_table_content(self, sheet_id: str, range: str):
        self.sheet_reader.init_service(self.google_auth)
        return self.sheet_reader.get_values(sheet_id, range)

    def generate_mail_from_template(self, template_file, table_content):
        j2_env = Environment(loader=FileSystemLoader(args.template_dir), trim_blocks=True)
        template = j2_env.get_template(template_file)
        return template.render(values=table_content)


    def send_mail(self, send_to: str, email_subject:str, email_body:str):
        self.mail.init_service(self.google_auth)
        message = self.mail.create_message('gabor.bereczki@icellmobilsoft.hu', send_to, email_subject, email_body)
        self.mail.send_message('me', message)

if __name__ == '__main__':

    gsmain = GSMain()
    args = gsmain.parse_args()
    gsmain.init_google_api(args.oauth_store, args.credential)
    values = gsmain.get_table_content(args.sheet, args.range)
    msg = gsmain.generate_mail_from_template('mail_template.html', values)
    gsmain.send_mail('gabor.bereczki@icell.hu', 'tttt', msg)

