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
        else:
            return mongodb.findCommand(msg['Content'][1:])
            
            
            
    defaultReply = u'I received: ' + msg['Content']
    reply = get_response(msg['Content'])
    return reply or defaultReply
#    itchat.send(defaultReply,msg['FromUserName'])

########Group Chat########
@itchat.msg_register(TEXT,isGroupChat=True)
def group_reply(msg):
    if msg['isAt']:
        defaultReply = u'I received: ' + msg['Content']
#itchat.get_friends(update=True)   获取好友列表，首位为自己
#弃用，效率低，每次需要获取好友列表，后续改进：分析 msg 内容，获取本机器人名称，在此暂时为手动设置
#        reply = get_response(msg['Content'][(len(itchat.get_friends(update=True)[0]['NickName'])+2):])
        reply = get_response(msg['Content'][(len(info.robotName)+2):])
        return reply or defaultReply
        



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

