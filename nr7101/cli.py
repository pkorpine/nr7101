#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import http.client
from .nr7101 import get_status

def cli():
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser(description='NR7101 status fetcher')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('url')
    parser.add_argument('username')
    parser.add_argument('password')

    args = parser.parse_args()

    if args.verbose > 0:
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    try:
        status = get_status(args.url, args.username, args.password)
        if status:
            pprint(status)
    except OSError:
        logger.error("Unable to connect")

if __name__ == "__main__":
    cli()