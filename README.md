 a wechat robot for mongodb


#####You need modify the client login access in mongodb.py

You can add your command by modify the dbCommand.ini or use the wechat command


######command
1.    $menu  ~~~list the menu

2.    $inscmd:'command':'alias'  ~~~add a command
    eg:
        $inscmd:db.serverStatus():123
3.    $alias  ~~~run the command in menu
    eg:
        $123
