# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

import re

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'alertmanager_checksum': self.checksum,
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
