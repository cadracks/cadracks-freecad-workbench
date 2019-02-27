# coding: utf-8

r"""Anchorable object open Command"""

from os.path import join, dirname

import FreeCAD as App
from PySide import QtGui

from freecad_logging import debug, error

if App.GuiUp:
    import FreeCADGui as Gui
else:
    msg_no_ui = "Opening an anchorable object requires the FreeCAD Gui to be up"
    error(msg_no_ui)


class CommandAnchorableObjectOpen:
    r"""Anchorable object open command

    Command to open an anchorable object from a stepzip format

    """

    def __init__(self):
        pass

    def Activated(self):
        r"""The Open anchorable object Command was activated"""
        dialog = QtGui.QFileDialog.getOpenFileName(
            filter="Stepzip files (*.stepzip)")
        # todo : open logic
        #   unzip
        #   open the step
        #   make it an anchorable object
        #   add the anchors to the anchorable object
        debug("Will open %s" % str(dialog))

    def GetResources(self):
        r"""Resources for command integration in the UI"""
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_open.png")
        return {"MenuText": "Open anchorable object",
                "Accel": "Ctrl+O",
                "ToolTip": "Open an anchorable object",
                "Pixmap": icon}

    def IsActive(self):
        r"""Determines if the command is active or inactive (greyed out)

        This method is called periodically, avoid calling other methods
        that print to the console

        """
        if App.ActiveDocument is None:
            return False
        else:
            return True