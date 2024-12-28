# -------------- #
# System imports #

import asyncio


# ------------------- #
# Third patry imports #


# ------------- #
# Local imports #



class ShellCMD:
    """
    Intended to call system shell commands (cmds) in async and return
    responces if needed (pipe also works).
    """


    def __init__(self) -> None:
        ...


    async def cmd_query(self, cmd:str) -> tuple[bool,str]:
        """
        Executes cmd and returns tuple(success:bool, responce:str).
        If success = false, responce would be error message.
        """

        proc = await asyncio.create_subprocess_shell(
                cmd,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                )
        stdout, stderr = [ val.decode("utf-8") for val in await proc.communicate() ]
    
        if not stderr:
            return True, stdout
        else:
            return False, stderr


    async def util_presence_check(self, util_name:str) -> bool:
        """
        Return True if util_name present in the system,
        False otherwise.
        """
        
        cmd = f"command -v {util_name}"
        success, responce = await self.cmd_query(cmd)
        if not success:
            return False
        elif len(responce) == 0:
            return False
        return True
