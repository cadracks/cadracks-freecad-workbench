# coding: utf-8

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
