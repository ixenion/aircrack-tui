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
        )


###########
# CLASSES #
###########

class PageMainContainer(Container):
    """
    """

    def __init__(self,
                 classes:str="PageMainContainer",
                 _id:str="PageMainContainer",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes, id=_id)


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        self.temp = Label(
                renderable="MAIN",
                classes="Temp",
                disabled=True,
                )

        yield self.temp


    def on_resize(self, event:Resize):
        """
        Switch to PageSizeCheck.
        """

        ...
            
    
class PageMain(Widget):
    """
    """

    BINDINGS = [
        # ("r", "remove_stopwatch", "Remove"),
    ]
    CSS_PATH = [
            Path(STYLES_PATH, "page_main.tcss"),
            ]

    def __init__(self, classes:str="PageMain", _id:str="PageMain") -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes, id=_id,)
        self.enbs_dict:dict[str,str]|None = None


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        yield PageMainContainer()


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")
