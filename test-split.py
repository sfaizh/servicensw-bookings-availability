#!/usr/bin/python
from datetime import datetime
import functools

# newTime
input = "Fri 13/09|8:05 am"

getTime = input.split('|',1)[1]
timeRaw = getTime.split(' am',1)[0]
'''
oldTime = datetime.strptime(timeRaw, "%H:%M").time()
newTime = oldTime.replace(hour=10, minute=5, second=0, microsecond=0)

print(oldTime)
# check both time objects
if(newTime > oldTime): # 10:05 > 8:05
        oldTime = newTime # set old time before loop to newTime

getDate1 = input.split('|',1)[0]
dateRaw = getDate1.split(' ',1)[1]
oldDate = datetime.strptime(dateRaw, "%d/%m").date()
'''



print(getTime.split(' ',1)[1])
