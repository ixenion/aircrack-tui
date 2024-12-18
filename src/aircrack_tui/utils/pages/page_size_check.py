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


class PageSizeCheckContainer(Container):
    """
    """

    def __init__(self,
                 classes:str="PageSizeCheckContainer",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

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

        # Had to wrap button into Container because
        # Cant set align for button dirrectly.
        self.btn_continue_container = Container(
                self.btn_exit,
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
        yield self.btn_continue_container

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



    def on_resize(self, event:Resize):
        """
        Called every time terminal window was resized or
        terminal font size was changed.
        """
            
        # Get the terminal size
        terminal_size = get_terminal_size()
        # Access the width (columns) and height (lines)
        width = terminal_size.columns
        height = terminal_size.lines
        ratio = round(width/height, 2)

        # Check width:
        if width > 48 or width < 44:
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
        param2_color = self.parameter_2.value.styles.color
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
            self.btn_continue.add_class("-hidden")
        else:
            self.btn_continue.remove_class("-hidden")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button pressed which (buttons) are defined
        inside that class.
        """

        # PageSizeCheckContainer -> PageSizeCheck -> Screen -> TUIMain
        the_app:App = self.parent.parent.parent
        the_app.exit(str(event.button))


# class LoadingErrorPage(Container):
#     """
#         This page will be shown if 'Common._get_enbs_integrated()'
#         returns empty dict, which means that no one integrated
#         eNB was found.
#     """

#     def __init__(self,
#                  classes:str="eNBsLoadingError",
#                  _id:str="eNBsLoadingError") -> None:
#         """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

#         super().__init__(classes=classes, id=_id,)


#     def compose(self) -> ComposeResult:
#         """ Here default (or other custom) Widgets are combined."""

#         with Vertical(classes="LoadingErrorBox"):
#             with Vertical(classes="LoadingErrorBox"):
#                 yield Label(
#                         "Ошибка подключения!",
#                         id="LoadingErrorText",
#                         classes="LoadingErrorText",
#                         disabled=True,
#                         )
#             with Vertical(classes="LoadingErrorBox"):
#                 yield Button(
#                         "Повторить попытку",
#                         id="LoadingErrorBtn",
#                         classes="LoadingErrorBtn",
#                         disabled=False,
#                         )
    
#     async def on_button_pressed(self, event:Button.Pressed) -> None:
#         # common = LoadingErrorPage -> ScrollableContainer -> Common
#         common = self.parent
#         # loading = LoadingErrorPage -> ScrollableContainer -> LoadingPage
#         loading = self.parent.query_one(LoadingPage)
#         loading_error = self.parent.query_one(LoadingErrorPage)
#         loading_success = self.parent.query_one(LoadingSuccessPage)
#         match event.button.id:
#             case "LoadingErrorBtn":
#                 loading.remove_class("-hidden")
#                 loading_error.add_class("-hidden")
#                 loading_success.add_class("-hidden")
#                 logger.main.debug(f"LoadingErrorBtn pressed.")
#                 loop = asyncio.get_running_loop()
#                 loop.create_task(common.get_enbs_integrated())
#             case _: pass
#         pass


# class LoadingSuccessPage(Container):
#     """
#         This page will be shown if 'Common._get_enbs_integrated()'
#         returns empty dict, which means that no one integrated
#         eNB was found.
#     """

#     def __init__(self,
#                  classes:str="eNBsLoadingSuccess",
#                  _id:str="eNBsLoadingSuccess") -> None:
#         """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

#         super().__init__(classes=classes, id=_id,)


#     def compose(self) -> ComposeResult:
#         """ Here default (or other custom) Widgets are combined."""

#         # test = ENB(id="bs450", name="БС 450")
#         # test2 = ENB(id="bs450", name="БС 900")
#         yield Container(
#                 # LoadingSuccessPageItem(test),
#                 # LoadingSuccessPageItem(test2),
#                 classes="LoadingSuccessContainer",
#                 )

# class ENBSwitch(Switch):
#     def __init__(self,
#                  *args, **kwargs,
#                  ) -> None:
#         super().__init__(*args, **kwargs)
#         self._programmatic_change = False  # Flag to track programmatic changes
#         self._manual_change = False  # Flag to track user input changes


# class LoadingSuccessPageItem(Widget):
#     """
#         Single item (line) of LoadingSuccessPage.
#     """


#     def __init__(self, enb_item:str,
#                  classes:str="eNBsLoadingSuccessItem",
#                  ) -> None:
#         """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

#         super().__init__(classes=classes,)
#         self.enb_item = enb_item
#         self.last_state:None|str = None


#     def compose(self) -> ComposeResult:
#         """ Here default (or other custom) Widgets are combined."""

#         with Horizontal(classes="CommonItem"):
#             # Label
#             # Replace 'bs' with 'бс'
#             label = "бс" + self.enb_item[2:]
#             yield Container(
#                     Label(
#                         # f"{self.enb_item}",
#                         f"{label}",
#                         classes="CommonItem Name",
#                         ),
#                     classes="CommonItem Name"
#                     )
#             # Status
#             yield Container(
#                     Label(
#                         "загрузка..",
#                         classes=f"CommonItem Status {self.enb_item}",
#                         ),
#                     classes="CommonItem Status"
#                     )
#             # Switch
#             yield ENBSwitch(
#                     value=False,
#                     classes=f"CommonItem Switch {self.enb_item}"
#                     )

    
#     def on_mount(self) -> None:
#         self.set_interval(2, self.enb_status_check)


#     async def on_switch_changed(self, event:ENBSwitch.Changed):
#         switch = event.switch
#         value = event.value

#         # If there was programmatic change (not user input)
#         # Just switch Switch and do not send any directives to the backend.
#         if switch._programmatic_change:
#             switch._programmatic_change = False
#             return


#         # CONFIRM MENU
#         # ENBSetterableItem -> eNBPageContainer_1 -> ENBPage -> Main
#         # confirm_menu = self.parent.parent.parent.query_one(
#         confirm_menu = self.parent.parent.parent.parent.query_one(
#                 f".ConfirmMenu_1.Window")
#         tabs = self.parent.parent.parent.parent.query_one("Tabs.Main")
#         # To make focusable only ConfirmMenu_1
#         # Disable ENBPage and Tabs
#         self.parent.parent.disabled = True
#         tabs.disabled = True
#         # Set description for ConfirmMenu
#         # (contains parameter and its new value)
#         confirm_menu.set_description(
#                 parameter=self.enb_item,
#                 value=value)
#         confirm_menu.remove_class("-hidden")
#         confirm_menu.disabled = False
#         confirm_menu.focus()
#         # Await button pressed
#         btn = await confirm_menu.btn_pressed.get()
#         # Hide ConfirmMenu
#         confirm_menu.add_class("-hidden")
#         confirm_menu.disabled = True
#         # Return focus back to input item
#         tabs.disabled = False
#         self.parent.parent.disabled = False
#         switch.focus()
#         # If button pressed is 'cancel' - return
#         if btn == "cancel":
#             switch.value = not switch.value
#             switch._programmatic_change = True
#             return


#         logger.main.info(f"Switching {self.enb_item} state to: {value}")

#         switch.styles.background = "yellow 60%"
#         try:
#             success:bool = await bcom.enable(
#                     bs_name=self.enb_item, state=value)

#             if success:
#                 switch.styles.background = "lime 60%"
#                 logger.main.info(
#                     f"Switching {self.enb_item} state to: {value} - success")
#             else:
#                 switch.styles.background = "red 60%"

#         except Exception as e:
#             logger.main.error(
#                     f"Switching {self.enb_item} state to: {value} - fail.")
#             logger.main.error(f"Exception: {e}")
#             switch.styles.background = "red 60%"
        



#     async def enb_status_check(self) -> None:

#         # if not self.may_update_switch_value:
#         #     return

#         result_eng = "disabled"
#         enb_id = self.enb_item
#         logger.main.debug(f"Checking status for: {enb_id}")
#         try:
#             response:dict[str,str] = await asyncio.wait_for(
#                     bcom.devices_integrated_status(), timeout=5)
#             for device in response.items():
#                 if device[0] == enb_id:
#                     # 'result' may be "online" | "offline"
#                     result_eng = device[1]
#                     break
#             # Russify
#             match result_eng:
#                 case "online":
#                     result = "В работе"
#                 case "disabled":
#                     result = "Отключено"
#                 case "offline":
#                     result = "Отключено"
#                 case "Offline":
#                     result = "Отключено"
#                 case "error":
#                     result = "Ошибка"
#                 case "loading":
#                     result = "Загрузка"
#                 case "isolated":
#                     result = "Отключено"

#         except TimeoutError:
#             logger.main.debug(f"Timeout. Cant retreive status for {enb_id}")
#         except Exception as e:
#             logger.main.debug(f"Cant retreive status for {enb_id}. Exception: {e}")

#         logger.main.debug(f"Status for {enb_id}:{result_eng}")
#         label = self.query_one(f".CommonItem.Status.{enb_id}")
#         label.update(result)
#         switch = self.query_one(f".CommonItem.Switch.{self.enb_item}")

#         # First of all - Update Switch background to default grey
#         # (or white if it's light theme)
#         if not switch.has_focus:
#             switch.styles.background = label.styles.background

#         # If new state (result) is not differ from the last state - do not
#         # try to update switch.value, because it can cause problems
#         # If we try to change state manually and update
#         # value programmaticaly simultaniously.
#         if self.last_state == result_eng:
#             return
#         self.last_state = result_eng
        
#         # But if we got new state (stored in 'result') - update switch
#         # value and set flag 'switch._programmatic_change' to True to
#         # avoid repeating sending of the same state.
#         if result_eng == "online" or result_eng == "loading" \
#                 or result_eng == "isolated":
#             # Also we check that switch already not in the target position
#             # Because if it is - that means we'v just switch the switch
#             # state and dont want to call new switch event one more time
#             # because if we are - there also be second call to endpoint
#             # With same value and we prefer avoid repeating meaningless
#             # messages.
#             if not switch.value:
#                 switch.value = True
#                 switch._programmatic_change = True
#         elif result_eng == "offline" or result_eng == "disabled" \
#                 or result_eng == "error" or result_eng == "Offline":
#             if switch.value:
#                 switch.value = False
#                 switch._programmatic_change = True
#         else:
#             # "Loading..", etc - just ignore
#             pass



    
class PageSizeCheck(Widget):
    """
    """

    BINDINGS = [
        # ("r", "remove_stopwatch", "Remove"),
    ]
    CSS_PATH = [
            Path(STYLES_PATH, "page_check_size.tcss"),
            ]

    def __init__(self, classes:str="PageSizeCheck") -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes)
        self.border_subtitle = "bottom right"
        self.border_title = "top left"


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        yield PageSizeCheckContainer()


    def on_mount(self) -> None:
        """
        """

        self.remove_class("-hidden")
