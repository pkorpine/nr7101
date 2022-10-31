#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import time
import requests

logger = logging.getLogger(__name__)


def is_connection_ok(urls):
    for url in urls:
        try:
            with requests.get(url, timeout=5) as r:
                # OK
                return True
        except Exception as e:
            logger.error(f"{url} failed: {e}")
    return False


def rebooter(nr, sleep, threshold, reboot_delay, urls):
    last_up: datetime = datetime.now()

    while True:
        logger.debug("Sleeping...")
        time.sleep(sleep.total_seconds())

        if is_connection_ok(urls):
            # All good.
            logger.info("Check OK.")
            last_up = datetime.now()
            continue

        logger.warning("Check failed.")
        if (datetime.now() - last_up) < threshold:
            # Still within limits
            continue

        # Not good, issue a reboot.
        try:
            logger.warning("Not good, issuing a reboot.")

            nr.reboot()
        except Exception as e:
            logger.error(f"reboot failed: {e}")

        logger.debug("Waiting after reboot...")
        time.sleep(reboot_delay.total_seconds())
