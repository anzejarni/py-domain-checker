#!/usr/bin/python
import pythonwhois
import sys
import datetime
import socket
import smtplib


domainnames = {
               'example': {'com', 'net', 'org'},
              }

# Days before expiry on which you would like to be reminded
periods = [30, 14, 7]
# Send warning to the emails
emails = ['user@example.net']
# SMTP authentication data
smtp_auth = {'host': 'mail.example.net', 'user': 'username', 'pass': 'password'}

def main():
  messages = ''
  problems = ''
  for domain, exts in domainnames.items():
    for ext in exts:
      d = domain+"."+ext
      try:
        w = pythonwhois.get_whois(d)
        if w:
          if type(w['expiration_date'][0]) is not datetime.date:
            days = (w['expiration_date'][0] - datetime.datetime.utcnow()).days
            for p in periods:
              if days < p:
                messages = messages + "Domain "+d+" will expire in "+str(days)+" days!\n"
          else:
            problems = problems+"No expiration date found for: "+d+"\n"

        else:
          problems = problems+"Domain not found: "+d+"\n"
      except Exception as e:
        problems = problems+d+": "+str(e)+"\n"

  if messages != '' and problems == '':
    for email in emails:
      send_mail(email, messages)

  if problems != '' and messages != '':
    for email in emails:
        send_mail(email, messages+"\n I encountered some problems: \n"+problems)

def send_mail(email, message):
  message = 'Subject: %s\n\n Hi there!\n\n %s \n\n Have a beautiful day, \n your Domain Notifier.' % ('IMPORTANT: Domain Notifier', message)
  smtp.sendmail(smtp_auth['user'], email, message)



if __name__ == '__main__':
  smtp = smtplib.SMTP(smtp_auth['host'], 25)
  smtp.login(smtp_auth['user'], smtp_auth['pass'])
  main()

