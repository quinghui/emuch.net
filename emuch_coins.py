#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, re
import http.cookiejar, urllib.request
import json
from datetime import datetime

EMUCH_COOKIE_FILE = 'emuch_cookies.json'
EMUCH_DOMAIN = r'emuch.net'
EMUCH_URL = r'http://' + EMUCH_DOMAIN
EMUCH_CREDIT_ACTION = EMUCH_URL + r'/bbs/memcp.php?action=getcredit'
EMUCH_CREDIT_TOKEN = u'creditsubmit=领取红包'.encode('utf8')
EMUCH_CREDIT_RSPD = u'(已经连续 \d+ 天坚持领取红包了|今天的红包，您已经领取了)'.encode('gb18030')
EMUCH_CREDITS = U'>金币: \d+(|\.|\.\d+)<'.encode('gb18030')

# Get the current script file's absolute path where the EMUCH_COOKIE_FILE is located in. 
def get_file_path():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

if __name__ == '__main__':
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Add following contents of HTTP header fields, pretend a browser to access the site.
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; rv:38.0) Gecko/20100101 Firefox/38.0')
        , ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        , ('Accept-Language', 'en-US,en;q=0.5')
        , ('Referer', EMUCH_CREDIT_ACTION)
    ]
    rqst = urllib.request.Request(EMUCH_URL)
    rspd = opener.open(rqst)
    
# Read a JSON file for cookies' name and value.
    cookie_filename = '{}/{}'.format(get_file_path(), EMUCH_COOKIE_FILE)
    with open(cookie_filename, encoding='utf8') as cookie_file:
        emuch_cookie = json.loads(cookie_file.read())
        
# Add cookie name and value in CookieJar cj.
    for name, value in emuch_cookie.items():
        rspd.headers.add_header('Set-Cookie', '{}={}'.format(name, value))
    cj.extract_cookies(rspd, rqst)

# Take the daily credits
    data = (opener.open(EMUCH_CREDIT_ACTION, data=EMUCH_CREDIT_TOKEN)).read()

# Check the response data if got the daily credits. 
    match = re.search(EMUCH_CREDIT_RSPD, data)
    if match:
        rspd = re.search(EMUCH_CREDITS, data)
        print(datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"), '%s。您总共有-%s-' 
            %((match.group()).decode('gb18030'), (rspd.group()).decode('gb18030')))
    else:
        print(datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"), 
              'Oops! There\'s something wrong with taking Emuch Coins.')
    

