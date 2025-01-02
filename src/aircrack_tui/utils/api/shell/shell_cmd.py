# -------------- #
# System imports #

import asyncio


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


    async def get_all_sys_ifaces_names(self) -> tuple[bool, list[str]|str]:
        """
        Returns a list of system interfaces like:
        ['wlan0', 'wlan1', ...]
        return values are: tuple[success:bool, interfaces:list[str]]
        """

        cmd = f"sudo iwconfig"
        success, response = await self.cmd_query_finite(cmd)
        if not success:
            return False, response
        elif len(response) == 0:
            return False, []

        # Split the data (response) into lines and extract interface names
        interfaces = [line.split()[0] for line in response.strip().split('\n') if line and not line.startswith(' ')]
        
        return True, interfaces
