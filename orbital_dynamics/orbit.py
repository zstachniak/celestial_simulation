from orbital_dynamics.orbital_calculations import *
from celestial_bodies.celestial_bodies import *


class CollisionError(ValueError):
    """Exception raised when a user-supplied orbital value would lead to a
    near-term collision. For example, if an elliptical orbit were so flat
    that the planet would collide with its sun on the first pass.

    For long-term collisions (i.e., for orbits that would eventually become
    unstable leading to collision), use UnstableOrbit. CollisionError is
    intended for orbits that are essentially impossible.
    """
    pass


class UnstableOrbit(ValueError):
    """Exception raised when a user-supplied orbital value would eventually
    lead to instability and a collision in the far-off future. This is
    separate from a CollisionError in that the user may accept an unstable
    orbit if the anticipated collision is far enough in the future."""
    pass


class Orbit:
    """Defines an orbit of one celestial body around another.

    To Do List:
    [ ] instability detection
    [ ] determine position at time t
    [ ] update orbiting body to contain the basic stats of its own orbit
    (probably best accomplished by storing a pointer to this instance)
    [ ] str (pretty print)
    """

    def __init__(self, primary_body: CelestialBody,
                 orbiting_body: CelestialBody, semimajor_axis: float,
                 eccentricity: float):
        """Initializes an orbit by performing basic calculations and
        checking the orbit for obvious near-term collision.

        :param CelestialBody primary_body: the primary body (e.g., Sun)
        :param CelestialBody orbiting_body: the orbiting body (e.g., Earth)
        :param float semimajor_axis: 1/2 the major axis, which runs through
        the center of the ellipse, passes through a focus, and to the perimeter
        :param float eccentricity: the eccentricity of the orbit (0 <= e < 1)
        """
        self.primary_body = primary_body
        self.orbiting_body = orbiting_body
        if semimajor_axis <= 0:
            raise ValueError(f"semimajor_axis {semimajor_axis} must be > 0.")
        if eccentricity < 0 or eccentricity >= 1:
            raise ValueError(f"Eccentricity {eccentricity} must be "
                             f"between 0 and 1; 0 <= e < 1")
        self.semimajor_axis = semimajor_axis
        self.eccentricity = eccentricity
        self._collison_detection()
        self._update_celestial_bodies()

    @property
    def semiminor_axis(self):
        """Calculates the semi-minor axis of the orbit.

        :return: semi-minor axis of orbit
        :rtype: float
        """
        return calculate_semiminor_axis_of_ellipse(
            self.semimajor_axis, self.eccentricity)

    @property
    def perihelion(self):
        """Calculates the perihelion of the orbit.

        :return: perihelion of orbit
        :rtype: float
        """
        return calculate_perihelion_of_ellipse(
            self.semimajor_axis, self.eccentricity)

    @property
    def aphelion(self):
        """Calculates the aphelion of the orbit.

        :return: aphelion of orbit
        :rtype: float
        """
        return calculate_aphelion_of_ellipse(
            self.semimajor_axis, self.eccentricity)

    @property
    def period(self):
        """Calculates the period of the orbit (in days).

        :return: period of orbit
        :rtype: float
        """
        return calculate_orbital_period(
            self.semimajor_axis, self.primary_body.mass,
            self.orbiting_body.mass)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.primary_body)}, " \
            f"{repr(self.orbiting_body)}, {self.semimajor_axis}, " \
            f"{self.eccentricity})"

    def _update_celestial_bodies(self):
        """Updates the base celestial bodies to include references to their
        primary or orbiting bodies.

        :return: None
        """
        getattr(self.primary_body, "orbiting_bodies").append(
            self.orbiting_body)
        setattr(self.orbiting_body, "primary_body", self.primary_body)

    def _collison_detection(self):
        """Tests for obvious near-term collisions and raises CollisionError
        exception if found.

        Assertions:
            - An orbit cannot be so flat that the orbiting body cannot pass
            by its primary body without running into it.
            - An orbit's perihelion must be at least greater than the
            combined radii of the primary body and orbiting body.

        :return: None
        :raises: CollisionError
        """
        if self.primary_body.radius + self.orbiting_body.radius >= \
                self.semiminor_axis:
            raise CollisionError(f"The semi-minor axis is so small that the "
                                 f"orbiting body could not successfully pass "
                                 f"by its primary body without colliding.")
        if self.primary_body.radius + self.orbiting_body.radius >= \
                self.perihelion:
            raise CollisionError(f"The perihelion is so close that the "
                                 f"orbiting body could not successfully "
                                 f"circle its primary body without colliding.")
