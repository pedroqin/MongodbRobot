#!/usr/bin/python
#coding:utf-8
from pymongo import MongoClient as Client
import datetime
import info
#create line
client=Client(info.signInClient)
#connect to database
db=client[info.signInDatabase]
#collections
posts=db[info.signInCollections1]
glogs=db[info.signInCollections1]
perlogs=db.perOneDaily#save the each  person's Msg number in one day one group
#print db.collection_names()

#print posts.find_one({"name":"pedro","group":"myGroup"})


# sign in num , return :your signIn number and total signIn number
def signIn(name,group):
    string=posts.find_one({"name":name,"group":group})
#    print "+++",string,"+++"
    if  string  != None:
        if string["date"] != datetime.datetime.now().strftime('%b-%d-%y'):
             posts.update({"name":name,"group":group},{ "$set" : {"date":datetime.datetime.now().strftime('%b-%d-%y')}},True,False)
             posts.update({"name":name,"group":group},{ "$inc" : {"time": 1}},True,False)
        else:
             return "False"
    else:
        new_post={"name":name,"group":group,"time":1,"date":datetime.datetime.now().strftime('%b-%d-%y')}
        posts.save(new_post)
    return [posts.find_one({"name":name,"group":group})["time"],daily(group)]
#
def daily(group):
    number=glogs.find_one({"daily_report":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})
    if number == None:
        new={"daily_report":"Yes","date":datetime.datetime.now().strftime('%b-%d-%y'),"number":1,"group":group}
        glogs.save(new)
    else:
#        if number["date"] != datetime.datetime.now().strftime('%b-%d-%y'):
#             posts.update({"daily_report":"Yes","group":group},{ "$set" : {"date":datetime.datetime.now().strftime('%b-%d-%y'),"number":1}},True,False)
#        else:
         glogs.update({"daily_report":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')},{ '$inc' :{"number": 1}})
    return glogs.find_one({"daily_report":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})["number"]

##return yesterday Msg total num, and accumulate today Msg num
#def dailyLogMsg(group):
#    allMsg=glogs.find_one({"daily_Sum":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})
#    if allMsg == None:# create today's log
#        yester=datetime.date.today()-datetime.timedelta(days=1)#yesterday 's date
#        allMsg_yester=glogs.find_one({"daily_Sum":"Yes","group":group,"date":yester.strftime('%b-%d-%y')})
#        if allMsg_yester ==None:
#            yester_sum=0#if yesterday has no log ,the sum is 0
#        else:
#            yester_sum=allMsg_yester["today"]#get yesterday 's "today"num to today 's "yesterday"
#        new={"daily_Sum":"Yes","date":datetime.datetime.now().strftime('%b-%d-%y'),"today":1,"yesterday":yester_sum,"group":group}
#        glogs.save(new)
#        
#    else:
#        glogs.update({"daily_Sum":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')},{ '$inc' :{"today": 1}})
#    return glogs.find_one({"daily_Sum":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})["yesterday"]#return yesterday 's sum for create the picture

#return today Msg total num, and accumulate today Msg num
def dailyLogMsg(group):
    allMsg=glogs.find_one({"daily_Sum":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})
    if allMsg == None:# create today's log
        new={"daily_Sum":"Yes","date":datetime.datetime.now().strftime('%b-%d-%y'),"today":1,"group":group}
        glogs.save(new)
    else:
        glogs.update({"daily_Sum":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')},{ '$inc' :{"today": 1}})
    return glogs.find_one({"daily_Sum":"Yes","group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})["today"]#return today 's sum for create the picture

#accumulate everyone's total Msg num
def perNum(name,group):
    perNum=perlogs.find_one({"per_daily":"Yes","name":name,"group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})
    if perNum == None:
        new={"per_daily":"Yes","date":datetime.datetime.now().strftime('%b-%d-%y'),"number":1,"group":group,"name":name}
        perlogs.save(new)
    else:
        perlogs.update({"per_daily":"Yes","group":group,"name":name,"date":datetime.datetime.now().strftime('%b-%d-%y')},{ '$inc' :{"number": 1}})
    return perlogs.find_one({"per_daily":"Yes","name":name,"group":group,"date":datetime.datetime.now().strftime('%b-%d-%y')})["number"]

#list top 5 people who had sent most msg yesterday
def listGroup(date,group):
    result=perlogs.find({"date":date,"group":group}).limit(5).sort([("number",-1)])
    return result

#find a person's Msg number in one day one group
def findOneNum(date,personName,group):
    result=perlogs.find({"date":date,"group":group,"name":personName})["number"]
    return result



#for list1 in listGroup("Jul-29-17","Mongodb论坛技术讨论二群"): 
#    print list1["name"],list1["number"]

#for i in range(0,5):
#    print listGroup("Jul-29-17","Mongodb论坛技术讨论二群")[i]

#print posts.find_one({"name":"pedro"})
#posts.save(new_post)
#print "over"
#print signIn("pedro","myGroupe")
#print str(daily("123"))
