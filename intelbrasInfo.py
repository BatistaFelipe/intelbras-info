#!/usr/bin/env python3

import requests
from datetime import datetime
from config import USER, PASSWORD

# Intelbras API https://intelbras-caco-api.intelbras.com.br/

def getSystemInfo(host, digest_auth):
	url = 'http://%s/cgi-bin/magicBox.cgi?action=getSystemInfo' % host
	res = requests.get(url, auth=digest_auth)
	return res.text

def getConfigSip(host, digest_auth):
	url = 'http://%s/cgi-bin/configManager.cgi?action=getConfig&name=SIP' % host
	res = requests.get(url, auth=digest_auth)
	return res.text

def getCurrentTime(host, digest_auth):
	url = 'http://%s/cgi-bin/global.cgi?action=getCurrentTime' % host
	res = requests.get(url, auth=digest_auth)
	return res.text

def setCurrentTime(host, digest_auth):
	try:
		current_datetime = datetime.today().strftime('%Y-%m-%d') + '%20' + datetime.today().strftime('%H:%M:%S')
		url = "http://{}/cgi-bin/global.cgi?action=setCurrentTime&time={}".format(str(host), str(current_datetime),)     
		res = requests.get(url, auth=digest_auth, stream=True, timeout=20, verify=False)
		if res.status_code != 200:
			raise Exception()
		return str(res.text)
	except Exception:
		raise Exception("ERROR - During Set Current Time")

def main():
	digest_auth = requests.auth.HTTPDigestAuth(USER, PASSWORD)

	host = input("<IP:porta>: ").strip().lower()

	info = getSystemInfo(host, digest_auth)
	sip = getConfigSip(host, digest_auth)
	datetime = getCurrentTime(host, digest_auth)

	print('--------------------------')
	print(info)
	print('--------------------------')
	print(sip)
	print('--------------------------')
	print(datetime)
	print('--------------------------')

	ask_to_update_time = str(input('Atualizar dia/hora? (S/N) '))
	while True:
		if ask_to_update_time.upper() == 'S':
			setCurrentTime(host, digest_auth)
			datetime = getCurrentTime(host, digest_auth)
			print('--------------------------')
			print(datetime)
			print('--------------------------')
			break
		elif ask_to_update_time.upper() == 'N':
			break
		else:
			ask_to_update_time = str(input('Atualizar dia/hora? (S/N) '))

if __name__ == '__main__':
	main()
