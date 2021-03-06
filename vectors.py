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

r"""Vector math utilities"""

import random

import numpy as np


def perpendicular(a, normalize_=True, randomize_=False):
    r"""Find an arbitrary perpendicular vector
    
    Parameters
    ----------
    a : tuple or list or array
    normalize_ : bool
    randomize_ : bool
    
    Returns
    -------
    numpy array

    """
    if len(a) != 3:
        raise ValueError("Expecting a 3D vector")

    if not isinstance(a, np.ndarray):
        a = np.array(a)

    b = np.ones(3)

    # some components of a might be 0, deal with that
    divisor = np.nonzero(a)[0]

    # There may be more than 1 nonzero value, but we only need 1
    if len(divisor) > 1:
        divisor = [divisor[-1]]

    not_divisor = np.delete([0, 1, 2], [divisor])

    if randomize_ is False:
        b[not_divisor[0]] = 1
        b[not_divisor[1]] = 1
    else:
        b[not_divisor[0]] = random.random()
        b[not_divisor[1]] = random.random()

    b[divisor[0]] = -(a[not_divisor[0]]*b[not_divisor[0]] + a[not_divisor[1]]*b[not_divisor[1]]) / a[divisor[0]]

    assert np.dot(a, b) == 0.

    if normalize_ is True:
        return normalize(b)
    else:
        return b


def normalize(a):
    r"""Normalize a vector"""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    return a/np.linalg.norm(a)


if __name__ == "__main__":
    a = [1, 0, 0]
    print(perpendicular(a))
    print(perpendicular(a, normalize_=False))
    print(perpendicular(a, randomize_=True))
    print(perpendicular(a, randomize_=True))

