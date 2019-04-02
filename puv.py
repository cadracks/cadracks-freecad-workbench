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

r"""Determination of p, u, v components of anchors from part geometry"""

import Part

from freecad_logging import debug
from vectors import perpendicular


def puv_from_face(face):
    u00, u10, v00, v10 = face.ParameterRange
    u05 = (u00 + u10) / 2
    v05 = (v00 + v10) / 2
    p = face.valueAt(u05, v05)
    u = face.normalAt(u05, v05)

    v = perpendicular(u, normalize_=True, randomize_=False)

    return p, u, v


def puv_from_circular_edge(edge):
    face_virtual = \
        Part.Face(Part.Wire(edge))
    return puv_from_face(face_virtual)


def puv_from_linear_edge(edge):
    raise NotImplementedError


def puv_from_edge(edge):
    raise NotImplementedError


def puv_from_wire(wire):
    raise NotImplementedError


def puv_from_vertex(vertex):
    raise NotImplementedError


def puv(subselected_object):
    # if isinstance(subselected_object, Part.Solid):
    #     debug("It is a Solid")
    # elif isinstance(subselected_object, Part.Shell):
    #     debug("It is a Shell")
    if isinstance(subselected_object, Part.Face):
        debug("It is a Face")
        face = subselected_object
        p, u, v = puv_from_face(face)

    elif isinstance(subselected_object, Part.Wire):
        debug("It is a Wire")
    elif isinstance(subselected_object, Part.Edge):
        debug("It is an Edge")
        debug('TYPE : %s' % type(subselected_object.Curve))

        if str(type(subselected_object.Curve)) == "<type 'Part.Circle'>":
            debug("it is a circle")
            edge = subselected_object
            p, u, v = puv_from_circular_edge(edge)
        elif str(type(
                subselected_object.Curve)) == "<type 'Part.Line'>":
            debug("it is a line")
        else:
            # known other possibilities
            # -  <type 'Part.BSplineCurve'>
            debug("it is NOT a circle and NOR a line")
    elif isinstance(subselected_object, Part.Vertex):
        debug("It is a Vertex")
    else:
        debug("What is that?")

    return p, u, v


