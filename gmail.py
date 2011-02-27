#!/usr/bin/python
#coding:utf-8 
from email.mime.text import MIMEText
import smtplib 

class gmail:
	def __init__(self):	
		pass
	def send_to_gmail (self,title,content):
		server = smtplib.SMTP('smtp.gmail.com' )
		server.docmd("EHLO server" )
		server.starttls()
		server.login('wliment@gmail.com','ZHENGTAO5655327') 
		msg = MIMEText(content)
		msg['Content-Type' ]='text/plain; charset="utf-8"' 
		msg['Subject' ] = title
		msg['From' ] =	'wliment@gmail.com' 
		msg['To' ] = 'wliment@gmail.com'
		server.sendmail('wliment@gmail.com', 'wliment@gmail.com' ,msg.as_string())
		server.close()
