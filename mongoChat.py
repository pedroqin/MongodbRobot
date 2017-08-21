#!/usr/bin/python
#coding:utf-8
import itchat
from itchat.content import *
import ConfigParser
import requests
import thread
import time
import commands
import os
import mongodb
import info
from  sign_in import *
#tuling

#this is your key
KEY = info.tulingKey
#print info.admin_name
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'Pedro-wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


###
def load_dict_from_file(filepath):
    _dict = {}
    try:
        with open(filepath, 'r') as dict_file:
            for line in dict_file:
                (key, value) = line.strip().split(':')
                _dict[key] = value
    except IOError as ioerr:
        print "文件 %s 不存在" % (filepath)
     
    return _dict
###
def save_dict_to_file(_dict, filepath):
    try:
        with open(filepath, 'w') as dict_file:
            for (key,value) in _dict.items():
                dict_file.write('%s:%s\n' % (key, value))
    except IOError as ioerr:
        print "文件 %s 无法创建" % (filepath)




#personal chat
@itchat.msg_register(TEXT)
def tuling_reply(msg):
    if msg['Content'].startswith('$'):
        if msg['Content'][1:]=='menu':
            return mongodb.myMenu()
        elif msg['Content'][1:].startswith('inscmd:'):
            return mongodb.insertMenuByU(msg['Content'][8:])
        else:
            return mongodb.findCommand(msg['Content'][1:])
            
            
    defaultReply = u'I received: ' + msg['Content']
    reply = get_response(msg['Content'])
    return reply or defaultReply
#    itchat.send(defaultReply,msg['FromUserName'])

########Group Chat########
@itchat.msg_register(TEXT,isGroupChat=True)
def group_reply(msg):
    dailyLogMsg(msg["User"]["NickName"])#accumulate group 's message sum
    perNum(msg["ActualNickName"],msg["User"]["NickName"])#accumulate group everyone message sum
    if msg['User']["NickName"] in wechatGroupMem:
        if msg['ActualNickName']!=info.adminName:
            return 
        else:
            if msg['Content']=="打开群聊":
                wechatGroupMem.remove(msg['User']["NickName"])
                itchat.send(u'@%s\u2005 Reboot robot Successfully !' % msg['ActualNickName'],msg['FromUserName'])
            else:
                return
    if msg['Content']=="关闭群聊":
        if msg['ActualNickName']==info.adminName:
            wechatGroup=msg['FromUserName']
            wechatGroupMem.add(msg['User']["NickName"])
            itchat.send(u'@%s\u2005 Shutdown robot Successfully !' % msg['ActualNickName'],msg['FromUserName'])
    if msg['Content']=="签到" or msg['Content']=="qiandao" or msg['Content']=="簽到":
        result=signIn(msg['ActualNickName'],msg['User']["NickName"])
        if result == "False" :
            itchat.send(u'@%s\u2005 您今天已经签过到啦，不用重复签哦~' % (msg['ActualNickName']),msg['FromUserName'])
        else:
		#if result[0].isdigit():
            itchat.send(u'签到成功！\n @%s\u2005 ,您是今天第%s个签到的，已累计签到%s天' % (msg['ActualNickName'],result[1],result[0]),msg['FromUserName'])
#        else :
 #           itchat.send(u'@%s\u2005 啊咧~签到失败，请稍后再试' % (msg['ActualNickName']),msg['FromUserName'])
#        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'],msg['Content']),msg['FromUserName'])
#        defaultReply = 'I received: ' + msg['Text']

#####my robot name :  @robot_P len=8
#    if msg['Content'][(len(info.robotName)+2):]=="昨日统计":
    if msg['Content']=="昨日发言统计":
        day=datetime.date.today()-datetime.timedelta(days=1)#yesterday 's date
        countStr="%s日 发言排行: \n名次\t   昵称\t   发言数\n" % day.strftime('%Y-%b-%d')
        i=1
        for member in listGroup(day.strftime('%b-%d-%y'),msg['User']['NickName']):
            countStr=countStr +'第'+str(i)+'名'+':'+ member["name"] + '\t' + str(member["number"]) +'\n'
            i+=1
        itchat.send(u'%s' % countStr,msg['FromUserName'])

#    elif msg['Content'][(len(info.robotName)+2):]=="今日统计" or msg['Content'][(len(info.robotName)+2):]=="统计":
    elif msg['Content']=="今日发言统计" or msg['Content']=="发言统计":
        day=datetime.date.today()
        countStr="%s日 发言排行: \n名次\t   昵称\t   发言数\n" % day.strftime('%Y-%b-%d')
        i=1
        for member in listGroup(day.strftime('%b-%d-%y'),msg['User']['NickName']):
            countStr=countStr +'第'+str(i)+'名'+':'+ member["name"] + '\t' + str(member["number"]) +'\n'
            i+=1
        itchat.send(u'%s' % countStr,msg['FromUserName'])
        
    if msg['isAt']:
        reply = get_response(msg['Content'][(len(info.robotName)+2):])
        itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'],reply),msg['FromUserName'])
    return #### need it,dont del it !!!!!!!!!!!!!!
#    if msg['isAt']:
#        defaultReply = u'I received: ' + msg['Content']
#itchat.get_friends(update=True)   获取好友列表，首位为自己
#弃用，效率低，每次需要获取好友列表，后续改进：分析 msg 内容，获取本机器人名称，在此暂时为手动设置
#        reply = get_response(msg['Content'][(len(itchat.get_friends(update=True)[0]['NickName'])+2):])
#        reply = get_response(msg['Content'][(len(info.robotName)+2):])
#        return reply or defaultReply
        



#[RecommendInfo][UserName]    [RecommendInfo][Content]  [][NickName]
@itchat.msg_register(FRIENDS)
def add_friend(msg):

# 你可以设置好友认证信息，以便将好友加至对应群组
    VerList=load_dict_from_file(info.configFil)
    if msg['RecommendInfo']['Content'] in VerList:
# 该操作会自动将新好友的消息录入，不需要重载通讯录
        itchat.add_friend(**msg['Text'])
# 根据验证消息更改新加好友的备注
        itchat.set_alias(msg['RecommendInfo']['UserName'],u'%s--%s' % (VerList[msg['RecommendInfo']['Content']],msg['RecommendInfo']['NickName']))
        
    else:    
        itchat.add_friend(**msg['Text'])
    
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

# 接收用户发送的文件并保存
@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])
def download_files(msg):
    file_name='%s/%s' % (info.downloadPath,msg.fileName)
    msg.download(file_name)
    itchat.send('@%s@%s' % ('img' if msg['Type'] =='Picture' else 'fil',msg['FileName']),msg['FromUserName'])
    return '%s received,Path : %s' % (msg['Type'],file_name)

###动态信息发送测试
def test_function():
#    (status_cmd,output_cmd) = commands.getstatusoutput()
    return os.path.exists('/Pedro/chat/flag.txt')
    pass



mongodb.insertCommand(info.mongoIni)
wechatGroupMem=set()
#itchat.auto_login(hotReload=True,enableCmdQR=2) 
itchat.auto_login(hotReload=True) 
thread.start_new_thread(itchat.run,())
#itchat.run()
while 1:
    if test_function():
        admin_id=itchat.search_friends(name=info.adminName)[0]['UserName']
        itchat.send('flag file exist!',admin_id)
        os.remove('/Pedro/chat/flag.txt')
    time.sleep(.1)

