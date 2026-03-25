from datetime import datetime
import os
import time
import logging
import cv2
import random
import string
import urllib.request
from cam_config import *
TGT_DIR = "data/"
tgt_log_fn = "tl.log"
tgt_log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=TGT_DIR+tgt_log_fn,format=tgt_log_format,level=logging.INFO)


#https://192.168.6.219/cgi-bin/api.cgi?cmd=Snap&channel=1&iLogicChannel=1&snapType=main
#&rs=(any combination of numbers and letters)&user=admin&password=(user password)
def get_snapshot():
	tgt_url = "http://" + tgt_ip
	tgt_url += "/cgi-bin/api.cgi?cmd=Snap"
	tgt_url += "&channel=0&iLogicChannel=1&snapType=main"
	characters = string.ascii_letters + string.digits
	random_string = ''.join(random.choices(characters, k=32))
	tgt_url += "rs="+random_string + "&"
	tgt_url += "&user="+tgt_username
	tgt_url += "&password="+tgt_password

	now = datetime.now()
	cur_date = now.strftime("%Y-%m-%d")
	cur_time = now.strftime("%H_%M_%S.jpg")
	print(tgt_url)
	tgt_file_path = TGT_DIR + cur_date +"/"+cur_time
	print(tgt_file_path)
	try:
		urllib.request.urlretrieve(tgt_url, tgt_file_path)
		print(f"Image successfully downloaded and saved to {tgt_file_path}")
	except Exception as e:
		print(f"An error occurred: {e}")

for i in range(0,5):
	now = datetime.now()
	cur_date = now.strftime("%Y-%m-%d")
	cur_dir = TGT_DIR+cur_date
	if not os.path.exists(cur_dir):
		logging.info("creating dir " + cur_dir)
		os.makedirs(cur_dir)
	get_snapshot()
	time.sleep(1)




logging.info("done")