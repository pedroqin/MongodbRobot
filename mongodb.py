#!/usr/bin/python
#coding:utf-8
import pymongo
from pymongo import MongoClient as Client
import datetime
import commands
import info
#create line
client=Client('mongodb://root:123456@127.0.0.1:27017/')
#connect to database
db=client.mongodb
#collections
menu=db.menu
#print db.collection_names()



# { "_id" : ObjectId("5986a816c8d00cd85382cc21"), "number" : "a", "command" : "db.serverStatus()" }
def insertCommand(filepath):
    _dict = {}
    try:
        with open(filepath, 'r') as dict_file:
            for line in dict_file:
                if not line.startswith('#'):
                    if line.find(':') != -1:
                        (value, alias) = line.strip().split(':')
                        alias=int(alias)#the number need int to sort
                        while menu.find_one({'number':alias}) != None :
                            alias=alias+1##make the number unique
                        new={"Auto":"no","number":alias,"command":value}
##the "Auto" is to diff the alise is defind or not,if defind,no
                    else:
                        value = line.strip()
                        if menu.find_one({"Auto":"yes"})==None:#the first one need defind
                            alias=0
                        else:
                            alias = int(menu.find({"Auto":"yes"}).limit(1).sort([("number",-1)])[0]['number'])+1
                        new={"Auto":'yes',"number":alias,"command":value}
                    if  menu.find_one({'command':value}) == None :
                        menu.save(new)
        dict_file.close
    except IOError as ioerr:
        print "文件 %s 不存在" % (filepath)
     
    return _dict
###
def myMenu():
    strings=menu.find()    
    if strings != None:
        result= 'Menu:\n'
        result=result+'Alias | Command\n'
        for string in strings:
            result=result+str(string['number'])+' | '+string['command']+'\n'
        return result
    else:
        return 'NULL'
    return strings
def findCommand(commandNum):
    commandNum=int(commandNum)
    command=menu.find_one({'number':commandNum})
    if command != None:
        return runCommand(command['command'])
    else:
        return 'Can not find the command,list menu by "$menu"'

def runCommand(command):

    (status_cmd,output_cmd) = commands.getstatusoutput('mongo admin -u root -p 123456 -quiet --eval "printjson(%s)"' % command)
    return 'result : %s\ndescrip: \n%s' % (str(status_cmd),str(output_cmd))


###insert menu
###insert menu by :    'command:alias' or 'command'    and alias must be Int
def insertMenuByU(line):
    if line.find(':') != -1:
        (value, alias) = line.strip().split(':')
        if not alias.isdigit():
            return 'The alias type must be Int'
        alias=int(alias)#the number need int to sort
        while menu.find_one({'number':alias}) != None :
            alias=alias+1##make the number unique
        new={"Auto":"no","number":alias,"command":value}
    ##the "Auto" is to diff the alise is defind or not,if defind,no
    else:
        value = line.strip()
        if menu.find_one({"Auto":"yes"})==None:#the first one need defind
            alias=0
        else:
            alias = int(menu.find({"Auto":"yes"}).limit(1).sort([("number",-1)])[0]['number'])+1
        new={"Auto":'yes',"number":alias,"command":value}
    if  menu.find_one({'command':value}) == None :
        menu.save(new)
        with open(info.mongoIni, 'a') as dict_file:
            dict_file.write('%s:%s\n' % (value,str(alias)))
            dict_file.close
        return 'Insert %s as %s' % (value,str(alias))
    else:
        return 'This CMD is Exist'
    

if __name__ == '__main__':
#    print str(db.getCollenctionNames())
    insertCommand('dbCommand.ini')
    print str(myMenu())
    print str(findCommand(1))





