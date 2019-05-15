GSheet Sender
============
Send google sheet content in mail, based on html email template.

## The project contain sample implementation for
- google spreadsheet api usage, read content from google spread sheet.
- gmail api usage, send email by gmail api
- google drive api usage
- google api authentication
- HTML Email message rendering by jinja2 template

The tool is export google sheet content, build and email from template and send them.

## Install
Local version can be installed running
```
sudo python3 setup.py install [--record files.txt]
```

Local develop version can be uninstalled running
```
sudo cat files.txt | sudo xargs rm -rf
```
if previously option "--record files.txt" was used at previous installation.

### PreReqs
The setup will install this modules.

- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- oauth2client
- jinja2

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client jinja2
```


### Create Google credential info
Quick guide to use GSuite APIs:
[Access to GSuite APIs](https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#5)  

You have to create (or use an exists) a project and enable google APIs (Google Sheets API, Gmail API) in [Google developer console](https://console.developers.google.com/projectselector2/apis/dashboard)
and create and download oauth credential json.  

## Usage
Sample script
```
gsheetsender.py --credential=client_secret.json --oauth_store=storage.json --sheet=[sheetlongid] --range=Sheet1!A2:P --email_config=email_config.json
```

### Parameters
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
	"subject": "Test mail",
	"add_attachment": false,
	"attachment_file_name": "release_plan.xlsx",
	"named_ranges": "release_table=Projects!A2:D4",
	"cell_values": "example_cell=Example!K3"	
}
```
- template_dir: The directory contain **mail_template.html**. The tool looking for the **mail_template.html** jinja2 template file in this folder.
- send_from: **from** email header
- send_to: **to** email header. More mail address can add with , separator.
- subject: **subject** email header
- add_attachment: **logical value**. If true sheet will attached to mail as xlsx document
- attachment_file_name: **file name** of attachment. Used if add_attachment is true
- named_ranges: range list with name. Can use this ranges from template. Syntax: [name]=[sheet]![left/top corner]:[right/bottom corner]. More range can add with , separator.
- cell_values: Cell list with name. Syntax: [name]=[sheet]![cell]. More cell can add with , separator.


The email body will generate from template. Template can use the datas read from spreadsheet range.  
The template can use **values** array variable contain the values.

**template sample detail** 
```
{% for value in values %}
 <tr>
  <td>{{ value[0] }}</td>
  <td>{{ value[1] }}</td>
  <td>{{ value[2] }}</td>
 </tr>
{% endfor %}
```

**named_range usage sample**  
sample config in json:
	"named_ranges": "release_table=Projects!A2:D4,other_table=OtherSheet!C3:G",

Can refer to this values from template under the named_ranges template variable.
In this sample the template can access the values as **named_ranges**.release_table and **named_ranges**.other_table.  
"release_table" and "other_table" are the names of the ranges defined in named_ranges option.

Use this range values from template
```
<table>
{% for value in named_ranges.release_table %}
  <tr>
  <td>{{ value[0] }}</td>
  <td>{{ value[1] }}</td>
  <td>{{ value[2] }}</td>
 </tr>
{% endfor %}
</table>
Some static text in template... :)
----------
<table>
{% for value in named_ranges.other_table %}
  <tr>
  <td>{{ value[0] }}</td>
  <td>{{ value[1] }}</td>
  <td>{{ value[2] }}</td>
 </tr>
{% endfor %}
</table>
```

**cell_values usage sample**  
sample config in json:
	"cell_values": "example_cell=Projects!A2,other_cell=OtherSheet!C3",

Can refer to this values from template under the cell_values template variable.
In this sample the template can access the values as **cell_values**.example_cell and **cell_values**.other_cell.  
"example_cell" and "other_cell" are the names of the cells defined in cell_values option.

Use this cell values from template
```
<p>Example cell value:</p>
<p>{{cell_values.example_cell}}</p>
<br>
<p>And the other cell value:</p>
<p>{{cell_values.other_cell}}</p>

```
