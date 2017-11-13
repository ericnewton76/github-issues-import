import urllib.request, urllib.error, urllib.parse
import json
import base64
import sys, os
import datetime
import argparse, configparser
import time

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
default_config_file = os.path.join(__location__, 'config.ini')
config = configparser.RawConfigParser()

def init_config():
	
	config.add_section('login')
	config.add_section('source')
	config.add_section('target')
	config.add_section('format')
	config.add_section('settings')
	
	def load_config_file(config_file_name):
		try:
			config_file = open(config_file_name)
			config.read_file(config_file)
			return True
		except (FileNotFoundError, IOError):
			return False
			
	config_file_name = "config.ini"
	if load_config_file(config_file_name):
		print("Loaded options from default config file in '%s'" % config_file_name)
	else:
		print("Default config file not found in '%s'" % config_file_name)
		print("You may be prompted for some missing settings.")
	
def get_rate_limit(which):

	username = "ericnewton76" #config.get(which, 'username')
	password = "c00lstuf"     #config.get(which, 'password')

	rate_req = urllib.request.Request('https://api.github.com/rate_limit', None)
	rate_req.add_header("Authorization", b"Basic " + base64.urlsafe_b64encode(username.encode("utf-8") + b":" + password.encode("utf-8")))

	rate_req.add_header("Content-Type", "application/json")
	rate_req.add_header("Accept", "application/vnd.github.v3+json")

	rate_req.add_header("User-Agent", "IQAndreas/github-issues-import")

	rate_response = urllib.request.urlopen(rate_req)
	rate_datastr = rate_response.read()

	print("rate_datastr:",rate_datastr)
	rate_data = json.loads(rate_datastr.decode("utf-8"))

	return rate_data
	
def wait_period(which):
	rate_data = get_rate_limit(which)
	
	core_limits = rate_data['resources']['core']
	
	print(core_limits)

init_config()
get_rate_limit("target")
