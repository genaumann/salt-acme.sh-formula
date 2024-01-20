"""
acme.sh state module

This module interacts with acme_sh salt module
"""

import time
import logging
import salt.exceptions

log = logging.getLogger(__name__)

if "__context__" not in globals():
    __context__ = {}

if "__opts__" not in globals():
    __opts__ = {}

if "__salt__" not in globals():
    __salt__ = {}


def __virtual__():
    """
    Only load if the acme_sh module is available in __salt__
    """
    if "acme_sh.issue" in __salt__:
        return "acme_sh"
    return False, "acme_sh module could not be loaded"


def installed(
    name,
    email,
    user="root",
    upgrade=False,
    force=False,
):
    """
    Ensure that acme.sh is installed

    email
      Email address to use for acme registration

    user
      User to install acme.sh for

    upgrade
      Upgrade acme.sh if already installed

    force
      Force reinstallation of acme.sh
    """

    ret = {
        "name": name,
        "changes": {},
        "result": True,
        "comment": "",
    }

    home_dir = __salt__["user.info"](user)["home"]

    # if acme.sh is not installed or force is enabled
    if not __salt__["file.file_exists"](home_dir + "/.acme.sh/acme.sh"):
        # if test mode is enabled
        if __opts__["test"]:
            ret["result"] = None
            ret["comment"] = "acme.sh would be installed"
            return ret

        # Install acme.sh
        if __salt__["acme_sh.install"](email, user=user):
            ret["changes"]["acme_sh"] = "Installed"
            ret["comment"] = "acme.sh has been installed"
        # if failed to install acme.sh
        else:
            ret["result"] = False
            ret["comment"] = "Failed to install acme.sh"
        return ret
    # if acme.sh is installed and force is enabled
    elif force:
        # if test mode is enabled
        if __opts__["test"]:
            ret["result"] = None
            ret["comment"] = "acme.sh would be reinstalled"
            return ret

        # Reinstall acme.sh
        if __salt__["acme_sh.install"](email, user=user, force=force):
            ret["changes"]["acme_sh"] = "Reinstalled"
            ret["comment"] = "acme.sh has been reinstalled"
        # if failed to reinstall acme.sh
        else:
            ret["result"] = False
            ret["comment"] = "Failed to reinstall acme.sh"
        return ret
    # if upgrade is enabled
    elif upgrade:
        # if test mode is enabled
        if __opts__["test"]:
            ret["result"] = None
            ret["comment"] = "acme.sh would be upgraded"
            return ret

        upgrade_cmd = __salt__["acme_sh.install"](email, user=user, upgrade=upgrade)
        if isinstance(upgrade_cmd, str):
            ret["comment"] = "Up-to-date"
        elif isinstance(upgrade_cmd, dict):
            ret["changes"]["acme_sh"] = upgrade_cmd
            ret["comment"] = "acme.sh has been upgraded"
    else:
        # if acme.sh is already installed
        ret["comment"] = "acme.sh is already installed"

    return ret


def cert(
    name,
    acme_mode,
    aliases=None,
    server=None,
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
):
    """
    Ensure that a certificate is issued

    name
      Domain name to issue certificate for

    acme_mode
      ACME mode to use for certificate issuance (webroot, standalone, standalone-tls-alpn, dns)

    aliases
      List of aliases to issue certificate for

    server
      ACME server to use for certificate issuance

    keysize
      Key size to use for certificate issuance
      default = 4096
      possible values:
        ec-256 (prime256v1, "ECDSA P-256", which is the default key type)
        ec-384 (secp384r1, "ECDSA P-384")
        ec-521 (secp521r1, "ECDSA P-521", which is not supported by Let's Encrypt yet.)
        2048 (RSA2048)
        3072 (RSA3072)
        4096 (RSA4096)

    dns_plugin
      DNS plugin to use for certificate issuance
      see https://github.com/acmesh-official/acme.sh/wiki/dnsapi

    webroot
      Webroot to use for certificate issuance
      Full path needed, user needs write access to this directory

    http_port
      Port to use for certificate issuance
      default = 80

    user
      User to issue certificate for

    cert_path
      Path to store certificate at
      default = ~/.acme.sh

    dns_credentials
      Dictionary of credentials to use for DNS plugin
      Every value needs to be a string
      see https://github.com/acmesh-official/acme.sh/wiki/dnsapi

    force
      Force reissue of certificate

    valid_to
      NotAfter field in cert
      see https://github.com/acmesh-official/acme.sh/wiki/Validity

    valid_from
      NotBefore field in cert
      see https://github.com/acmesh-official/acme.sh/wiki/Validity
    """

    ret = {
        "name": name,
        "changes": {},
        "result": True,
        "comment": "",
    }

    # error checking

    # aliases can be a string ?
    if aliases and aliases != "None" and not isinstance(aliases, list):
        raise salt.exceptions.SaltInvocationError("aliases must be a list")

    if dns_credentials and not isinstance(dns_credentials, dict):
        raise salt.exceptions.SaltInvocationError(
            "dns_credentials must be a dictionary"
        )

    if valid_to and not isinstance(valid_to, str):
        raise salt.exceptions.SaltInvocationError("valid_to must be a string")

    if valid_from and not isinstance(valid_from, str):
        raise salt.exceptions.SaltInvocationError("valid_from must be a string")

    if acme_mode == "dns" and not dns_plugin:
        raise salt.exceptions.SaltInvocationError(
            "dns_plugin must be specified when acme_mode is dns"
        )

    if acme_mode == "dns" and not dns_credentials:
        raise salt.exceptions.SaltInvocationError(
            "dns_credentials must be specified when acme_mode is dns"
        )

    if acme_mode == "webroot" and not webroot:
        raise salt.exceptions.SaltInvocationError(
            "webroot must be specified when acme_mode is webroot"
        )

    # check cert is available and set for renewal

    crt_info = __salt__["acme_sh.info"](name, user=user, cert_path=cert_path)

    if (
        __context__["acme_sh.info"]["code"] == 1
        or "Le_NextRenewTime" not in crt_info
        or force
    ):
        log.debug("Certificate is not available or force is enabled")
        # if test mode is enabled
        if __opts__["test"]:
            ret["result"] = None
            ret["comment"] = "Certificate would be issued"
            return ret

        # issue certificate
        issue = __salt__["acme_sh.issue"](
            name,
            acme_mode,
            aliases=",".join(aliases) if aliases else None,
            server=server,
            keysize=str(keysize),
            dns_plugin=dns_plugin,
            webroot=webroot,
            http_port=str(http_port),
            user=user,
            cert_path=cert_path,
            dns_credentials=dns_credentials,
            force=force,
            valid_to=valid_to,
            valid_from=valid_from,
        )

        if __context__["retcode"] == 0:
            ret["changes"][name] = issue
            ret["comment"] = "Certificate has been issued"
            # if failed to issue certificate
        else:
            ret["result"] = False
            ret["comment"] = issue["stderr"]

    # if certificate is available and set for renewal
    elif int(time.time()) > int(crt_info["Le_NextRenewTime"]):
        log.debug("Certificate is available and set for renewal")
        # if test mode is enabled
        if __opts__["test"]:
            ret["result"] = None
            ret["comment"] = "Certificate would be renewed"
            return ret

        # renew certificate
        renew = __salt__["acme_sh.renew"](
            name,
            user=user,
            cert_path=cert_path,
            force=force,
        )

        if __context__["retcode"] == 0:
            ret["changes"][name] = renew
            ret["comment"] = "Certificate has been renewed"
        # if failed to renew certificate
        else:
            ret["result"] = False
            ret["comment"] = renew["stderr"]
    else:
        ret["comment"] = "Certificate is already up-to-date"

    return ret
