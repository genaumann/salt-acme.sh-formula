"""
acme.sh module

This module interacts with acme.sh https://github.com/acmesh-official/acme.sh
"""

import logging

from salt.exceptions import CommandExecutionError, SaltInvocationError


log = logging.getLogger(__name__)

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
