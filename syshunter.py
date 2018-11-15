# This script will search for systems running after work hours and send email.
import csv
import subprocess
import logging
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("syshunter.log"),
        logging.StreamHandler()
    ])

#function to send emails
def send_email(toaddr,username,time):
    fromaddr = "from eamil id"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Leave It Turned On"
    body = """Hi {u},<br>
You've been caught working after hours.
Your system is still running at "{d}"
""".format(u=username,d=time)
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP_SSL('smtp server ', port)
    server.ehlo()
    server.login('from email id', 'password')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

#function to ping hosts passed to it
def check_ping(staticIPaddress):
    hostname = staticIPaddress
    response = subprocess.call("ping -w1 -c1 " + hostname, shell=True)

    if response == 0:
        return True
    else:
        return False

#This is what will store all the IP, username, and email info
database = dict()

#Open the csv, make sure to change the name of the csv file here.
with open('users.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for eachRow in reader:
        #eachRow returns a list of each row
        #ex: ['192.168.1.1', 'username', 'username@company.com']

        #assign the first value in the list of each row as a key name
        staticIPaddress = eachRow[0]
        #Create a key for the IP and assign the username and email values to it
        database[staticIPaddress] = [eachRow[1] , eachRow[2]]

#This creates a list of every key in database / each IP found in the csv file
listofIPs = database.keys()

for eachIP in listofIPs:
    #ping each IP in the dictionary of IPs
    pingstatus = check_ping(eachIP)
    
    #if the ping was successful send the email
    if pingstatus:
        #This grabs the email address and username of the computer that is up
        #                  0          1
        # {192.168.1.1 : 'user1' , 'user1@company.com}
        username = database[eachIP][0]
        email = database[eachIP][1]
        dateo = datetime.datetime.now().ctime()
        logging.info("{u} system still running at {date}".format(u=username, date=dateo))
        send_email(email,username,dateo)