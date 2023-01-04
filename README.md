
# Ansible Role:  `alertmanager` 

Ansible role to install and configure [alertmanager](https://github.com/prometheus/alertmanager).

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-alertmanager/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-alertmanager)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-alertmanager)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-alertmanager/actions
[issues]: https://github.com/bodsch/ansible-alertmanager/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-alertmanager/releases
[quality]: https://galaxy.ansible.com/bodsch/alertmanager


If `latest` is set for `alertmanager_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/alertmanager/${alertmanager_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The alertmanager archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/alertmanager`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `alertmanager_direct_download` to `true`.


## Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.10


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-alertmanager/tags)!

## Configuration

```yaml
alertmanager_version: 0.25.0

alertmanager_release_download_url: https://github.com/prometheus/alertmanager/releases

alertmanager_system_user: alertmanager
alertmanager_system_group: alertmanager
alertmanager_config_dir: /etc/alertmanager
alertmanager_data_dir: /var/lib/alertmanager

alertmanager_enable_experimental: false

alertmanager_direct_download: false

alertmanager_amtool: {}

alertmanager_service: {}
alertmanager_global: {}
alertmanager_templates:
  - '{{ alertmanager_config_dir }}/templates/*.tmpl'

alertmanager_receivers: []
alertmanager_routes: {}
alertmanager_inhibit_rules: []
alertmanager_time_intervals: {}
```

----

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
