"""
acme.sh state module

This module interacts with acme_sh salt module
"""

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
