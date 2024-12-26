# ----------------#
# System imports #
# ----------------#

import asyncio
from dataclasses            import asdict
from os                     import geteuid, system
from pprint                 import pprint
from time                   import time, gmtime, strftime
from typing                 import AsyncGenerator, Optional


# ------------------- #
# Third party imports #

import typer


# -------------#
# Local imports
# -------------#

from aircrack_tui import __app_name__, __version__

from aircrack_tui.utils.api     import (
        TUIMain,
        )
from aircrack_tui.utils.datastructures  import (
        IS_ANDROID,
        )
from aircrack_tui.utils.simple_tasks    import (
        is_root,
        android_hide_keyboard,
        )


# --------- #
# FUNCTIONS #

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


# ------- #
# CLASSES #




# ------ #
#  MAIN  #
# ------ #

def main(
        no_auto_checks:bool|None,
        force_checks_skip:bool|None,
        ) -> None:
    """
    """

    if IS_ANDROID:
        system("sudo echo [*] Requesting root access...")

    with TUIMain(
            no_auto_checks,
            force_checks_skip,
            ) as tui_app:
        tui_app.run()





#################
# BUILD CLI APP #
#################

# 'add_completion=False' - get rid of
# --install-completion, --show-completion
# app = typer.Typer(add_completion=False)
app = typer.Typer()

@app.command()
def control(
        version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True),

        no_auto_checks: Optional[bool] = typer.Option(
            None,
            "--no-auto-checks",
            help=f"Make term size and dependencies to be checked with manual control (dont auto continue on check success).",
            is_eager=True,
            ),

        force_checks_skip: Optional[bool] = typer.Option(
            None,
            "-f",
            help=f"Skip term size check and dependencies checks.",
            is_eager=True,
            )
        ):

    """
    """


    # asyncio.run(main(debug))
    main(
            no_auto_checks=no_auto_checks,
            force_checks_skip=force_checks_skip,
            )


def app_entry_point():
    """
        To run dirrectly from console (uses pdm build engine).
        Example:
    """

    app()


if __name__ == "__main__":
    app()
