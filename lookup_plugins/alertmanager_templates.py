#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2022-2023, Bodo Schulz <bodo@boone-schulz.de>
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

- name: Copy each template over that matches the given pattern
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: "/etc/alertmanager/templates/"
    owner: "root"
    mode: 0640
  with_fileglob:
    - ".tmpl"
  vars:
    alertmanager:
      search_path:
        - ".."
        - "../.."
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
        ansible_search_path = variables.get('ansible_search_path', None)
        role_path = variables.get('role_path')
        alertmanager_search_path = variables.get('alertmanager', {}).get('search_path', None)

        # display.v(f" - ansible_search_path : {ansible_search_path}")
        # display.v(f" - base dir            : {self.get_basedir(variables)}")
        # display.v(f" - role path           : {role_path}")
        # display.v(f" - template search path: {alertmanager_search_path}")
        # display.v(f" - alertmanager        : {variables.get('alertmanager', {})}")

        if ansible_search_path:
            paths = ansible_search_path
        else:
            paths.append(self.get_basedir(variables))

        if alertmanager_search_path:
            if isinstance(alertmanager_search_path, list):
                for p in alertmanager_search_path:
                    paths.append(os.path.join(role_path, p))

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

        display.vv(f"found_templates {ret}")

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
