#Caroline Trimble
#Program that encryped the password file with the SHA hash
#The file is now read only

import hashlib

#function to encrypt rewrite the file to encrypt passwords
def encrypt(filename):
    #opens file for both reading and writing
    f = open(filename, 'r+')
    #reads file into a string and then splits to array
    userString = f.read();
    users = userString.split()
    i = 1
    #hashes the password and saves it into a new array
    hashedp = []
    while i < len(users):
        password = users[i]
        newpass = hashlib.sha1(password).hexdigest()
        hashedp.append(newpass)
        i = i + 2
    #deletes original content from file
    users = users[0::2]
    f.seek(0)
    f.truncate()
    #writes users with hashed password
    i = 0
    while i < len(users):
        term = users[i] + ' ' +  hashedp[i] + '\n'
        f.write(term)
        i = i+1

encrypt('user_pass.txt')
#after this was excuted once, the file goes into read only state


