# Execution Module acme_sh

The `acme_sh` module provides an interface to [acme.sh](https://acme.sh).

`acme.sh` is installed in the user's home directory.
You can specify a different user with the `user` parameter, but you are not able to specify a different install path.
Of course you can change the cert path with the `cert_path` parameter.

## Available functions

- [acme_sh.issue](#acme_shissue)
- [acme_sh.install](#acme_shinstall)
- [acme_sh.renew](#acme_shrenew)
- [acme_sh.info](#acme_shinfo)
- [acme_shl.version](#acmesh_version)

### acme_sh.issue

Issues a certificate with `acme.sh`.

| Parameter         | Type      | Required                                | Default          | Description                                                                     |
| ----------------- | --------- | --------------------------------------- | ---------------- | ------------------------------------------------------------------------------- |
| `name`            | `str`     | `True`                                  |                  | Domain to issue certificate for.                                                |
| `acme_mode`       | `str`     | `True`                                  |                  | Mode to issue certificate with. (webroot, standalone, standalone-tls-alpn, dns) |
| `aliases`         | `str,str` | `False`                                 | `None`           | List of aliases to issue certificate for.                                       |
| `server`          | `str`     | `False`                                 | `letsencrypt`    | ACME server to use.                                                             |
| `keysize`         | `str`     | `False`                                 | `4096`           | Key size to use.                                                                |
| `dns_plugin`      | `str`     | `False`, `True` if acme_mode is dns     | `None`           | DNS plugin to use.                                                              |
| `dns_credentials` | `dict`    | `False`, `True` if acme_mode is dns     | `None`           | DNS plugin credentials to use.                                                  |
| `webroot`         | `str`     | `False`, `True` if acme_mode is webroot | `None`           | Webroot path to use.                                                            |
| `http_port`       | `str`     | `False`                                 | `80`             | HTTP port to use.                                                               |
| `user`            | `str`     | `False`                                 | `root`           | User to run acme.sh as.                                                         |
| `cert_path`       | `str`     | `False`                                 | `$HOME/.acme.sh` | Path to store certificates in.                                                  |
| `force`           | `bool`    | `False`                                 | `False`          | Force issue certificate.                                                        |
| `valid_to`        | `str`     | `False`                                 | `None`           | Validity of certificate.                                                        |
| `valid_from`      | `str`     | `False`                                 | `None`           | Validity of certificate.                                                        |
| `insecure`        | `bool`    | `False`                                 | `False`          | Don't verify SSL-Cert of acme server                                            |

**Server**

You can define a custom server, or use one of the following:

https://github.com/acmesh-official/acme.sh/wiki/Server

**DNS Plugins**

You can use the following DNS plugins:

https://github.com/acmesh-official/acme.sh/wiki/dnsapi

**DNS Credentials**

Credentials are defined as a dictionary:

`{ "key": "value" }`

If acme mode is `dns`, this parameter is required.

**Keysize**

The following key sizes are supported:

https://github.com/acmesh-official/acme.sh#10-issue-ecc-certificates

**Cert Path**

The cert path default is `$HOME/.acme.sh`.
If you specify a different path, e.g. `/etc/acme`, your certificate will be stored `/etc/acme/example.com`.

### acme_sh.install

Installs `acme.sh`.

| Parameter | Type   | Required | Default | Description                            |
| --------- | ------ | -------- | ------- | -------------------------------------- |
| `email`   | `str`  | `True`   |         | Email address to use for registration. |
| `user`    | `str`  | `False`  | `root`  | User to run acme.sh as.                |
| `upgrade` | `bool` | `False`  | `False` | Upgrade acme.sh.                       |
| `force`   | `bool` | `False`  | `False` | Force install acme.sh.                 |

The installation is done with `--nocron` parameter.

### acme_sh.register

Register account @ zeroSSL CA.

| Parameter | Type  | Required | Default | Description             |
| --------- | ----- | -------- | ------- | ----------------------- |
| `email`   | `str` | `True`   |         | Email address to use.   |
| `user`    | `str` | `False`  | `root`  | User to run acme.sh as. |

### acme_sh.renew

Renews a certificate with `acme.sh`.

| Parameter   | Type   | Required | Default          | Description                          |
| ----------- | ------ | -------- | ---------------- | ------------------------------------ |
| `name`      | `str`  | `True`   |                  | Domain to renew certificate for.     |
| `user`      | `str`  | `False`  | `root`           | User to run acme.sh as.              |
| `cert_path` | `str`  | `False`  | `$HOME/.acme.sh` | Path to store certificates in.       |
| `force`     | `bool` | `False`  | `False`          | Force renew certificate.             |
| `insecure`  | `bool` | `False`  | `False`          | Don't verify SSL-Cert of acme server |

### acme_sh.info

Returns information about a certificate.

| Parameter   | Type  | Required | Default          | Description                           |
| ----------- | ----- | -------- | ---------------- | ------------------------------------- |
| `name`      | `str` | `True`   |                  | Domain name of certificate            |
| `user`      | `str` | `False`  | `root`           | User to run acme.sh as.               |
| `cert_path` | `str` | `False`  | `$HOME/.acme.sh` | Path where certificates are stored in |

### acme_sh.version

Returns the version of `acme.sh`.

| Parameter | Type  | Required | Default | Description             |
| --------- | ----- | -------- | ------- | ----------------------- |
| `user`    | `str` | `False`  | `root`  | User to run acme.sh as. |

## Examples

### Install acme.sh for user acme

```bash
salt '*' acme_sh.install user=acme
```

### Upgrade acme.sh installation

```bash
salt '*' acme_sh.install user=acme upgrade=True
```

### Issue certificate with webroot

```bash
salt '*' acme_sh.issue example.com acme_mode=webroot webroot=/var/www
```

### Issue certificate with Hetzner dns

```bash
salt '*' acme_sh.issue example.com acme_mode=dns dns_plugin=dns_hetzner dns_credentials='{"HETZNER_Token": "tokenxxxxx"}'
```

### Issue certificate with standalone and aliases

```bash
salt '*' acme_sh.issue example.com acme_mode=standalone aliases=www.example.com,example.org
```

### Renew certificate

```bash
salt '*' acme_sh.renew example.com
```
