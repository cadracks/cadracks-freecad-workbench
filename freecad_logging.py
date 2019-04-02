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

r"""Utilities for the Anchors Workbench"""

from datetime import datetime

import FreeCAD


def _formatted_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def debug(msg):
    r"""Print a debug message"""
    msg = "%s - DEBUG - %s\n" % (_formatted_time(), msg)
    FreeCAD.Console.PrintMessage(msg)


def info(msg):
    r"""Print an info message"""
    msg = "%s - INFO - %s\n" % (_formatted_time(), msg)
    FreeCAD.Console.PrintMessage(msg)


def warning(msg):
    r"""Print a warning message"""
    msg = "%s - WARNING - %s\n" % (_formatted_time(), msg)
    FreeCAD.Console.PrintWarning(msg)


def error(msg):
    r"""Print an error message"""
    msg = "%s - ERROR - %s\n" % (_formatted_time(), msg)
    FreeCAD.Console.PrintError(msg)
