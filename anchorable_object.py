# coding: utf-8

r"""Anchorable Object Python Feature

An anchorable object is:
- a FreeCAD object
- one or more Anchors

"""
from os.path import join, dirname

import FreeCAD as App

from freecad_logging import debug, error


def is_anchorable_object(object_):
    if "nchor" in object_.Name \
            or "nchor" in object_.Label \
            or hasattr(object_, "Anchors"):
        return True
    else:
        return False


def make_anchorable_object_feature():
    r"""makes an anchorable object feature

    Returns
    -------
    the new object.

    """
    obj = App.ActiveDocument.addObject("Part::FeaturePython",
                                       "AnchorableObject")

    # no document object found of type Part::DocumentObjectGroupPython
    # obj = App.ActiveDocument.addObject("Part::DocumentObjectGroupPython",
    #                                    "AnchorableObject")

    # type App::Part cannot dynamically add properties
    # obj = App.ActiveDocument.addObject("App::Part",
    #                                    "AnchorableObject")

    AnchorableObject(obj)
    ViewProviderAnchorableObject(obj.ViewObject)
    return obj


class AnchorableObject:
    def __init__(self, obj):
        # obj.addExtension('App::OriginGroupExtensionPython', self)
        obj.addProperty("App::PropertyLink",
                        "Base",
                        "AnchorableObject",
                        "Input")

        obj.addProperty("App::PropertyLinkList",
                        "Anchors",
                        "AnchorableObject",
                        "A link list")

        obj.Proxy = self

    def onChanged(self, feature, prop):
        r"""Do something when a property has changed"""
        debug("Change property: " + str(prop) + "\n")
        if prop in ['Base']:
            self.execute(feature)
            feature.Base.ViewObject.hide()

    def execute(self, feature):
        r"""Do something when doing a recomputation, this method is mandatory"""
        feature.Shape = feature.Base.Shape

        for anchor in feature.Anchors:
            anchor.Proxy.execute(anchor)
        # feature.Label = "Anchorable" + feature.Base.Label


class ViewProviderAnchorableObject:
    def __init__(self, vobj):
        r"""Set this object to the proxy object of the actual view provider"""
        # vobj.addExtension("Gui::ViewProviderGeoFeatureGroupExtensionPython",
        #                   self)
        vobj.Proxy = self

    def attach(self, vobj):
        r"""Setup the scene sub-graph of the view provider,
        this method is mandatory
        """
        self.ViewObject = vobj
        self.Object = vobj.Object
        # self.onChanged(vobj, "Color")

    def getIcon(self):
        r"""Return the icon in XPM format which will appear in the tree view.
        This method is\ optional and if not defined a default icon is shown.
        """
        return join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_add_anchorable_object.svg")

    def claimChildren(self):
        r"""Parametric dependencies display?"""
        children = [self.Object.Base]
        for anchor in self.Object.Anchors:
            children.append(anchor)
        return children

    def onDelete(self, feature, subelements):
        try:
            self.Object.Base.ViewObject.show()
        except Exception as err:
            App.Console.PrintError("Error in onDelete: " + err.message)
        return True

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
