"""
acme.sh module

This module interacts with acme.sh https://github.com/acmesh-official/acme.sh
"""

import logging

import salt.utils.path
from salt.exceptions import CommandExecutionError, SaltInvocationError, CommandNotFoundError


log = logging.getLogger(__name__)

def _get_acme_bin(
    script_path,
    home_dir
):

  acme_bin = script_path if script_path else f"{home_dir}/.acme.sh/acme.sh"
  if not salt.utils.path.which_bin([acme_bin]):
    raise CommandNotFoundError("acme.sh script is not available. Specify the absolute script path in `script_path`")

  return acme_bin

def install(
    email,
    user='root',
    system=False,
    home=None,
):
  """
  Install acme.sh

  email
    used to register an account to acme server, you will receive a renewal notice email here

  user
    user to install
    default = root

  system
    system installation to /opt/acme.sh
    default = False

  home
    customized dir to install acme.sh in.
    When system is False, default: it installs into ~/.acme.sh
  """

  # check input
  if user != 'root' and system:
    raise SaltInvocationError("Specify either user or sytem")

  # clone https://github.com/acmesh-official/acme.sh

  clone_name = f"acme.sh-{'global' if system else user}"
  clone = __salt__["git.clone"]("/tmp", url="https://github.com/acmesh-official/acme.sh", name=clone_name)

  if not clone:
    CommandExecutionError("Failed to clone the acme.sh repository")

  cmd = ["./acme.sh", "--install", "--accountemail", email, "--nocron"]

  # if system
  if system:
    cmd.append("--home /opt/acme.sh")
  
  # if user config
  if user and home:
    cmd.append(f"--home {home}")

  install = __salt__["cmd.run_all"](" ".join(cmd), cwd=f"/tmp/{clone_name}", runas=user)
  __salt__["file.remove"](f"/tmp/{clone_name}")
  
  # check install process successfully
  if install["retcode"] == 0:
    log.debug("acme.sh successfully installed")
  else:
    return (False, "Installation failed, see logfiles for more information")

  if user and not system and not home:
    install_dir = __salt__["user.info"](user)["home"]
  elif user and home:
    install_dir = home
  else:
    install_dir = "/opt/acme.sh"
  
  return(f"acme.sh successfully installed in {install_dir}")


def cert(
    name,
    acme_mode,
    aliases=None,
    server='letsencrypt',
    keysize='4096',
    dns_plugin=None,
    webroot=None,
    http_port=None,
    run_as="root",
    script_path=None,
    cert_path=None,
    dns_credentials=None,
    force=False
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

  run_as
    run the command as a specified user, default: root

  script_path
    absolute path to acme.sh script
    default = ~/.acme.sh/acme.sh

  cert_path
    installation dir of certs
    default = ~/.acme.sh

  dns_credentials
    dns crededentials as python dict
    see https://github.com/acmesh-official/acme.sh/wiki/dnsapi

  force
    force issuing a certificate
    default = False
  """

  home_dir = __salt__['user.info'](run_as)['home']

  if acme_mode == "standalone" or acme_mode == "standalone-tls-alpn":
    # check socat is installed, when standalone
    if not salt.utils.path.which_bin(["socat"]):
      __context__["retcode"] = 1
      return "Install socat to use standalone mode first"

  acme_bin = _get_acme_bin(script_path, home_dir)

  # check keysize
  possible_keylength = ["ec-256", "ec-384", "ec-521", "2048", "3072", "4096"]
  if not keysize in possible_keylength:
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

  if acme_mode =="dns" and not isinstance(dns_credentials, dict):
    raise SaltInvocationError("Specify `dns_credentials` as dict")

  # build cmd
  cmd = [acme_bin, "--issue", "-d", name, "--server", server, "--keylength", str(keysize)]

  # if aliases are specified
  if aliases:
    alias_cmd = []
    for domain in aliases.split(","):
      alias_cmd.extend(["-d", domain])
    cmd.extend(alias_cmd)

  # if cert_path specified
  if cert_path:
    cmd.extend(["--home", cert_path])
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

  if acme_mode == "dns":
    log.debug("Set dns_credentials as temporary env")
    __salt__["environ.setenv"](dns_credentials)

  issue = __salt__["cmd.run_all"](" ".join(cmd), python_shell=False, run_as=run_as)

  if issue["retcode"] == 0:
    ret = {
      "certificate": f"{cert_path}/{name}/{name}.cer",
      "private_key": f"{cert_path}/{name}/{name}.key"
    }
  else:
    if issue["stdout"].find("Next renewal time is") != -1:
      ret = f"Certificate in {cert_path}/{name} is valid, re run with `force=True`"
    else:
      ret = issue

  return ret
