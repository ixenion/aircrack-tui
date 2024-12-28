# -------------- #
# System imports #

import asyncio


# ------------------- #
# Third-party imports #

from textual.app        import ComposeResult
from textual.containers import (
        Container, Vertical,
        Horizontal,
        )
from textual.widgets    import (
        Label,
        Button,
        )

# ------------- #
# Local imports #



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
                renderable="None",
                classes="WidgetInterface ParameterValue",
                disabled=True,
                )

        yield self.parameter_label
        yield self.parameter_value


class ParametersList(Vertical):
    """
    Contains two buttons: select - selects interface and
    settings - setup selected interface.
    """

    def __init__(self,
                 classes:str="WidgetInterface ParametersList",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""
        
        self.iface_name     = Parameter(parameter_name="Name:")
        self.iface_mode     = Parameter(parameter_name="Mode:")
        self.iface_channel  = Parameter(parameter_name="Channel:")
        self.iface_mac      = Parameter(parameter_name="MAC:")

        yield self.iface_name
        yield self.iface_mode
        yield self.iface_channel
        yield self.iface_mac


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
                classes="WidgetInterface BtnSelect",
                disabled=False,
                )
        self.btn_settings = Button(
                label="SETTINGS",
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

        with Horizontal(
                classes="WidgetInterface Layout",
                ):
            yield self.parameters_list
            yield self.control_panel


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")
