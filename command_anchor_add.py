# coding: utf-8

r"""Anchor Add Command"""

from os.path import join, dirname

import FreeCAD as App

from freecad_logging import debug, error
from anchor import Anchor, ViewProviderAnchor
from puv import puv

if App.GuiUp:
    import FreeCADGui as Gui
else:
    msg_no_ui = "Adding an anchorable object requires the FreeCAD Gui to be up"
    error(msg_no_ui)


class CommandAnchorAdd:
    r"""AnchorAddCommand
    
    Command to add an anchor to a Part
    
    """
    def __init__(self):
        pass

    def Activated(self):
        r"""The Add Anchor Command was activated"""
        # selection = Gui.Selection.getSelection()
        selection_ex = Gui.Selection.getSelectionEx()

        debug("len selection_ex = %i" % len(selection_ex))

        if len(selection_ex) != 1:
            msg = "Anchors : " \
                  "Select feature(s) on only 1 solid to add anchors to"
            error(msg)
            return
        else:
            # https://forum.freecadweb.org/viewtopic.php?t=7249
            unique_selection = selection_ex[0]
            selected_object = unique_selection.Object
            debug("  Selection : %s || %s" % (selected_object,
                                              selected_object.Shape.ShapeType))

            subselected_objects = unique_selection.SubObjects

            for i, subselected_object in enumerate(subselected_objects):
                debug("SubSelection : %s || %s" % (subselected_object,
                                                   type(subselected_object)))

                p, u, v = puv(subselected_object)

                # make_anchor_feature(p, u, v)

                print("SubElementName : %s" %
                      unique_selection.SubElementNames[0])

                a = App.ActiveDocument.addObject("App::FeaturePython", "Anchor")
                Anchor(a,
                       p,
                       u,
                       v,
                       topo_element=(unique_selection.Object,
                                     unique_selection.SubElementNames[i]))
                ViewProviderAnchor(a.ViewObject)

                # -- Add the anchor to the App::PropertyLinkList
                #    of the selected AnchorableObject --
                try:
                    l = selected_object.Anchors
                    l.append(a)
                    selected_object.Anchors = l
                except AttributeError:
                    msg = "Are you adding anchors to an AnchorableObject?"
                    error(msg)

                # -- Show the anchors as children
                # selected_object.ViewObject.claimChildren()

    def GetResources(self):
        r"""Resources for command integration in the UI"""
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_add_anchor.svg")
        return {"MenuText": "Add anchor",
                "Accel": "Alt+C",
                "ToolTip": "Add an anchor to a part",
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
