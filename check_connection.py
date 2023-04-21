#!./venv/bin/python
import subprocess
import os
import datetime

###
# 
#           In order to ensure that a particular web server is
#           always connected to the network, I have made this simple script to 
#           ping Google's DNS server (8.8.8.8) 15 times and email the return code and output text of the 
#           ping command to email. This could be ran by cronjob.
#
#           No email would means the server is not online. Furthermore, a local log is maintained, so 
#           the local admin can know when the disconnection happened.
#
#           Please configure the .env file.
#               EMAIL_PASSWORD=""
#               EMAIL_SENDER=""
#               EMAIL_RECEIVER=""
#
#           Email password may have to be setup with your email host like Gmail or Hotmail
#           Also, port might have to change depending on email host.
#
#           Make sure python-dotenv is installed to the local virtual environment.
#               python3 -m venv venv
#               source venv/bin/activate
#               pip install python-dotenv 
#
# ###


# Ping Google DNS Server (8.8.8.8)

def ping_google():
    ping = subprocess.Popen(['ping', "8.8.8.8", "-c", "15"], stdout=subprocess.PIPE)
    return ping

# Doing the two ping processes and storing them in vars
google_ping = ping_google()

# Getting text output
google_ping_output = google_ping.communicate()[0]

# Getting exit code and setting Sucess as true or false
google_ping_returncode = google_ping.returncode

success = False

if google_ping_returncode == 0:
    success = True

### 
# 
# Local Logging Portion 
# 
# ###

log_path = os.path.join(os.getcwd(), "logs", "google_dns_ping_errors.txt")

if not os.path.exists(log_path):
    with open(log_path, "w") as f:
        f.write("Error Log for Google DNS Failed Pings with date")

with open(log_path, "a") as f:
    if google_ping_returncode != 0:
        f.write(f"\n{datetime.datetime.now()} - Failed")

### 
# 
# Email Portion
# 
# ###

import smtplib
from dotenv import load_dotenv

load_dotenv()

port = 465
email_password = os.getenv("EMAIL_PASSWORD")

sender_mail = os.getenv("EMAIL_SENDER")
receiver_email = os.getenv("EMAIL_RECEIVER")
smtp_server_host = "smtp.gmail.com"
message = f"""\
    Subject: Ping Google DNS result {datetime.datetime.now()}

    
    Successfull: {success}
    Returncode was: {google_ping_returncode}

    Command Output: {google_ping_output}
    """

with smtplib.SMTP_SSL(smtp_server_host, port) as server:
    # server.starttls()
    server.login(sender_mail, email_password)
    server.sendmail(sender_mail, receiver_email, message)

###
#
#       That's it. Please, any feedback or improvments are appricated.
#       - Jamie Lynn
#
###


