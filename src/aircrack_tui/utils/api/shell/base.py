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
        stdout, stderr = await proc.communicate()
        
        # Decode the outputs
        stdout_decoded = stdout.decode("utf-8")
        stderr_decoded = stderr.decode("utf-8")

        # Check if the command executed successfully
        success = proc.returncode == 0
        if success:
            if stdout_decoded:
                return True, stdout_decoded
            elif stderr_decoded:
                # For some reasons there may be commands
                # That run successfully and return meaningfull output,
                # but their output is inside stderr :(
                # Like "sudo iwconfig"
                return True, stderr_decoded
        else:
            # Log both stdout and stderr for debugging
            error_message = stderr_decoded if stderr_decoded else stdout_decoded
            return False, error_message
