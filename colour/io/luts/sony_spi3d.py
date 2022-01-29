"""
Sony .spi3d LUT Format Input / Output Utilities
===============================================

Defines the *Sony* *.spi3d* *LUT* format related input / output utilities
objects:

-   :func:`colour.io.read_LUT_SonySPI3D`
-   :func:`colour.io.write_LUT_SonySPI3D`
"""

from __future__ import annotations

import numpy as np

from colour.io.luts import LUT3D, LUTSequence
from colour.io.luts.common import path_to_title
from colour.hints import Boolean, Integer, List, Tuple, Union
from colour.utilities import (
    as_float_array,
    as_int_array,
    as_int_scalar,
    attest,
    usage_warning,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright (C) 2013-2022 - Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "read_LUT_SonySPI3D",
    "write_LUT_SonySPI3D",
]


def read_LUT_SonySPI3D(path: str) -> LUT3D:
    """
    Reads given *Sony* *.spi3d* *LUT* file.

    Parameters
    ----------
    path
        *LUT* path.

    Returns
    -------
    :class:`colour.LUT3D`
        :class:`LUT3D` class instance.

    Examples
    --------
    Reading an ordered and an unordered 3D *Sony* *.spi3d* *LUT*:

    >>> import os
    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spi3d',
    ...     'Colour_Correct.spi3d')
    >>> print(read_LUT_SonySPI3D(path))
    LUT3D - Colour Correct
    ----------------------
    <BLANKLINE>
    Dimensions : 3
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (4, 4, 4, 3)
    Comment 01 : Adapted from a LUT generated by Foundry::LUT.
    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spi3d',
    ...     'Colour_Correct_Unordered.spi3d')
    >>> print(read_LUT_SonySPI3D(path))
    LUT3D - Colour Correct Unordered
    --------------------------------
    <BLANKLINE>
    Dimensions : 3
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (4, 4, 4, 3)
    Comment 01 : Adapted from a LUT generated by Foundry::LUT.
    """

    title = path_to_title(path)
    domain_min, domain_max = np.array([0, 0, 0]), np.array([1, 1, 1])
    size: Integer = 2
    data_table = []
    data_indexes = []
    comments = []

    with open(path) as spi3d_file:
        lines = filter(None, (line.strip() for line in spi3d_file.readlines()))
        for line in lines:
            if line.startswith("#"):
                comments.append(line[1:].strip())
                continue

            tokens = line.split()
            if len(tokens) == 3:
                attest(
                    len(set(tokens)) == 1,
                    'Non-uniform "LUT" shape is unsupported!',
                )

                size = as_int_scalar(tokens[0])
            if len(tokens) == 6:
                data_table.append(as_float_array(tokens[3:]))
                data_indexes.append(as_int_array(tokens[:3]))

    indexes = as_int_array(data_indexes)
    sorting_indexes = np.lexsort((indexes[:, 2], indexes[:, 1], indexes[:, 0]))

    attest(
        np.array_equal(
            indexes[sorting_indexes],
            as_int_array(
                np.around(LUT3D.linear_table(size) * (size - 1))
            ).reshape((-1, 3)),
        ),
        'Indexes do not match expected "LUT3D" indexes!',
    )

    table = as_float_array(data_table)[sorting_indexes].reshape(
        [size, size, size, 3]
    )

    return LUT3D(
        table, title, np.vstack([domain_min, domain_max]), comments=comments
    )


def write_LUT_SonySPI3D(
    LUT: Union[LUT3D, LUTSequence], path: str, decimals: Integer = 7
) -> Boolean:
    """
    Writes given *LUT* to given *Sony* *.spi3d* *LUT* file.

    Parameters
    ----------
    LUT
        :class:`LUT3D` or :class:`LUTSequence` class instance to write at given
        path.
    path
        *LUT* path.
    decimals
        Formatting decimals.

    Returns
    -------
    :class:`bool`
        Definition success.

    Warnings
    --------
    -   If a :class:`LUTSequence` class instance is passed as ``LUT``, the
        first *LUT* in the *LUT* sequence will be used.

    Examples
    --------
    Writing a 3D *Sony* *.spi3d* *LUT*:

    >>> LUT = LUT3D(
    ...     LUT3D.linear_table(16) ** (1 / 2.2),
    ...     'My LUT',
    ...     np.array([[0, 0, 0], [1, 1, 1]]),
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT_SonySPI3D(LUT, 'My_LUT.cube')  # doctest: +SKIP
    """

    if isinstance(LUT, LUTSequence):
        usage_warning(
            '"LUT" is a "LUTSequence" instance was passed, '
            'using first sequence "LUT":\n'
            "{}".format(LUT)
        )
        LUTxD = LUT[0]
    else:
        LUTxD = LUT

    attest(not LUTxD.is_domain_explicit(), '"LUT" domain must be implicit!')

    attest(isinstance(LUTxD, LUT3D), '"LUT" must be either a 3D "LUT"!')

    attest(
        np.array_equal(
            LUTxD.domain,
            np.array(
                [
                    [0, 0, 0],
                    [1, 1, 1],
                ]
            ),
        ),
        '"LUT" domain must be [[0, 0, 0], [1, 1, 1]]!',
    )

    def _format_array(array: Union[List, Tuple]) -> str:
        """
        Formats given array as a *Sony* *.spi3d* data row.
        """

        return "{1:d} {2:d} {3:d} {4:0.{0}f} {5:0.{0}f} {6:0.{0}f}".format(
            decimals, *array
        )

    with open(path, "w") as spi3d_file:
        spi3d_file.write("SPILUT 1.0\n")

        spi3d_file.write("3 3\n")

        spi3d_file.write("{0} {0} {0}\n".format(LUTxD.size))

        indexes = as_int_array(
            np.around(LUTxD.linear_table(LUTxD.size) * (LUTxD.size - 1))
        ).reshape([-1, 3])
        table = LUTxD.table.reshape([-1, 3])

        for i, row in enumerate(indexes):
            spi3d_file.write(f"{_format_array(list(row) + list(table[i]))}\n")

        if LUTxD.comments:
            for comment in LUTxD.comments:
                spi3d_file.write(f"# {comment}\n")

    return True
