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

- [`acme_sh`](acme_sh/init.sls)
- [`acme_sh.install`](acme_sh/install.sls)
- [`acme_sh.issue`](acme_sh/issue.sls)

### `acme_sh`

Includes the following states:

- `acme_sh.install`
- `acme_sh.issue`

### `acme_sh.install`

Installs `acme.sh`.

### `acme_sh.issue`

Issues or renews certificate with `acme.sh`.

## Available execution modules

- [`acme_sh`](docs/module_acme_sh.md)

## Available state modules

- [`acmesh`](docs/state_acme_sh.md)

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

[install]: https://docs.saltproject.io/en/latest/topics/development/conventions/formulas.html
[lint_badge]: https://github.com/genaumann/salt-acme.sh-formula/actions/workflows/lint.yml/badge.svg?branch=main
[test_badge]: https://github.com/genaumann/salt-acme.sh-formula/actions/workflows/salt-kitchen.yml/badge.svg?branch=main
