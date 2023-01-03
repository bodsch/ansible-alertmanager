# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

import os
import re
import json
import base64

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'alertmanager_checksum': self.checksum,
            'remove_empty_elements': self.remove_empty_elements,
            'jinja_encode': self.jinja_encode,
        }
    def checksum(self, data, os, arch):
        """
        """
        display.v(f"checksum(self, data, {os}, {arch})")

        checksum = None

        if isinstance(data, list):
            # 206cf787c01921574ca171220bb9b48b043c3ad6e744017030fed586eb48e04b  alertmanager-0.25.0.linux-amd64.tar.gz
            # filter OS
            # linux = [x for x in data if re.search(fr".*alertmanager-.*.{os}.*.tar.gz", x)]
            # filter OS and ARCH
            checksum = [x for x in data if re.search(fr".*alertmanager-.*.{os}-{arch}.tar.gz", x)][0]

        if isinstance(checksum, str):
            checksum = checksum.split(" ")[0]

        display.v(f"= checksum: {checksum}")

        return checksum

    def remove_empty_elements(self, data):
        """
        """
        data_copy = data.copy()

        if isinstance(data_copy, dict):
            """
            """
            result = {k: v for k, v in data_copy.items() if v}

            display.v(f"= result: {result}")

            return result

    def jinja_encode(self, data):
        """
        """
        # display.v(f"jinja_encode({data})")
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True).encode('utf-8')
        elif isinstance(data, list):
            data = json.dumps(data, sort_keys=True).encode('utf-8')
        else:
            data = data.encode('utf-8')

        result = base64.b64encode(data).decode('utf-8')
        # display.v(f"= result: {result}")

        return result
