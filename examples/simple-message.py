from O365 import *
import getpass
import json
import argparse

description = '''Welcome to the O365 simple message script! Usage is pretty straight forward.
Run the script and you will be asked for username, password, reciving address,
subject, and then a body. When these have all come and gone your message will
be sent straight way. 

For attachments, include the path to the attachment in the call and the script
will attach the files or crash trying. (hopefully not the latter) 
e.g.: python simple-message.py that_file_you_want_but_could_only_ssh_in.jpg
'''

parser = argparse.ArgumentParser(description=description)
parser.add_argument("--userid", help="user id that will be used to fetch the secret", type=str)
parser.add_argument("--toemail", help="receipient of the email", type=str)
parser.add_argument("--subject", help="email subject", type=str)
parser.add_argument("--body", help="body of the message", type=str)
parser.add_argument("--attachments", help="list of attachments", nargs='+', default=list())

args = parser.parse_args()
userid = args.userid
(uname, password) = O365.creds.getCredentials(userid)
rec = args.toemail
subject=args.subject
body=args.body

#get login credentials that will be needed to send the message.
if not uname:
	uname = raw_input('Enter your user name: ')

if not password:
	password = getpass.getpass('Enter your password: ')

auth = (uname,password)

#get the address that the message is to be sent to.
if not rec:
	rec = raw_input('Reciving address: ')

#get the subject line.
if not subject:
	subject = raw_input('Subject line: ')

#get the body.
if not body:
	line = 'please ignore.'
	body = ''
	print 'Now enter the body of the message. leave a blank line when you are done.'
	while line != '':
		line = raw_input()
		body += line

#Give the authentication to the message as instantiate it. then set it's values.
m = Message(auth=auth)
m.setRecipients(rec)
m.setSubject(subject)
m.setBody(body)

for attachment in args.attachments:
	a = Attachment(path=attachment)
	m.attachments.append(a)

#send the message and report back.
print 'Sending message...'
print m.sendMessage()

