import argparse
import json
from gsheetsender.google_auth import GoogleAuth
from oauth2client import tools
from gsheetsender.gsheet_reader import GSheetReader
from gsheetsender.google_mail import GMail
from gsheetsender.google_drive import GDrive
from jinja2 import Environment, FileSystemLoader


class GSMain:
    email_config = {
        "template_dir": "",
        "send_from": "",
        "send_to": "",
        "subject": "",
    }

    def __init__(self):
        self.google_auth = None
        self.sheet_reader: GSheetReader = GSheetReader()
        self.mail: GMail = GMail()
        self.drive: GDrive = GDrive()
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
        parser.add_argument('--email_config', type=str, help='Email config json file',
                            required=True)

        self.args = parser.parse_args()
        try:
            with open(self.args.email_config, "r") as json_file:
                input_conf = json.load(json_file)
                self.email_config.update(input_conf)
        except Exception as ex:
            raise argparse.ArgumentTypeError(
                "file:{0} is not a valid json file. Read error: {1}".format(self.args.email_config, ex))
        return self.args

    def init_google_api(self, oauth_store, oauth_credential):
        self.google_auth = GoogleAuth(oauth_store)
        self.google_auth.oauth(oauth_credential, GSheetReader.SCOPES+GMail.SCOPES+GDrive.SCOPES, self.args)

    def get_table_content(self, sheet_id: str, cell_range: str):
        self.sheet_reader.init_service(self.google_auth)
        return self.sheet_reader.get_values(sheet_id, cell_range)

    def generate_mail_from_template(self, template_file, table_content):
        j2_env = Environment(loader=FileSystemLoader(self.email_config['template_dir']), trim_blocks=True)
        template = j2_env.get_template(template_file)
        return template.render(values=table_content)

    def get_excel_file(self, file_id):
        self.drive.init_service(self.google_auth)
        content = self.drive.export_xlsx(file_id)
        return content

    def send_mail(self, send_from: str, send_to: str, email_subject: str, email_body: str,
                  attachment_name=None, attachment_content=None):
        self.mail.init_service(self.google_auth)
        message = self.mail.create_message(send_from, send_to, email_subject, email_body,
                                           attachment_name=attachment_name,
                                           attachment_content=attachment_content)
        self.mail.send_message('me', message)


if __name__ == '__main__':

    gsmain = GSMain()
    args = gsmain.parse_args()
    gsmain.init_google_api(args.oauth_store, args.credential)
    values = gsmain.get_table_content(args.sheet, args.range)
    msg = gsmain.generate_mail_from_template('mail_template.html', values)
    file_name = None
    attachment_content = None
    if "add_attachment" in gsmain.email_config.keys() and gsmain.email_config["add_attachment"]:
        file_name = gsmain.email_config["attachment_file_name"]
        attachment_content = gsmain.get_excel_file(args.sheet)

    gsmain.send_mail(gsmain.email_config['send_from'],
                     gsmain.email_config['send_to'],
                     gsmain.email_config['subject'],
                     msg, file_name, attachment_content)
