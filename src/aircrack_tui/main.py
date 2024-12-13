# ----------------#
# System imports #
# ----------------#

import asyncio
from dataclasses            import asdict
from os                     import geteuid
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
        TUIDebug,
        )


# --------- #
# FUNCTIONS #

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def _app_tui_debug():
    """
    Run TUI Debug page.
    """

    with TUIDebug() as tui_app:
        tui_app.run()


# ------- #
# CLASSES #




# ------ #
#  MAIN  #
# ------ #

async def main() -> None:
    """
    """
    
    ...





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

        debug: Optional[bool] = typer.Option(
            None,
            "-d",
            "--debug",
            help=f"Start debug display with terminal window specs.",
            callback=_app_tui_debug,
            is_eager=True,
            )

        # mode:Keys.MODE = typer.Option(
        #     default=Keys.MODE.real,
        #     help="Set NMEA source. Real data only with root."),
        # consumer:Keys.CONSUMER = typer.Option(
        #     default=Keys.CONSUMER.stdout,
        #     help="Set data consumer."),
        # delay:float = typer.Option(
        #     default=0.2,
        #     help="Set GNSS position fix in sec.",
        #     min=0.2,
        #     max=10,
        #     ),

        ):

    """
    """

    # asyncio.run(main(mode, consumer, delay))
    asyncio.run(main())


def app_entry_point():
    """
        To run dirrectly from console (uses pdm build engine).
        Example:
    """

    app()


if __name__ == "__main__":
    app()
