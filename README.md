daily_harvest v2.0
===================

Daily Email Report of Time Entries using the Harvest API and Mailgun API

## Description
v1.0.0 was originally discussed in our workshop blog post here: [Daily Harvest](https://workshop.avatarnewyork.com/project/daily-harvest/).  Since writing that blog post, iron.io has come out with their dockerized worker which we have adopted in this version 2.0.  You can now use this project as either:

1. python script
2. docker app
3. iron.io worker

There are 2 components to daily-harvest.  You can choose to use one or both (they are not interdepentant)

#### daily-harvest:email
Sends an email out to a list of receiptients with detailed timesheets as well as total hours by employee and project.

#### daily-harvest:backup
Replicates the past 24 hours of punches inside a MySQL database table called "timesheet"

## Requirements 
The following services are required:

#### daily-harvest:email
* mailgun account
* email list
* harvest account

#### daily-harvest:backup
* harvest account
* mysql database - you must install `harvest_backup.sql` on a mysql database and make it accessable to the backup app.

## Usage

### Python Execution
This has been tested on python 2.7

1. Install the requirements.  If you have any issues, be sure to have already installed python development libraries for your OS (i.e. python-dev or python-devel).

    ```bash
    pip install -t packages -r requirements.txt
    ```

2. The script reads environment variables rather than passing parameters (this is to keep compliant with docker/iron.io).  Set environment variables as you normally work for you operating system and be sure python has access to them.  The following environment variables are required:

    ```bash
	# HARVEST CREDENCIALS
	HARVEST_URI
	HARVEST_EMAIL
	HARVEST_PASSWORD
	
	# daily-harvest:email
	# MAILGUN SETTINGS
	MAILGUN_KEY=
	MAILGUN_DOMAIN=
	MAILGUN_FROM=
	
	# COMMA SEPARATED LIST OF EMAIL ADDRESSES (NO SPACES)
	RECIPIENTS=
	
	# daily-harvest:backup
	# MYSQL SETTINGS
	MYSQL_USER=
	MYSQL_PASSWORD=
	MYSQL_DATABASE=
	MYSQL_HOST=
	MYSQL_PORT=
	```

3. Run the script

    ```bash
	# Email
	python harvest_email.py
	
	# Backup
	python harvest_backup.py
	```
	
### Docker Execution

1. pull the image

    ```bash
	# Pull the email version
	docker pull docker.io/avatarnewyork/daily-harvest:email
	
	# Pull the backup version
	docker pull docker.io/avatarnewyork/daily-harvest:backup

2. Execute and pass appropriate environment variables

    ```bash
	# Email
	docker run --rm -e 'HARVEST_URI=https://myco.harvestapp.com' -e 'HARVEST_EMAIL=some@email.com' -e 'HARVEST_PASSWORD=secret' -e 'MAILGUN_DOMAIN=mg.mydomain.com' -e 'MAILGUN_KEY=key-asdfkljasdf' -e 'MAILGUN_FROM=timesheets@mg.mydomain.com' -e 'RECIPIENTS=manager@mydomain.com' daily-harvest:email
	
	# Backup
	docker run --rm -e 'HARVEST_URI=https://myco.harvestapp.com' -e 'HARVEST_EMAIL=some@email.com' -e 'HARVEST_PASSWORD=secret' -e 'MYSQL_USER=harvest' -e 'MYSQL_PASSWORD=secretpwd' -e 'MYSQL_DATABASE=harvest' -e 'MYSQL_HOST=72.43.52.10' -e 'MYSQL_PORT=3306' daily-harvest:email
	```

### iron.io Execution

1. Setup your credencials / projectid, etc.  See: http://dev.iron.io/worker/getting_started/
2. Register email

    ```bash
	iron register -e 'HARVEST_URI=https://myco.harvestapp.com' -e 'HARVEST_EMAIL=some@email.com' -e 'HARVEST_PASSWORD=secret' -e 'MAILGUN_DOMAIN=mg.mydomain.com' -e 'MAILGUN_KEY=key-asdfkljasdf' -e 'MAILGUN_FROM=timesheets@mg.mydomain.com' -e 'RECIPIENTS=manager@mydomain.com' daily-harvest:backup
	```
	
3. Register backup

    ```bash
	iron register e 'HARVEST_URI=https://myco.harvestapp.com' -e 'HARVEST_EMAIL=some@email.com' -e 'HARVEST_PASSWORD=secret' -e 'MYSQL_USER=harvest' -e 'MYSQL_PASSWORD=secretpwd' -e 'MYSQL_DATABASE=harvest' -e 'MYSQL_HOST=72.43.52.10' -e 'MYSQL_PORT=3306' daily-harvest:baclkup
	```
	
4. queue / schedule on iron.io.  See: http://dev.iron.io/worker/getting_started/

## v1.0.0 (Deprecated)

For information regarding the v1.0 version, checkout the v1.0.0 branch or tag.
