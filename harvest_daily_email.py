import sys
from Harvest.harvest import Harvest, HarvestError
from datetime import datetime, timedelta
import time
import simplejson as json
import requests
#import pprint

#Mailgun Setup
mailgun_creds = json.loads(open('mailgun.json').read())
mgkey = mailgun_creds['key']
mgdomain = mailgun_creds['domain']
request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(mgdomain)
recipients = json.loads(open('recipients.json').read()).keys()

# Harvest Setup
harvest_creds = json.loads(open('harvest.json').read())
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

t = "<table>"
tr = "<tr>"
td = "<td>"
etr = "</tr>"
etd = "</td>"
et = "</table>"

# Yesterday - adjust to your liking
end = datetime.today().replace( hour=0, minute=0, second=0 )
start = end + timedelta(-1)

try:
        for user in h.users():
                user_hours[user.email] = 0
                user_names[user.email] = user.first_name + " " + user.last_name
                for entry in user.entries( start, end ):
                        user_hours[user.email] += entry.hours                                
                        project = h.project(entry.project_id)
                        client = h.client(project.client_id)
                        if(project_hours.has_key(project.name)):
                                project_hours[project.name] += entry.hours
                        else:
                                project_hours[project.name] = entry.hours
                        timesheet_punches[entry.id] = td + str(user.first_name) + etd + td + str(user.last_name) + etd + td + str(client.name) + etd + td + str(project.name) + etd + td + str(entry.hours) + etd
                                
        email_html += "<br><br>User Hours"
        email_html += t
        for email in sorted(user_names.keys()):
                email_html += tr + td + user_names[email] + etd + td + str(user_hours[email]) + etd + etr
        email_html += et

        email_html += "<br><br>Project Hours"
        email_html += t
        for project in sorted(project_hours.keys()):
                email_html += tr + td + project + etd + td + str(project_hours[project]) + etd + etr
        email_html += et
        
        email_html += "<br><br>Timesheet"
        email_html += t
        for punch in sorted(timesheet_punches.values()):
                email_html += tr + punch + etr
        email_html += et
        
        for recipient in recipients:
                request = requests.post(request_url, auth=('api', mgkey), data={
                        'from': 'timetracker@mg.avatarnewyork.com',
                        'to': recipient,
                        'subject': 'Harvest Daily Report - Yesterday',
                        'text': 'sent via mailgun',
                        'html': email_html
                })
                #print 'Status: {0}'.format(request.status_code)
                #print 'Body:   {0}'.format(request.text)
                
except HarvestError:
        print "error"
