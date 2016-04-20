Caroline Trimble
cdt2132
Networks Homework 3: Socket Programming

NOTE: Due to confusion on the piazza, in office hours, etc I have utilized the lines
os.environ["TIME_OUT"] = "1800" and os.environ["BLOCK_TIME"] = "60". Becuase of this one
would have to delete or edit this line to change these variables.

My code has two main modules, Server.py and Client.py. Server.py also includes 3 modules:
authenticateUser.py, handleMessage.py, and timeOut.py. When the server program is executed,it initiates, binds, and then starts listening. Each time a client connects it starts a new thread to deal with that client. This thread utilizes authenticateUser.py to
handle the login of each client connection. Then, each time it receives a message
it utilizes handleMessage.py to interpret and respond to the message. In Client.py,
the client server first goes through the user authentication process and then
starts a infinite while loop that prompts the user with a Command, and then sends
that Command to the server. Each time this while loop is executed, it starts a
different thread that attempts to receive a message from the server. The
external modules I used for this project are: sys, socket, thread, threading, os, hashlib, and datetime.

This assignment was developed in the IDE pyCharm but terminal was used to test.

To run Server.py, simply type

python Server.py <PORT>

example:
python Server.py 1995

To run Client.py simply  type
python Client.py <SERVER IP> <SERVER PORT>

example:
python Client.py localhost 1995

The additional functionality that I added was the use of an away message. The user can utilize
this by typing:

away <Message>

for example:

away I am away from my desk right now!

Additionally, if the user simply enters the command

away

then their away message will automatically be set to "I am away"

Then, any time another user uses “send” (either directly to that user or in a list)
to send a message to a user who has set an away message, they will automatically
get the away message text back. However, the away message is not sent back
when a user sends a message to the “away” user via broadcast. This is just a
design choice because in my opinion “broadcast” does not usually warrant
individual responses.

Example:
*Columbia*
away I am away from my desk right now!

*Google*
send columbia hi

*Columbia*
google: hi
#still receives the message

*Google*
columbia: I am away from my desk right now!

After any user who has sets an away message sends a new message,
they are no longer  considered “away” and their away message disappears.

Furthermore, the timeout function is not called for users who have set themselves as
“away,” so that a user can stay “away” for a few hours, even though the
timeout is 30 minutes.

One can execute this function by typing the away command. One can test this function
by setting an away message and messaging that user, and then having the user that set
an away message send a new command, and then messaging that user again (this time
there will be no automatic away response). Also the fact that there is no timeout
for “away” users can be done by setting an away message and then remaining idle
for TIME_OUT minutes.


