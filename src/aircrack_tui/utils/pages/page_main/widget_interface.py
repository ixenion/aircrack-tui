# -------------- #
# System imports #

import asyncio


# ------------------- #
# Third-party imports #

from textual.app        import ComposeResult
from textual.color import Color
from textual.containers import (
        Container, Vertical,
        Horizontal, Grid,
        )
from textual.reactive           import reactive
from textual.widgets    import (
        Label,
        Button,
        )

# ------------- #
# Local imports #

from aircrack_tui.utils.api.models  import (
        InterfaceParams,
        interface_params_main,
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
                 classes:str="WidgetInterface Parameter",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.parameter_name:str = parameter_name


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameter_label = Label(
                renderable=self.parameter_name,
                classes="WidgetInterface ParameterName",
                disabled=True,
                )

        self.parameter_value = Label(
                renderable="",
                classes="WidgetInterface ParameterValue",
                disabled=True,
                )

        yield self.parameter_label
        yield self.parameter_value


class ParametersList(Vertical):
    """
    Contains All parameters list with corresponding values.
    """

    # Reactive Interface parameters:
    iface_params:reactive[InterfaceParams] = \
            reactive(InterfaceParams(), layout=True)

    
    def __init__(self,
                 id:str="WidgetInterface_ParametersList",
                 classes:str="WidgetInterface ParametersList",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes, id=id)

        self.color_text     = Color(255, 205, 77)
        self.color_success  = Color(78, 191, 113)
        self.color_error    = Color(208, 80, 109)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""
        
        self.iface_name     = Parameter(parameter_name="Name:")
        self.iface_mode     = Parameter(parameter_name="Mode:")
        self.iface_channel  = Parameter(parameter_name="Channel:")
        self.iface_mac      = Parameter(parameter_name="MAC:")

        self.parameters:list[Parameter] = [
                self.iface_name,
                self.iface_mode,
                self.iface_channel,
                self.iface_mac,
                ]

        yield self.iface_name
        yield self.iface_mode
        yield self.iface_channel
        yield self.iface_mac


    def watch_iface_params(self,
            old:InterfaceParams,
            new:InterfaceParams,
            ) -> None:
        """
        Update labels of selected interface.
        """

        iface_name = new.iface_name
        iface_mac = new.iface_mac
        iface_mode = new.iface_mode
        # iface_standart = new.iface_standart
        iface_channel = new.iface_channel

        self.iface_name.parameter_value.update(str(iface_name))
        self.iface_mode.parameter_value.update(str(iface_mode))
        self.iface_channel.parameter_value.update(str(iface_channel))
        self.iface_mac.parameter_value.update(str(iface_mac))
        
        # Update parameter value color: if not None - yellow, else - red.
        for parameter in self.parameters:
            if parameter.parameter_value.renderable == "None":
                parameter.parameter_value.add_class("-is_empty")
            elif parameter.parameter_value.renderable != "None":
                parameter.parameter_value.remove_class("-is_empty")

        # Update global 'interface_params_main' to make shure
        # other widgets could get actual info.
        interface_params_main = new


class ControlPanel(Vertical):
    """
    Contains two buttons: select - select interface and
    settings - setup selected interface.
    """


    def __init__(self,
                 classes:str="WidgetInterface ControlPanel",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.btn_select = Button(
                label="SELECT",
                id="WidgetInterface_BtnSelect",
                classes="WidgetInterface BtnSelect",
                disabled=False,
                )
        self.btn_settings = Button(
                label="SETTINGS",
                id="WidgetInterface_BtnSettings",
                classes="WidgetInterface BtnSettings",
                disabled=True,
                )

        yield self.btn_select
        yield self.btn_settings


class WidgetInterface(Container):
    """
    Contains params such as:
        - iface name,
        - iface current mode (managed, monitor, etc),
        - iface current channel,
        - iface MAC.

    Also two buttons: select (different) interface and settings - setup
    currently selected.
    """


    def __init__(self,
            classes:str="WidgetInterface Box",
            ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.border_title = "Interface"


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameters_list:ParametersList = ParametersList()
        self.control_panel:ControlPanel = ControlPanel()

        with Grid(
                classes="WidgetInterface Layout",
                ):
            yield self.parameters_list
            yield self.control_panel


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")
