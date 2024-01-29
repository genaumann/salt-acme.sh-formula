# State Module acme_sh

You can use this state module to issue or renew certificates with `acme.sh`.

## Available state functions

- [acme_sh.installed](#acme_shinstalled)
- [acme_sh.cert](#acme_shcert)

### acme_sh.installed

Installs `acme.sh`.

| Parameter | Type   | Required | Default | Description                            |
| --------- | ------ | -------- | ------- | -------------------------------------- |
| `email`   | `str`  | `True`   |         | Email address to use for registration. |
| `user`    | `str`  | `False`  | `root`  | User to run acme.sh as.                |
| `upgrade` | `bool` | `False`  | `False` | Upgrade acme.sh.                       |
| `force`   | `bool` | `False`  | `False` | Force install acme.sh.                 |

### acme_sh.cert

Ensures that a certificate is issued and valid with `acme.sh`.

| Parameter         | Type   | Required                                | Default          | Description                                                                     |
| ----------------- | ------ | --------------------------------------- | ---------------- | ------------------------------------------------------------------------------- |
| `name`            | `str`  | `True`                                  |                  | Domain to issue certificate for.                                                |
| `acme_mode`       | `str`  | `True`                                  |                  | Mode to issue certificate with. (webroot, standalone, standalone-tls-alpn, dns) |
| `aliases`         | `list` | `False`                                 | `None`           | List of aliases to issue certificate for.                                       |
| `server`          | `str`  | `False`                                 | `letsencrypt`    | ACME server to use.                                                             |
| `keysize`         | `str`  | `False`                                 | `4096`           | Key size to use.                                                                |
| `dns_plugin`      | `str`  | `False`, `True` if acme_mode is dns     | `None`           | DNS plugin to use.                                                              |
| `dns_credentials` | `dict` | `False`, `True` if acme_mode is dns     | `None`           | DNS plugin credentials to use.                                                  |
| `webroot`         | `str`  | `False`, `True` if acme_mode is webroot | `None`           | Webroot path to use.                                                            |
| `http_port`       | `str`  | `False`                                 | `80`             | HTTP port to use.                                                               |
| `user`            | `str`  | `False`                                 | `root`           | User to run acme.sh as.                                                         |
| `cert_path`       | `str`  | `False`                                 | `$HOME/.acme.sh` | Path to store certificates in.                                                  |
| `force`           | `bool` | `False`                                 | `False`          | Force issue certificate.                                                        |
| `valid_to`        | `str`  | `False`                                 | `None`           | Validity of certificate.                                                        |
| `valid_from`      | `str`  | `False`                                 | `None`           | Validity of certificate.                                                        |
| `insecure`        | `bool` | `False`                                 | `False`          | Don't verify SSL-Cert of acme server                                            |

**DNS Credentials**

Credentials are defined as a dictionary.
You are able to define the credentials by creating environment variables.
The environment variables must be prefixed with `ACMESH_` and have the following format:

`ACMESH_{user}_{domain}_{key}`: `ACMESH_root_exampleCom_HETZNER_Token`

Please note the camel case of the domain:

`example.com` -> `exampleCom`  
`example.co.uk` -> `exampleCoUk`

A dash `-` in the domain is currently not supported.

**Further information**

[See execution module documentation](./module_acme_sh.md#acme_shissue)

## Examples

You can use the predefined salt states in combination with the pillar structure from [`example.yml`](../example.yml).
