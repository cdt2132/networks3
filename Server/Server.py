#Caroline Trimble
#Server program
#Server portion of the chat server


import sys
import socket
import threading
import authenticateUser
import handleMessage as hm
import os
import timeout

userpass = authenticateUser.impUsers()
#reads the file of usernames and passwords into a dictionary
activeClients = {}
#blank dictionary for active clients (used for who and last)
os.environ["TIME_OUT"] = "1800"
#MUST COMMENT THIS OUT!!!!
class ChatServer(object):
    try:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
        #initiates and binds the server socket
        def listen(self):
            self.sock.listen(5)
            #Listen -- python recommmends using 5 as the backlog
            print "Serving on port %s" %port
            while True:
                client, address = self.sock.accept()
                print "Client %s connected at address %s"%(client, address)
                client.send("continue")
                threading.Thread(target = self.clientThread,args = (client,address)).start()
                #Accepts a client connection, opens a thread for that client


        def clientThread(self, client, address):
            client.send("Please enter your username and password.")
            accept = authenticateUser.login(client, userpass, activeClients, address)
            #Checks whether username and password is correct
            if accept[0] == True:
                activeClients[accept[1]] = client
                #adds the username and file descriptor of client to activeClients
            else:
                if accept[1] == "logout" :
                    return 0
                #if client logged out, return
                if accept[1] == "Block":
                    name = accept[2]
                    authenticateUser.block(address, name)
                    client.send("Too many attempts. Closing Connection")
                    client.close()
                #if > 3 attemps, tell client that is is blocked, quit
                if accept[1] == "blocked":
                    client.send("Access for this user at this IP address is blocked.")
                    client.close()
                #if a blocked user/IP combo tries to log in, notify and close

            while True:
                t = 0
                if hm.checkAway == False:
                    timeout.get(client, activeClients)
                    time = int(os.environ.get("TIME_OUT"))
                    t = threading.Timer(time, timeout.timeout)
                    t.start()
                #uses threading.timer and timeout to keep track of inactivity for TIME_OUT seconds
                try:
                    data = client.recv(1024) + "\n"
                    print data
                except:
                    print "Client Log Off"
                    return 0
                if data:
                    if t != 0:
                        t.cancel()
                    #if recieve data from client, cancel the timer thread
                    hm.handle(client, data, activeClients)
                    #calls handle to handle the client's message
    except KeyboardInterrupt:
        print 'Goodbye\n'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    #quit on CTRL C

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
        ChatServer('',port).listen()
    except KeyboardInterrupt:
        print '\n Goodbye!'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    #Main, invokes listen, quit on CTRL C
