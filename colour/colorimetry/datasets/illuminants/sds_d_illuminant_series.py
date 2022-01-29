"""
CIE Illuminant D Series :math:`S_n(\\lambda)` Distributions
===========================================================

Defines the *CIE Illuminant D Series* :math:`S_n(\\lambda)` distributions
involved in the computation of *CIE Illuminant D Series* spectral
distributions.

References
----------
-   :cite:`Lindbloom2007a` : Lindbloom, B. (2007). Spectral Power Distribution
    of a CIE D-Illuminant. Retrieved April 5, 2014, from
    http://www.brucelindbloom.com/Eqn_DIlluminant.html
-   :cite:`Wyszecki2000z` : Wyszecki, Günther, & Stiles, W. S. (2000). CIE
    Method of Calculating D-Illuminants. In Color Science: Concepts and
    Methods, Quantitative Data and Formulae (pp. 145-146). Wiley.
    ISBN:978-0-471-39918-6
"""

from __future__ import annotations

from functools import partial

from colour.colorimetry import SpectralDistribution
from colour.hints import Dict
from colour.utilities import LazyCaseInsensitiveMapping

__author__ = "Colour Developers"
__copyright__ = "Copyright (C) 2013-2022 - Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DATA_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES",
    "SDS_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES",
]

DATA_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES: Dict = {
    "S0": {
        300: 0.04,
        305: 3.02,
        310: 6.00,
        315: 17.80,
        320: 29.60,
        325: 42.45,
        330: 55.30,
        335: 56.30,
        340: 57.30,
        345: 59.55,
        350: 61.80,
        355: 61.65,
        360: 61.50,
        365: 65.15,
        370: 68.80,
        375: 66.10,
        380: 63.40,
        385: 64.60,
        390: 65.80,
        395: 80.30,
        400: 94.80,
        405: 99.80,
        410: 104.80,
        415: 105.35,
        420: 105.90,
        425: 101.35,
        430: 96.80,
        435: 105.35,
        440: 113.90,
        445: 119.75,
        450: 125.60,
        455: 125.55,
        460: 125.50,
        465: 123.40,
        470: 121.30,
        475: 121.30,
        480: 121.30,
        485: 117.40,
        490: 113.50,
        495: 113.30,
        500: 113.10,
        505: 111.95,
        510: 110.80,
        515: 108.65,
        520: 106.50,
        525: 107.65,
        530: 108.80,
        535: 107.05,
        540: 105.30,
        545: 104.85,
        550: 104.40,
        555: 102.20,
        560: 100.00,
        565: 98.00,
        570: 96.00,
        575: 95.55,
        580: 95.10,
        585: 92.10,
        590: 89.10,
        595: 89.80,
        600: 90.50,
        605: 90.40,
        610: 90.30,
        615: 89.35,
        620: 88.40,
        625: 86.20,
        630: 84.00,
        635: 84.55,
        640: 85.10,
        645: 83.50,
        650: 81.90,
        655: 82.25,
        660: 82.60,
        665: 83.75,
        670: 84.90,
        675: 83.10,
        680: 81.30,
        685: 76.60,
        690: 71.90,
        695: 73.10,
        700: 74.30,
        705: 75.35,
        710: 76.40,
        715: 69.85,
        720: 63.30,
        725: 67.50,
        730: 71.70,
        735: 74.35,
        740: 77.00,
        745: 71.10,
        750: 65.20,
        755: 56.45,
        760: 47.70,
        765: 58.15,
        770: 68.60,
        775: 66.80,
        780: 65.00,
        785: 65.50,
        790: 66.00,
        795: 63.50,
        800: 61.00,
        805: 57.15,
        810: 53.30,
        815: 56.10,
        820: 58.90,
        825: 60.40,
        830: 61.90,
    },
    "S1": {
        300: 0.02,
        305: 2.26,
        310: 4.50,
        315: 13.45,
        320: 22.40,
        325: 32.20,
        330: 42.00,
        335: 41.30,
        340: 40.60,
        345: 41.10,
        350: 41.60,
        355: 39.80,
        360: 38.00,
        365: 40.20,
        370: 42.40,
        375: 40.45,
        380: 38.50,
        385: 36.75,
        390: 35.00,
        395: 39.20,
        400: 43.40,
        405: 44.85,
        410: 46.30,
        415: 45.10,
        420: 43.90,
        425: 40.50,
        430: 37.10,
        435: 36.90,
        440: 36.70,
        445: 36.30,
        450: 35.90,
        455: 34.25,
        460: 32.60,
        465: 30.25,
        470: 27.90,
        475: 26.10,
        480: 24.30,
        485: 22.20,
        490: 20.10,
        495: 18.15,
        500: 16.20,
        505: 14.70,
        510: 13.20,
        515: 10.90,
        520: 8.60,
        525: 7.35,
        530: 6.10,
        535: 5.15,
        540: 4.20,
        545: 3.05,
        550: 1.90,
        555: 0.95,
        560: 0.00,
        565: -0.80,
        570: -1.60,
        575: -2.55,
        580: -3.50,
        585: -3.50,
        590: -3.50,
        595: -4.65,
        600: -5.80,
        605: -6.50,
        610: -7.20,
        615: -7.90,
        620: -8.60,
        625: -9.05,
        630: -9.50,
        635: -10.20,
        640: -10.90,
        645: -10.80,
        650: -10.70,
        655: -11.35,
        660: -12.00,
        665: -13.00,
        670: -14.00,
        675: -13.80,
        680: -13.60,
        685: -12.80,
        690: -12.00,
        695: -12.65,
        700: -13.30,
        705: -13.10,
        710: -12.90,
        715: -11.75,
        720: -10.60,
        725: -11.10,
        730: -11.60,
        735: -11.90,
        740: -12.20,
        745: -11.20,
        750: -10.20,
        755: -9.00,
        760: -7.80,
        765: -9.50,
        770: -11.20,
        775: -10.80,
        780: -10.40,
        785: -10.50,
        790: -10.60,
        795: -10.15,
        800: -9.70,
        805: -9.00,
        810: -8.30,
        815: -8.80,
        820: -9.30,
        825: -9.55,
        830: -9.80,
    },
    "S2": {
        300: 0.00,
        305: 1.00,
        310: 2.00,
        315: 3.00,
        320: 4.00,
        325: 6.25,
        330: 8.50,
        335: 8.15,
        340: 7.80,
        345: 7.25,
        350: 6.70,
        355: 6.00,
        360: 5.30,
        365: 5.70,
        370: 6.10,
        375: 4.55,
        380: 3.00,
        385: 2.10,
        390: 1.20,
        395: 0.05,
        400: -1.10,
        405: -0.80,
        410: -0.50,
        415: -0.60,
        420: -0.70,
        425: -0.95,
        430: -1.20,
        435: -1.90,
        440: -2.60,
        445: -2.75,
        450: -2.90,
        455: -2.85,
        460: -2.80,
        465: -2.70,
        470: -2.60,
        475: -2.60,
        480: -2.60,
        485: -2.20,
        490: -1.80,
        495: -1.65,
        500: -1.50,
        505: -1.40,
        510: -1.30,
        515: -1.25,
        520: -1.20,
        525: -1.10,
        530: -1.00,
        535: -0.75,
        540: -0.50,
        545: -0.40,
        550: -0.30,
        555: -0.15,
        560: 0.00,
        565: 0.10,
        570: 0.20,
        575: 0.35,
        580: 0.50,
        585: 1.30,
        590: 2.10,
        595: 2.65,
        600: 3.20,
        605: 3.65,
        610: 4.10,
        615: 4.40,
        620: 4.70,
        625: 4.90,
        630: 5.10,
        635: 5.90,
        640: 6.70,
        645: 7.00,
        650: 7.30,
        655: 7.95,
        660: 8.60,
        665: 9.20,
        670: 9.80,
        675: 10.00,
        680: 10.20,
        685: 9.25,
        690: 8.30,
        695: 8.95,
        700: 9.60,
        705: 9.05,
        710: 8.50,
        715: 7.75,
        720: 7.00,
        725: 7.30,
        730: 7.60,
        735: 7.80,
        740: 8.00,
        745: 7.35,
        750: 6.70,
        755: 5.95,
        760: 5.20,
        765: 6.30,
        770: 7.40,
        775: 7.10,
        780: 6.80,
        785: 6.90,
        790: 7.00,
        795: 6.70,
        800: 6.40,
        805: 5.95,
        810: 5.50,
        815: 5.80,
        820: 6.10,
        825: 6.30,
        830: 6.50,
    },
}

SDS_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES: (
    LazyCaseInsensitiveMapping
) = LazyCaseInsensitiveMapping(
    {
        "S0": partial(
            SpectralDistribution,
            DATA_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES["S0"],
            name="S0",
        ),
        "S1": partial(
            SpectralDistribution,
            DATA_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES["S1"],
            name="S1",
        ),
        "S2": partial(
            SpectralDistribution,
            DATA_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES["S2"],
            name="S2",
        ),
    }
)
SDS_BASIS_FUNCTIONS_CIE_ILLUMINANT_D_SERIES.__doc__ = """
*CIE Illuminant D Series* :math:`S_n(\\lambda)` spectral distributions.

References
----------
:cite:`Lindbloom2007a`, :cite:`Wyszecki2000z`
"""
