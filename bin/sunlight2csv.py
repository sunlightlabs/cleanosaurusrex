import csv
import json
import sys
import urllib2

AVATAR_URL = "http://assets.sunlightfoundation.com/images/blog/avatars/300/300x300_%s.jpg"

res = urllib2.urlopen('http://sunlightfoundation.com/people/?json')
staff = json.load(res)

writer = csv.writer(sys.stdout)
writer.writerow(('first_name','last_name','email','avatar_url'))

for role in ('founders', 'general_staff'):
    for employee in staff[role]:
        if employee['username'] != 'mklein':
            writer.writerow((
                employee['first_name'],
                employee['last_name'],
                employee['email'],
                AVATAR_URL % employee['username'],
            ))