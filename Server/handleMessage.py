#Caroline Trimble
#Handles all the messages once a message is sent from client to server
#Creates a response and sends it to the appropriate user

import datetime

last = {}
away = {}

def handle(client, data, users):
    dataList = data.split()
    if len(dataList) < 1:
        client.send("Error! This is not a recognized command!\n")
        return 0
    #tests which command the user has send, if not one of the specified commands
    #sends error
    if client in away:
        del away[client]
    #If a client sends a message, they are now "active"
    #and their away message is deleted
    if dataList[0] == "who":
        who(client, users)
    elif dataList[0] == "send":
        send(users, data, client)
    elif dataList[0] == "broadcast":
        broadcast(users, data, client)
    elif dataList[0] == "logout":
        logout(users,client)
    elif dataList[0] == "last":
        lastList(client, users, data)
    elif dataList[0] == "away":
        awayMessage(data, client, users)
    else:
        client.send("Error! This is not a recognized command!\n")

def getUsername(client, users):
    for key in users.keys():
        if users[key] == client:
            return key
    #function to get the username of a client when only the
    #file descriptor is available

def who(client, users):
    userList = []
    for value in users:
        userList.append(value)
        #appends the usernames of active users to userList
    userList = str(userList) + "\n"
    #turns it into a string and adds new line
    try:
        client.send(userList)
    except:
        print "User disconnect"

def lastList(client, users, data):
    print data
    data = data.split()
    print len(data)
    if len(data) != 2:
        try:
            client.send("Last command must be formatted 'last <length in minutes>'\n")
            return
            #if user does not specify amount of minutes, send message detailing this
        except:
            print "Client disconnect"
    data = int(data[1])
    if data < 0 or data > 60:
        try:
            client.send("Minutes specified must be between 0 and 60\n")
            return
        except:
            print "Client disconnect"
    #If minutes specified is not between 0 and 60, send message
    response = []
    time = datetime.datetime.now()
    for value in users:
        response.append(value)
    #appends currently active users
    print last
    for value in last:
        dif = time - last[value]
        dif = divmod(dif.days * 86400 + dif.seconds, 60)
        if dif[1]  <= data:
            response.append(value)
        #for all users in lest, check if the time they logged out - current time
        #is less than time specified by "last" command
    response = str(response) + "\n"
    try:
        client.send(response)
    except:
        print "User Disconnect"

def send(users, data, client):
    message = data.split()
    userList = []
    word = 0
    if ("(" in message[1]):
        #if the message has a ( , it is directed towards > 1 user
        u = message[1]
        u = u[1:]
        userList.append(u)
        listover = False
        word = 2
        while listover == False:
            if (")" in message[word]):
                #close paren means list is over
                u = message[word]
                u = u[:-1]
                userList.append(u)
                word += 1
                listover = True
                #append username to list
            else:
                userList.append(message[word])
                word += 1
                #append username to list
        #while there are still users on the list, add the user names
    else:
        userList.append(message[1])
        #if just one user, just append that username to the userList
    data = ""
    word = len(userList) + 1
    while word < len(message):
        data = data + message[word] + ' '
        word += 1
    #gets the message the user wanted to send
    c = client
    user = str(getUsername(c, users))
    data = user + ": " + data + "\n"
    #sends the message in the format <user>:<message>
    for value in userList:
        if value in users:
            #if the user is online, he/she is sent the message
            rec = users[value]
            try:
                rec.send(data)
            except:
                print "User disconnect"
            if rec in away:
                c.send(away[rec])
        #if the user that is being sent a message has an "away message" set,
        #then that user's away message is sent to the sender of the message

    #sends message to user(s)


def broadcast(users, data, client):
    sender = str(getUsername(client, users))
    #gets the username of the sender of this message
    data = data.partition(' ')[2]
    data = sender + ': ' + data
    #appends <user>: to the message to be send
    for user in users:
        if user == sender:
            continue
        #if user in user list is same as sender, disregard
        #(broadcast does not go to one's self)
        else:
            client = users[user]
            #otherwise, get client from username and user list
            try:
                client.send(data)
                #sends client the data
            except:
                print "User disconnect"

def logout(users, client):
    time = datetime.datetime.now()
    sender = str(getUsername(client,users))
    if sender in users.keys():
        del users[sender]
    print users
    #deletes the username from the active clients dictionary
    last[sender] = time
    #adds username and logout time to last dictionary
    client.close()
    #closes connection

def awayMessage(data, client, users):
    d = data
    test = d.split()
    if len(test) == 1:
        d = d + "I am away"
    d = d.split(' ', 1)[1]
    username = getUsername(client, users)
    data = username + ": " + d
    away[client] = d
    client.send("Away message set!\n")
#Function for an away message. A client sets an away message to be send to anyone
#who directly sends them (not broadcast)

def checkLast(userName):
    if userName in last:
        del last[userName]
    #before adding a client to the active users dictionary, it must delete it from the
    #last dictionary, so it does not appear twice in the last command

def checkAway(client):
    if client in away:
        return True
    return False
