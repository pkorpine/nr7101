#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import base64
import json
import requests
import urllib3

logger = logging.getLogger(__name__)

def get_status(url, username, password, cookiefile=None):
    password_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    login = '{"Input_Account":"%s","Input_Passwd":"%s","currLang":"en","RememberPassword":0,"SHA512_password":false}' % (username, password_b64)

    with requests.Session() as s:
        # NR7101 is using by default self-signed certificates
        s.verify = False
        urllib3.disable_warnings()

        # Read cookiefile
        if cookiefile:
            try:
                with open(cookiefile, 'rt') as f:
                    cookies = json.load(f)
                requests.utils.add_dict_to_cookiejar(s.cookies, cookies)
                logger.debug("Loaded cookies")
            except FileNotFoundError:
                logger.debug("Cookie file does not exist, ignoring.")

        # Check connection
        r = s.get(url + '/getBasicInformation')
        assert r.status_code == 200
        assert r.json()['result'] == 'ZCFG_SUCCESS', 'Connection failure'

        # Login
        r = s.post(url + '/UserLogin', data=login)
        if r.status_code != 200:
            logger.error('Unauthorized')
            return
        sessionkey = r.json()['sessionkey']

        # (optional)
        r = s.get(url + '/UserLoginCheck')
        assert r.status_code == 200

        # Get data
        r = s.get(url + '/cgi-bin/DAL?oid=cellwan_status')
        assert r.status_code == 200
        j = r.json()
        assert j['result'] == 'ZCFG_SUCCESS'
        status = j['Object'][0]

        # Logout
        r = s.get(f'{url}/cgi-bin/UserLogout?sessionkey={sessionkey}')
        assert r.status_code == 200

        # Write cookiefile
        if cookiefile:
            cookies = requests.utils.dict_from_cookiejar(s.cookies)
            with open(cookiefile, 'wt') as f:
                json.dump(cookies, f)
            logger.debug("Cookies saved")

    return status