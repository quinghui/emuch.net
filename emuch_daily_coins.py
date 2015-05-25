#!/usr/bin/python3
# -*- coding: utf-8 -*-

import http.cookiejar, urllib.request
import re
from datetime import datetime

# After log the emuch.net in, take the cookies' 
# names "_discuz_uid" and "_discuz_pw" with their 
# contents' value in the site emuch.net.
EMUCH_UID_NAME = '_discuz_uid'    
EMUCH_UID_VALUE = ' '       # the value of the cookie [_discuz_uid]
EMUCH_PW_NAME = '_discuz_pw'
EMUCH_PW_VALUE = ' '        # the value of the cookie [_discuz_pw]

EMUCH_DOMAIN = r'emuch.net'
EMUCH_URL = r'http://' + EMUCH_DOMAIN

EMUCH_CREDIT_ACTION = EMUCH_URL + r'/bbs/memcp.php?action=getcredit'
EMUCH_CREDIT_TOKEN = u'creditsubmit=领取红包'.encode('utf8')
EMUCH_CREDIT_RSPD = u'(已经连续 \d+ 天坚持领取红包了|今天的红包，您已经领取了)'.encode('gb18030')
EMUCH_CREDITS = U'>金币: \d+(|\.|\.\d+)<'.encode('gb18030')

if __name__ == '__main__':
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Add following contents of HTTP header fields, and pretend a browser to access the site. 
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; rv:38.0) Gecko/20100101 Firefox/38.0')
        , ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        , ('Accept-Language', 'en-US,en;q=0.5')
        , ('Referer', EMUCH_CREDIT_ACTION)
    ]
    request = urllib.request.Request(EMUCH_URL)
    response = opener.open(request)

# Add cookies '_discuz_uid' and '_discuz_pw', and their values in CookieJar cj.
    response.headers.add_header('Set-Cookie', '%s=%s' %(EMUCH_UID_NAME, EMUCH_UID_VALUE))
    response.headers.add_header('Set-Cookie', '%s=%s' %(EMUCH_PW_NAME, EMUCH_PW_VALUE))
    cj.extract_cookies(response, request)

# Take the daily credits in emuch.net
    data = opener.open(EMUCH_CREDIT_ACTION, data=EMUCH_CREDIT_TOKEN).read()

# Check the response data if got the daily credits. 
    match = re.search(EMUCH_CREDIT_RSPD, data)
    if match:
        rspd = re.search(EMUCH_CREDITS, data)
        print(datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"), '%s。您总共有-%s-' 
            %((match.group()).decode('gb18030'), (rspd.group()).decode('gb18030')))
    else:
        print(datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"), 
            'Oops! There\'s something wrong with taking Emuch Coins.')

