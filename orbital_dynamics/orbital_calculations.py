import math
from numbers import Real
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
    if not isinstance(semimajor_axis, Real):
        raise TypeError(f"semi-major axis ({semimajor_axis}) must be a Real "
                        f"number.")
    if semimajor_axis <= 0:
        raise ValueError(f"semi-major axis {semimajor_axis} must be positive.")
    if not isinstance(eccentricity, Real):
        raise TypeError(f"eccentricity {eccentricity} must be a Real number.")
    if eccentricity < 0 or eccentricity >= 1:
        raise ValueError(f"eccentricity {eccentricity} must be in the range "
                         f"0 <= e < 1")
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
    if not isinstance(semimajor_axis, Real):
        raise TypeError(f"semi-major axis ({semimajor_axis}) must be a Real "
                        f"number.")
    if semimajor_axis <= 0:
        raise ValueError(f"semi-major axis {semimajor_axis} must be positive.")
    if not isinstance(eccentricity, Real):
        raise TypeError(f"eccentricity {eccentricity} must be a Real number.")
    if eccentricity < 0 or eccentricity >= 1:
        raise ValueError(f"eccentricity {eccentricity} must be in the range "
                         f"0 <= e < 1")
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
    if not isinstance(semimajor_axis, Real):
        raise TypeError(f"semi-major axis ({semimajor_axis}) must be a Real "
                        f"number.")
    if semimajor_axis <= 0:
        raise ValueError(f"semi-major axis {semimajor_axis} must be positive.")
    if not isinstance(eccentricity, Real):
        raise TypeError(f"eccentricity {eccentricity} must be a Real number.")
    if eccentricity < 0 or eccentricity >= 1:
        raise ValueError(f"eccentricity {eccentricity} must be in the range "
                         f"0 <= e < 1")
    return semimajor_axis * (1 + eccentricity)


def calculate_orbital_period(
        semimajor_axis: float, primary_body_mass: float,
        orbiting_body_mass: float) -> float:
    """Calculates the orbital period for an elliptical orbit.

    Formula: T^2 = (4pi^2 * a^3) / G(M1 + M2)

    :param float semimajor_axis: the semi-major axis of the ellipse in km
    :param float primary_body_mass: the mass of the primary body in kg
    :param float orbiting_body_mass: the mass of the orbiting body in kg
    :return: the orbital period in days
    :rtype: float
    """
    if not isinstance(semimajor_axis, Real):
        raise TypeError(f"semi-major axis ({semimajor_axis}) must be a Real "
                        f"number.")
    if semimajor_axis <= 0:
        raise ValueError(f"semi-major axis {semimajor_axis} must be positive.")
    if not isinstance(primary_body_mass, Real):
        raise TypeError(f"primary_body_mass {primary_body_mass} must be a "
                        f"Real number.")
    if primary_body_mass <= 0:
        raise ValueError(f"primary_body_mass {primary_body_mass} must be "
                         f"positive.")
    if not isinstance(orbiting_body_mass, Real):
        raise TypeError(f"orbiting_body_mass {orbiting_body_mass} must be a "
                        f"Real number.")
    if orbiting_body_mass <= 0:
        raise ValueError(f"orbiting_body_mass {orbiting_body_mass} must be "
                         f"positive.")
    return math.pow(
        ((4 * math.pow(math.pi, 2))
         / (gravitational_constant * (primary_body_mass + orbiting_body_mass)))
        * math.pow(semimajor_axis * 1000, 3),
        1/2) / (60 * 60 * 24)


def calculate_planetary_surface_temperature(
        semimajor_axis: float, solar_radius: float,
        solar_temperature: float) -> float:
    """Calculates the average surface temperature of an orbiting planet
    based solely on its proximity to its star (i.e., the effects of
    atmosphere are ignored).

    Formula: Tp = (Rs / 2a)^1/2 * Ts

    :param float semimajor_axis: semimajor axis of orbiting planet (i.e.,
    average distance to sun)
    :param float solar_radius: radius of sun
    :param float solar_temperature: average surface temperature (Kelvin) of sun
    :return: average surface temperature (Kelvin) of planet
    :rtype: float
    """
    if not isinstance(semimajor_axis, Real):
        raise TypeError(f"semi-major axis ({semimajor_axis}) must be a Real "
                        f"number.")
    if semimajor_axis <= 0:
        raise ValueError(f"semi-major axis {semimajor_axis} must be positive.")
    if not isinstance(solar_radius, Real):
        raise TypeError(f"solar_radius ({solar_radius}) must be a Real "
                        f"number.")
    if solar_radius <= 0:
        raise ValueError(f"solar_radius {solar_radius} must be positive.")
    if not isinstance(solar_temperature, Real):
        raise TypeError(f"solar_temperature ({solar_temperature}) must be a "
                        f"Real number.")
    if solar_temperature <= 0:
        raise ValueError(f"solar_temperature {solar_temperature} must be "
                         f"positive.")
    return math.pow(
        (solar_radius / (2 * semimajor_axis)), 0.5) * solar_temperature
