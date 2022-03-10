# import os 
# import time 
# import pathlib
# import getpass
import win32com.client
#from datetime import datetime, timedelta
#import re

#Settings to select the mail client
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace('MAPI')


##########Unused code to find the flow of the Inbox Data
#messages = mapi.Folders("Warehouse").Folders("ASAP").Items

# for idx, folder in enumerate(mapi.Folders):
#     #index starts from 1
#     print(idx+1, folder)

# for idx, folder in enumerate(mapi.Folders("Warehouse").Folders):
#     print(idx+1, folder)

##################################################################

#Inbox Settings
inbox = mapi.Folders['Warehouse'].Folders['Auto Onboard Alerts']
messages = inbox.Items
keyword = input("Enter FamilyID: ")
for message in list(messages):
    body_content = message.body
    if keyword in body_content:
        print("\n")
        print(keyword)
        print(message.Subject, message.ReceivedTime)
        print(body_content)
inbox = mapi.Folders['Warehouse'].Folders['Auto POD Alerts']
messages = inbox.Items
for message in list(messages):
    body_content = message.body
    if keyword in body_content:
        print(message.Subject, message.ReceivedTime)
        print(body_content)