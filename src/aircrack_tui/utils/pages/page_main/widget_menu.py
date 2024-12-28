# -------------- #
# System imports #

import asyncio
from functools          import partial
from math               import ceil
from pathlib            import Path
from shutil             import get_terminal_size
from time               import sleep


# ------------------- #
# Third-party imports #

from textual.app        import App, ComposeResult
from textual.events     import Resize
from textual.containers import (
        Container,
        Horizontal, VerticalScroll,
        )
from textual.widgets    import (
        Button,
        )

# ------------- #
# Local imports #



###########
# CLASSES #
###########



class WidgetMenu(Container):
    """
    Contains menu buttons.
    """


    def __init__(self,
            classes:str="WidgetMenu Box",
            ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        # self.border_title = "Interface"


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.btn_placeholder_1 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_exit = Button(
                label="EXIT",
                classes = "WidgetMenu Btn Exit",
                id = "WidgetMenu_Btn_Exit",
                disabled = False,
                )

        self.btn_placeholder_2 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_3 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_4 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_5 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_6 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_7 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_8 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_9 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_10 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.btn_placeholder_11 = Button(
                label="P-HOLDER",
                classes = "WidgetMenu Btn Placeholder",
                disabled = True,
                )

        self.menu_btns = [
                self.btn_placeholder_1,
                self.btn_exit,
                self.btn_placeholder_2,
                self.btn_placeholder_3,
                self.btn_placeholder_4,
                self.btn_placeholder_5,
                self.btn_placeholder_6,
                self.btn_placeholder_7,
                self.btn_placeholder_8,
                self.btn_placeholder_9,
                self.btn_placeholder_10,
                self.btn_placeholder_11,
                ]

        # Id like to use Grid with columns of 2,
        # But the Grid is not scrollable.
        # So have to improvice:
        with VerticalScroll(
                classes="WidgetMenu CustomGridVertical",
                ):
            for row in range( ceil(len(self.menu_btns)/2) ):
                with Horizontal(
                    classes="WidgetMenu CustomGridHorizontal",
                    ):
                    yield self.menu_btns[row*2]
                    yield self.menu_btns[row*2+1]


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button pressed.
        """

        # WidgetMenu -> PageMain -> \
        # ContentSwitcher_Primary -> Screen -> TUIMain
        the_app:App = self.parent.parent.parent.parent.parent
        
        match event.button.id:

            case "WidgetMenu_Btn_Exit":
                the_app.exit(str(event.button))
