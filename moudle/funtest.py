__author__ = 'fuqiang'

import tablib
import time
import datetime

headers = ('first_name', 'last_name')

data = [

]

data = tablib.Dataset(*data, headers=headers)
data.json = '[{"last_name": "Adams","first_name": "John"},{"last_name": "fff","first_name": "hhh"}]'
print data.json
#open('people.xls', 'wb')

ff='[{"id":"sd<br>sd"}]'
print(ff)
dd=ff.replace('<br>','\n')
print dd
print(time.time())