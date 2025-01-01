# -------------- #
# System inports #

from collections    import namedtuple
from dataclasses    import dataclass, field
from enum           import Enum
from os             import getcwd, path as os_path
from pathlib        import Path


# ------------------- #
# Third-party imports #

# import toml
from textual.reactive                   import reactive


# ------------- #
# Local imports #

from aircrack_tui.utils.api             import (
        ShellCMD,
        )

from aircrack_tui.utils.simple_tasks    import (
        get_system,
        )

# from aircrack_tui.utils.api.models      import (
#         InterfaceFull,
#         )



#############
# CONSTANTS #
#############

LOG_PATH  = Path(
        # Equals to "../logs/"
        Path(os_path.abspath(__file__)).parent.parent,
        "logs"
        )
CONF_PATH  = Path(
        # Equals to "./config.toml"
        Path(os_path.abspath(__file__)).parent,
        "config.toml"
        )
STYLES_PATH  = Path(
        # Equals to "./styles/"
        Path(os_path.abspath(__file__)).parent,
        "styles"
        )

IS_ANDROID:bool = get_system()


DEPENDENCIES:list[str] = [
        "aircrack-ng",
        "crunch",
        "iwlist",
        ]

shell_cmd = ShellCMD()

# Interface, selected to conduct vulnurability testing

# InterfaceFull.iface_name = None
        # iface_mac=None,
        # iface_standart=None,
        # iface_mode=None,
        # iface_channel=None,


########
# MAIN #
########

# # Read the config.toml file
# with open(CONF_PATH, "r") as file:
#     config = toml.load(file)
#     # Access .toml variables
#     # config["web"]["mock"]

# # Write data to a TOML file
# def config_write() -> None:
#     with open(CONF_PATH, "w") as file:
#         toml.dump(config, file)
