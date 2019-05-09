from oauth2client import file, client, tools


class GoogleAuth():

    def __init__(self, oauth_store_json: str):
        self.store = file.Storage(oauth_store_json)
        self.creds = self.store.get()

    def oauth(self, credential_json, scope, args):
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets(credential_json, scope)
            self.creds = tools.run_flow(flow, self.store, flags=args)

    def get_store(self):
        return self.store

    def get_credential(self):
        return self.creds