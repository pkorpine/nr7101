#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import json
import http.client
from datetime import timedelta
from .nr7101 import NR7101
from .rebooter import rebooter
from .version import __version__

RETRY_COUNT = 2

logger = logging.getLogger(__name__)


def cli():
    parser = argparse.ArgumentParser(
        description=f"NR7101 status fetcher v{__version__}", fromfile_prefix_chars="@"
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
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor given URLs and issue reboot if no response",
    )
    parser.add_argument(
        "--monitor-interval", type=int, default=60, help="Monitor interval in seconds"
    )
    parser.add_argument(
        "--monitor-threshold",
        type=int,
        default=300,
        help="Grace period before issueing reboot",
    )
    parser.add_argument("--monitor-url", "-u", action="append", help="URL to monitor")
    parser.add_argument("url")
    parser.add_argument("username")
    parser.add_argument("password")

    args = parser.parse_args()

    dev = NR7101(args.url, args.username, args.password)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )

    if args.verbose > 0:
        http.client.HTTPConnection.debuglevel = 1
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    status = None

    if args.monitor:
        delay = timedelta(seconds=args.monitor_interval)
        threshold = timedelta(seconds=args.monitor_threshold)
        reboot_delay = timedelta(minutes=5)
        if len(args.monitor_url) == 0:
            logger.error("Use --monitor-url/-u to define URLs to monitor")
            return -1
        rebooter(dev, delay, threshold, reboot_delay, args.monitor_url)
        return 0  # Never reached

    if not args.no_cookie:
        dev.load_cookies(args.cookie)

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
