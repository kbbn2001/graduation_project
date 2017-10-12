import os

def dirCheck(path):
	directory = os.path.dirname(path)
	try:
		os.stat(directory)
	except:
		os.mkdir(directory)

def enc_tem(ctem):
	return (ctem-(-15))/60

def dec_tem(ktem):
	return (60*ktem)-15

