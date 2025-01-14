# -------------- #
# System imports #

import asyncio
from pathlib            import Path
from shutil             import get_terminal_size


# ------------------- #
# Third-party imports #

from textual.app        import App, ComposeResult
from textual.events     import Resize
from textual.color import Color
from textual.containers import (
        Container,
        )
from textual.widget     import Widget
from textual.await_complete    import AwaitComplete
from textual.widgets    import (
        Label, LoadingIndicator,
        Button, ContentSwitcher,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.datastructures  import (
        STYLES_PATH,
        IS_ANDROID,
        )
from aircrack_tui.utils.simple_tasks    import (
        android_hide_keyboard,
        android_term_inc,
        android_term_dec,
        android_is_keyboard_shown,
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
        """ Set 'classes' attribute to the Container."""

        super().__init__(classes=classes)
        self.parameter_name = parameter_name


    def compose(self) -> ComposeResult:
        """
        Here components are combined.
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


class PageSizeCheckContainer(Container):
    """
    Page size check main container cintaining all info
    to check screen size.
    """

    def __init__(self,
                 no_auto_checks:bool|None=None,
                 classes:str="PageSizeCheckContainer",
                 ) -> None:
        """ Set 'classes' to the Container."""

        super().__init__(classes=classes)
        self.term_max_width = 49
        self.term_min_width = 47
        self.autocontinue:bool = False if no_auto_checks == True else True
        self.first_on_resize_check:bool = True
        self.autosize_pressed:bool = False

        # Gather colors
        self.color_text     = Color(255, 205, 77)
        self.color_success  = Color(78, 191, 113)
        self.color_error    = Color(208, 80, 109)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.title = Label(
                renderable="Checking term window size",
                classes="PageSizeCheck_Title",
                disabled=True,
                )

        self.indicator = LoadingIndicator(
                id="PageSizeCheck_LoadingIndicator_1",
                classes="PageSizeCheck_LoadingIndicator_1",
                disabled=True,
                )

        self.parameter_1 = ParameterValue1(
                parameter_name="Width:")

        self.parameter_2 = ParameterValue1(
                parameter_name="Height:")

        self.parameter_3 = ParameterValue1(
                parameter_name="Ratio:")

        self.hint_1 = Label(
                renderable="( Set 'Width' between 44-48 )",
                classes="PageSizeCheck_Hint_1",
                disabled=True,
                )

        self.hint_2 = Label(
                renderable="( Make screen vertical OR hide keyboard)",
                classes="PageSizeCheck_Hint_1",
                disabled=True,
                )

        self.btn_exit = Button(
                label="EXIT",
                id="PageSizeCheck_Btn_Exit",
                classes="PageSizeCheck_Btn_1",
                )

        self.btn_continue = Button(
                label="CONTINUE",
                id="PageSizeCheck_Btn_Continue",
                classes="PageSizeCheck_Btn_1",
                )

        self.btn_term_autosize = Button(
                label="AUTOSIZE",
                id="PageSizeCheck_Btn_TermAutosize",
                classes="PageSizeCheck_Btn_1",
                )

        # Had to wrap button into Container because
        # Cant set align for button dirrectly.
        self.btns_container = Container(
                self.btn_exit,
                self.btn_term_autosize,
                self.btn_continue,
                classes="PageSizeCheck_Btn_1_Container",
                )

        yield self.title
        yield self.indicator
        yield self.parameter_1
        yield self.parameter_2
        yield self.parameter_3
        yield self.hint_1
        yield self.hint_2
        yield self.btns_container


    def on_resize(self, event:Resize):
        """
        Called every time terminal window was resized or
        terminal font size was changed.
        """

        if IS_ANDROID:
            if android_is_keyboard_shown():
                android_hide_keyboard()
                return
            
        # Get the terminal size
        terminal_size = get_terminal_size()
        # Access the width (columns) and height (lines)
        width = terminal_size.columns
        height = terminal_size.lines
        ratio = round(width/height, 2)

        # Check width:
        if width > self.term_max_width or width < self.term_min_width:
            self.parameter_1.value.styles.color = \
                    self.color_error
        else:
            self.parameter_1.value.styles.color = \
                    self.color_success

        # Check height
        self.parameter_2.value.styles.color = self.color_text

        # Check ratio:
        if ratio > 1.25 or ratio < 0.75:
            self.parameter_3.value.styles.color = \
                    self.color_error
        else:
            self.parameter_3.value.styles.color = \
                    self.color_success

        self.parameter_1.value.update(str(width))
        self.parameter_2.value.update(str(height))
        self.parameter_3.value.update(str(ratio))


        # Gather parameters' colors
        param1_color = self.parameter_1.value.styles.color
        # param2_color = self.parameter_2.value.styles.color
        param3_color = self.parameter_3.value.styles.color
        
        # Show hint for Width
        if param1_color == self.color_error:
            self.hint_1.remove_class("-hidden")
        else:
            self.hint_1.add_class("-hidden")

        # Show hint for Ratio
        if param3_color == self.color_error:
            self.hint_2.remove_class("-hidden")
        else:
            self.hint_2.add_class("-hidden")

        # Show btn_continue
        if param1_color == self.color_error or param3_color == self.color_error:
            self.btn_continue.disabled = True
        else:
            self.autosize_pressed = False
            self.btn_continue.disabled = False

        # Show BTN Autoresize
        if (width < self.term_min_width or width > self.term_max_width) \
                and IS_ANDROID:
            # Terminal font size to big
            self.btn_term_autosize.remove_class("-hidden")
        else:
            # Terminal font size is good
            self.btn_term_autosize.add_class("-hidden")

        # IF AUTO CONTINUE
        if param1_color != self.color_error and self.autocontinue \
                and self.first_on_resize_check \
                and not android_is_keyboard_shown():
            self.btn_continue.press()

        # IF autosize btn pressed
        if self.autosize_pressed:
            if width > self.term_max_width:
                android_term_inc()
            elif width < self.term_min_width:
                android_term_dec()


        self.first_on_resize_check = False



    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button pressed which (buttons) are defined
        inside that class.
        """
        
        match event.button.id:

            case "PageSizeCheck_Btn_Exit":
                self.app.exit(str(event.button))

            case "PageSizeCheck_Btn_TermAutosize":
                self.autosize_pressed = True
                self.btn_term_autosize.add_class("-hidden")
                android_term_inc()

            case "PageSizeCheck_Btn_Continue":
                content_switcher:ContentSwitcher = self.app.query_one("#ContentSwitcher_Primary")
                if content_switcher.current == "PageSizeCheck":
                    content_switcher.current = "PageDependenciesCheck"



    
class PageSizeCheck(Widget):
    """
    Main Container page for size check params.
    """

    def __init__(self,
                 no_auto_checks:bool|None=None,
                 classes:str="PageSizeCheck",
                 id:str="PageSizeCheck",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes, id=id)
        self.border_subtitle = "bottom right"
        self.border_title = "top left"

        self.no_auto_checks:bool|None = no_auto_checks


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        yield PageSizeCheckContainer(
                no_auto_checks=self.no_auto_checks,
                )


    def on_mount(self) -> None:
        """
        Do staff when app initialising.
        """

        self.remove_class("-hidden")
