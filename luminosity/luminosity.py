import math
from numbers import Real
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
        raise ValueError(f"temperature ({temperature}) must be greater than 0.")
    return 4 * math.pi * math.pow(radius * 1000, 2) * \
           stefan_boltzmann_constant * math.pow(temperature, 4)
