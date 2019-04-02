# coding: utf-8

# Copyright 2018-2019 Guillaume Florent

# This file is part of cadracks-freecad-workbench.
#
# cadracks-freecad-workbench is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# cadracks-freecad-workbench is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cadracks-freecad-workbench.  If not, see <https://www.gnu.org/licenses/>.

r"""Anchor Add Command"""

from os.path import join, dirname

import FreeCAD as App

from freecad_logging import info, error, debug
from anchorable_object import make_anchorable_object_feature

if App.GuiUp:
    import FreeCADGui as Gui
else:
    msg = "Adding an anchorable object requires the FreeCAD Gui to be up"
    error(msg)


class CommandAnchorableObjectAdd:
    r"""Command to make an object anchorable
    
    An anchorable object is a container for:
    - a FreeCAD object
    - one or more Anchors

    """

    def __init__(self):
        pass

    def Activated(self):
        r"""The command has been clicked"""

        debug("CommandAnchorableObjectAdd, Activated")

        sel = Gui.Selection.getSelectionEx()
        try:
            if len(sel) != 1:
                raise Exception("Select one shape to make it anchorable")
            try:
                App.ActiveDocument.openTransaction("Anchorable Object")
                obj = make_anchorable_object_feature()
                obj.Base = sel[0].Object
                obj.Base.ViewObject.hide()
                obj.Proxy.execute(obj)
            finally:
                App.ActiveDocument.commitTransaction()
        except Exception as err:
            from PySide import QtGui
            mb = QtGui.QMessageBox()
            mb.setIcon(mb.Icon.Warning)
            mb.setText(err.message)
            mb.setWindowTitle("Anchorable Object")
            mb.exec_()

    def GetResources(self):
        r"""Icon, text and shortcut for CommandAnchorableObjectAdd"""
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_add_anchorable_object.svg")
        return {"MenuText": "Add anchorable object",
                "Accel": "Alt+P",
                "ToolTip": "Make a part anchorable",
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
