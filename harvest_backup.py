import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
sys.path.append("packages")
#from Harvest.harvest import Harvest, HarvestError
import os
from harvest import Harvest, HarvestError
from datetime import datetime, timedelta
import time
#import simplejson as json
import json
import mysql.connector
from mysql.connector import errorcode
#import pprint

# Harvest Setup
#harvest_creds = json.loads(open('harvest.json').read())
harvest_creds = json.loads(os.getenv("HARVEST"))
URI = harvest_creds['uri']
EMAIL = harvest_creds['email']
PASS = harvest_creds['password']
h = Harvest(URI,EMAIL,PASS)

# Var Setup
user_hours={}
user_names={}
project_hours={}
timesheet_punches={}
email_html=""

# Yesterday - adjust to your liking
end = datetime.today().replace( hour=0, minute=0, second=0 )
start = end + timedelta(-1)

#mysql_creds = json.loads(open('mysql.json').read())
mysql_creds = json.loads(os.getenv("MYSQL"))
cnx = mysql.connector.connect(user=mysql_creds['user'],
                              password=mysql_creds['password'],
                              host=mysql_creds['host'],
                              database=mysql_creds['database'])
cursor = cnx.cursor()
    

    
try:
    for user in h.users():
        user_hours[user.email] = 0
        user_names[user.email] = user.first_name + " " + user.last_name
        for entry in user.entries( start, end ):
            if(not entry.adjustment_record):
                user_hours[user.email] += entry.hours                                
                project = h.project(entry.project_id)
                client = h.client(project.client_id)
                task = h.task(entry.task_id)
                if(project_hours.has_key(project.name)):
                    project_hours[project.name] += entry.hours
                else:
                    project_hours[project.name] = entry.hours

                add_entry = ("INSERT INTO timesheet "
                             "(id, project_id, task_id, user_id, hours, "
                             "notes, client, created_at, updated_at, project, task) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )")
            
                entry_data = (entry.id, project.id, entry.task_id, entry.user_id, entry.hours,
                              entry.notes, client.name, entry.created_at, entry.updated_at, project.name, task.name)
                cursor.execute(add_entry, entry_data)
                #print cursor.lastrowid
                cnx.commit()

except HarvestError:
    print "error"

cursor.close()
cnx.close()
