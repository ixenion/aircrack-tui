# -------------- #
# System imports #

import asyncio
from functools          import partial
from pathlib            import Path
from shutil             import get_terminal_size
from time               import sleep


# ------------------- #
# Third-party imports #

from textual.app        import App, ComposeResult
from textual.events     import Resize
from textual.color import Color
from textual.containers import (
        Container, ScrollableContainer, Vertical,
        Horizontal, VerticalScroll,
        )
from textual.widget     import Widget
from textual.await_complete    import AwaitComplete
from textual.widgets    import (
        Static, Tab, Rule, Label, LoadingIndicator,
        Input, Button, Switch, Tabs
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.datastructures  import (
        STYLES_PATH,
        IS_ANDROID,
        )
from aircrack_tui.utils.simple_tasks    import (
        android_term_inc,
        android_term_dec,
        )


###########
# CLASSES #
###########

class ParameterValue1(Container):
    """
    To represent screen params and their values.
    """

    def __init__(self,
                 parameter_name:str,
                 classes:str="ParameterValue1",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes)
        self.parameter_name = parameter_name


    def compose(self) -> ComposeResult:
        """
        Here default (or other custom) Widgets are combined.
        """

        self.parameter = Label(
                renderable=self.parameter_name,
                classes="Parameter_1",
                disabled=True,
                )

        self.value = Label(
                renderable="Loading...",
                classes="Value_1",
                disabled=True,
                )

        yield self.parameter
        yield self.value


    def on_mount(self) -> None:
        """
        Do staff when app initialising
        """

        ...


class PageDependenciesCheckContainer(Container):
    """
    """

    def __init__(self,
                 classes:str="PageDependenciesCheckContainer",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        self.title = Label(
                renderable="Checking dependencies",
                classes="PageDependenciesCheck_Title",
                disabled=True,
                )

        self.indicator = LoadingIndicator(
                id="PageDependensiesCheck_LoadingIndicator_1",
                classes="PageDependenciesCheck_LoadingIndicator_1",
                disabled=True,
                )

        self.btn_exit = Button(
                label="EXIT",
                id="PageDependenciesCheck_Btn_Exit",
                classes="PageDependenciesCheck_Btn_1",
                )

        self.btn_continue = Button(
                label="CONTINUE",
                id="PageDependenciesCheck_Btn_Continue",
                classes="PageDependenciesCheck_Btn_1",
                )

        # Had to wrap button into Container because
        # Cant set align for button dirrectly.
        self.btns_container = Container(
                self.btn_exit,
                self.btn_continue,
                classes="PageDependenciesCheck_Btn_1_Container",
                )


        yield self.title
        yield self.indicator
        yield self.btns_container


    def on_mount(self):
        """
        Called on container creation.
        """

        # Gather colors
        self.color_text     = Color(255, 205, 77)
        self.color_success  = Color(78, 191, 113)
        self.color_error    = Color(208, 80, 109)

        # self.btn_continue.styles.align = ("center", "bottom")
        # self.btn_continue.styles.align_horizontal = "right"
        self.btn_continue.disabled = True


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button pressed which (buttons) are defined
        inside that class.
        """

        the_app:App = self.parent.parent.parent.parent
        
        match event.button.id:

            case "PageDependenciesCheck_Btn_Exit":
                # PageSizeCheckContainer -> PageSizeCheck -> \
                # ContentSwitcher_Primary -> Screen -> TUIMain
                the_app.exit(str(event.button))

            case "PageDependenciesCheck_Btn_Continue":
                content_switcher = the_app.query_one("#ContentSwitcher_Primary")
                # if content_switcher.current == "PageSizeCheck":
                #     content_switcher.current = "PageDependenciesCheck"
                ...

    
class PageDependenciesCheck(Widget):
    """
    """

    BINDINGS = [
        # ("r", "remove_stopwatch", "Remove"),
    ]
    CSS_PATH = [
            Path(STYLES_PATH, "page_check_size.tcss"),
            ]

    def __init__(self,
                 classes:str="PageDependenciesCheck",
                 id:str="PageDependenciesCheck",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(
                classes=classes,
                id=id,
                )


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        yield PageDependenciesCheckContainer()


    def on_mount(self) -> None:
        """
        """

        # self.add_class("-hidden")
        self.remove_class("-hidden")
