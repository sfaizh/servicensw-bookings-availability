#!/usr/bin/python

# Send email with RMS booking information
import subprocess
from datetime import datetime

from json import loads
from urllib.request import urlopen
import time
import smtplib
from smtplib import SMTPException

data_prev = subprocess.check_output('sudo node ~/Documents/getEarliestAvailableDate.js', shell=True).decode("utf-8").rstrip()
#data_prev = "Fri 13/09|8:05 am"
#Get time value
getTime1 = data_prev.split('|',1)[1]
timeRaw1 = getTime1.split(' ',1)[0]
oldTime = datetime.strptime(timeRaw1, "%H:%M").time()

#Get date value
getDate1 = data_prev.split('|',1)[0]
dateRaw = getDate1.split(' ',1)[1]
oldDate = datetime.strptime(dateRaw, "%d/%m").date()

print (data_prev)

while True:
        time.sleep(300)
        # Check for time change
        data_next = subprocess.check_output('sudo node ~/Documents/getEarliestAvailableDate.js', shell=True).decode("utf-8").rstrip()
        #data_next = "Fri 13/09|7:05 am" # data_next is the newTime for the working code.

        #Get time value
        getTime2 = data_next.split('|',1)[1]
        timeRaw2 = getTime2.split(' ',1)[0]
        newTime = datetime.strptime(timeRaw2, "%H:%M").time()

        #Get date value
        getDate2 = data_next.split('|',1)[0]
        dateRaw2 = getDate2.split(' ',1)[1]
        newDate = datetime.strptime(dateRaw2, "%d/%m").date()

        #newTime = oldTime.replace(hour=10, minute=5, second=0, microsecond=0)

        if (newDate.month <= oldDate.month):# check if date month is earlier
                if (newDate.day < oldDate.day):# check if date day is earlier
                        data_prev = data_next
                        print ("Found earlier DAY!")
                        print (data_prev) # this should show 7:05 time
                        try:
                                server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                server_ssl.ehlo()
                                server_ssl.login("", "")
                                SUBJECT = "NEW RMS DAY " + data_next
                                msg = "Subject: {}\n\n{}".format(SUBJECT, SUBJECT, "Earlier day available: " + data_next)
                                server_ssl.sendmail("", "", msg)
                                print("Successfully sent email!")
                                #time.sleep(1800)
                        except SMTPException:
                                print("Something went wrong...")

                elif (newDate.day == oldDate.day): # if same day, check if time is earlier
                        #if(((getTime1.split(' ',1)[1] == "am") and (getTime2.split(' ',1)[1] == "am")) or ((getTime1.split(' ',1)[1] == "pm") and (getTime2.split(' ',1)[1] == "pm"))): # check if both am or pm
                        if(newTime < oldTime): # 7:05 < 8:05
                                #oldTime = newTime
                                print ("Found earlier TIME!")
                                data_prev = data_next
                                oldTime = newTime
                                try:
                                        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                        server_ssl.ehlo()
                                        server_ssl.login("", "")
                                        SUBJECT = "NEW RMS TIME " + data_next
                                        msg = "Subject: {}\n\n{}".format(SUBJECT, "Earlier time available on same day: " + data_next)
                                        server_ssl.sendmail("", "", msg)
                                        print("Successfully sent email!")
                                except SMTPException:
                                        print("Something went wrong...")
                        else:
                               print ("No earlier date available since last check") 
                        #elif (((getTime1.split(' ',1)[1] == "am") and (getTime2.split(' ',1)[1] == "pm")) or ((getTime1.split(' ',1)[1] == "pm") and (getTime2.split(' ',1)[1] == "am"))): # not both am or pm
                                # do required subtractions
                else:
                        print ("No earlier date available since last check")
        else:
                print ("No earlier date available since last check")
