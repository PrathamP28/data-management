run:
	py main.py

test:
	py testing\\test.py 

sql:
	py testing\\testmysql.py

env:
	powershell -NoExit -ExecutionPolicy Bypass -File data_management/Scripts/Activate.ps1