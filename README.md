
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

## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```

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

### An important note for Go Templates

The Alertmanager uses Go templates to customise the notifications to individual needs.  
Unfortunately, I have not been able to find much useful documentation or howtos for creating my own templates.

The default mail templates are compiled directly in the Alertmanager binary.  
You can see the default templates on GitHub:
 - [default.tmpl](https://raw.githubusercontent.com/prometheus/alertmanager/master/template/default.tmpl)
 - [email.tmpl](https://raw.githubusercontent.com/prometheus/alertmanager/master/template/email.tmpl)

My own poor attempt can be seen [here](files/alertmanager/templates/mail.example).

Maybe there is someone who can find a good howto and give me a link to it?


> Go templates offer a similar syntax to Jinja2.  
> Therefore, it is difficult to transfer them cleanly via Ansible to the target system.  
> You can transfer the templates as base64 coded strings, but then you have to take
> care of decoding them yourself.  
> This always requires more effort in the form of a separate module.
>
> Alternatively, you can mark the corresponding string with [`!unsafe`](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_advanced_syntax.html#unsafe-or-raw-strings).
>
> Ansible can handle this. But then the molecule tests fail!
>
> Yes, you could also use `{% raw %}{% endraw %}`, but then filters like `combine()`
> are no longer usable.

Here is an example of how to use unsafe:
```
alertmanager_receivers:
  blackhole: {}
  team-X-mails:
    email_configs:
      - to: 'team-X+alerts@example.org'
        headers:
          subject: !unsafe "{{ template \"custom_mail_subject\" . }}"
        html: !unsafe '{{ template "custom_mail_html" . }}'
```


### `alertmanager_amtool`

```yaml
alertmanager_amtool:
  config_dir: /etc/amtool
  # Location (URL) of the alertmanager
  alertmanager_url: "{{ alertmanager_service.web.external_url }}"
  # Extended output of `amtool` commands, use '' for less verbosity
  output: extended
```

### `alertmanager_service`

```yaml
alertmanager_service:
  log:
    level: debug
    format: ""
  web:
    listen_address: '127.0.0.1:9093'
    external_url: 'http://molecule.docker.local'
```

### `alertmanager_global`

```yaml
alertmanager_global:
  resolve_timeout: 5m
  smtp:
    smarthost: 'localhost:25'
    from: 'alertmanager@example.org'
    auth_username: 'alertmanager'
    auth_password: 'password'
  opsgenie: {}
  slack: {}
```

### `alertmanager_receivers`

```yaml
alertmanager_receivers:
  blackhole: {}
  team-X-mails:
    email_configs:
      - to: 'team-X+alerts@example.org'
        headers:
          subject: !unsafe "{{ template \"custom_mail_subject\" . }}"
        html: !unsafe '{{ template "custom_mail_html" . }}'

  team-DB-pager:
    pagerduty_configs:
      - service_key: <team-DB-key>
  smtp: {}
  slack: {}
  slack_qa: {}
  opsgenie: {}
```

### `alertmanager_routes`

```yaml
alertmanager_route:
  group_by:
    - 'alertname'
    - 'service'
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  default_receiver: blackhole

  routes:
    # capture all 'test' severity
    - description: capture all 'test' severity for blackhole
      receiver: blackhole
      match:
        severity: test

    # capture 'critical' severity
    - description: capture 'critical' severity
      matchers:
        - severity="critical"
      receiver: blackhole

      routes:
        # forward DEV to 'blackhole'
        - matchers:
            - environment=DEV
          receiver: blackhole

        - description: "Forward all \"service: cadvisor\" to 'blackhole'"
          match:
            service: cadvisor
          receiver: blackhole

        - description: "forward DEV to 'blackhole'"
          matchers:
            - environment=~".*(-dev).*"
          receiver: blackhole
```

### `alertmanager_inhibit_rules`

```yaml
alertmanager_inhibit_rules:
  - description: >
      inhibit rule for flimflamflum
      and foo with bar
    source_matchers: [severity="critical"]
    target_matchers: [severity="warning"]
    # Apply inhibition if the alertname is the same.
    # CAUTION:
    #   If all label names listed in `equal` are missing
    #   from both the source and target alerts,
    #   the inhibition rule will apply!
    equal: [alertname, cluster, service]
  - target_matchers: [environment="QA"]
  - target_matchers:
      - severity=~"warning|info"
    source_matchers:
      - severity=critical
    equal:
      - cluster
      - namespace
      - alertname
```

### `alertmanager_time_intervals`

```yaml
alertmanager_time_intervals:
  out-of-business-hours:
    description: only receive alarms during weekdays, between 08:00 and 18:00
    time_intervals:
      # Mute on Saturdays and Sundays, all day.
      - weekdays:
        - 'Saturday'
        - 'Sunday'
      # Mute in the morning and in the evening, any day.
      - times:
          - start_time: '00:00'
            end_time: '08:00'
          - start_time: '18:00'
            end_time: '24:00'
  foo:
    time_intervals:
      # - times:
      - weekdays:
          - 'monday:friday'
```

### `alertmanager_templates`

In order to be able to use your own templates, it is sufficient to provide these files with a file extension 
`.tmpl` and to make them available to the role in a directory called `files` or `templates`.
The lookup plugin `bodsch.core.file_glob` will pick up these files.  

```yaml
alertmanager_templates:
  - '{{ alertmanager_config_dir }}/templates/*.tmpl'
```


----

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
