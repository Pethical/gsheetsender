GSheet Sender
============
Send google sheet content in mail, based on html email template.

## The project contain sample implementation for
- spreadsheet api usage, read content from google spread sheet.
- gmail api usage, send email by gmail api
- google api authentication
- HTML Email message rendering by jinja2 template

The tool is export google sheet content, build and email from template and send them.

## PreReqs
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- oauth2client
- jinja2

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client jinja2
```


### Create Google creditials info
Quick guide to use GSuite APIs:
[Access to GSuite APIs](https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#5)  

You have to create (or use an exists) a project and enable google APIs (Google Sheets API, Gmail API) in [Google developer console](https://console.developers.google.com/projectselector2/apis/dashboard)
and create and download oauth credential json.  

Sample script
```
gsheetsender.py --credential=client_secret.json --oauth_store=storage.json --sheet=sheetlongid --range=Sheet1!A2:P --email_config=email_config.json
```

## Parameters
```
  --oauth_store OAUTH_STORE
                        Google oauth token store json file
  --credential CREDENTIAL
                        Google credential json file for oauth
  --sheet SHEET         Google sheet id
  --range RANGE         Range from sheet. example: Sheet1!A1:R.
                        [sheet]![left]:[right]
  --email_config EMAIL_CONFIG
                        Email config json file
```
#### oauth_store
json file for store info for oauth processes to authentication and authorization.
If the file not exists the script will create them. 
If the store json not exists or not contain valid credential, 
the script will open a browser and start the google login/auth and permission granting process.  
This will tipically run first time usage.
#### credential
You can download this file from google developer console. 
This contain the client_id and client_secret for this application.
#### sheet
Google sheet document id.  
This is a long id.
#### range
The email will contain the datas from this cell range of the sheet.  
The range structure: [sheet name]![left/top corner]:[right/bottom corner]
Ex: Sheet1![A1:Z3] or Sheet1![A1:Z]
If you left the row number from right bottom corner section the api automatically calculate it by filled rows in sheet.

#### email_config
This is a json config file contain the parameters to mail sending.  
**Sample json**
```
{
	"template_dir": "/tmp/template",
	"send_from": "test@test.com",
	"send_to": "test_to@test.com",
	"subject": "Test mail"
}
```
- template_dir: The directory contain **mail_template.html**. The tool looking for the **mail_template.html** jinja2 template file in this folder.
- send_from: **from** email header
- send_to: **to** email header
- subject: **subject** email header

The email body will generate from template. Template can use the datas read from spreadsheet range.  
The template can use **values** array variable contain the values.

**template sample  detail** 
```
{% for value in values %}
 <tr>
  <td>{{ value[0] }}</td>
  <td>{{ value[1] }}</td>
  <td>{{ value[2] }}</td>
 </tr>
{% endfor %}
```
