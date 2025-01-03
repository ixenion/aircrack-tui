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
        RadioSet, RadioButton, Select, SelectionList, ContentSwitcher,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.datastructures  import (
        STYLES_PATH,
        )

from aircrack_tui.utils.pages           import (
        PageMain,
        PageSizeCheck,
        PageDependenciesCheck,
        )

from aircrack_tui.utils.pages.page_main.interface.interface_select import (
        PageInterfaceSelect,
        )


###########
# CLASSES #
###########


class TUIMain(App):
    """
    A Termux textual TUI app.
    """


    # BINDINGS = [
    #         ("enter", "toogle_dark", "Dark"),
    #         ("down", "focus_next", "Next"),
    #         ("up", "focus_previous", "Prev"),
    #         ]
    CSS_PATH = [
            # ContentSwitcher tcss
            Path(STYLES_PATH, 'page_primary.tcss'),
            # Checkers tcss'
            Path(STYLES_PATH, 'page_size_check.tcss'),
            Path(STYLES_PATH, 'page_dependencies_check.tcss'),
            # Main page tcss
            Path(STYLES_PATH, 'page_main', 'page_main.tcss'),
            # Main page widgets tcss
            Path(STYLES_PATH, 'page_main', 'widget_interface.tcss'),
            Path(STYLES_PATH, 'page_main', 'widget_menu.tcss'),
            Path(STYLES_PATH, 'page_main', 'widget_target.tcss'),
            # Main page interface widget buttons
            Path(STYLES_PATH, 'page_main', 'interface', 'interface_select.tcss'),
            ]


    def __init__(self,
                 no_auto_checks:bool|None,
                 force_checks_skip:bool|None,
                 ) -> None:
        # logger.main.info(f"\n\n\n")
        # logger.main.info(f"Initialising app...")
        super().__init__()

        # Apply theme (light/dark) from config
        # self.dark = config["dark"]

        self.no_auto_checks:bool|None = no_auto_checks
        self.force_checks_skip:bool|None = force_checks_skip
        # Log it out
        # logger.main.info(f"Initialising done.")
        # logger.main.info(f"BINDINGS are:\n{self.BINDINGS}")
        # logger.main.info(f"CSS_PATH are:\n{self.CSS_PATH}")


    def compose(self) -> ComposeResult:
        """ Create child widgets for the app."""
        
        # CHECKS PAGES
        page_size_check = PageSizeCheck(
                no_auto_checks=self.no_auto_checks,
                )
        page_dependencies_check = PageDependenciesCheck(
                no_auto_checks=self.no_auto_checks,
                )
        # MAIN PAGE WITH MENU
        page_main = PageMain()

        # MAIN PAGE INTERFACE WIDGET
        interface_select = PageInterfaceSelect()

        if self.force_checks_skip == True:
            initial = "PageMain"
        else:
            initial = "PageSizeCheck"

        self.main_content_switcher = ContentSwitcher(
                id="ContentSwitcher_Primary",
                initial=initial,
                )
        with self.main_content_switcher:
            yield page_size_check
            yield page_dependencies_check
            yield page_main
            # Main page interface select
            yield interface_select


    def on_button_pressed(self, event:Button.Pressed) -> None:
        """
        Handle buttons pressed
        """

        match event.button.id:

            # INTERFACE WIDGET BUTTONS
            case "WidgetInterface_BtnSelect":
                # self.notify(f"btn select", title="Event")
                self.main_content_switcher.current = "InterfaceSelect_Box"

            case "WidgetInterface_BtnSettings":
                self.notify(f"btn settings", title="Event")

            # INTERFACE SELECT IFACE BUTTONS
            case "InterfaceSelect_BtnBack":
                self.main_content_switcher.current = "PageMain"


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
