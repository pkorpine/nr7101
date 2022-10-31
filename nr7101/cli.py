#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import json
import http.client
from .nr7101 import NR7101
from .version import __version__

RETRY_COUNT = 2

logger = logging.getLogger(__name__)


def cli():
    parser = argparse.ArgumentParser(
        description=f"NR7101 status fetcher v{__version__}"
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--cookie", default=".nr7101.cookie")
    parser.add_argument("--no-cookie", action="store_true")
    parser.add_argument(
        "--reboot",
        action="store_true",
        help="Reboot the unit if the connection is down",
    )
    parser.add_argument(
        "--force-reboot",
        action="store_true",
        help="Reboot the unit regardless of the connection status",
    )
    parser.add_argument("url")
    parser.add_argument("username")
    parser.add_argument("password")

    args = parser.parse_args()

    dev = NR7101(args.url, args.username, args.password)

    if not args.no_cookie:
        dev.load_cookies(args.cookie)

    if args.verbose > 0:
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    status = None

    for _retry in range(RETRY_COUNT):
        try:
            status = dev.get_status(RETRY_COUNT)
            if not args.no_cookie:
                dev.store_cookies(args.cookie)
            break
        except OSError:
            logger.warn("Unable to connect")
        except TimeoutError:
            logger.warn("Timeout")
        except ConnectionError:
            pass

    print(json.dumps(status, indent=2))

    if status is None:
        return 1

    do_reboot = False
    if status["cellular"]["INTF_Status"] == "Down":
        logger.warn("The connection is down.")
        if args.reboot:
            do_reboot = True

    if do_reboot or args.force_reboot:
        logger.warn("Rebooting")
        dev.reboot()

    return 0


if __name__ == "__main__":
    import sys

    rc = cli()
    sys.exit(rc)
