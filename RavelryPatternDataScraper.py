# import sqlite3 as sq
import requests as rq #Import the requests library--a library that makes it easy to make HTTP requests to APIs
# import time as time
# import matplotlib.pyplot as plt
import RavelryFunctions as rav

#Open my Ravelry authentication values
path = 'C:/Users/Jamie/Desktop/RavelrySecret.txt' #Path to the file that holds my keys--the username and password given to me by Ravelry for my Basic Auth, read only app
mode = 'r' #read mode--I'll only need to read the username and password from the file

keys = []  # The list where I'll store my username and password
with open(path, mode) as f:  # Open the file
    for line in f:
        keys.append(line)  # The first line is the username, and the second line is the password--add each of these lines to the keys list

user = keys[0].rstrip()  # The username is held in the first element of the keys list
pswd = keys[1].rstrip()  # The password is the second element of the keys list


# Test out parsePatData
patID = '10'  # '791180', '10' #21, 696580, 796580
requestString = 'https://api.ravelry.com/patterns.json?ids=' + patID

# Request data from one pattern
response = rq.get(requestString, auth=(user, pswd))
print(response)

# Pull out desired data and format it into a dictionary
patDict = rav.parsePatData(response.json()['patterns'][patID])
print(patDict)

print('\n\n')
for key in response.json()['patterns'][patID].keys():
    print(key)
    print('\t' + str(response.json()['patterns'][patID][key]))




