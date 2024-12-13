# -------------- #
# System imports #

import asyncio
from multiprocessing    import Process as mpProcess
from pathlib            import Path


# ------------------- #
# Third-party imports #

from textual.app        import App, ComposeResult
from textual.containers import (
        Container, VerticalScroll, Grid,
        )
from textual import events
from textual.widgets    import (
        Button, Label, Switch, Input, OptionList,
        TextArea, ListView, ListItem, DataTable,
        RadioSet, RadioButton, Select, SelectionList,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.datastructures  import (
        STYLES_PATH,
        )

from aircrack_tui.utils.pages           import (
        PageDebug,
        )


###########
# CLASSES #
###########


class TUIDebug(App):
    """
    A Termux textual TUI debug app.
    The main purpose is collect and show
    different terminal specs (width, height, font size etc.).
    """


    BINDINGS = [
            ("enter", "toogle_dark", "Dark"),
            ("down", "focus_next", "Next"),
            ("up", "focus_previous", "Prev"),
            ]
    CSS_PATH = [
            Path(STYLES_PATH, 'page_debug.tcss'),
            ]


    def __init__(self) -> None:
        # logger.main.info(f"\n\n\n")
        # logger.main.info(f"Initialising app...")
        super().__init__()
        self.tab_pages:list = []
        self.gpio_process:mpProcess|None = None

        # Apply theme (light/dark) from config
        # self.dark = config["dark"]

        self.pressed_keys:list = []

        # Log it out
        # logger.main.info(f"Initialising done.")
        # logger.main.info(f"BINDINGS are:\n{self.BINDINGS}")
        # logger.main.info(f"CSS_PATH are:\n{self.CSS_PATH}")


    def compose(self) -> ComposeResult:
        """ Create child widgets for the app."""
        
        page_debug = PageDebug()

        # self.tab_pages.append(page_common)
        # page_main = Main(self.tab_pages)

        yield page_debug


    # def action_toggle_dark(self) -> None:
    #     tabs_widget = self.query_one("Tabs.Main")
    #     logger.main.debug(f"Theme switched. 1")
    #     if tabs_widget.has_focus:
    #         logger.main.debug(f"Theme switched.")
    #         self.dark = not self.dark


    # def action_reload_app(self) -> None:
    #     logger.main.debug(f"GOT keycombo to reset app.")
    #     # Refresh entire screen
    #     self.refresh()
    #     # Render screen background
    #     self.render()


    # def on_key(self, event: events.Key) -> None:
    #     """
    #         Press '0' 5 times to reload screen.
    #     """
    #     # Add the key to the set of pressed keys
    #     self.pressed_keys.append(event.key)

    #     # Check if the combination is complete
    #     if self.pressed_keys == ["0", "0", "0", "0"]:
    #         # Call the action if the combination is pressed
    #         self.action_reload_app()
    #         self.pressed_keys.clear()

    #     if len(self.pressed_keys) > 4:
    #         self.pressed_keys.clear()


    def __enter__(self):
        """
        """

        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """
        """

        # # Save current theme
        # config["dark"] = self.dark
        # config_write()
        ...


def main():
    with TUIDebug() as app:
        app.run()

if __name__ == "__main__":
    main()
