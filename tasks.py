from celery import Celery
import requests
from mail_parser import mail_parser
import json
from config import BASE_API, BASE_ZOHO, AUTH_ZOHO

app = Celery('tasks')
app.config_from_object('config')


@app.task
def print_hello():
    print('hello there')


@app.task
def get_unread_emails():
	read_mail = []
	mail_list = []
	request_url =  BASE_ZOHO + "/messages/view?AUTHTOKEN=" + AUTH_ZOHO + "&includeTo=true&status=unread&sortorder=true"
	unread_mails = requests.get(request_url)
	mail_object = unread_mails.json().get('data')
	headers = {'content-type': "application/json"}
	for mail in mail_object:
		mail_list.append([mail.get('messageId'), mail.get('folderId'), mail.get('toAddress'), mail.get('fromAddress')])

	for mail in mail_list[:-1]:
		content_request = BASE_ZOHO + "/folders/%s/messages/%s/content?AUTHTOKEN=" %(mail[1], mail[0]) + AUTH_ZOHO
		content = requests.get(content_request)
		mail_content = content.json().get('data').get('content')
		event_data = mail_parser(mail_content)

		if event_data:
			read_mail.append(str(mail[0]))
			event_data["from"] = mail[3]
			event_data["email_list"] = mail[2].replace('&lt;', '').replace('&gt;', '').split(',')
			create_request = BASE_API + "/v1/create-event-from-email"
			event_create = requests.post(create_request, data = json.dumps(event_data), headers = headers)


	read_request = BASE_ZOHO + "/updatemessage?AUTHTOKEN=" + AUTH_ZOHO
	payload = {"mode": "markAsRead", "messageId": read_mail}
	print(payload)
	mark_read = requests.put(read_request, data = json.dumps(payload), headers = headers)

	print(mark_read)




