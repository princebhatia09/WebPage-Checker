from urllib2 import urlopen
from hashlib import md5
from os import path
import smtplib

stateFilePath = "/tmp/.pageChecker"

def send_email(receiver, subject, body):
    sender = "samet.atdag@mynet.com"
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"
        %(sender, receiver, subject, body))
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [receiver], msg)
    s.quit()


def saveStateFile(stateFilePath, newMD5Sum, newLastModifiedTime):
    stateFile = open(stateFilePath, "w")
    stateFile.write(newPageMD5Sum)
    stateFile.write("\n")
    stateFile.write(lastModifiedTime)
    stateFile.close()

url = "http://yxy.in/dir/test.html"

socket = urlopen(url)

# Fresh page info
pageContent = socket.read()
lastModifiedTime = socket.info()["Last-Modified"]

md5Object = md5()
md5Object.update(pageContent)
newPageMD5Sum = md5Object.hexdigest()

# Previous page info
if path.exists(stateFilePath) and path.isfile(stateFilePath) and open(stateFilePath).read() != "":
    stateFileHandler = open(stateFilePath)
    stateFile = stateFileHandler.read()
    savedMD5Sum = stateFile.split("\n")[0]
    savedLastModifidTime = stateFile.split("\n")[1]
    stateFileHandler.close()
    changes = []
    if newPageMD5Sum != savedMD5Sum:
        changes.append("MD5")
        print "md5 changed"
    if lastModifiedTime != savedLastModifidTime:
        changes.append("Last modified time")
        print "modified time changed"
    mailBody = "These are changed: "
    if len(changes) > 0:
        for i in changes:
            mailBody += "\n" + i
        mailBody += "\nYou can check that web page <a href='" + url + "'>here</a>"
        saveStateFile(stateFilePath, newPageMD5Sum, lastModifiedTime)
        send_email("samet.atdag@mynet.com", "The webpage has some changes: " + url, mailBody)
else:
    saveStateFile(stateFilePath, newPageMD5Sum, lastModifiedTime)
    print "State file created: " + stateFilePath
