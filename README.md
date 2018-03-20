# Demo Work

# Requirement:
	OS: Windows 7 + 
	Database : MongoDB Community Edition.
	Tools: Python 3.6 (Anaconda 3 is recommended).
	
# Module used:
	pymongo
	json
	falcon
	BeautifulSoup
	jwt
	datetime import datetime
	waitress(for hosting)

# How to run:
	open and run file waitressServer.py 
	goto localhost:8000
	
	Username = Could be anythings.
	password = 1234
	
# Note
	Data directory is store at default location(C:\data\db).
	Name of Database and Collection of this Demo are testDB and testCOL.
	JWT duration is set to expire in 30 seconds, this can be change by editing file content.py (line 14).
	
# Reminder
	localhost:8000 -- login page
	localhost:8000/home -- homepage
	localhost:8000/contents -- show all datas that store in testCOL.
	
	
	
	


