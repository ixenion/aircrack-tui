# -------------- #
# System imports #

import asyncio


# ------------------- #
# Third patry imports #


# ------------- #
# Local imports #



class ShellCMDBase:
    """
    Intended to call system shell commands (cmds) in async and return
    responces if needed (pipe also works).
    """


    def __init__(self) -> None:
        ...


    async def cmd_query_finite(self, cmd:str) -> tuple[bool,str]:
        """
        Executes cmd and returns tuple(success:bool, responce:str).
        If success = false, responce would be error message.
        Finite - because cmd used is intended to return in finite
        time.
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
