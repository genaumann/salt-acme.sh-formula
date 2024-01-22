# Salt acme.sh Formula

![GitHub release](https://img.shields.io/github/v/release/genaumann/salt-acme.sh-formula)
![lint][lint_badge]
![test][test_badge]

Interacts with [acme.sh](https://acme.sh):

- install acme.sh
- issue certificates
- renew certificates

The following modes are supported:

- standalone
- webroot
- dns

## General notes

See the full [SaltStack Formulas installation and usage instructions][install].

See [`example.yml`](example.yml) on how to configure the formula.

If you want to use this formula, please pay attention to the [`FORMULA`](FORMULA) file and/or `git tag`,
which contains the currently released version.
This formula is versioned according to [Semantic Versioning](http://semver.org/).

## Available states

- [`acme.sh`](acme.sh/init.sls)
- [`acme.sh.install`](acme.sh/install.sls)
- [`acme.sh.issue`](acme.sh/issue.sls)

### `acme.sh`

Includes the following states:

- `acme.sh.install`
- `acme.sh.issue`

### `acme.sh.install`

Installs `acme.sh`.

### `acme.sh.issue`

Issues or renews certificate with `acme.sh`.

## Available execution modules

- [`acme.sh`](docs/module_acme_sh.md)

## Available state modules

- [`acme.sh`](docs/state_acme_sh.md)

## Testing

Linux testing is done with `kitchen-salt`.

All tests and lint jobs are executed in GitHub Actions.

### Requirements

You can test the formula locally after installing the following requirements.

- vagrant
- VirtualBox
- Ruby
- bundler

### Run Test

```bash
bundle install
kitchen list # list all available test instances
kitchen test <instance>
```

## OS support matrix

This formula has been tested under the following operating systems and salt versions.

| OS           | 3006.0 | 3006.5       |
| ------------ | ------ | ------------ |
| Debian 12    | :x:    | ✅           |
| Ubuntu 22.04 | :x:    | ✅           |
| Rocky 9      | :x:    | ✅           |
| Fedora 38    | :x:    | ✅           |
| OpenSUSE 15  | ✅     | Not released |

[install]: https://docs.saltproject.io/en/latest/topics/development/conventions/formulas.html
[lint_badge]: https://github.com/genaumann/salt-acme.sh-formula/actions/workflows/lint.yml/badge.svg?branch=main
[test_badge]: https://github.com/genaumann/salt-acme.sh-formula/actions/workflows/salt-kitchen.yml/badge.svg?branch=main
