"""
acme.sh module

This module interacts with acme.sh https://github.com/acmesh-official/acme.sh
"""

import os
import logging
import re

import salt.utils.path
from salt.exceptions import (
    CommandExecutionError,
    SaltInvocationError,
    CommandNotFoundError,
)

log = logging.getLogger(__name__)

if "__context__" not in globals():
    __context__ = {}

if "__opts__" not in globals():
    __opts__ = {}

if "__salt__" not in globals():
    __salt__ = {}


def _get_acme_bin(home_dir):
    script_path = f"{home_dir}/.acme.sh/acme.sh"

    if not salt.utils.path.which_bin([script_path]):
        raise CommandNotFoundError(
            f"{script_path} is not available, please install with `acme_sh.install my@example.com`"
        )

    return script_path


def _upgrade(home_dir, user):
    acme_bin = _get_acme_bin(home_dir)
    old_version = version(user)

    cmd = [acme_bin, "--upgrade"]

    upgrade = __salt__["cmd.run_all"](" ".join(cmd), python_shell=False, runas=user)

    if upgrade["retcode"] == 0:
        new_version = version(user)

        if old_version == new_version:
            ret = "Already up-to-date"
        else:
            ret = {"old": old_version, "new": new_version}

    else:
        ret = upgrade

    return ret


def _generate_crt_ret(name, cert_path):
    return {
        "certificate": f"{cert_path}/{name}/{name}.cer",
        "private_key": f"{cert_path}/{name}/{name}.key",
        "fullchain": f"{cert_path}/{name}/fullchain.cer",
        "ca": f"{cert_path}/{name}/ca.cer",
    }


def install(email, user="root", upgrade=False, force=False):
    """
    Install acme.sh

    email
      used to register an account to acme server, you will receive a renewal notice email here

    user
      user to install
      default: root

    upgrade
      upgrade acme.sh
      default: False

    force
      force installation
      default: False
    """

    home_dir = __salt__["user.info"](user)["home"]
    script_path = f"{home_dir}/.acme.sh/acme.sh"

    # if already installed
    if __salt__["file.file_exists"](script_path):
        if upgrade:
            return _upgrade(home_dir, user)

        if not force:
            return "Already installed, re-run with force=True to force installation"

    # clone https://github.com/acmesh-official/acme.sh
    clone_name = f"acme.sh-{user}"
    __salt__["git.clone"](
        "/tmp", url="https://github.com/acmesh-official/acme.sh", name=clone_name
    )

    if __context__["retcode"] == 1:
        raise CommandExecutionError("Failed to clone the acme.sh repository")

    cmd = ["./acme.sh", "--install", "--accountemail", email, "--nocron"]

    install_cmd = __salt__["cmd.run_all"](
        " ".join(cmd), cwd=f"/tmp/{clone_name}", runas=user
    )
    __salt__["file.remove"](f"/tmp/{clone_name}")

    # check install process successfully
    if install_cmd["retcode"] == 0:
        log.debug("acme.sh successfully installed")
    else:
        __context__["retcode"] = 1
        return "Installation failed, see logfiles for more information"

    return f"acme.sh successfully installed in {os.path.dirname(script_path)}"


def register(email, user="root"):
    """
    Register account @ zeroSSL CA
    This step is required if you are using zeroSSL CA

    email
      email to register

    user
      run the command as a specified user
      default: root
    """

    home_dir = __salt__["user.info"](user)["home"]

    acme_bin = _get_acme_bin(home_dir)

    cmd = [acme_bin, "--register-account", "-m", email]

    register_cmd = __salt__["cmd.run_all"](
        " ".join(cmd), python_shell=False, runas=user
    )

    if register_cmd["retcode"] == 0:
        match = re.search(r"ACCOUNT_THUMBPRINT='([^']+)'", register_cmd["stdout"])
        if match:
            ret = {"account_thumbprint": match.group(1)}
        else:
            __context__["retcode"] = 1
            ret = "Account registration failed"

    return ret


def issue(
    name,
    acme_mode,
    aliases=None,
    server="letsencrypt",
    keysize="4096",
    dns_plugin=None,
    webroot=None,
    http_port=None,
    user="root",
    cert_path=None,
    dns_credentials=None,
    force=False,
    valid_to=None,
    valid_from=None,
    insecure=False,
):
    """
    Obtain a certificate

    name
      Common name of the certificate

    acme_mode
      choose one acme mode (webroot, standalone, standalone-tls-alpn, dns)

    aliases
      comma seperated, subjectAltNames

    server
      acme server
      default = letsencrypt

    keysize
      RSA key bits
      default = 4096
      possible values:
        ec-256 (prime256v1, "ECDSA P-256", which is the default key type)
        ec-384 (secp384r1, "ECDSA P-384")
        ec-521 (secp521r1, "ECDSA P-521", which is not supported by Let's Encrypt yet.)
        2048 (RSA2048)
        3072 (RSA3072)
        4096 (RSA4096)

    dns_plugin
      dns plugin to use
      see https://github.com/acmesh-official/acme.sh/wiki/dnsapi

    webroot
      if acme_mode == webroot, full path to webroot

    http_port
      the port the server listen on during standalone or standalone-tls-alpn

    user
      run the command as a specified user
      default: root

    cert_path
      installation dir of certs
      default = ~/.acme.sh

    dns_credentials
      dns crededentials as python dict
      see https://github.com/acmesh-official/acme.sh/wiki/dnsapi

    force
      force issuing a certificate
      default = False

    valid_to
      NotAfter field in cert
      see https://github.com/acmesh-official/acme.sh/wiki/Validity

    valid_from
      NotBefore field in cert
      see https://github.com/acmesh-official/acme.sh/wiki/Validity

    insecure
      disable ssl verification
      default: False
    """

    home_dir = __salt__["user.info"](user)["home"]

    if acme_mode == "standalone" or acme_mode == "standalone-tls-alpn":
        # check socat is installed, when standalone
        if not salt.utils.path.which_bin(["socat"]):
            __context__["retcode"] = 1
            return "Install socat to use standalone mode first"

    acme_bin = _get_acme_bin(home_dir)

    # check keysize
    possible_keylength = ["ec-256", "ec-384", "ec-521", "2048", "3072", "4096"]
    if keysize not in possible_keylength:
        raise SaltInvocationError(f"Keysize {keysize} not supported")

    # check mode
    possible_mode = ["standalone", "standalone-tls-alpn", "dns", "webroot"]
    if not acme_mode in possible_mode:
        raise SaltInvocationError(f"Acme mode {acme_mode} not supported")

    # error when mode == webroot and webroot unset
    if acme_mode == "webroot" and not webroot:
        raise SaltInvocationError("Specify `webroot` path")

    # error when mode == dns and dns_plugin unset
    if acme_mode == "dns" and not dns_plugin:
        raise SaltInvocationError("Specify `dns_plugin`")

    # error when dns mode an no credentials specified

    if acme_mode == "dns" and not isinstance(dns_credentials, dict):
        raise SaltInvocationError("Specify `dns_credentials` as dict")

    # build cmd
    cmd = [
        acme_bin,
        "--issue",
        "-d",
        name,
        "--server",
        server,
        "--keylength",
        str(keysize),
    ]

    # if aliases are specified
    if aliases:
        alias_cmd = []
        for domain in aliases.split(","):
            alias_cmd.extend(["-d", domain])
        cmd.extend(alias_cmd)

    # if cert_path specified
    if cert_path:
        cmd.extend(["--cert-home", cert_path])
    else:
        cert_path = f"{home_dir}/.acme.sh"

    # modes
    if acme_mode == "webroot":
        cmd.extend(["-w", webroot])
    elif acme_mode == "standalone":
        cmd.append("--standalone")
        if http_port:
            cmd.extend(["--httpport", str(http_port)])
    elif acme_mode == "standalone-tls-alpn":
        cmd.append("--alpn")
        if http_port:
            cmd.extend(["--tlsport", http_port])
    elif acme_mode == "dns":
        cmd.extend(["--dns", dns_plugin])

    # force
    if force:
        cmd.append("--force")

    # validity
    if valid_to:
        cmd.extend(["--valid-to", valid_to])
    if valid_from:
        cmd.extend(["--valid-from", valid_from])

    # insecure
    if insecure:
        cmd.append("--insecure")

    if acme_mode == "dns":
        log.debug("Set dns_credentials as temporary env")
        __salt__["environ.setenv"](dns_credentials)

    issue_cmd = __salt__["cmd.run_all"](" ".join(cmd), python_shell=False, runas=user)

    if issue_cmd["retcode"] == 0:
        ret = _generate_crt_ret(name, cert_path)
    else:
        if issue_cmd["stdout"].find("Next renewal time is") != -1:
            ret = (
                f"Certificate in {cert_path}/{name} is valid, re run with `force=True`"
            )
        elif (
            issue_cmd["stdout"].find("acme.sh --register-account -m my@example.com")
            != -1
        ):
            ret = "Please register your account: acme_sh.register my@example.com"
        else:
            ret = issue_cmd

    return ret


def list_crt(user="root", cert_path=None):
    """
    List all certificates in given cert_path

    user
      run the command as a specified user
      default: root

    cert_path
      installation dir of certs
      default = ~/.acme.sh
    """

    home_dir = __salt__["user.info"](user)["home"]

    acme_bin = _get_acme_bin(home_dir)

    cmd = [acme_bin, "--list"]

    if cert_path:
        cmd.extend(["--cert-home", cert_path])

    list_crt_cmd = __salt__["cmd.run_all"](
        " ".join(cmd), python_shell=False, runas=user
    )

    if list_crt_cmd["retcode"] == 0:
        # map output
        lines = list_crt_cmd["stdout"].strip().split("\n")
        keys = lines[0].split()
        ret = []
        for line in lines[1:]:
            values = line.split()
            entry = dict(zip(keys, values))
            ret.append(entry)
    else:
        ret = list_crt_cmd

    return ret


def info(name, user="root", cert_path=None):
    """
    Get info about a certificate

    name
      Common name of the certificate (main_domain)

    user
      run the command as a specified user
      default: root

    cert_path
      installation dir of certs
      default: ~/.acme.sh
    """

    if "acme_sh.info" not in __context__:
        __context__["acme_sh.info"] = {"code": 0}

    home_dir = __salt__["user.info"](user)["home"]

    acme_bin = _get_acme_bin(home_dir)

    cmd = [acme_bin, "--info", "--domain", name]

    if cert_path:
        cmd.extend(["--cert-home", cert_path])
    else:
        cert_path = f"{home_dir}/.acme.sh"

    # check if cert_path exists
    if not __salt__["file.directory_exists"](cert_path):
        __context__["acme_sh.info"]["code"] = 1
        __context__["retcode"] = 1
        return f"Certificate path {cert_path} does not exist"
    # check if cert exists
    if not __salt__["file.directory_exists"](f"{cert_path}/{name}"):
        __context__["acme_sh.info"]["code"] = 1
        __context__["retcode"] = 1
        return f"Certificate {name} does not exist"

    info_cmd = __salt__["cmd.run_all"](" ".join(cmd), python_shell=False, runas=user)

    if info_cmd["retcode"] == 0:
        # map output to dict
        info_dict = {}
        lines = info_cmd["stdout"].strip().split("\n")
        for line in lines:
            key, value = line.split("=")
            info_dict[key] = value

        ret = info_dict
    else:
        ret = info_cmd

    return ret


def renew(name, user="root", cert_path=None, force=False, insecure=False):
    """
    Renew a certificate

    name
      Common name of the certificate (main_domain)

    user
      run the command as a specified user
      default: root

    cert_path
      installation dir of certs
      default: ~/.acme.sh

    force
      force renewing a certificate
      default: False

    insecure
      disable ssl verification
      default: False
    """

    home_dir = __salt__["user.info"](user)["home"]

    acme_bin = _get_acme_bin(home_dir)

    cmd = [acme_bin, "--renew", "--domain", name]

    if cert_path:
        cmd.extend(["--cert-home", cert_path])
    else:
        cert_path = f"{home_dir}/.acme.sh"

    if force:
        cmd.append("--force")

    if insecure:
        cmd.append("--insecure")

    renew_cmd = __salt__["cmd.run_all"](" ".join(cmd), python_shell=False, runas=user)

    if renew_cmd["retcode"] == 0:
        ret = _generate_crt_ret(name, cert_path)
    else:
        next_renew = re.search(r"Next renewal time is: (.*)", renew_cmd["stdout"])
        if next_renew:
            ret = f"Next renewal time is {next_renew.group(1)}, add force=True to renew"
        elif renew_cmd["stdout"].find("is not an issued domain, skip") != -1:
            ret = f"Domain {name} is not an issued domain"
        else:
            ret = renew_cmd

    return ret


def version(user="root"):
    """
    Get version of acme.sh

    user
      run the command as a specified user
      default: root
    """

    home_dir = __salt__["user.info"](user)["home"]

    acme_bin = _get_acme_bin(home_dir)

    cmd = [acme_bin, "--version"]

    version_cmd = __salt__["cmd.run_all"](" ".join(cmd), python_shell=False, runas=user)

    if version_cmd["retcode"] == 0:
        ret = re.search(r"v(.*)", version_cmd["stdout"]).group(1)
    else:
        ret = version_cmd

    return ret
