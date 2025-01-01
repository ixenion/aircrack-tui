# -------------- #
# System imports #

import asyncio


# ------------------- #
# Third-party imports #

from textual.app        import ComposeResult
from textual.containers import (
        Container, Vertical, Grid,
        Horizontal, ScrollableContainer,
        )
from textual.widgets    import (
        Label,
        Button,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.api.models      import (
        InterfaceParams,
        )

from aircrack_tui.utils.pages.page_main.widget_interface    import (
        # ParametersList as InterfaceParametersList,
        ParametersList as InterfaceParametersList,
        WidgetInterface,
        )



###########
# CLASSES #
###########

class Parameter(Horizontal):
    """
    Contains two Labels: parameter name and parameter value.
    """

    def __init__(self,
                 parameter_name:str,
                 parameter_value:str|None,
                 classes:str="InterfaceSelect Parameter",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.parameter_name:str = parameter_name
        self.parameter_val:str = str(parameter_value)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameter_label = Label(
                renderable=self.parameter_name,
                classes="InterfaceSelect ParameterName",
                disabled=True,
                )

        self.parameter_value = Label(
                renderable=self.parameter_val,
                classes="InterfaceSelect ParameterValue",
                disabled=True,
                )

        yield self.parameter_label
        yield self.parameter_value


class ParametersList(Vertical):
    """
    Contains All parameters list with corresponding values.
    """

    def __init__(self,
                 iface_name:str,
                 iface_mac:str|None,
                 iface_standart:str|None,
                 classes:str="InterfaceSelect ParametersList",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.iface_name_val     = iface_name
        self.iface_mac_val      = iface_mac
        self.iface_standart_val = iface_standart


    def compose(self) -> ComposeResult:
        """ Here components are combined."""
        
        self.iface_name     = Parameter(
                parameter_name="Name:",
                parameter_value=self.iface_name_val,
                )
        self.iface_standart = Parameter(
                parameter_name="Standart:",
                parameter_value=self.iface_standart_val,
                )
        self.iface_mac      = Parameter(
                parameter_name="MAC:",
                parameter_value=self.iface_mac_val,
                )

        yield self.iface_name
        yield self.iface_mac
        yield self.iface_standart


class CardControlPanel(Vertical):
    """
    Contains one button: set - select interface and
    the same button to unset that interface.
    """


    def __init__(self,
                 classes:str="InterfaceSelect CardControlPanel",
                 ) -> None:
        """
        Set 'classes' attribute to the widget.
        id here is just iface name, nothing else.
        """

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.btn_set_unset = Button(
                label="SET",
                classes="InterfaceSelect BtnSetUnset",
                disabled=False,
                )

        yield self.btn_set_unset


class InterfaceCard(Grid):
    """
    Contains single iface short info and button to set/unset.
    """


    def __init__(self,
                 iface_name:str,
                 iface_mac:str|None = None,
                 iface_standart:str|None = None,
                 iface_mode:str|None = None,
                 iface_channel:str|None = None,
                 classes:str="InterfaceSelect InterfaceCard",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        id=f"InterfaceSelect_InterfaceCard_{iface_name}"
        super().__init__(classes=classes, id=id)
        
        self.iface_name = iface_name
        self.iface_mac = iface_mac
        self.iface_standart = iface_standart
        self.iface_mode = iface_mode
        self.iface_channel = iface_channel


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameters_list:ParametersList = ParametersList(
                iface_name=self.iface_name,
                iface_mac=self.iface_mac,
                iface_standart=self.iface_standart,
                )
        self.control_panel:CardControlPanel = CardControlPanel(
                )

        yield self.parameters_list
        yield self.control_panel


class PageInterfaceSelect(ScrollableContainer):
    """
    Contains interface cards with params such as:
        - iface name,
        - iface MAC,
        - iface standart.

    And one button to select one particulat interface.
    """


    def __init__(self,
            id:str="InterfaceSelect_Box",
            classes:str="InterfaceSelect Box",
            ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes, id=id)

        self.border_title = "INTERFACE SELECT"


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.btn_back = Button(
                label="BACK",
                id="InterfaceSelect_BtnBack",
                classes="InterfaceSelect BtnBack",
                )
        self.btn_update_ifaces = Button(
                label="UPDATE",
                id="InterfaceSelect_BtnUpdateIfaces",
                classes="InterfaceSelect BtnUpdateIfaces",
                )

        self.interface_card_1 = InterfaceCard(
                iface_name="wlan0",
                iface_mac="28:1F:35:4D:56:88",
                iface_standart="802.11",
                )
        self.interface_card_2 = InterfaceCard(
                iface_name="wlan1",
                iface_mac="28:1F:35:4D:56:88",
                iface_standart="802.11",
                )
        self.interface_card_3 = InterfaceCard(
                iface_name="wlan2",
                iface_mac="28:1F:35:4D:56:88",
                iface_standart="802.11",
                )
        self.interface_card_4 = InterfaceCard(
                iface_name="wlan3",
                iface_mac="28:1F:35:4D:56:88",
                iface_standart="802.11",
                )
        self.interface_card_5 = InterfaceCard(
                iface_name="wlan4",
                iface_mac="28:1F:35:4D:56:88",
                iface_standart="802.11",
                )
        self.interface_card_6 = InterfaceCard(
                iface_name="wlan5",
                iface_mac="28:1F:35:4D:56:88",
                iface_standart="802.11",
                )

        with Horizontal(
                classes="InterfaceSelect ControlPanel",
                ):
            yield self.btn_back
            yield self.btn_update_ifaces
        yield self.interface_card_1
        yield self.interface_card_2
        yield self.interface_card_3
        yield self.interface_card_4
        yield self.interface_card_5
        yield self.interface_card_6


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")


    async def on_button_pressed(self, event:Button.Pressed) -> None:
        """
        Handle buttons press on this page.
        """

        if event.button.id == "InterfaceSelect_BtnUpdateIfaces":
            #TODO: Update ifaces list
            ...

        else:
            # It's iface set/unset pressed.
            button = event.button
            card_selected:InterfaceCard = button.parent.parent
            iface_main:InterfaceParametersList = \
                    self.app.query_one(
                            "#WidgetInterface_ParametersList")

            # Here user wants to set new card:
            if str(button.label) == "SET":
                if iface_main.iface_params.iface_name is not None:
                    # If we here that means there was some interface
                    # selected before. So before selecting new one,
                    # need to clear (unset) old button.
                    
                    iface_selected_button_old:Button = self.query_one(
                            f".InterfaceSelect.BtnSetUnset.-selected")
                    iface_selected_button_old.label = "SET"
                    iface_selected_button_old.remove_class("-selected")
                
                # Selected card
                button.label = "UNSET"
                button.add_class("-selected")
                # Card set button has iface name as ID, extract it
                iface_name = card_selected.iface_name
                iface_mac = card_selected.iface_mac
                iface_mode = card_selected.iface_mode
                iface_standart = card_selected.iface_standart
                iface_channel = card_selected.iface_channel

                # Set iface card as current:
                iface_main.iface_params = InterfaceParams(
                        iface_name=iface_name,
                        iface_mac=iface_mac,
                        iface_mode=iface_mode,
                        iface_standart=iface_standart,
                        iface_channel=iface_channel,
                        )
                
                self.notify(
                        title="Interface",
                        message=f"You'v set {iface_name}",
                        )

            # Here user wants to unset card:
            elif str(button.label) == "UNSET":
                # Unselected card
                button.label = "SET"
                button.remove_class("-selected")
                # Clear current card selected:
                iface_main.iface_params = InterfaceParams(
                        iface_name=None,
                        iface_mac=None,
                        iface_mode=None,
                        iface_standart=None,
                        iface_channel=None,
                        )

                self.notify(
                        title="Interface",
                        message=f"You'v unset {card_selected.iface_name}",
                        severity="warning",
                        )
