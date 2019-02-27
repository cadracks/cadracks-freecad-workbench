# coding: utf-8

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
