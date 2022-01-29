"""
References
----------
-   :cite:`AdobeSystems2013b` : Adobe Systems. (2013). Cube LUT Specification.
    https://drive.google.com/open?id=143Eh08ZYncCAMwJ1q4gWxVOqR_OSWYvs
-   :cite:`Chamberlain2015` : Chamberlain, P. (2015). LUT documentation (to
    create from another program). Retrieved August 23, 2018, from
    https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=40284#p232952
-   :cite:`RisingSunResearch` : Rising Sun Research. (n.d.). cineSpace LUT
    Library. Retrieved November 30, 2018, from
    https://sourceforge.net/projects/cinespacelutlib/
"""

from __future__ import annotations

import os

from colour.hints import Any, Boolean, Integer, Literal, Optional, Union, cast
from colour.utilities import (
    CaseInsensitiveMapping,
    filter_kwargs,
    optional,
    validate_method,
)

from .lut import LUT1D, LUT3x1D, LUT3D, LUT_to_LUT
from .operator import AbstractLUTSequenceOperator, LUTOperatorMatrix
from .sequence import LUTSequence
from .iridas_cube import read_LUT_IridasCube, write_LUT_IridasCube
from .resolve_cube import read_LUT_ResolveCube, write_LUT_ResolveCube
from .sony_spi1d import read_LUT_SonySPI1D, write_LUT_SonySPI1D
from .sony_spi3d import read_LUT_SonySPI3D, write_LUT_SonySPI3D
from .sony_spimtx import read_LUT_SonySPImtx, write_LUT_SonySPImtx
from .cinespace_csp import read_LUT_Cinespace, write_LUT_Cinespace

__all__ = [
    "LUT1D",
    "LUT3x1D",
    "LUT3D",
    "LUT_to_LUT",
]
__all__ += [
    "AbstractLUTSequenceOperator",
    "LUTOperatorMatrix",
]
__all__ += [
    "LUTSequence",
]
__all__ += [
    "read_LUT_IridasCube",
    "write_LUT_IridasCube",
]
__all__ += [
    "read_LUT_ResolveCube",
    "write_LUT_ResolveCube",
]
__all__ += [
    "read_LUT_SonySPI1D",
    "write_LUT_SonySPI1D",
]
__all__ += [
    "read_LUT_SonySPI3D",
    "write_LUT_SonySPI3D",
]
__all__ += [
    "read_LUT_SonySPImtx",
    "write_LUT_SonySPImtx",
]
__all__ += [
    "read_LUT_Cinespace",
    "write_LUT_Cinespace",
]

EXTENSION_TO_LUT_FORMAT_MAPPING: CaseInsensitiveMapping = (
    CaseInsensitiveMapping(
        {
            ".cube": "Iridas Cube",
            ".spi1d": "Sony SPI1D",
            ".spi3d": "Sony SPI3D",
            ".spimtx": "Sony SPImtx",
            ".csp": "Cinespace",
        }
    )
)
"""
Extension to *LUT* format.
"""

LUT_READ_METHODS: CaseInsensitiveMapping = CaseInsensitiveMapping(
    {
        "Cinespace": read_LUT_Cinespace,
        "Iridas Cube": read_LUT_IridasCube,
        "Resolve Cube": read_LUT_ResolveCube,
        "Sony SPI1D": read_LUT_SonySPI1D,
        "Sony SPI3D": read_LUT_SonySPI3D,
        "Sony SPImtx": read_LUT_SonySPImtx,
    }
)
LUT_READ_METHODS.__doc__ = """
Supported *LUT* reading methods.

References
----------
:cite:`AdobeSystems2013b`, :cite:`Chamberlain2015`
"""


def read_LUT(
    path: str,
    method: Optional[
        Union[
            Literal[
                "Cinespace",
                "Iridas Cube",
                "Resolve Cube",
                "Sony SPI1D",
                "Sony SPI3D",
                "Sony SPImtx",
            ],
            str,
        ]
    ] = None,
    **kwargs: Any
) -> Union[LUT1D, LUT3x1D, LUT3D, LUTSequence, LUTOperatorMatrix]:
    """
    Reads given *LUT* file using given method.

    Parameters
    ----------
    path
        *LUT* path.
    method
        Reading method, if *None*, the method will be auto-detected according
        to extension.

    Returns
    -------
    :class:`colour.LUT1D` or :class:`colour.LUT3x1D` or :class:`colour.LUT3D` \
or :class:`colour.LUTSequence` or :class:`colour.LUTOperatorMatrix`
        :class:`colour.LUT1D` or :class:`colour.LUT3x1D` or
        :class:`colour.LUT3D` or :class:`colour.LUTSequence` or
        :class:`colour.LUTOperatorMatrix` class instance.

    References
    ----------
    :cite:`AdobeSystems2013b`, :cite:`Chamberlain2015`,
    :cite:`RisingSunResearch`

    Examples
    --------
    Reading a 3x1D *Iridas* *.cube* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'iridas_cube',
    ...     'ACES_Proxy_10_to_ACES.cube')
    >>> print(read_LUT(path))
    LUT3x1D - ACES Proxy 10 to ACES
    -------------------------------
    <BLANKLINE>
    Dimensions : 2
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (32, 3)

    Reading a 1D *Sony* *.spi1d* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spi1d',
    ...     'eotf_sRGB_1D.spi1d')
    >>> print(read_LUT(path))
    LUT1D - eotf sRGB 1D
    --------------------
    <BLANKLINE>
    Dimensions : 1
    Domain     : [-0.1  1.5]
    Size       : (16,)
    Comment 01 : Generated by "Colour 0.3.11".
    Comment 02 : "colour.models.eotf_sRGB".

    Reading a 3D *Sony* *.spi3d* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spi3d',
    ...     'Colour_Correct.spi3d')
    >>> print(read_LUT(path))
    LUT3D - Colour Correct
    ----------------------
    <BLANKLINE>
    Dimensions : 3
    Domain     : [[ 0.  0.  0.]
                  [ 1.  1.  1.]]
    Size       : (4, 4, 4, 3)
    Comment 01 : Adapted from a LUT generated by Foundry::LUT.

    Reading a *Sony* *.spimtx* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spimtx',
    ...     'dt.spimtx')
    >>> print(read_LUT(path))
    LUTOperatorMatrix - dt
    ----------------------
    <BLANKLINE>
    Matrix     : [[ 0.864274  0.        0.        0.      ]
                  [ 0.        0.864274  0.        0.      ]
                  [ 0.        0.        0.864274  0.      ]
                  [ 0.        0.        0.        1.      ]]
    Offset     : [ 0.  0.  0.  0.]
    """

    method = cast(
        str,
        optional(
            method, EXTENSION_TO_LUT_FORMAT_MAPPING[os.path.splitext(path)[-1]]
        ),
    )

    method = validate_method(method, LUT_READ_METHODS)

    function = LUT_READ_METHODS[method]

    try:
        return function(path, **filter_kwargs(function, **kwargs))
    except ValueError as error:
        # Case where a "Resolve Cube" with "LUT3x1D" shaper was read as an
        # "Iridas Cube" "LUT".
        if method == "iridas cube":
            function = LUT_READ_METHODS["Resolve Cube"]
            return function(path, **filter_kwargs(function, **kwargs))
        else:
            raise error


LUT_WRITE_METHODS = CaseInsensitiveMapping(
    {
        "Cinespace": write_LUT_Cinespace,
        "Iridas Cube": write_LUT_IridasCube,
        "Resolve Cube": write_LUT_ResolveCube,
        "Sony SPI1D": write_LUT_SonySPI1D,
        "Sony SPI3D": write_LUT_SonySPI3D,
        "Sony SPImtx": write_LUT_SonySPImtx,
    }
)
LUT_WRITE_METHODS.__doc__ = """
Supported *LUT* reading methods.

References
----------
:cite:`AdobeSystems2013b`, :cite:`Chamberlain2015`
"""


def write_LUT(
    LUT: Union[LUT1D, LUT3x1D, LUT3D, LUTSequence, LUTOperatorMatrix],
    path: str,
    decimals: Integer = 7,
    method: Optional[
        Union[
            Literal[
                "Cinespace",
                "Iridas Cube",
                "Resolve Cube",
                "Sony SPI1D",
                "Sony SPI3D",
                "Sony SPImtx",
            ],
            str,
        ]
    ] = None,
    **kwargs: Any
) -> Boolean:
    """
    Writes given *LUT* to given file using given method.

    Parameters
    ----------
    LUT
        :class:`colour.LUT1D` or :class:`colour.LUT3x1D` or
        :class:`colour.LUT3D` or :class:`colour.LUTSequence` or
        :class:`colour.LUTOperatorMatrix` class instance to write at given
        path.
    path
        *LUT* path.
    decimals
        Formatting decimals.
    method
        Writing method, if *None*, the method will be auto-detected according
        to extension.

    Returns
    -------
    :class:`bool`
        Definition success.

    References
    ----------
    :cite:`AdobeSystems2013b`, :cite:`Chamberlain2015`,
    :cite:`RisingSunResearch`

    Examples
    --------
    Writing a 3x1D *Iridas* *.cube* *LUT*:

    >>> import numpy as np
    >>> from colour.algebra import spow
    >>> domain = np.array([[-0.1, -0.2, -0.4], [1.5, 3.0, 6.0]])
    >>> LUT = LUT3x1D(
    ...     spow(LUT3x1D.linear_table(16, domain), 1 / 2.2),
    ...     'My LUT',
    ...     domain,
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT(LUT, 'My_LUT.cube')  # doctest: +SKIP

    Writing a 1D *Sony* *.spi1d* *LUT*:

    >>> domain = np.array([-0.1, 1.5])
    >>> LUT = LUT1D(
    ...     spow(LUT1D.linear_table(16, domain), 1 / 2.2),
    ...     'My LUT',
    ...     domain,
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT(LUT, 'My_LUT.spi1d')  # doctest: +SKIP

    Writing a 3D *Sony* *.spi3d* *LUT*:

    >>> LUT = LUT3D(
    ...     LUT3D.linear_table(16) ** (1 / 2.2),
    ...     'My LUT',
    ...     np.array([[0, 0, 0], [1, 1, 1]]),
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT(LUT, 'My_LUT.cube')  # doctest: +SKIP
    """

    method = cast(
        str,
        optional(
            method, EXTENSION_TO_LUT_FORMAT_MAPPING[os.path.splitext(path)[-1]]
        ),
    )

    method = validate_method(method, LUT_WRITE_METHODS)

    if method == "iridas cube" and isinstance(LUT, LUTSequence):
        method = "resolve cube"

    function = LUT_WRITE_METHODS[method]

    return function(LUT, path, decimals, **filter_kwargs(function, **kwargs))


__all__ += [
    "LUT_READ_METHODS",
    "read_LUT",
    "LUT_WRITE_METHODS",
    "write_LUT",
]
