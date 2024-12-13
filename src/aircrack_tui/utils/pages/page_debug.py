# -------------- #
# System imports #

import asyncio
from functools          import partial
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





from rich_pixels import Pixels
from rich.console import Console
from rich.segment import Segment
from rich.style import Style

console = Console()

# Draw your shapes using any character you want
grid = """\
     xx   xx
     ox   ox
     Ox   Ox
xx             xx
xxxxxxxxxxxxxxxxx
"""

# Map characters to different characters/styles
# mapping = {
#     "x": Segment(" ", Style.parse("yellow on yellow")),
#     "o": Segment(" ", Style.parse("on white")),
#     "O": Segment(" ", Style.parse("on blue")),
# }

# pixels = Pixels.from_ascii(grid, mapping)
# pixels = Pixels.from_ascii(grid)
# console.print(pixels)
pixels = Pixels.from_image_path("/home/arix/Downloads/logo_2.png")

class ImageWidget(Widget):
    # def __init__(self, image_path: str):
    def __init__(self, pixels:Pixels):
        super().__init__()
        self.pixels = pixels

    def render(self):
        return self.pixels



###########
# CLASSES #
###########

class PageDebugContainer(Container):
    """
    """

    def __init__(self,
                 classes:str="PageDebugContainer",
                 _id:str="PageDebugContainer",
                 ) -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes, id=_id)


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        self.indicator = LoadingIndicator(
                id="PageDebug_LoadingIndicator",
                classes="PageDebug_LoadingIndicator",
                disabled=True,
                )

        self.text_1 = Label(
                renderable="( Resize terminal window )",
                id="PageDebug_Text_1",
                classes="PageDebug_Text",
                disabled=True,
                )

        self.text_2 = Label(
                renderable="Loading...",
                id="PageDebug_Text_2",
                classes="PageDebug_Text",
                disabled=True,
                )

        self.text_3 = Label(
                renderable="Loading...",
                id="PageDebug_Text_3",
                classes="PageDebug_Text",
                disabled=True,
                )

        self.text_4 = Label(
                renderable="Loading...",
                id="PageDebug_Text_4",
                classes="PageDebug_Text",
                disabled=True,
                )

        yield self.indicator
        yield self.text_1
        yield self.text_2
        yield self.text_3
        yield self.text_4

        # yield pixels
        yield ImageWidget(pixels)


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
        self.text_2.update(f"Width: {width} / Height: {height}\nRatio: {round(width/height,2)}")

        size = event.size
        virt_size = event.virtual_size
        cont_size = event.container_size
        pix_size = event.pixel_size

        self.text_3.update(f"Size: {size}\nVirtual size: {virt_size}")
        self.text_4.update(
                f"Container size: {cont_size}\nPixel size: {pix_size}")


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



    
class PageDebug(Widget):
    """
    """

    BINDINGS = [
        # ("r", "remove_stopwatch", "Remove"),
    ]

    def __init__(self, classes:str="PageDebug", _id:str="PageDebug") -> None:
        """ Set 'classes' and 'id' attribute to the page - 'Common' class."""

        super().__init__(classes=classes, id=_id,)
        self.enbs_dict:dict[str,str]|None = None
        self.border_subtitle = "bottom right"
        self.border_title = "top left"


    def compose(self) -> ComposeResult:
        """ Here default (or other custom) Widgets are combined."""

        yield PageDebugContainer()


    def on_mount(self) -> None:
        # Show LoadingPage and hide other
        page_debug = self.query_one(PageDebugContainer)
        page_debug.remove_class("-hidden")

        # loading_error.add_class("-hidden")
        # loading_success.add_class("-hidden")
        # logger.main.debug(f"LoadingPage showed.")

        # # Stasrt eNBs search
        # loop = asyncio.get_running_loop()
        # loop.create_task(self.get_enbs_integrated())
        # # Start bcom.bs_status_update task
        # loop.create_task(bcom.bs_status_update())
