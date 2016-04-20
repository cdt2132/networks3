#Caroline Trimble
#Server.py uses authenticateUser.py to make sure that the
#login / password combo is correct and also to block users that
#try to log in more than 3 times

import hashlib
import handleMessage
import datetime
import os

blockedIPs = []
blockedUsers = []
times = []
#used for recording blocked user/IP combos
os.environ["BLOCK_TIME"] = "60"
#As of now, I have set the BLOCK_TIME varible to 60 seconds

def impUsers():
    f = open('user_pass.txt', 'r')
    u = f.read()
    u = u.split()
    f.close()
    users = {}
    i = 0
    while i < len(u) -1:
        users[u[i]] = u[i+1]
        i += 2
    return users
    #Reads in the (encryped) user pass file and returns a dictionary

def authUser(client, lp, userD, activeClients, address):
    if lp == "logout":
        handleMessage.logout(userD, client)
        return [False, "logout"]
    #if user logs out during signin
    lp = lp.split()
    #gets username and password
    if len(lp) != 2:
        return [False, "reject"]
    #if input did not contain a username and password, rejects
    login = lp[0]
    password = lp[1]
    BLOCKTIME = os.environ.get('BLOCK_TIME')
    blocked = checkBlocked(address,BLOCKTIME, login)
    #Checks if the user for that specific IP is blocked
    if blocked == True:
        accept = [False, "blocked"]
        return accept
    #If blocked, returns this info
    if login in userD:
        if login in activeClients.keys():
            return [False, "double"]
        if login not in activeClients.keys():
            password = hashlib.sha1(password).hexdigest()
        if userD[login] == password:
            handleMessage.checkLast(login)
            return [True, login]
    #Checks whether the provided login matches the password, if it does returns true
    return [False, "reject", login]

def login(client, userpass, activeClients, address):
    tries = 1
    accept = False
    while tries < 3:
        #gives the user three tries
        try:
            auth = str(client.recv(1024))
        except:
            print "Client disconnect."
        accept = authUser(client, auth, userpass, activeClients, address)
        if accept[0] == True:
            client.send("Welcome to Chat!")
            break
            #If accepted, notifies the client and breaks the loop
        else:
            if accept[1] == "blocked":
                return [False, "blocked"]
            #If user is blocked, returns this info
            elif accept[1] == "reject":
                client.send("Incorrect username/password combination. Try again.")
                tries+=1
                print tries
                #If incorrect, asks the user to enter their username and password again
            elif accept[1] == "double":
                client.send("Someone is already logged in under this username.")
                #If someone is already logged in, the prompt to login continues
                #but this does not count as one of the 3 tries
            elif accept[1] == "logout":
                break
            #If client does CTRL-C during login, breaks the loop
    if accept[0] == False and accept[1] == "reject" :
        name = accept[2]
        accept = [False, "Block", name]
    #If rejected 3 times, returns the command to block the user
    return (accept)

def block(address, name):
    time = datetime.datetime.now()
    blockedA = str(address[0])
    blockedIPs.append(blockedA)
    blockedUsers.append(name)
    times.append(time)
    #Appends current time, the blocked IP, and the blocked username to the list

def checkBlocked(address, BLOCKTIME, name):
    ad = str(address[0])
    time = datetime.datetime.now()
    e = False
    if blockedIPs:
        for element in blockedIPs:
            if ad == element:
                #If current element is equal to the blockedIP
                index = blockedIPs.index(ad)
                #get index
                if name == blockedUsers[index]:
                    #If usernames are the same
                    blockedTime = times[index]
                    #Get time blocked
                    dif = time - blockedTime
                    dif = divmod(dif.days * 86400 + dif.seconds, 60)
                    dif = dif[0]*60 + dif[1]
                    #Get difference of time blocked and current time
                    if int(dif) <= int(BLOCKTIME):
                        #if more than block time, the user is blocked
                        return True
                    else:
                        del blockedIPs[index]
                        del times [index]
                        del blockedUsers[index]
                    #If time dif is greater than BLOCKTIME, removes the user, IP, and time from lists

    return False

