#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import json
import base64
import requests
import urllib3

logger = logging.getLogger(__name__)


class NR7101Exception(Exception):
    def __init__(self, error):
        self.error = error


class NR7101:
    def __init__(self, url, username, password, params={}):
        self.url = url
        self.params = params
        password_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        self.login_params = {
            'Input_Account': username,
            'Input_Passwd': password_b64,
            'currLang': 'en',
            'RememberPassword': 0,
            'SHA512_password': False,
        }

        # NR7101 is using by default self-signed certificates, so ignore the warnings
        self.params['verify'] = False
        urllib3.disable_warnings()

    def load_cookies(self, cookiefile):
        cookies = {}
        try:
            with open(cookiefile, 'rt') as f:
                cookies = json.load(f)
            logger.debug('Cookies loaded')
            self.params['cookies'] = cookies
        except FileNotFoundError:
            logger.debug('Cookie file does not exist, ignoring.')
        except json.JSONDecodeError:
            logger.warn('Ignoring invalid cookie file.')

    def store_cookies(self, cookiefile):
        try:
            cookies = self.params['cookies']
        except KeyError:
            logger.warn('No cookie to write')
            return

        with open(cookiefile, 'wt') as f:
            json.dump(cookies, f)
        logger.debug('Cookies saved')

    def login(self):
        login_json = json.dumps(self.login_params)

        with requests.post(self.url + '/UserLogin', data=login_json, **self.params) as r:
            if r.status_code != 200:
                logger.error('Unauthorized')
                return

            # Update cookies
            self.params['cookies'] = requests.utils.dict_from_cookiejar(r.cookies)

            return r.json()['sessionkey']

    def logout(self, sessionkey):
        with requests.get(f'{self.url}/cgi-bin/UserLogout?sessionkey={sessionkey}', **self.params) as r:
            assert r.status_code == 200

    def connect(self):
        with requests.get(self.url + '/getBasicInformation', **self.params) as r:
            assert r.status_code == 200
            assert r.json()['result'] == 'ZCFG_SUCCESS', 'Connection failure'

        # Check login
        with requests.get(self.url + '/UserLoginCheck', **self.params) as r:
            assert r.status_code == 200

    def get_status(self, retries=1):
        def parse_traffic_object(obj):
            ret = {}
            for iface, iface_st in zip(obj['ipIface'], obj['ipIfaceSt']):
                ret[iface['X_ZYXEL_IfName']] = iface_st
            return ret

        while retries > 0:
            try:
                cellular = self.get_json_object('cellwan_status')
                traffic = parse_traffic_object(self.get_json_object('Traffic_Status'))
                return {
                    'cellular': cellular,
                    'traffic': traffic,
                }
            except requests.exceptions.HTTPError as e:
                logger.warn(e)
                if e.response.status_code == 401:
                    # Unauthorized
                    self.info('Login')
                    self.login()
                else:
                    retries -= 1

        return None

    def get_json_object(self, oid):
        with requests.get(self.url + '/cgi-bin/DAL?oid=' + oid, **self.params) as r:
            r.raise_for_status()
            j = r.json()
            assert j['result'] == 'ZCFG_SUCCESS'
            return j['Object'][0]
