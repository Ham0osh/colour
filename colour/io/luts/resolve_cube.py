"""
Resolve .cube LUT Format Input / Output Utilities
=================================================

Defines the *Resolve* *.cube* *LUT* format related input / output utilities
objects:

-   :func:`colour.io.read_LUT_ResolveCube`
-   :func:`colour.io.write_LUT_ResolveCube`

References
----------
-   :cite:`Chamberlain2015` : Chamberlain, P. (2015). LUT documentation (to
    create from another program). Retrieved August 23, 2018, from
    https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=40284#p232952
"""

from __future__ import annotations

import numpy as np

from colour.hints import Boolean, Integer, List, Tuple, Union
from colour.io.luts import LUT1D, LUT3x1D, LUT3D, LUTSequence
from colour.io.luts.common import path_to_title
from colour.utilities import as_float_array, as_int_scalar, attest, tstack

__author__ = "Colour Developers"
__copyright__ = "Copyright (C) 2013-2022 - Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "read_LUT_ResolveCube",
    "write_LUT_ResolveCube",
]


def read_LUT_ResolveCube(path: str) -> Union[LUT3x1D, LUT3D, LUTSequence]:
    """
    Reads given *Resolve* *.cube* *LUT* file.

    Parameters
    ----------
    path
        *LUT* path.

    Returns
    -------
    :class:`colour.LUT3x1D` or :class:`colour.LUT3D` or \
:class:`colour.LUTSequence`
        :class:`LUT3x1D` or :class:`LUT3D` or :class:`LUTSequence` class
        instance.

    References
    ----------
    :cite:`Chamberlain2015`

    Examples
    --------
    Reading a 3x1D *Resolve* *.cube* *LUT*:

    >>> import os
    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'resolve_cube',
    ...     'ACES_Proxy_10_to_ACES.cube')
    >>> print(read_LUT_ResolveCube(path))
    LUT3x1D - ACES Proxy 10 to ACES
    -------------------------------
    <BLANKLINE>
    Dimensions : 2
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (32, 3)

    Reading a 3D *Resolve* *.cube* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'resolve_cube',
    ...     'Colour_Correct.cube')
    >>> print(read_LUT_ResolveCube(path))
    LUT3D - Generated by Foundry::LUT
    ---------------------------------
    <BLANKLINE>
    Dimensions : 3
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (4, 4, 4, 3)

    Reading a 3D *Resolve* *.cube* *LUT* with comments:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'resolve_cube',
    ...     'Demo.cube')
    >>> print(read_LUT_ResolveCube(path))
    LUT3x1D - Demo
    --------------
    <BLANKLINE>
    Dimensions : 2
    Domain     : [[ 0.  0.  0.]
                  [ 3.  3.  3.]]
    Size       : (3, 3)
    Comment 01 : Comments can't go anywhere

    Reading a 3x1D + 3D *Resolve* *.cube* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'resolve_cube',
    ...     'Three_Dimensional_Table_With_Shaper.cube')
    >>> print(read_LUT_ResolveCube(path))
    LUT Sequence
    ------------
    <BLANKLINE>
    Overview
    <BLANKLINE>
        LUT3x1D --> LUT3D
    <BLANKLINE>
    Operations
    <BLANKLINE>
        LUT3x1D - LUT3D with My Shaper - Shaper
        ---------------------------------------
    <BLANKLINE>
        Dimensions : 2
        Domain     : [[-0.1 -0.1 -0.1]
                      [ 3.   3.   3. ]]
        Size       : (10, 3)
    <BLANKLINE>
        LUT3D - LUT3D with My Shaper - Cube
        -----------------------------------
    <BLANKLINE>
        Dimensions : 3
        Domain     : [[-0.1 -0.1 -0.1]
                      [ 3.   3.   3. ]]
        Size       : (3, 3, 3, 3)
        Comment 01 : A first "Shaper" comment.
        Comment 02 : A second "Shaper" comment.
        Comment 03 : A first "LUT3D" comment.
        Comment 04 : A second "LUT3D" comment.
    """

    title = path_to_title(path)
    domain_3x1D, domain_3D = None, None
    size_3x1D: Integer = 2
    size_3D: Integer = 2
    data = []
    comments = []
    has_3x1D, has_3D = False, False

    with open(path) as cube_file:
        lines = cube_file.readlines()
        for line in lines:
            line = line.strip()

            if len(line) == 0:
                continue

            if line.startswith("#"):
                comments.append(line[1:].strip())
                continue

            tokens = line.split()
            if tokens[0] == "TITLE":
                title = " ".join(tokens[1:])[1:-1]
            elif tokens[0] == "LUT_1D_INPUT_RANGE":
                domain_3x1D = tstack([tokens[1:], tokens[1:], tokens[1:]])
            elif tokens[0] == "LUT_3D_INPUT_RANGE":
                domain_3D = tstack([tokens[1:], tokens[1:], tokens[1:]])
            elif tokens[0] == "LUT_1D_SIZE":
                has_3x1D = True
                size_3x1D = as_int_scalar(tokens[1])
            elif tokens[0] == "LUT_3D_SIZE":
                has_3D = True
                size_3D = as_int_scalar(tokens[1])
            else:
                data.append(tokens)

    table = as_float_array(data)

    LUT: Union[LUT3x1D, LUT3D, LUTSequence]
    if has_3x1D and has_3D:
        table_1D = table[: int(size_3x1D)]
        # The lines of table data shall be in ascending index order,
        # with the first component index (Red) changing most rapidly,
        # and the last component index (Blue) changing least rapidly.
        table_3D = table[int(size_3x1D) :].reshape(
            (size_3D, size_3D, size_3D, 3), order="F"
        )
        LUT = LUTSequence(
            LUT3x1D(
                table_1D,
                f"{title} - Shaper",
                domain_3x1D,
            ),
            LUT3D(
                table_3D,
                f"{title} - Cube",
                domain_3D,
                comments=comments,
            ),
        )
    elif has_3x1D:
        LUT = LUT3x1D(table, title, domain_3x1D, comments=comments)
    elif has_3D:
        # The lines of table data shall be in ascending index order,
        # with the first component index (Red) changing most rapidly,
        # and the last component index (Blue) changing least rapidly.
        table = table.reshape([size_3D, size_3D, size_3D, 3], order="F")
        LUT = LUT3D(table, title, domain_3D, comments=comments)

    return LUT


def write_LUT_ResolveCube(
    LUT: Union[LUT1D, LUT3x1D, LUT3D, LUTSequence],
    path: str,
    decimals: Integer = 7,
) -> Boolean:
    """
    Writes given *LUT* to given  *Resolve* *.cube* *LUT* file.

    Parameters
    ----------
    LUT
        :class:`LUT1D`, :class:`LUT3x1D` or :class:`LUT3D` or
        :class:`LUTSequence` class instance to write at given path.
    path
        *LUT* path.
    decimals
        Formatting decimals.

    Returns
    -------
    :class:`bool`
        Definition success.

    References
    ----------
    :cite:`Chamberlain2015`

    Examples
    --------
    Writing a 3x1D *Resolve* *.cube* *LUT*:

    >>> from colour.algebra import spow
    >>> domain = np.array([[-0.1, -0.1, -0.1], [3.0, 3.0, 3.0]])
    >>> LUT = LUT3x1D(
    ...     spow(LUT3x1D.linear_table(16, domain), 1 / 2.2),
    ...     'My LUT',
    ...     domain,
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT_ResolveCube(LUT, 'My_LUT.cube')  # doctest: +SKIP

    Writing a 3D *Resolve* *.cube* *LUT*:

    >>> domain = np.array([[-0.1, -0.1, -0.1], [3.0, 3.0, 3.0]])
    >>> LUT = LUT3D(
    ...     spow(LUT3D.linear_table(16, domain), 1 / 2.2),
    ...     'My LUT',
    ...     domain,
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT_ResolveCube(LUT, 'My_LUT.cube')  # doctest: +SKIP

    Writing a 3x1D + 3D *Resolve* *.cube* *LUT*:

    >>> from colour.models import RGB_to_HSV, HSV_to_RGB
    >>> from colour.utilities import tstack
    >>> def rotate_hue(a, angle):
    ...    H, S, V = RGB_to_HSV(a)
    ...    H += angle / 360
    ...    H[H > 1] -= 1
    ...    H[H < 0] += 1
    ...    return HSV_to_RGB([H, S, V])
    >>> domain = np.array([[-0.1, -0.1, -0.1], [3.0, 3.0, 3.0]])
    >>> shaper = LUT3x1D(
    ...     spow(LUT3x1D.linear_table(10, domain), 1 / 2.2),
    ...     'My Shaper',
    ...     domain,
    ...     comments=[
    ...         'A first "Shaper" comment.', 'A second "Shaper" comment.'])
    >>> LUT = LUT3D(
    ...     rotate_hue(LUT3D.linear_table(3, domain), 10),
    ...     'LUT3D with My Shaper',
    ...     domain,
    ...     comments=['A first "LUT3D" comment.', 'A second "LUT3D" comment.'])
    >>> LUT_sequence = LUTSequence(shaper, LUT)
    >>> write_LUT_ResolveCube(LUT_sequence, 'My_LUT.cube')  # doctest: +SKIP
    """

    has_3D, has_3x1D = False, False

    if isinstance(LUT, LUTSequence):
        attest(
            len(LUT) == 2
            and isinstance(LUT[0], (LUT1D, LUT3x1D))
            and isinstance(LUT[1], LUT3D),
            "LUTSequence must be 1D + 3D or 3x1D + 3D!",
        )

        if isinstance(LUT[0], LUT1D):
            LUT[0] = LUT[0].as_LUT(LUT3x1D)

        name = f"{LUT[0].name} - {LUT[1].name}"
        has_3x1D = True
        has_3D = True
    elif isinstance(LUT, LUT1D):
        name = LUT.name
        has_3x1D = True
        LUT = LUTSequence(LUT.as_LUT(LUT3x1D), LUT3D())
    elif isinstance(LUT, LUT3x1D):
        name = LUT.name
        has_3x1D = True
        LUT = LUTSequence(LUT, LUT3D())
    elif isinstance(LUT, LUT3D):
        name = LUT.name
        has_3D = True
        LUT = LUTSequence(LUT3x1D(), LUT)
    else:
        raise ValueError("LUT must be 1D, 3x1D, 3D, 1D + 3D or 3x1D + 3D!")

    for i in range(2):
        attest(
            not LUT[i].is_domain_explicit(), '"LUT" domain must be implicit!'
        )

    attest(
        (
            len(np.unique(LUT[0].domain)) == 2
            and len(np.unique(LUT[1].domain)) == 2
        ),
        '"LUT" domain must be 1D!',
    )

    if has_3x1D:
        attest(
            2 <= LUT[0].size <= 65536,
            "Shaper size must be in domain [2, 65536]!",
        )
    if has_3D:
        attest(
            2 <= LUT[1].size <= 256, "Cube size must be in domain [2, 256]!"
        )

    def _format_array(array: Union[List, Tuple]) -> str:
        """
        Formats given array as a *Resolve* *.cube* data row.
        """

        return "{1:0.{0}f} {2:0.{0}f} {3:0.{0}f}".format(decimals, *array)

    def _format_tuple(array: Union[List, Tuple]) -> str:
        """
        Formats given array as 2 space separated values to *decimals*
        precision.
        """

        return "{1:0.{0}f} {2:0.{0}f}".format(decimals, *array)

    with open(path, "w") as cube_file:
        cube_file.write(f'TITLE "{name}"\n')

        if LUT[0].comments:
            for comment in LUT[0].comments:
                cube_file.write(f"# {comment}\n")

        if LUT[1].comments:
            for comment in LUT[1].comments:
                cube_file.write(f"# {comment}\n")

        default_domain = np.array([[0, 0, 0], [1, 1, 1]])

        if has_3x1D:
            cube_file.write(
                "{} {}\n".format("LUT_1D_SIZE", LUT[0].table.shape[0])
            )
            if not np.array_equal(LUT[0].domain, default_domain):
                cube_file.write(
                    "LUT_1D_INPUT_RANGE {}\n".format(
                        _format_tuple(
                            [LUT[0].domain[0][0], LUT[0].domain[1][0]]
                        )
                    )
                )

        if has_3D:
            cube_file.write(
                "{} {}\n".format("LUT_3D_SIZE", LUT[1].table.shape[0])
            )
            if not np.array_equal(LUT[1].domain, default_domain):
                cube_file.write(
                    "LUT_3D_INPUT_RANGE {}\n".format(
                        _format_tuple(
                            [LUT[1].domain[0][0], LUT[1].domain[1][0]]
                        )
                    )
                )

        if has_3x1D:
            table = LUT[0].table
            for row in table:
                cube_file.write(f"{_format_array(row)}\n")
            cube_file.write("\n")

        if has_3D:
            table = LUT[1].table.reshape([-1, 3], order="F")
            for row in table:
                cube_file.write(f"{_format_array(row)}\n")

    return True
