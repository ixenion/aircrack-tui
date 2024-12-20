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
        TUIDebug,
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
        debug:bool|None,
        no_size_check_auto:bool|None,
        ) -> None:
    """
    """

    if debug:
        with TUIDebug() as tui_app:
            tui_app.run()
        return

    with TUIMain(
            no_size_check_auto,
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

        debug: Optional[bool] = typer.Option(
            None,
            "-d",
            "--debug",
            help=f"Start debug display with terminal window specs.",
            # callback=_app_tui_debug,
            is_eager=True,
            ),

        no_size_check_auto: Optional[bool] = typer.Option(
            None,
            "--no-size-check-auto",
            help=f"Forse term size check to manual mode.",
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

    # asyncio.run(main(debug))
    main(
            debug=debug,
            no_size_check_auto=no_size_check_auto,
            )


def app_entry_point():
    """
        To run dirrectly from console (uses pdm build engine).
        Example:
    """

    app()


if __name__ == "__main__":
    app()
