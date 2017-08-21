 a wechat robot for mongodb


#####You need modify the client login access in mongodb.py

You can add your command by modify the dbCommand.ini or use the wechat command

#####function
1.    receive and save the PICTURE,RECORDING,ATTACHMENT,VIDEO
2.    Judge the 'add friend' requirement (base on admin.conf)and add the friend ,and add a alias
3.    Group chat can sign in and chat with robot  until admin turn off the robot,robot will calculate the chat number
######command
1.    $menu  ~~~list the menu

2.    $inscmd:'command':'alias'  ~~~add a command
    eg:
        $inscmd:db.serverStatus():123
3.    $alias  ~~~run the command in menu
    eg:
        $123

4.   turn on/off the group chat:打开群聊/关闭群聊


5.   昨日发言统计   今日发言统计/发言统计   
