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
        Input, Button, Switch, Tabs, ContentSwitcher,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.datastructures  import (
        STYLES_PATH,
        DEPENDENCIES,
        shell_cmd,
        )


###########
# CLASSES #
###########

class Dependency(Container):
    """
    To represent screen params and their values.
    """

    def __init__(self,
                 dep_name:str,
                 classes:str="DependencyWidget1",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes)
        self.dep_name = dep_name



    def compose(self) -> ComposeResult:
        """
        Here default (or other custom) Widgets are combined.
        """

        self.dependency = Label(
                renderable=self.dep_name,
                classes="Dependency_1",
                disabled=True,
                )

        self.status = Label(
                renderable="Loading...",
                classes="Status_1",
                disabled=True,
                )

        yield self.dependency
        yield self.status


    def on_mount(self) -> None:
        """
        Do staff when app initialising
        """

        ...


class PageDependenciesCheckContainer(Container):
    """
    """

    def __init__(self,
            no_auto_checks:bool|None,
            classes:str="PageDependenciesCheckContainer",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes)

        self.no_auto_checks:bool|None=no_auto_checks


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

        self.deps_container = ScrollableContainer(
                # Display all dependencies:
                # *[Dependency(dep) for dep in DEPENDENCIES],
                # *[Dependency(str(dep)) for dep in range(30)],
                classes="DepsContainer",
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
        yield self.deps_container
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
        # self.notify("Hello, from Textual!", title="Welcome")


    async def on_event(self, event) -> None:
        """
        Catch 'Show()' event to start checking dependencies.
        """

        match event.__repr__():
            case "Show()":
                # self.notify(f"{event}", title="Event")
                loop = asyncio.get_event_loop()
                check_dependencies_task = loop.create_task(
                        self.check_dependencies_sequence(),
                        )
            case "Leave()":
                ...
            case "Enter()":
                ...

        await super().on_event(event)


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
                if content_switcher.current == "PageDependenciesCheck":
                    content_switcher.current = "PageMain"
                ...


    async def check_dependencies_sequence(self) -> None:
        """
        Check does DEPENDENCIES are present and sends info to the display.
        """

        all_deps_are_installed:bool = True

        for dep in DEPENDENCIES:
            widget = Dependency(f"{dep}:")
            await self.deps_container.mount(widget)
            if await shell_cmd.util_presence_check(util_name=dep):
                widget.status.update(str(True))
                widget.status.styles.color = self.color_success
            else:
                widget.status.update(str(False))
                widget.status.styles.color = self.color_error
                all_deps_are_installed = False
            # Cool animation sleep timer :)
            await asyncio.sleep(0.1)

        # All deps are checked, now decide to continue or not.
        if not all_deps_are_installed:
            return
        self.btn_continue.disabled = False

        # If no_auto_checks is False - auto continue to the next page
        if not self.no_auto_checks:
            self.btn_continue.press()

    
class PageDependenciesCheck(Widget):
    """
    """

    BINDINGS = [
        # ("r", "remove_stopwatch", "Remove"),
    ]
    CSS_PATH = [
            Path(STYLES_PATH, "page_check_dependencies.tcss"),
            ]

    def __init__(self,
            no_auto_checks:bool|None,
            classes:str="PageDependenciesCheck",
            id:str="PageDependenciesCheck",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(
                classes=classes,
                id=id,
                )

        self.no_auto_checks=no_auto_checks
        

    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        yield PageDependenciesCheckContainer(
                no_auto_checks=self.no_auto_checks,
                )


    def on_mount(self) -> None:
        """
        """

        # self.add_class("-hidden")
        self.remove_class("-hidden")
