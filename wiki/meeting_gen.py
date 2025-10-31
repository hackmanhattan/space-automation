import requests
from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta, TH
import pprint
import calendar
import time
pp = pprint.PrettyPrinter(indent=4)
tgt_host = "https://wiki.hackmanhattan.com"
session = requests.session()

USERNAME = ""
PASSWORD = ""
def get_last_wednesdays_of_next_12_months():
	today = date.today()
	last_wednesdays = []

	for i in range(1, 13):
		if today.day == 1:
			target_month_date = date(today.year, today.month, 1)
		else:
			target_month_date = date(today.year, today.month, 1) + timedelta(days=32)
			target_month_date = date(target_month_date.year, target_month_date.month, 1)
		for _ in range(i - 1):
			target_month_date = date(target_month_date.year, target_month_date.month, 1) + timedelta(days=32)
			target_month_date = date(target_month_date.year, target_month_date.month, 1)
		_, num_days = calendar.monthrange(target_month_date.year, target_month_date.month)
		current_day = date(target_month_date.year, target_month_date.month, num_days)
		while current_day.weekday() != calendar.WEDNESDAY:
			current_day -= timedelta(days=1)
		last_wednesdays.append(current_day)
	return last_wednesdays

def get_page_content(tgt_page_title):
	tgt_api = "/api.php?action=query&prop=revisions&rvslots=*&rvprop=content&formatversion=2&format=json"
	tgt_api += "&titles="+tgt_page_title
	tgt_url = tgt_host + tgt_api
	resp = session.get(tgt_url)
	ret_data = resp.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]
	return ret_data
	
def get_login_token():
	tgt_api = "/api.php?action=query&meta=tokens&type=login&format=json"
	tgt_url = tgt_host + tgt_api
	tgt_data = {"lgname":USERNAME}
	tgt_data["lgpassword"] = PASSWORD
	resp = session.get(tgt_url)
	return resp.json()["query"]["tokens"]["logintoken"]

def login(tgt_login_token):
	tgt_api = "/api.php"
	tgt_url = tgt_host + tgt_api
	tgt_data = {"action": "login"}
	tgt_data["lgname"] = USERNAME
	tgt_data["lgpassword"] = PASSWORD
	tgt_data["lgtoken"] = tgt_login_token
	tgt_data["format"] = "json"
	resp = session.post(tgt_url,data=tgt_data)

def get_csrf_token():
	tgt_api = "/api.php"
	tgt_url = tgt_host + tgt_api
	tgt_param = {"action": "query"}
	tgt_param["meta"] = "tokens"
	tgt_param["format"] = "json"
	resp = session.get(tgt_url,params=tgt_param)
	return resp.json()["query"]["tokens"]["csrftoken"]

def edit_page(tgt_page_title, tgt_page_content,tgt_csrf_token,tgt_content_format,tgt_content_model):
	tgt_api = "/api.php"
	tgt_url = tgt_host + tgt_api
	tgt_data = {"action": "edit"}
	tgt_data["title"] = tgt_page_title
	tgt_data["token"] = tgt_csrf_token
	tgt_data["format"] = "json"
	tgt_data["text"] = tgt_page_content
	tgt_data["contentformat"] = tgt_content_format
	tgt_data["contentmodel"] = tgt_content_model
	resp = session.post(tgt_url,data=tgt_data)
	pp.pprint(resp.json())

next_wednesdays = get_last_wednesdays_of_next_12_months()
ltoken = get_login_token()
login(ltoken)
csrf_token = get_csrf_token()
meeting_template_data = get_page_content("Meeting_Template")
for cur_day in next_wednesdays:
	cur_page_title = "Meeting " + cur_day.strftime("%Y-%m-%d")
	print(cur_page_title)
	edit_page(cur_page_title,meeting_template_data["content"],csrf_token,tgt_content_format=meeting_template_data["contentformat"],tgt_content_model=meeting_template_data["contentmodel"])
	time.sleep(3)

