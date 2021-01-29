#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import json
import base64
import requests
import urllib3

logger = logging.getLogger(__name__)


def get_status(url, username, password, params={}):
    password_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    login = {
        'Input_Account': username,
        'Input_Passwd': password_b64,
        'currLang': 'en',
        'RememberPassword': 0,
        'SHA512_password': False,
    }
    login_json = json.dumps(login)

    # NR7101 is using by default self-signed certificates, so ignore the warnings
    params['verify'] = False
    urllib3.disable_warnings()

    # Check connection
    with requests.get(url + '/getBasicInformation', **params) as r:
        assert r.status_code == 200
        assert r.json()['result'] == 'ZCFG_SUCCESS', 'Connection failure'

    # Login
    with requests.post(url + '/UserLogin', data=login_json, **params) as r:
        if r.status_code != 200:
            logger.error('Unauthorized')
            return
        sessionkey = r.json()['sessionkey']

        # Update cookies
        params['cookies'] = requests.utils.dict_from_cookiejar(r.cookies)

    # Check login
    with requests.get(url + '/UserLoginCheck', **params) as r:
        assert r.status_code == 200

    # Get cellular status
    with requests.get(url + '/cgi-bin/DAL?oid=cellwan_status', **params) as r:
        if r.status_code == 504:
            # NR7101 sometimes respons "Timeout"
            raise TimeoutError
        if r.status_code != 200:
            logger.error('Unable to fetch cellwan_status. Status=%d %s', r.status_code, r.text)
            raise ConnectionError
        j = r.json()
        assert j['result'] == 'ZCFG_SUCCESS'
        status = j['Object'][0]

    # Logout
    with requests.get(f'{url}/cgi-bin/UserLogout?sessionkey={sessionkey}', **params) as r:
        assert r.status_code == 200

    return status
