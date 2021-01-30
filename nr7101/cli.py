#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import json
import http.client
from .nr7101 import get_status
from .version import __version__

RETRY_COUNT = 5

logger = logging.getLogger(__name__)


def load_cookies(cookiefile):
    cookies = {}
    try:
        with open(cookiefile, 'rt') as f:
            cookies = json.load(f)
        logger.debug("Cookies loaded")
    except FileNotFoundError:
        logger.debug("Cookie file does not exist, ignoring.")
    except json.JSONDecodeError:
        logger.warn("Ignoring invalid cookie file.")
    return cookies


def store_cookies(cookies, cookiefile):
    with open(cookiefile, 'wt') as f:
        json.dump(cookies, f)
    logger.debug("Cookies saved")


def cli():
    parser = argparse.ArgumentParser(description=f'NR7101 status fetcher v{__version__}')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--cookie', default='.nr7101.cookie')
    parser.add_argument('--no-cookie', action='store_true')
    parser.add_argument('url')
    parser.add_argument('username')
    parser.add_argument('password')

    args = parser.parse_args()

    params = {}
    if not args.no_cookie:
        params['cookies'] = load_cookies(args.cookie)

    if args.verbose > 0:
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    for _retry in range(RETRY_COUNT):
        try:
            status = get_status(args.url, args.username, args.password, params)
            print(json.dumps(status, indent=2))

            if not args.no_cookie:
                store_cookies(params['cookies'], args.cookie)
            break
        except OSError:
            logger.warn("Unable to connect")
        except TimeoutError:
            logger.warn("Timeout")
        except ConnectionError:
            pass


if __name__ == "__main__":
    cli()
