import math
from numbers import Real


def calculate_density(mass: float, volume: float) -> float:
    """Function calculates density as mass / volume.

    :param float mass: the mass of the object
    :param float volume: the volume of the object
    :return: the density of the object
    :rtype: float
    """
    if not isinstance(mass, Real):
        raise TypeError(f"mass ({mass}) must be a Real number.")
    if mass <= 0:
        raise ValueError(f"mass ({mass}) must be greater than 0.")
    if not isinstance(volume, Real):
        raise TypeError(f"volume ({volume}) must be a Real number.")
    if volume <= 0:
        raise ValueError(f"volume ({volume}) must be greater than 0.")
    return mass / volume


def calculate_volume_of_sphere(radius: float) -> float:
    """Function calculates the volume of a spherical object.

    :param float radius: the radius of the spherical object
    :return: the volume of the spherical object
    :rtype: float
    """
    if not isinstance(radius, Real):
        raise TypeError(f"radius ({radius}) must be a Real number.")
    if radius <= 0:
        raise ValueError(f"radius ({radius}) must be greater than 0.")
    return math.pow(radius, 3) * math.pi * (4/3)


def convert_weight_in_newtons_to_kilograms(
        weight_in_newtons: float, gravitational_acceleration: float) -> float:
    """Function converts weight in Newtons to kilograms.

    :param float weight_in_newtons: weight of object in Newtons
    :param float gravitational_acceleration: gravity on planetary body
    :return: weight of object in kilograms
    :rtype: float
    """
    if not isinstance(weight_in_newtons, Real):
        raise TypeError(f"weight_in_newtons ({weight_in_newtons}) must be a "
                        f"Real number.")
    if weight_in_newtons <= 0:
        raise ValueError(f"weight_in_newtons ({weight_in_newtons}) must be "
                         f"greater than 0.")
    if not isinstance(gravitational_acceleration, Real):
        raise TypeError(f"gravitational_acceleration "
                        f"({gravitational_acceleration}) must be a Real "
                        f"number.")
    if gravitational_acceleration <= 0:
        raise ValueError(f"gravitational_acceleration "
                         f"({gravitational_acceleration}) must be greater "
                         f"than 0.")
    return weight_in_newtons / gravitational_acceleration
