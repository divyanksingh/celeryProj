from bs4 import BeautifulSoup
from datetime import datetime


def mail_parser(mail_content):
	event_data = {}
	soup = BeautifulSoup(mail_content, "html.parser")
	string_arr =list(soup.stripped_strings)
	if len(string_arr) < 4:
		return None
	try:	
		event_data["title"] = string_arr[0]
		date_str = string_arr[1]
		event_data["duration"] = string_arr[2]
		event_data["timezone"] = string_arr[3]
		date_obj = datetime.strptime(date_str, '%Y-%m-%d %I:%M %p')
		event_data["start_date_time"] = date_obj.strftime('%Y-%m-%d %H:%M:%S')
	except Exception as e:
		return None
		
	return event_data

def mail_cleaner(email):
	start = '&lt;'
	end = '&gt;'
	mail_list = []
	components = email.split(',')
	for s in components:
		mail_list.append(s[s.find(start)+len(start):s.rfind(end)])
	return mail_list
		