# coding: utf-8

r"""Anchorable object save"""

from os import remove
from os.path import join, dirname, splitext, basename
import json
import zipfile

import FreeCAD as App
from PySide import QtGui

from anchorable_object import is_anchorable_object
from freecad_logging import debug, error, info

if App.GuiUp:
    import FreeCADGui as Gui
else:
    msg_no_ui = "Saving an anchorable object requires the FreeCAD Gui to be up"
    error(msg_no_ui)


def create_stepzip(step_file, anchors_file):
    r"""Procedure to create a zip file from a STEP file and an anchors file

    Parameters
    ----------
    step_file : str
        Path to the STEP file
    anchors_file : str
        Path to the anchors file

    """
    zf = zipfile.ZipFile("%s/%s.stepzip" % (dirname(step_file),
                                            basename(splitext(step_file)[0])),
                         "w",
                         zipfile.ZIP_DEFLATED)
    zf.write(step_file, basename(step_file))
    zf.write(anchors_file, basename(anchors_file))
    zf.close()
    remove(step_file)
    remove(anchors_file)


class CommandAnchorableObjectSave:
    r"""Anchorable object save command

    Command to write an anchorable object to a stepzip format

    """

    def __init__(self):
        pass

    def Activated(self):
        r"""The Save anchorable object Command was activated"""
        # selection = Gui.Selection.getSelection()
        selection_ex = Gui.Selection.getSelectionEx()

        debug("len selection_ex = %i" % len(selection_ex))

        if len(selection_ex) != 1:
            msg = "Anchors : " \
                  "Select only 1 anchorable object to save"
            error(msg)
            return
        else:
            # https://forum.freecadweb.org/viewtopic.php?t=7249
            unique_selection = selection_ex[0]
            selected_object = unique_selection.Object
            debug("  Selection : %s || %s" % (selected_object,
                                              selected_object.Shape.ShapeType))

            #  check is anchorable object
            if is_anchorable_object(selected_object):
                dialog = QtGui.QFileDialog.getSaveFileName(
                    filter="Stepzip files (*.stepzip)")
                #  save shape as step
                stepzip_path = dialog[0]
                stepfile = splitext(stepzip_path)[0] + ".stp"

                # adaptation to json anchors + properties file format
                # anchorsfile = splitext(stepzip_path)[0] + ".anchors"
                anchorsfile = splitext(stepzip_path)[0] + ".json"

                selected_object.Shape.exportStep(stepfile)
                #  save anchors file (+ feature attachment)

                # TODO : save more info about anchor (sub element link)

                # anchors_descs = []
                # for anchor in selected_object.Anchors:
                #     anchors_descs.append("%s %f,%f,%f,%f,%f,%f,%f,%f,%f" %
                #                          (anchor.Label,
                #                           anchor.p[0], anchor.p[1], anchor.p[2],
                #                           anchor.u[0], anchor.u[1], anchor.u[2],
                #                           anchor.v[0], anchor.v[1], anchor.v[2]))
                # with open(anchorsfile, 'w') as f:
                #     f.write("\n".join(anchors_descs))

                # adaptation to json anchors + properties file format
                json_content = {'anchors': {}, 'properties': {}}
                for anchor in selected_object.Anchors:
                    json_content['anchors'][anchor.Label] = {
                        'p': [anchor.p[0], anchor.p[1], anchor.p[2]],
                        'u': [anchor.u[0], anchor.u[1], anchor.u[2]],
                        'v': [anchor.v[0], anchor.v[1], anchor.v[2]]}

                with open(anchorsfile, 'w') as fp:
                    json.dump(json_content, fp, indent=4)

                #  zip it to a stepzip
                create_stepzip(stepfile, anchorsfile)
                info("Anchorable object saved to %s" % dialog[0])
            else:
                error("The object to save should be an anchorable object")

    def GetResources(self):
        r"""Resources for command integration in the UI"""
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_save.png")
        return {"MenuText": "Save anchorable object",
                "Accel": "Ctrl+S",
                "ToolTip": "Save an anchorable object",
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
