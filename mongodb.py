#!/usr/bin/python
#coding:utf-8
import pymongo
from pymongo import MongoClient as Client
import datetime
import commands
#create line
client=Client('mongodb://root:123456@127.0.0.1:27017/')
#connect to database
db=client.mongodb
#collections
menu=db.menu
#print db.collection_names()



# { "_id" : ObjectId("5986a816c8d00cd85382cc21"), "number" : "a", "command" : "db.serverStatus()" }
def myMenu():
    strings=menu.find()    
    if strings != None:
        result= 'Menu:\n'
        for string in strings:
            result=result+string['number']+' | '+string['command']+'\n'
        return result
    else:
        return 'NULL'
    return strings
def findCommand(commandNum):
    command=menu.find_one({'number':commandNum})['command']
    if command != None:
        return runCommand(command)
    else:
        return 'Can not find the command,list menu by "$menu"'

def runCommand(command):

    (status_cmd,output_cmd) = commands.getstatusoutput('mongo admin -u root -p 123456 -quiet --eval "printjson(%s)"' % command)
    return 'result : %s\ndescrip: \n%s' % (str(status_cmd),str(output_cmd))

if __name__ == '__main__':
    print str(myMenu())
#    print str(findCommand('a'))
    print str(db.getCollenctionNames())





