
# Ansible Role:  `alertmanager` 

Ansible role to install and configure [alertmanager](https://github.com/prometheus/alertmanager).

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-alertmanager/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-alertmanager)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-alertmanager)][releases]

[ci]: https://github.com/bodsch/ansible-alertmanager/actions
[issues]: https://github.com/bodsch/ansible-alertmanager/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-alertmanager/releases


If `latest` is set for `prometheus_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/alertmanager/${prometheus_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The alertmanager archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/alertmanager`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `prometheus_direct_download` to `true`.


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

```

----

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
