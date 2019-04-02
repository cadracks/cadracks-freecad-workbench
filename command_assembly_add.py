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

r"""Assembly Add Command"""

from os.path import join, dirname

import FreeCAD as App

from freecad_logging import info


class CommandAssemblyAdd:
    r"""AssemblyAddCommand

    Command to add an assembly to a Part

    """

    def __init__(self):
        pass

    def Activated(self):
        r""""""
        info("This command will, in the future, add an assembly to a Document")

    def GetResources(self):
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_add_assembly.svg")
        return {"MenuText": "Add assembly",
                "Accel": "Alt+A",
                "ToolTip": "Add an assembly to the document",
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
