#!/usr/bin/python

# Send email to me with RMS booking information
import subprocess
from datetime import datetime
import os

from json import loads
from urllib.request import urlopen
import time
import smtplib
from smtplib import SMTPException

location = os.getcwd() + '/getEarliestAvailableDate.js'
data_prev = 'Thurs 14/01|12:00 pm'
#data_prev = "Fri 13/09|8:05 am"

print (data_prev)

while True:
        time.sleep(500)
        # Check for time change
        data_next = subprocess.check_output('sudo node ' + location, shell=True).decode("utf-8").rstrip()
        while not data_next:
                print("Booking call function failed, trying again...")
                data_next = subprocess.check_output('sudo node ' + location, shell=True).decode("utf-8").rstrip()
        print (data_next)
        #data_next = "Fri 13/09|7:05 am" # data_next is the newTime for the working code.

        #Get time value
        getTime1 = data_prev.split('|',1)[1]
        timeRaw1 = getTime1.split(' ',1)[0]
        oldTime = datetime.strptime(timeRaw1, "%H:%M").time()

        #Get date value
        getDate1 = data_prev.split('|',1)[0]
        dateRaw1 = getDate1.split(' ',1)[1]
        oldDate = datetime.strptime(dateRaw1, "%d/%m").date()

        #Get time value
        getTime2 = data_next.split('|',1)[1]
        timeRaw2 = getTime2.split(' ',1)[0]
        newTime = datetime.strptime(timeRaw2, "%H:%M").time()

        #Get date value
        getDate2 = data_next.split('|',1)[0]
        dateRaw2 = getDate2.split(' ',1)[1]
        newDate = datetime.strptime(dateRaw2, "%d/%m").date()

        #newTime = oldTime.replace(hour=10, minute=5, second=0, microsecond=0)

        if (newDate.month == oldDate.month):# check if date month is the same
                if (newDate.day < oldDate.day) and (newDate.day > 8) and (newDate.day <= 14):# check if date day is earlier
                        data_prev = data_next
                        print ("Found earlier DAY!")
                        #print (data_prev) # this should show 7:05 time
                        try:
                                server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                server_ssl.ehlo()
                                server_ssl.login("fsocietypriv@gmail.com", "Faizan360")
                                SUBJECT = "NEW RMS DAY " + data_next
                                msg = "Subject: {}\n\n{}".format(SUBJECT, SUBJECT, "Earlier day available: " + data_next)

                                server_ssl.sendmail("fsocietypriv@gmail.com", "faizanh53@gmail.com", msg)
                                print("Successfully sent email!")
                                #time.sleep(1800)
                        except SMTPException:
                                print("Something went wrong...")

                elif (newDate.day == oldDate.day) and (newDate.day > 8) and (newDate.day <= 14): # if same day, check if time is earlier
                        #if(((getTime1.split(' ',1)[1] == "am") and (getTime2.split(' ',1)[1] == "am")) or ((getTime1.split(' ',1)[1] == "pm") and (getTime2.split(' ',1)[1] == "pm"))): # check if both am or pm
                        if(newTime < oldTime): # 7:05 < 8:05
                                #oldTime = newTime
                                print ("Found earlier TIME!")
                                data_prev = data_next
                                oldTime = newTime
                                try:
                                        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                        server_ssl.ehlo()
                                        server_ssl.login("fsocietypriv@gmail.com", "Faizan360")
                                        SUBJECT = "NEW RMS TIME " + data_next
                                        msg = "Subject: {}\n\n{}".format(SUBJECT, "Earlier time available on same day: " + data_next)
                                        
                                        server_ssl.sendmail("fsocietypriv@gmail.com", "faizanh53@gmail.com", msg)
                                        print("Successfully sent email!")
                                        #time.sleep(1800)
                                except SMTPException:
                                        print("Something went wrong...")
                        #else:
                               #print ("No earlier time available since last check") 
                        #elif (((getTime1.split(' ',1)[1] == "am") and (getTime2.split(' ',1)[1] == "pm")) or ((getTime1.split(' ',1)[1] == "pm") and (getTime2.split(' ',1)[1] == "am"))): # not both am or pm
                                # do required subtractions
                else:
                        print ("Latest date taken - Rollback day to earliest available")
                        data_prev = data_next
                        oldTime = newTime
			# Could be that the latest time has been taken, so we need to rollback to the last available time
                        # This use case only happens if the newest date retrieved has been filled and we are left with a later date.
                        #print ("No earlier date available since last check")
        elif (newDate.month > oldDate.month):# new year special case
                print ("Found earlier DAY!")
                data_prev = data_next
                try:
                        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        server_ssl.ehlo()
                        server_ssl.login("fsocietypriv@gmail.com", "Faizan360")
                        SUBJECT = "NEW RMS DAY " + data_next
                        msg = "Subject: {}\n\n{}".format(SUBJECT, SUBJECT, "Earlier day available: " + data_next)

                        server_ssl.sendmail("fsocietypriv@gmail.com", "faizanh53@gmail.com", msg)
                        print("Successfully sent email!")
                        #time.sleep(1800)
                except SMTPException:
                        print("Something went wrong...")
        else:
                 # This use case only happens if the newest date retrieved has been filled and we are left with a later date.
                print ("Latest date taken - Rollback month to earliest available")
                data_prev = data_next
                oldTime = newTime