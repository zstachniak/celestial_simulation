import math
from numbers import Real
from typing import Tuple
from facts.numerical_constants import stefan_boltzmann_constant


def calculate_stefan_boltzmann_luminosity(radius: float,
                                          temperature: float) -> float:
    """Returns luminosity of a celestial body by treating it as black body
    radiation (i.e., using the Stefan-Boltzmann law).

    :param float radius: radius of the celestial body in kilometers
    :param float temperature: average temperature of the celestial body's
    surface in Kelvin
    :return: luminosity of the celestial body in Joules / second
    :rtype: float
    """
    if not isinstance(radius, Real):
        raise TypeError(f"radius ({radius}) must be a Real number.")
    if radius <= 0:
        raise ValueError(f"radius ({radius}) must be greater than 0.")
    if not isinstance(temperature, Real):
        raise TypeError(f"temperature ({temperature}) must be a Real number.")
    if temperature <= 0:
        raise ValueError(f"temperature ({temperature}) must be greater than "
                         f"0.")
    return 4 * math.pi * math.pow(radius * 1000, 2) * \
        stefan_boltzmann_constant * math.pow(temperature, 4)


def classify_harvard_spectral_classification(
        solar_temperature: float) -> Tuple[str, str]:
    """Classifies a solar body using the Harvard Spectral Classification
    system, returning both the letter classification and the chromaticity of
    the solar body.

    :param float solar_temperature: the temperature (in Kelvin) of the solar
    body
    :return: the classification and chromaticity of the solar body
    :rtype: Tuple[str, str]
    """
    if not isinstance(solar_temperature, Real):
        raise TypeError(f"solar_temperature ({solar_temperature}) must be a "
                        f"Real number.")
    if solar_temperature >= 30000:
        return "O", "blue"
    elif solar_temperature >= 10000:
        return "B", "deep blue white"
    elif solar_temperature >= 7500:
        return "A", "blue white"
    elif solar_temperature >= 6000:
        return "F", "white"
    elif solar_temperature >= 5200:
        return "G", "yellowish white"
    elif solar_temperature >= 3700:
        return "K", "pale yellow orange"
    elif solar_temperature >= 2400:
        return "M", "light orange red"
    else:
        raise ValueError(f"No classification is defined in the Harvard "
                         f"Spectral Classification for a solar body with "
                         f"temperature < 2400 Kelvin.")
