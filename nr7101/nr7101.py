#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import base64
import requests
import urllib3

logger = logging.getLogger(__name__)

def get_status(url, username, password):
    password_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    login = '{"Input_Account":"%s","Input_Passwd":"%s","currLang":"en","RememberPassword":0,"SHA512_password":false}' % (username, password_b64)

    with requests.Session() as s:
        # NR7101 is using by default self-signed certificates
        s.verify = False
        urllib3.disable_warnings()

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

        # Get data
        r = s.get(url + '/cgi-bin/DAL?oid=cellwan_status')
        assert r.status_code == 200
        j = r.json()
        assert j['result'] == 'ZCFG_SUCCESS'
        status = j['Object'][0]

        # Logout
        r = s.get(f'{url}/cgi-bin/UserLogout?sessionkey={sessionkey}')
        assert r.status_code == 200

    return status