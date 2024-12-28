# -------------- #
# System imports #

import asyncio
from pathlib            import Path


# ------------------- #
# Third-party imports #

from textual.app        import ComposeResult
from textual.events     import Resize
from textual.containers import (
        Container,
        )
from textual.widget     import Widget

# ------------- #
# Local imports #

from aircrack_tui.utils.pages.page_main import (
        WidgetInterface,
        WidgetMenu,
        WidgetTarget,
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
        """ Here components are combined."""

        self.widget_interface = WidgetInterface()
        self.widget_menu = WidgetMenu()
        self.widget_target = WidgetTarget()
        
        yield self.widget_interface
        yield self.widget_menu
        yield self.widget_target


    def on_resize(self, event:Resize):
        """
        Switch to PageSizeCheck.
        """

        #TODO: implemet logic
        ...
            
    
class PageMain(Widget):
    """
    Main page containing Interface widget, Menu widget, Target widget.
    """

    def __init__(self, classes:str="PageMain", _id:str="PageMain") -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes, id=_id,)
        self.enbs_dict:dict[str,str]|None = None


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        yield PageMainContainer()


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")
