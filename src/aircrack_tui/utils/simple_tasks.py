from os         import geteuid, system



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
    system("input keyevent 67")
