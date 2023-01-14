#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2023,Bodo Schulz <bodo@boone-schulz.de>
# Apache License  (see COPYING or https://opensource.org/licenses/Apache-2.0)
# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
from ansible.utils.display import Display
from ansible.plugins.lookup import LookupBase
import os
__metaclass__ = type

DOCUMENTATION = """
    name: alertmanager_templates
    author: Bodo Schulz
    version_added: "1.0"
    short_description: list alertmanager templates matching a pattern
    description:
        - Find all files in a directory tree that match a pattern (recursively).
    options:
      _terms:
        description: path(s) of files to read
        required: True
    notes:
      - Patterns are only supported on files, not directory/paths.
      - Matching is against local system files on the Ansible controller.
        To iterate a list of files on a remote node, use the M(ansible.builtin.find) module.
      - Returns a string list of paths joined by commas, or an empty list if no files match. For a 'true list' pass C(wantlist=True) to the lookup.
"""

EXAMPLES = """
- name: Display paths of all .tmpl files
  ansible.builtin.debug: msg={{ lookup('alertmanager_templates', '.tmpl') }}

- name: Copy each template over that matches the given pattern
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: "/etc/alertmanager/templates/"
    owner: "root"
    mode: 0640
  with_fileglob:
    - ".tmpl"
"""

RETURN = """
  _list:
    description:
      - list of files
    type: list
    elements: path
"""


display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        """
        """
        self.set_options(direct=kwargs)
        paths = []
        if 'ansible_search_path' in variables:
            paths = variables['ansible_search_path']
        else:
            paths = [self.get_basedir(variables)]

        search_path = ['templates', 'files']

        ret = []
        found_templates = []

        for term in terms:
            """
            """
            for p in paths:
                for sp in search_path:
                    path = os.path.join(p, sp)

                    display.vv(f" - lookup in directory: {path}")
                    r = self._find_recursive(folder=path, extension=term)
                    if len(r) > 0:
                        found_templates.append(r)

        ret = self._flatten(found_templates)

        display.v(f"found_templates {ret}")

        return ret

    def _find_recursive(self, folder, extension):
        """
        """
        matches = []

        for root, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if filename.endswith(extension):
                    matches.append(os.path.join(root, filename))

        return matches
