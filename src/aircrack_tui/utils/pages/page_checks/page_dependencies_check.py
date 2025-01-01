# -------------- #
# System imports #

import asyncio
from pathlib            import Path


# ------------------- #
# Third-party imports #

from textual.app        import App, ComposeResult
from textual.color import Color
from textual.containers import (
        Container, ScrollableContainer,
        )
from textual.widget     import Widget
from textual.widgets    import (
        Label, LoadingIndicator,
        Button, ContentSwitcher,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.datastructures  import (
        DEPENDENCIES,
        shell_cmd,
        )


###########
# CLASSES #
###########

class Dependency(Container):
    """
    To represent dependency name and its status (installed or not).
    """

    def __init__(self,
                 dep_name:str,
                 classes:str="DependencyWidget1",
                 ) -> None:
        """ Set 'classes' to the Container."""

        super().__init__(classes=classes)
        self.dep_name = dep_name


    def compose(self) -> ComposeResult:
        """
        Here components are combined.
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
        Do staff when app initialising.
        """

        ...


class PageDependenciesCheckContainer(Container):
    """
    Main Container for Page with Dependencies status.
    """

    def __init__(self,
            no_auto_checks:bool|None,
            classes:str="PageDependenciesCheckContainer",
                 ) -> None:
        """ Set 'classes' to the Container."""

        super().__init__(classes=classes)

        self.no_auto_checks:bool|None=no_auto_checks

        # Gather colors
        self.color_text     = Color(255, 205, 77)
        self.color_success  = Color(78, 191, 113)
        self.color_error    = Color(208, 80, 109)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

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

        self.btn_continue.disabled = True


    async def on_event(self, event) -> None:
        """
        Catch different events.
        """

        match event.__repr__():
            case "Show()":
                # Catch 'Show()' event to start checking dependencies.
                # self.notify(f"{event}", title="Event")
                loop = asyncio.get_event_loop()
                check_dependencies_task = loop.create_task(
                        self.check_dependencies_sequence(),
                        )
            case "Leave()":
                ...
            case "Enter()":
                ...

        # Propagate event:
        await super().on_event(event)


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button pressed.
        """
        
        match event.button.id:

            case "PageDependenciesCheck_Btn_Exit":
                self.app.exit(str(event.button))

            case "PageDependenciesCheck_Btn_Continue":
                content_switcher:ContentSwitcher = self.app.query_one("#ContentSwitcher_Primary")
                if content_switcher.current == "PageDependenciesCheck":
                    content_switcher.current = "PageMain"


    async def check_dependencies_sequence(self) -> None:
        """
        Checks if DEPENDENCIES are present and sends info to the display.
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

        # If self.no_auto_checks is False - auto continue to the next page
        if not self.no_auto_checks:
            self.btn_continue.press()

    
class PageDependenciesCheck(Widget):
    """
    Main Contanier Page for dependency checking.
    """

    def __init__(self,
            no_auto_checks:bool|None,
            classes:str="PageDependenciesCheck",
            id:str="PageDependenciesCheck",
                 ) -> None:
        """ Set 'classes' and 'id' attributes to the Container."""

        super().__init__(
                classes=classes,
                id=id,
                )

        self.no_auto_checks=no_auto_checks
        

    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        yield PageDependenciesCheckContainer(
                no_auto_checks=self.no_auto_checks,
                )


    def on_mount(self) -> None:
        """
        Do staff when app initialising.
        """

        self.remove_class("-hidden")
