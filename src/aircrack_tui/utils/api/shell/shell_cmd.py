# -------------- #
# System imports #

import asyncio
import re


# ------------------- #
# Third patry imports #


# ------------- #
# Local imports #

from .base  import ShellCMDBase



class ShellCMD(ShellCMDBase):
    """
    Intended to call system shell commands (cmds) in async and return
    responces if needed (pipe also works).
    """


    def __init__(self) -> None:
        ...


    async def util_presence_check(self, util_name:str) -> bool:
        """
        Return True if util_name present in the system,
        False otherwise.
        """
        
        cmd = f"command -v {util_name}"
        success, response = await self.cmd_query_finite(cmd)
        if not success:
            return False
        elif len(response) == 0:
            return False
        return True


    async def get_all_sys_ifaces_names(self) -> tuple[bool, list[str]]:
        """
        Returns a list of system interfaces like:
        ['wlan0', 'wlan1', ...]
        return values are: tuple[success:bool, interfaces:list[str]]
        """

        cmd = f"sudo iwconfig"
        success, response = await self.cmd_query_finite(cmd)
        if not success:
            return False, []
        elif len(response) == 0:
            return False, []

        # Split the data (response) into lines and extract interface names
        interfaces = [line.split()[0] for line in response.strip().split('\n') if line and not line.startswith(' ')]
        
        return True, interfaces


    async def get_iface_mac(self, iface_name:str) -> str|None:
        """
        Return iface MAC.
        """

        cmd = f"sudo iw dev {iface_name} info | grep addr"
        success, response = await self.cmd_query_finite(cmd)
        # If success - got response something like:
        # "    addr fa:be:12:34:56:78"
        if not success:
            return None
        elif len(response) == 0:
            return None

        mac = response.split("addr")[-1].strip()
        return mac


    async def get_iface_channel(self, iface_name:str) -> str|None:
        """
        Return iface channel.
        """

        cmd = f"sudo iwlist {iface_name} channel | grep Current"
        success, response = await self.cmd_query_finite(cmd)
        # If success - got response something like:
        # "    Current Frequency=2.442 GHz (Channel 7)"
        if not success:
            return None
        elif len(response) == 0:
            return None

        # Regular expression to extract a channel number
        match = re.search(r"\(Channel (\d+)\)", response)
        if match:
            channel_number = match.group(1)
            return channel_number
        else:
            return None


    async def get_iface_mode(self, iface_name:str) -> str|None:
        """
        Return iface mode.
        """

        cmd = f"sudo iwconfig {iface_name} | grep Mode"
        success, response = await self.cmd_query_finite(cmd)
        # If success - got response something like:
        # "    type managed"
        if not success:
            return None
        elif len(response) == 0:
            return None

        try:
            mode = response.split("Mode:")[1].split(" ")[0]
        except Exception as e:
            mode = None
        return mode
