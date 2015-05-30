#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, re
import http.cookiejar, urllib.request

from datetime import datetime
from user_info import username, password

DOMAIN = r'emuch.net'
URL = r'http://' + DOMAIN
LOGIN_URL = URL + r'/bbs/logging.php?action=login'
CREDIT_ACTION = URL + r'/bbs/memcp.php?action=getcredit'
CREDIT_TOKEN = u'creditsubmit=领取红包'
LOGIN_T_FHASH = u'action=login&t=(\d+)">\\n.*value="(.+)">\\n'.encode('gb18030')
LOGIN_VERF_CODE = u'>问题：(\d+)(.+)以(\d+)等于多少\?<br>.+name="post_sec_hash" value="(.+)" ><in'.encode('gb18030')
CREDIT_RSPD = u'(已经连续 \d+ 天坚持领取红包了|今天的红包，您已经领取了)'.encode('gb18030')
EMUCH_CREDITS = U'>金币: \d+(|\.|\.\d+)<'.encode('gb18030')

def verify_code(frst, oprt, secd):
    if oprt == '加':
       return int(frst) + int(secd)
    if oprt == '减':
       return int(frst) - int(secd)
    if oprt == '乘':
       return int(frst) * int(secd)
    if oprt == '除':
       return int(frst) // int(secd)

if __name__ == '__main__':
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Add following contents of HTTP header fields, pretend a browser to access the site.
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; rv:38.0) Gecko/20100101 Firefox/38.0')
        , ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        , ('Accept-Language', 'en-US,en;q=0.5')
        , ('Referer', LOGIN_URL)
    ]

# Get key 't' and 'formhash' value from emuch.net  
    data = opener.open(LOGIN_URL).read()
    rspd = re.search(LOGIN_T_FHASH, data)
    if rspd:
       t = (rspd.group(1)).decode('gb18030')
       formhash = (rspd.group(2)).decode('gb18030')
    else:
       print('Oops! Get nothing for the \'t\' and \'formhash\'.') 
       sys.exit()

# first sign in with username and password, and get verification code if ok
    login_url = '{}&t={}'.format(LOGIN_URL, t)
    post_data = 'username={}&password={}&formhash={}&referer=&loginsubmit=会员登录'\
              .format(username, password, formhash).encode('utf8')
    data = opener.open(login_url, data=post_data).read()
    rspd = re.search(LOGIN_VERF_CODE, data)
    if rspd:
       post_sec_code = verify_code(
                         (rspd.group(1)).decode('gb18030')
                         , (rspd.group(2)).decode('gb18030')
                         , (rspd.group(3)).decode('gb18030')
                        )
       post_sec_hash = (rspd.group(4)).decode('gb18030')
    else:
       print ('Oops! Get nothing for verification and \'post_sec_code\'.')
       sys.exit()

# second submit verification code to complete sign processing
    post_data ='post_sec_code={}&post_sec_hash={}&username={}&loginsubmit=提交'\
              .format(post_sec_code, post_sec_hash, username).encode('utf8')
    opener.open(login_url, data=post_data)

# Take the daily sign credits in emuch.net
    data = opener.open(CREDIT_ACTION, data=CREDIT_TOKEN.encode('utf8')).read()

# Check the response data if got the daily credits. 
    match = re.search(CREDIT_RSPD, data)
    if match:
        rspd = re.search(EMUCH_CREDITS, data)
        print(datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"), '%s。您总共有-%s-' 
            %((match.group()).decode('gb18030'), (rspd.group()).decode('gb18030')))
    else:
        print(datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"), 
            'Oops! There\'s something wrong with taking Emuch Coins.')

