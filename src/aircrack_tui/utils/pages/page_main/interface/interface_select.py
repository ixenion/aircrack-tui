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
from textual.css.query  import NoMatches
from textual.widgets    import (
        Label,
        Button,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.api.models      import (
        InterfaceParams,
        )

from aircrack_tui.utils.datastructures  import (
        shell_cmd,
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
                 classes:str="InterfaceSelect ParametersList",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.iface_name_val     = iface_name
        self.iface_mac_val      = iface_mac


    def compose(self) -> ComposeResult:
        """ Here components are combined."""
        
        self.iface_name     = Parameter(
                parameter_name="Name:",
                parameter_value=self.iface_name_val,
                )
        self.iface_mac      = Parameter(
                parameter_name="MAC:",
                parameter_value=self.iface_mac_val,
                )

        yield self.iface_name
        yield self.iface_mac


class CardControlPanel(Vertical):
    """
    Contains one button: set - select interface and
    the same button to unset that interface.
    """


    def __init__(self,
                 selected:bool=False,
                 classes:str="InterfaceSelect CardControlPanel",
                 ) -> None:
        """
        Set 'classes' attribute to the widget.
        id here is just iface name, nothing else.
        """

        super().__init__(classes=classes)

        self.selected = selected


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.btn_set_unset = Button(
                label="SET",
                classes="InterfaceSelect BtnSetUnset",
                disabled=False,
                )

        yield self.btn_set_unset


    def on_mount(self) -> None:
        """
        """

        if self.selected:
            self.btn_set_unset.label = "UNSET"
            self.btn_set_unset.add_class("-selected")


class InterfaceCard(Grid):
    """
    Contains single iface short info and button to set/unset.
    """


    def __init__(self,
                 iface_name:str,
                 iface_mac:str|None = None,
                 iface_mode:str|None = None,
                 iface_channel:str|None = None,
                 selected:bool=False,
                 classes:str="InterfaceSelect InterfaceCard",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        id=f"InterfaceSelect_InterfaceCard_{iface_name}"
        super().__init__(classes=classes, id=id)
        
        self.iface_name = iface_name
        self.iface_mac = iface_mac
        self.iface_mode = iface_mode
        self.iface_channel = iface_channel
        self.selected = selected


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameters_list:ParametersList = ParametersList(
                iface_name=self.iface_name,
                iface_mac=self.iface_mac,
                )
        self.control_panel:CardControlPanel = CardControlPanel(
                selected=self.selected,
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
        self.interfaces_cards:list[InterfaceCard] = []


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

        with Horizontal(
                classes="InterfaceSelect ControlPanel",
                ):
            yield self.btn_back
            yield self.btn_update_ifaces


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")
        # Send btn press event on mount to gather interfaces ASAP
        self.btn_update_ifaces.press()


    async def on_button_pressed(self, event:Button.Pressed) -> None:
        """
        Handle buttons press on this page.
        """

        if event.button.id == "InterfaceSelect_BtnUpdateIfaces":
            # Set button is loading
            event.button.loading = True
            # Save previously selected interface as main (working)
            try:
                iface_selected_button:Button = self.query_one(
                        f".InterfaceSelect.BtnSetUnset.-selected")
                old_card_iface_name_used:str = \
                        iface_selected_button.parent.parent.iface_name
            except NoMatches as e:
                # That exception means no iface was selected to be saved.
                # It can be on app startup, when updating first time.
                old_card_iface_name_used:None = None
                pass

            # Delete all Interface Cards before updating them:
            for interface_card_old in self.interfaces_cards:
                interface_card_old.remove()
            # Clear list of Current cards
            self.interfaces_cards.clear()

            # Update ifaces list
            success:bool
            response:list[str]
            success, response = await shell_cmd.get_all_sys_ifaces_names()
            if not success:
                self.notify(title="Interface", message="Could not gather sys ifaces. Check logs.", severity="error")
            elif success:
                # If we here that means we have at least one interface
                
                # Sort interfaces in alphabetic order:
                response.sort()

                # Create new interfaces' cards:
                for iface_name in response:
                    iface_mac = await shell_cmd.get_iface_mac(iface_name)
                    iface_channel = await shell_cmd.get_iface_channel(iface_name)
                    iface_mode = await shell_cmd.get_iface_mode(iface_name)
                    # Display InterfaceCards
                    interface_card_widget = InterfaceCard(
                            iface_name=iface_name,
                            iface_mac=iface_mac,
                            iface_mode=iface_mode,
                            iface_channel=iface_channel,
                            selected=iface_name == old_card_iface_name_used,
                            )
                    self.mount(interface_card_widget)
                    self.interfaces_cards.append(interface_card_widget)

            # Unset button is loading
            event.button.loading = False


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
                iface_channel = card_selected.iface_channel

                # Set iface card as current:
                iface_main.iface_params = InterfaceParams(
                        iface_name=iface_name,
                        iface_mac=iface_mac,
                        iface_mode=iface_mode,
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
                        iface_channel=None,
                        )

                self.notify(
                        title="Interface",
                        message=f"You'v unset {card_selected.iface_name}",
                        severity="warning",
                        )
