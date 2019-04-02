# coding : utf-8

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

r"""InitGui.py is loaded when FreeCAD runs in GUI mode"""


class AnchorWorkbench(Gui.Workbench):
    """Class that gets initiated at startup of the gui"""
    MenuText = "Anchors"
    ToolTip = "Anchors based assembly"
    user_app_data = App.getUserAppDataDir()
    Icon = user_app_data + \
           "Mod/freecad-workbench-anchors/resources/freecad_workbench_anchors.svg"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        Msg("Anchor workbench initialize\n")

        from command_anchorable_object_open import CommandAnchorableObjectOpen
        from command_anchorable_object_add import CommandAnchorableObjectAdd
        from command_anchor_add import CommandAnchorAdd
        from command_anchorable_object_save import CommandAnchorableObjectSave
        from command_assembly_add import CommandAssemblyAdd

        command_names = ["AnchorableObjectOpen",
                         "AnchorableObjectAdd",
                         "AnchorAdd",
                         "AnchorableObjectSave",
                         "AssemblyAdd"]

        commands = [CommandAnchorableObjectOpen(),
                    CommandAnchorableObjectAdd(),
                    CommandAnchorAdd(),
                    CommandAnchorableObjectSave(),
                    CommandAssemblyAdd()]

        for name, command in zip(command_names, commands):
            FreeCADGui.addCommand(name, command)

        # creates a new toolbar with your commands
        self.appendToolbar("Anchors commands toolbar", command_names)

        # creates a new menu
        self.appendMenu("Anchors", command_names)

        # appends a submenu to an existing menu
        # not useful in the Anchors Workbench context
        # self.appendMenu(["Tools", "My submenu"], commands.keys())

    def Activated(self):
        r"""code which should be computed when a user
        switches to this workbench"""
        Msg("Anchor workbench activated\n")

    def Deactivated(self):
        r"""code which should be computed when this workbench is deactivated"""
        Msg("Anchor workbench activated\n")


Gui.addWorkbench(AnchorWorkbench())
