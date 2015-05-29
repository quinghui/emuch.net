## README ##

The Python3 scripts log [emuch.net(小木虫论坛)][emuch] in, and take your sign coins in the BBS.
 According to [emuch.net][emuch], you can only get the coins once everyday.

### For the script *emuch_daily_coins.py*  ###

This script *emuch_daily_coins.py* which the cookies are hardcode in the script. 
 You may find out your emuch.net   cookies **'_discuz_uid'** and **'_discuz_pw'**,
 and hard code them into the script.   

The detials in the script are following:

    EMUCH_UID_VALUE = ' '  # here, hard code '_discuz_uid' value   
    EMUCH_PW_VALUE = ' '   # here, hard code '_discuz_pw' value 

### For the script *emuch_coins.py* ###

This script *emuch_coins.py* reads the json file *emuch_cookies.json* to grab your emuch.net cookies name and values,
 so you would not need to modify the script.
 The json file should be in same directory with *emuch_coins.py*.

The cookies file is following:

    {  
    "_discuz_uid": "  ",   
    "_discuz_pw": "  "  
    }   

### For the script *emuch_user_login.py* ###

This script *emuch_user_login.py* gets username and password from *user_info.py* 
 which is in same directory with the script, and signs in emuch.net via the username and password,
 not cookies. After log emuch.net in, the script will take daily award coins.
 
The file *user_info.py* is following:

    username = " "
    password = " "


[emuch]:http://emuch.net/bbs/
