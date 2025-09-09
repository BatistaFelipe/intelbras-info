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

def reboot(host, digest_auth):
	url = 'http://%s/cgi-bin/magicBox.cgi?action=reboot' % host
	res = requests.get(url, auth=digest_auth)
	return res.text + '\n'

def main():
	digest_auth = requests.auth.HTTPDigestAuth(USER, PASSWORD)
	host = input("<IP:porta>: ").strip().lower()

	while True:
		print(
			"---------------------------------\n"+
			"HOST: " + host + "\n" +	
			"---------------------------------\n"+
			"| 1. Informações gerais 	|\n"+
			"| 2. Informações sip 		|\n"+
			"| 3. Data e hora 		|\n"+
			"| 4. Ajustar data e hora 	|\n"+
			"| 5. Reiniciar 			|\n"+
			"| 0. Sair 			|\n"+
			"---------------------------------\n")
		opt = input("Digite: ").strip()
		if opt == "0":
			break
		elif opt == "1":
			info = getSystemInfo(host, digest_auth)
			print(info)
		elif opt == "2":
			sip = getConfigSip(host, digest_auth)
			print(sip)
		elif opt == "3":
			datetime = getCurrentTime(host, digest_auth)
			print(datetime)
		elif opt == "4":
			setCurrentTime(host, digest_auth)
			datetime = getCurrentTime(host, digest_auth)
			print(datetime)
		elif opt == "5":
			res = reboot(host, digest_auth)
			print(res)
		else:
			print("\nOpção inválida!\n")

if __name__ == '__main__':
	main()
