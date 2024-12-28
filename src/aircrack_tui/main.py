# ----------------#
# System imports #
# ----------------#

import asyncio
from os                     import system
from typing                 import Optional


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
    Main app entry point.
    """

    if IS_ANDROID:
        # Have to call some root commands, to raise root granting prompt
        # on android before textual app starts.
        # Otherwise there will be difficulties with soft keyboard hiding.
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
    For proper help displaying.
    """


    main(
            no_auto_checks=no_auto_checks,
            force_checks_skip=force_checks_skip,
            )


def app_entry_point():
    """
    console entry point to run dirrectly from console
    (uses pdm build engine).
    Example:
        $ aircrack-tui --help
    """

    app()


if __name__ == "__main__":
    app()
