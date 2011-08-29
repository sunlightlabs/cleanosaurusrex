import csv
import json
import urllib2

res = urllib2.urlopen('http://sunlightfoundation.com/people/?json')
staff = json.load(res)

writer = csv.writer(open('../data/workers.csv', 'w'))
writer.writerow(('first_name','last_name','email'))

for role in ('founders', 'general_staff'):
    for employee in staff[role]:
        if employee['username'] != 'mklein':
            writer.writerow((
                employee['first_name'],
                employee['last_name'],
                employee['email'],
            ))