## README ##

The Python scripts for log [emuch.net][emuch] in, and take your sign coins. 
 According to [emuch.net][emuch], you can only get the coins once everyday.

### For the script *emuch_daily_coins.py*  ###

You may need to properly hard code your emuch.net cookies **'_discuz_uid'** and **'_discuz_pw'** value in the script.   

The detials in the script are following:
>
   **EMUCH_UID_VALUE = ' '**, here, hard code **'_discuz_uid'** value   
   **EMUCH_PW_VALUE = ' '**, here, hard code **'_discuz_pw'** value 

### For the script *emuch_coins.py* ###

This script reads the json file *emuch_cookies.json* to grab your emuch.net cookies name and value,
 so you would not need to modify the script.  
The json file should be in same directory with *emuch_coins.py*.

The cookies file is following:
>
   {  
   "_discuz_uid": "  ",   
   "_discuz_pw": "  "}   


[emuch]:[http://emuch.net/bbs/]
