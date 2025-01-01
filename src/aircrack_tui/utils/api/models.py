# -------------- #
# System imports #

from dataclasses import dataclass


# ------------------- #
# Third party imports #


# ------------- #
# Local imports #




##########
#  MAIN  #
##########

@dataclass
class InterfaceParams:
    """Represents interface details."""
    iface_name: str | None = None
    iface_mac: str | None = None
    iface_standart: str | None = None
    iface_mode: str | None = None
    iface_channel: str | None = None

interface_params_main = InterfaceParams()
