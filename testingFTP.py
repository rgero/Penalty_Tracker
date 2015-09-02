''' This file is for me to test how to use the built-in FTP module '''
import sys
from ftplib import FTP
from credientials import *


try:
	#There are a couple ways I can do the storing of the login data.
	print 10/0
	if ( len(sys.argv) < 5 ):
		address = credientials["address"]
		user = credientials["username"]
		password = credientials["password"]
		filename = sys.argv[1]
	else:
		address = sys.argv[1]
		user = sys.argv[2]
		password = sys.argv[3]
		filename = sys.argv[4]

	ftp = FTP(address)
	ftp.login(user, password)
	ftp.storlines("STOR " + filename, open(filename, 'r'))
	ftp.close()
except:
	file = open("Error.txt", 'w')
	errorLog = sys.exc_info()
	for i in errorLog:
		file.write(str(i) + "\n")
	file.close()