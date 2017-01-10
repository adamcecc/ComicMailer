#Copyright Adam Cecchetti 2016

import smtplib
import time
import shutil
import os 
from HTMLParser import HTMLParser 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

comicList = []  

class ComicHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		index = 0 
		if tag == "img":
			for attr in attrs:
				if attr[0] == "src":
					comicList.insert(index, attr[1]) 	
					index = index + 1

class EmailMeImages(object): 
	filePath = "/path/to/dosage/comics"
	toEmail = ""
	fromEmail = ""
	smtpServer = ""
	smtpLogin = ""
	#quick and dirty, don't do this. 
	smtpPassword = ""
	date = time.strftime("%Y%m%d") 
	comicFile = '%scomics-%s.html' % (filePath, date)

	def getComicsList(self):
		#open file find all comics 
		fp = open(self.comicFile) 
		parser = ComicHTMLParser()
		contents = fp.read() 
		parser.feed(contents) 
		fp.close() 
		

	def sendEmail(self):
		msg = MIMEMultipart() 
		for comic in comicList: 
			fp = open(comic.replace("file:/", ""), 'rb')
			img = MIMEImage(fp.read())
			fp.close()
			msg.attach(img)


		# me == the sender's email address
		# you == the recipient's email address
		msg['Subject'] = 'Comics for %s' % time.strftime("%d/%m/%Y")
		msg['From'] = self.fromEmail 
		msg['To'] = self.toEmail 

		# Send the message via our own SMTP server, but don't include the
		# envelope header.
		s = smtplib.SMTP_SSL(self.smtpServer)
		s.login(self.fromEmail, self.smtpPassword) 
		s.sendmail(self.fromEmail, [self.toEmail], msg.as_string())
		s.quit()


comicMailer = EmailMeImages() 
comicMailer.getComicsList()
comicMailer.sendEmail()
