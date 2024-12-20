from os         import geteuid, system
import subprocess



def is_root() -> bool:
    """
    Does the script running with root priveleges.
    """

    if geteuid() != 0:
        return False
    return True


def android_hide_keyboard() -> None:
    """
    Hides android keyboard in termux emulating backspace key.
    """

    # Send backspace key event
    system("sudo input keyevent 4")


def get_system() -> bool:
    """
    Determines does the OS is Android or not.
    """

    # Example command
    command = "uname -a"

    # Run the command synchronously and capture the output
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    # Check if the command was successful
    if result.returncode == 0:
        # print("Command executed successfully.")
        # print("Output:", result.stdout)
        response = result.stdout
        if "Android" in response:
            return True
        return False
    else:
        # print(f"Command failed with exit code {result.returncode}.")
        # print("Error:", result.stderr)
        return False


def android_term_inc() -> None:
    
    # Data codes from https://www.temblast.com/ref/akeyscode.htm
    # Need to translate from hex to dec.
    # CTRL_LEFT ALT_LEFT NUMPAD_ADD (+)
    system("sudo input keycombination 113 57 157")

def android_term_dec() -> None:
    
    # Data codes from https://www.temblast.com/ref/akeyscode.htm
    # Need to translate from hex to dec.
    # CTRL_LEFT ALT_LEFT NUMPAD_SUBTRACT (-)
    system("sudo input keycombination 113 57 156")


def android_is_keyboard_shown() -> bool:
    """
    Check does keyboard hidden on android or where!?
    """

    # Example command
    command = "sudo dumpsys input_method | grep mInputShown"

    # Run the command synchronously and capture the output
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    # Check if the command was successful
    if result.returncode == 0:
        response = result.stdout
        if "true" in response:
            return True
        return False
    else:
        return False
