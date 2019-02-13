import math
from facts.numerical_constants import gravitational_constant


def calculate_semiminor_axis_of_ellipse(
        semimajor_axis: float, eccentricity: float) -> float:
    """Calculates the semi-minor axis of an ellipse, given the semi-major
    axis and eccentricity.

    Formula: b^2 = a^2 * (1 - e^2)

    :param float semimajor_axis: the semi-major axis of the ellipse
    :param float eccentricity: the eccentricty of the ellipse
    :return: the semi-minor axis of the ellipse
    :rtype: float
    """
    return math.pow(
        math.pow(semimajor_axis, 2) * (1 - math.pow(eccentricity, 2)), 1/2)


def calculate_perihelion_of_ellipse(
        semimajor_axis: float, eccentricity: float) -> float:
    """Calculates the perihelion of an ellipse.

    Formula: Rp = a(1 - e)

    :param float semimajor_axis: the semi-major axis of the ellipse
    :param float eccentricity: the eccentricty of the ellipse
    :return: the perihelion of the ellipse
    :rtype: float
    """
    return semimajor_axis * (1 - eccentricity)


def calculate_aphelion_of_ellipse(
        semimajor_axis: float, eccentricity: float) -> float:
    """Calculates the aphelion of an ellipse.

    Formula: Ra = a(1 + e)

    :param float semimajor_axis: the semi-major axis of the ellipse
    :param float eccentricity: the eccentricty of the ellipse
    :return: the aphelion of the ellipse
    :rtype: float
    """
    return semimajor_axis * (1 + eccentricity)


def calculate_orbital_period(
        semimajor_axis: float, primary_body_mass: float,
        orbiting_body_mass: float) -> float:
    """Calculates the orbital period for an elliptical orbit.

    Formula: T^2 = (4pi^2 * a^3) / G(M1 + M2)

    :param float semimajor_axis: the semi-major axis of the ellipse
    :param float primary_body_mass: the mass of the primary body
    :param float orbiting_body_mass: the mass of the orbiting body
    :return: the orbital period
    :rtype: float
    """
    return math.pow(
        (4 * math.pow(math.pi, 2) * math.pow(semimajor_axis, 3))
        / (gravitational_constant * (primary_body_mass + orbiting_body_mass)),
        1/2)
