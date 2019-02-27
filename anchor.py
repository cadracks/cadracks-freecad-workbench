# coding: utf-8

r"""Anchor Python Feature

Is made of a point and 2 unit and orthogonal vectors

"""

from __future__ import division

import math
from os.path import join, dirname

import numpy as np

from freecad_logging import debug
import FreeCAD as App

from pivy import coin

from transformations import superimposition_matrix, translation_from_matrix, \
    rotation_from_matrix
from puv import puv


# def make_anchor_feature(p, u, v):
#     r"""makes an anchorable object feature
#
#     Returns
#     -------
#     the new object.
#
#     """
#     obj = App.ActiveDocument.addObject("Part::FeaturePython",
#                                        "Anchor")
#     Anchor(obj, p, u, v)
#     ViewProviderAnchor(obj.ViewObject)
#     return obj

def anchor_transformation(p0, u0, v0, p1, u1, v1):
    r"""Find the 4x4 transformation matrix
    that superimposes anchor 0 on anchor 1

    Parameters
    ----------
    p0 : tuple
    u0 : tuple
    v0 : tuple
    p1 : tuple
    u1 : tuple
    v1 : tuple

    Returns
    -------
    4x4 matrix (numpy array)

    """
    p0x, p0y, p0z = p0
    u0x, u0y, u0z = u0
    v0x, v0y, v0z = v0

    p1x, p1y, p1z = p1
    u1x, u1y, u1z = u1
    v1x, v1y, v1z = v1

    # compute points to transform
    a0 = np.array(
        [np.array([p0x, p0y, p0z]),
         np.array([p0x + u0x, p0y + u0y, p0z + u0z]),
         np.array([p0x + v0x, p0y + v0y, p0z + v0z])])
    # v1 = np.array(
    #     [anchor_1.p, anchor_1.p - anchor_1.u, anchor_1.p + anchor_1.v])
    a1 = np.array(
        [np.array([p1x, p1y, p1z]),
         np.array([p1x - u1x, p1y - u1y, p1z - u1z]),
         np.array([p1x + v1x, p1y + v1y, p1z + v1z])])

    return superimposition_matrix(a0.T, a1.T, scale=False, usesvd=False)


class Anchor:
    def __init__(self, obj, p, u, v, topo_element):
        obj.addProperty("App::PropertyLink",
                        "parent",
                        "Definition",
                        "Anchor's parent").parent = topo_element[0]

        obj.addProperty("App::PropertyString",
                        "name_sub_element",
                        "Definition",
                        "Anchor's sub element name").name_sub_element = \
            topo_element[1]

        # https://forum.freecadweb.org/viewtopic.php?t=8224
        # -> The property editor doesn't support App::PropertyLinkSub
        #    at the moment. This will come sometime in the future...
        obj.addProperty("App::PropertyLinkSub",
                        "topo_element",
                        "Definition",
                        "Anchor's topo element").topo_element = topo_element

        obj.addProperty("App::PropertyVector",
                        "p",
                        "Definition",
                        "Anchor's origin").p = App.Vector(p[0], p[1], p[2])
        obj.addProperty("App::PropertyVector",
                        "u",
                        "Definition",
                        "Anchor's u vector").u = App.Vector(u[0], u[1], u[2])
        obj.addProperty("App::PropertyVector",
                        "v",
                        "Definition",
                        "Anchor's v vector").v = App.Vector(v[0], v[1], v[2])
        obj.Proxy = self

    def onChanged(self, fp, prop):
        r"""Do something when a property has changed"""
        debug("Change property of Anchor: " + str(prop) + "\n")

    def execute(self, fp):
        r"""Do something when doing a recomputation, this method is mandatory"""
        debug("Recompute Anchor feature\n")

        p, u, v = puv(fp.parent.Shape.getElement(fp.name_sub_element))
        fp.p = App.Vector(p[0], p[1], p[2])
        fp.u = App.Vector(u[0], u[1], u[2])
        fp.v = App.Vector(v[0], v[1], v[2])


class ViewProviderAnchor:
    def __init__(self, vobj):
        r"""Set this object to the proxy object of the actual view provider"""
        vobj.addProperty("App::PropertyColor",
                         "ColorU",
                         "Anchor",
                         "Color of the u vector").ColorU = (1.0, 0.0, 0.0)
        vobj.addProperty("App::PropertyColor",
                         "ColorV",
                         "Anchor",
                         "Color of the v vector").ColorV = (0.5, 0.5, 0.5)

        vobj.Proxy = self

    def attach(self, vobj):
        r"""Setup the scene sub-graph of the view provider,
        this method is mandatory
        
        See Also
        --------
        https://www.freecadweb.org/wiki/Scripted_objects

        """
        debug("AnchorViewProvider/attach")

        self.shaded = coin.SoSeparator()
        self.wireframe = coin.SoSeparator()

        # group u cone and cylinder
        self.group_u = coin.SoSeparator()
        self.color_u = coin.SoBaseColor()

        self.group_cyl_u = coin.SoSeparator()
        self.transform_cyl_u = coin.SoTransform()

        self.group_cone_u = coin.SoSeparator()
        self.transform_cone_u = coin.SoTransform()

        # group v cone and cylinder
        self.group_v = coin.SoSeparator()
        self.transform_v = coin.SoTransform()
        self.color_v = coin.SoBaseColor()

        self.group_cyl_v = coin.SoSeparator()
        self.transform_cyl_v = coin.SoTransform()

        self.group_cone_v = coin.SoSeparator()
        self.transform_cone_v = coin.SoTransform()

        # global
        self.scale = coin.SoScale()
        self.scale.scaleFactor.setValue(1., 1., 1.)
        self.transform = coin.SoTransform()

        # arrow dimensions
        self.arrow_length = 1
        cone_cyl_ratio = 0.2
        cyl_radius_ratio = 0.05
        cone_base_radius_ratio = 0.1

        # The cylinder is created from its middle at the origin
        # -> compensation
        self.transform_cyl_u.translation.setValue(
            (0.,
             self.arrow_length * (1 - cone_cyl_ratio) / 2,
             0.))
        self.transform_cone_u.translation.setValue(
            (0.,
             self.arrow_length * (1 - cone_cyl_ratio) + self.arrow_length * cone_cyl_ratio / 2,
             0.))

        self.transform_cyl_v.translation.setValue(
            (0.,
             self.arrow_length * (1 - cone_cyl_ratio) / 2,
             0.))
        self.transform_cone_v.translation.setValue(
            (0.,
             self.arrow_length * (1 - cone_cyl_ratio) + self.arrow_length * cone_cyl_ratio / 2,
             0.))

        # put v at 90 degrees
        self.transform_v.center.setValue((0, 0, 0))
        self.transform_v.rotation.setValue(coin.SbVec3f((1, 0, 0)), math.pi/2)

        # Cone and cylinder creation from dimensions
        cone_u = coin.SoCone()
        cone_u.height.setValue(self.arrow_length * cone_cyl_ratio)
        cone_u.bottomRadius.setValue(self.arrow_length * cone_base_radius_ratio)

        cylinder_u = coin.SoCylinder()
        cylinder_u.radius.setValue(self.arrow_length * cyl_radius_ratio)
        cylinder_u.height.setValue(self.arrow_length * (1 - cone_cyl_ratio))

        cone_v = coin.SoCone()
        cone_v.height.setValue(self.arrow_length * cone_cyl_ratio)
        cone_v.bottomRadius.setValue(self.arrow_length * cone_base_radius_ratio)

        cylinder_v = coin.SoCylinder()
        cylinder_v.radius.setValue(self.arrow_length * cyl_radius_ratio)
        cylinder_v.height.setValue(self.arrow_length * (1 - cone_cyl_ratio))

        # group_cyl_u
        self.group_cyl_u.addChild(self.transform_cyl_u)
        self.group_cyl_u.addChild(cylinder_u)

        # group_cone_u
        self.group_cone_u.addChild(self.transform_cone_u)
        self.group_cone_u.addChild(cone_u)

        # group_u
        self.group_u.addChild(self.color_u)
        self.group_u.addChild(self.group_cyl_u)
        self.group_u.addChild(self.group_cone_u)

        # group_cyl_v
        self.group_cyl_v.addChild(self.transform_cyl_v)
        self.group_cyl_v.addChild(cylinder_v)

        # group_cone_v
        self.group_cone_v.addChild(self.transform_cone_v)
        self.group_cone_v.addChild(cone_v)

        # group_v
        self.group_v.addChild(self.transform_v)
        self.group_v.addChild(self.color_v)
        self.group_v.addChild(self.group_cyl_v)
        self.group_v.addChild(self.group_cone_v)

        # ** shaded **
        self.shaded.addChild(self.transform)
        self.shaded.addChild(self.scale)
        self.shaded.addChild(self.group_u)
        self.shaded.addChild(self.group_v)
        vobj.addDisplayMode(self.shaded, "Shaded")

        # ** wireframe **
        style = coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.transform)
        self.wireframe.addChild(self.scale)
        self.wireframe.addChild(self.group_u)
        self.wireframe.addChild(self.group_v)
        vobj.addDisplayMode(self.wireframe, "Wireframe")

        self.onChanged(vobj, "ColorU")
        self.onChanged(vobj, "ColorV")

    def updateData(self, feature, prop):
        r"""If a property of the handled feature has changed,
        we have the chance to handle this here
        
        See Also
        --------
        https://www.freecadweb.org/wiki/Scripted_objects

        """
        debug("ViewProviderAnchor/updateData")
        p = feature.getPropertyByName("p")
        u = feature.getPropertyByName("u")
        v = feature.getPropertyByName("v")

        self.transform.translation.setValue((p[0], p[1], p[2]))

        at = anchor_transformation(p0=(0, 0, 0),
                                   u0=(0, -1, 0),
                                   v0=(0, 0, 1),
                                   p1=(p[0], p[1], p[2]),
                                   u1=(u[0], u[1], u[2]),
                                   v1=(v[0], v[1], v[2]))

        t = translation_from_matrix(at)

        self.transform.translation.setValue((t[0], t[1], t[2]))

        angle, direction, point = rotation_from_matrix(at)
        # print("angle : %f" % angle)
        # print("direction : %s" % str(direction))
        # print("point : %s" % str(point))

        self.transform.rotation.setValue(coin.SbVec3f(direction), angle)

        # mat = coin.SoSFMatrix()
        # mat.setValue(at[0][0], at[0][1], at[0][2], at[0][3],
        #              at[1][0], at[1][1], at[1][2], at[1][3],
        #              at[2][0], at[2][1], at[2][2], at[2][3],
        #              at[3][0], at[3][1], at[3][2], at[3][3])
        #
        # self.transform = mat

        # feature is the handled feature,
        # prop is the name of the property that has changed
        # l = feature.getPropertyByName("Length")
        # w = feature.getPropertyByName("Width")
        # h = feature.getPropertyByName("Height")
        # self.scale.scaleFactor.setValue(float(l), float(w), float(h))

    def getDisplayModes(self, obj):
        r"""Return a list of display modes"""
        modes = ["Shaded", "Wireframe"]
        return modes

    def getDefaultDisplayMode(self):
        r"""Return the name of the default display mode.
        It must be defined in getDisplayModes."""
        return "Shaded"

    def setDisplayMode(self, mode):
        r"""Map the display mode defined in attach with those
        defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional
        """
        return mode

    def onChanged(self, vp, prop):
        r"""Here we can do something when a single property got changed"""
        debug("Change property of ViewProvideAnchor: " + str(prop) + "\n")
        if prop == "ColorU":
            cu = vp.getPropertyByName("ColorU")
            self.color_u.rgb.setValue(cu[0], cu[1], cu[2])

        if prop == "ColorV":
            cv = vp.getPropertyByName("ColorV")
            self.color_v.rgb.setValue(cv[0], cv[1], cv[2])

    def getIcon(self):
        r"""Return the icon in XPM format which will appear in the tree view.
        This method is\ optional and if not defined a default icon is shown.
        """
        return join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_anchor.svg")

    def __getstate__(self):
        r"""When saving the document this object gets stored using
        Python's json module.
        Since we have some un-serializable parts here -- the Coin stuff --
        we must define this method to return a tuple of all serializable objects
        or None
        """
        return None

    def __setstate__(self, state):
        r"""When restoring the serialized object from document we have
        the chance to set some internals here.
        Since no data were serialized nothing needs to be done here.
        """
        return None
