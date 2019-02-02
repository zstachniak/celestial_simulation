import math
from numbers import Real
from facts.numerical_constants import gravitational_constant, \
    speed_of_light


def calculate_gravitational_force_between_two_objects(
        mass_one: float, mass_two: float, distance: float) -> float:
    """Function calculates the gravitational force between two objects using
    the Law of Gravitation.

    :param float mass_one: mass of the first object in kilograms
    :param float mass_two: mass of the second object in kilograms
    :param float distance: distance between the objects in kilometers
    :return: gravitational force in Newtons
    :rtype: float
    """
    if not isinstance(mass_one, Real):
        raise TypeError(f"mass_one ({mass_one}) must be a Real number.")
    if mass_one <= 0:
        raise ValueError(f"mass_one ({mass_one}) must be greater than 0.")
    if not isinstance(mass_two, Real):
        raise TypeError(f"mass_two ({mass_two}) must be a Real number.")
    if mass_two <= 0:
        raise ValueError(f"mass_two ({mass_two}) must be greater than 0.")
    if not isinstance(distance, Real):
        raise TypeError(f"distance ({distance}) must be a Real number.")
    if distance <= 0:
        raise ValueError(f"distance ({distance}) must be greater than 0.")
    return (gravitational_constant * mass_one * mass_two) \
           / math.pow(distance * 1000, 2)


def calculate_gravitational_acceleration(mass: float, radius: float) -> float:
    """Function calculates the gravitational acceleration of a planet.

    :param float mass: mass of the planet in kilograms
    :param float radius: radius of the planet in kilometers
    :return: gravitational acceleration of the planet in meters / second
    squared
    :rtype: float
    """
    if not isinstance(mass, Real):
        raise TypeError(f"mass ({mass}) must be a Real number.")
    if mass <= 0:
        raise ValueError(f"mass ({mass}) must be greater than 0.")
    if not isinstance(radius, Real):
        raise TypeError(f"radius ({radius}) must be a Real number.")
    if radius <= 0:
        raise ValueError(f"radius ({radius}) must be greater than 0.")
    return (gravitational_constant * mass) / math.pow(radius * 1000, 2)


def calculate_schwarzschild_radius(mass: float) -> float:
    """Returns the Schwarzschild radius (i.e., the radius of a black hole's
    event horizon) in meters.

    :param float mass: mass of object in kilograms
    :return: the Schwarzschild radius (event horizon) of the object in meters
    :rtype: float
    """
    if not isinstance(mass, Real):
        raise TypeError(f"mass ({mass}) must be a Real number.")
    if mass <= 0:
        raise ValueError(f"mass ({mass}) must be greater than 0.")
    return (2 * gravitational_constant * mass) / math.pow(speed_of_light, 2)
