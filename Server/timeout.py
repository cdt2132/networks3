#Caroline Trimble
#Timeout function for an inactive user

import socket
import handleMessage

client = None
users = {}
t = ""

def get(c, u):
    global client
    global users
    client = c
    users = u
#This function gets the client and user list from the main program and
#sets it to client and users (global variables)
#This is set up like this because the function was not working correctly if
#the function timeout had arguments
def timeout():
    try:
        client.send("Timeout. \n")
        #If timeout time is reached (set in server program)
        #noties client that there has been a client
        #Client responds by automatically sending "logout" and quitting
    except:
        return 0


