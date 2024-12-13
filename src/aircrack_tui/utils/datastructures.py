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