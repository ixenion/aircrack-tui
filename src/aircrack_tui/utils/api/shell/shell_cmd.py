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
        success, responce = await self.cmd_query_finite(cmd)
        if not success:
            return False
        elif len(responce) == 0:
            return False
        return True
