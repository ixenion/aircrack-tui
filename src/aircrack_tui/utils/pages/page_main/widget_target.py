# -------------- #
# System imports #

import asyncio


# ------------------- #
# Third-party imports #

from textual.app        import ComposeResult
from textual.containers import (
        Container, Vertical,
        Horizontal, Grid
        )
from textual.widgets    import (
        Label, Sparkline,
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
                 classes:str="WidgetTarget Parameter",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.parameter_name:str = parameter_name


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameter_label = Label(
                renderable=self.parameter_name,
                classes="WidgetTarget ParameterName",
                disabled=True,
                )

        self.parameter_value = Label(
                renderable="None",
                classes="WidgetTarget ParameterValue",
                disabled=True,
                )

        yield self.parameter_label
        yield self.parameter_value


class ParametersList(Grid):
    """
    Contains parameters list.
    """

    def __init__(self,
                 classes:str="WidgetTarget ParametersList",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""
        
        self.target_name    = Parameter(parameter_name="Name:")
        self.target_mac     = Parameter(parameter_name="MAC:")
        self.target_clients = Parameter(parameter_name="Clients:")
        self.target_channel = Parameter(parameter_name="Channel:")

        # with Horizontal(
        #         classes="WidgetTarget NameMac",):
        #     yield self.target_name
        #     yield self.target_channel
        # with Horizontal(
        #         classes="WidgetTarget ClCh",):
        #     yield self.target_mac
        #     yield self.target_clients

        yield self.target_name
        yield self.target_channel

        yield self.target_mac
        yield self.target_clients


class PowerWidget(Horizontal):
    """
    Contais line graph (textual.sparkline) and current number.
    """


    def __init__(self,
                 classes:str="WidgetTarget Power",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        # Dummy data
        data:list[int] = [-70, -70, -65, -68, -80, -60, -50, -55, -60, -70]

        self.power_graph = Sparkline(
                data,  
                summary_function=max,
                classes="WidgetTarget PowerGraph",
                )
        self.power_label = Label(
                renderable="None",
                classes="WidgetTarget PowerLabel",
                )

        yield self.power_graph
        yield self.power_label



class ControlPanel(Grid):
    """
    Contains two buttons: select - select target and
    specs - shows characteristics ot selected target.
    """


    def __init__(self,
                 classes:str="WidgetTarget ControlPanel",
                 ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.btn_select = Button(
                label="SELECT",
                classes="WidgetTarget BtnsControl",
                disabled=False,
                )
        self.btn_specs = Button(
                label="SPECS",
                classes="WidgetTarget BtnsControl",
                disabled=True,
                )

        yield self.btn_select
        yield self.btn_specs
            
    
class WidgetTarget(Vertical):
    """
    Contains params such as:
        - target name,
        - target MAC.
        - target current channel,
        - target current clients active

    Then a graph with label to track RX power.

    And two buttons: select between (different) targets and
    specs - show detailed specs for the target.
    """


    def __init__(self,
            classes:str="WidgetTarget Box",
            ) -> None:
        """ Set 'classes' attribute to the widget."""

        super().__init__(classes=classes)

        self.border_title = "Target"


    def compose(self) -> ComposeResult:
        """ Here components are combined."""

        self.parameters_list:ParametersList = ParametersList()
        self.power_panel:PowerWidget = PowerWidget()
        self.control_panel:ControlPanel = ControlPanel()

        yield self.parameters_list
        yield self.power_panel
        yield self.control_panel


    def on_mount(self) -> None:
        """
        Do staff on widget mount (called once at app startap).
        """

        self.remove_class("-hidden")
