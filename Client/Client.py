#Caroline Trimble
#Client server that allows a user to log on, send and recieve messages

import sys
import socket
import os
import thread
os.environ["TIME_OUT"] = "1800"
#must comment this out
TIMEOUT = int(os.environ.get("TIME_OUT"))
def serve():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverIP = sys.argv[1]
        serverPort = int(sys.argv[2])
        serverAddress = (serverIP, serverPort)
        clientSocket.connect(serverAddress)
        #initializes and connects to the server
        try:
            data = clientSocket.recv(1024)
        except:
            print "Problem connecting to the server. Exiting."
            try:
                 sys.exit(0)
            except SystemExit:
                os._exit(0)

        print "Connected to %s on port %s" %(serverIP, serverPort)
        try:
            data = clientSocket.recv(1024)
        except:
            print "Problem connecting to the server. Exiting."
        if data:
            print(data)
        accepted = False
        #while the username is not accepted...
        while accepted == False:
            user = str(raw_input("Username: "))
            password = str(raw_input("Password: "))
            #prompts the user for username password
            try:
                authenticate = "%s %s"%(user, password)
            except KeyboardInterrupt:
                authenticate = "logout"
            #gets the username and password, except if user does CTRL C
            #if user types CTRL c, just sends "logout" to server
            try:
                clientSocket.send(authenticate)
                #sends username
            except socket.error:
                print "Problem connecting to the server. Exiting."
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            try:
                data = clientSocket.recv(1024)
            except socket.error:
                print "Problem connecting to the server. Exiting."
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            print(str(data))
            if "Welcome" in str(data):
                accepted = True
                #if welcome in data, accept is true and chat session started
            if "Closing" in str(data):
                sys.exit(0)
                #if the username is being blocked (3 attempted tries) close
            if "blocked" in str(data):
                sys.exit(0)
                #if the username is currently blocked, close

        def receive(args):
            #a thread to recieve messages
            while True:
                done = False
                data = ""
                while done == False:
                    try:
                        data = data + clientSocket.recv(1024)
                    except socket.error:
                        print "Problem connecting to the server. Exiting."
                        try:
                            sys.exit(0)
                        except SystemExit:
                            os._exit(0)
                    #recieves data
                    if "\n" in data:
                        print data[:-1]
                        done = True
                    #if newline in data, prints data and sets done to true
                        if "Timeout" in data:
                            clientSocket.send("logout")
                            try:
                                sys.exit(0)
                            except SystemExit:
                                os._exit(0)
                        #if the data is "timeout", then the user has timed out and the server notifies
                        #from the timeout message the system automatically responds with a logout and then
                        #the system exits
                        print "Command: "
            return 0

        running = 1
        while (running == True):
            #arbitrary values allowing for threading
            args = (0,1)
            thread.start_new_thread(receive, (args,))
            #starts a new listening thread
            message = str(raw_input("Command: \n"))
            #prompts the user to enter a message
            try:
                clientSocket.send(message)
                #sends users message to client
            except socket.error:
                print "Problem connecting to the server. Exiting. "
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            if (message == "logout") or (message == "Logout"):
                clientSocket.close()
                print "Logging Off...Goodbye!"
                return 0
            #if user wants to logout, close the socket and print logout message
            #and return
    except KeyboardInterrupt:
        clientSocket.send("logout")
        clientSocket.close()
        print "Logging off...Goodbye!"
        return 0;
    #on CTRL-C the client sends "logout" and then closes

serve()