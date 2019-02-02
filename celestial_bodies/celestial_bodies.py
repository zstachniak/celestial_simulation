import math
from gravity import gravity
from luminosity import luminosity
from utilities import basic_math


class CelestialBody:
    """The standard units of measure used throughout are as follows:
        distance: kilometers
        mass: kilograms
        temperature: Kelvin
        volume: cubic kilometers
        gravitational force: Newtons
        gravitational acceleration: meters / second squared
    """
    default_unit = {
        "distance": "kilometers",
        "mass": "kilograms",
        "density": "kilograms per cubic meter",
        "volume": "cubic kilometers",
        "gravitational_force": "Newtons",
        "gravitational_acceleration": "meters / second squared",
        "luminosity": "Joules / second"
    }

    def __init__(self, mass: float, radius: float):
        """

        :param mass: the mass of the celestial body in kilograms
        :param radius: the radius of the celestial body (assumed to be roughly
        spherical) in meters
        """
        self.mass = mass
        self.radius = radius

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mass}, {self.radius})"

    def __str__(self):
        """To easily subclass, add subclass-specific stats to the
        additional_stats property."""
        return self.basic_stats + self.additional_stats

    @property
    def basic_stats(self) -> str:
        """Returns a string of the basic statistics of the celestial body
        (i.e., statistics that should be shared by all celestial bodies).

        :return: basic statistics of the celestial body
        :rtype: str
        """
        return f"""{self.__class__.__name__}:
    mass: {self.mass} {self.default_unit['mass']}
    radius: {self.radius} {self.default_unit['distance']}
    volume: {self.volume} {self.default_unit['volume']}
    density: {self.density} {self.default_unit['density']}
    gravitational_acceleration: {self.gravitational_acceleration} {
        self.default_unit['gravitational_acceleration']}"""

    @property
    def additional_stats(self) -> str:
        """Returns additional (i.e., subclass-specific) statistics of the
        celestial body.

        :return: subclass-specific statistics of the celestial body
        :rtype: str
        """
        return ""

    @property
    def volume(self):
        """Returns the volume of the celestial body.

        Assumption: the celestial body is roughly spherical. This should
        be a decent approximation for most celestial bodies, even black holes,
        but the method is provided here so as to be easily overridden by a
        subclass.

        Example:
            Earth's Radius: 6,371 kilometers
            Earth's Volume: 1,083,206,916,845.7535 cubic kilometers

        :return: the volume of the celestial body in cubic kilometers
        :rtype: float
        """
        return basic_math.calculate_volume_of_sphere(self.radius)

    @property
    def density(self):
        """Returns the density of the celestial body.

        Note the conversion to meters for more standard measure of density.

        :return: the density of the celestial body in kilograms per cubic
        meter
        :rtype: float
        """
        return basic_math.calculate_density(self.mass, self.volume *
                                            math.pow(1000, 3))

    @property
    def gravitational_acceleration(self):
        """Returns the gravitational acceleration of the celestial body.

        :return: the gravitational acceleration of the celestial body in
        meters / second squared
        :rtype: float
        """
        return gravity.calculate_gravitational_acceleration(
            self.mass, self.radius)


class BlackHole(CelestialBody):
    """subclasses CelestialBody : is a CelestialBody"""

    def __init__(self, mass: float):
        """Only the mass of the black hole is requested as a parameter,
        as the radius will be directly calculated.

        Assumptions:
            - The Schwarzschild radius (event horizon) will be used as an
            approximation of the size of a Black Hole.

        :param float mass: the mass of the black hole in kilograms
        """
        self.mass = mass
        super().__init__(self.mass, self.event_horizon)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mass})"

    @property
    def event_horizon(self) -> float:
        """Returns the Schwarzschild radius (i.e., the radius of a black
        hole's event horizon).

        :return: radius of event horizon of the black hole in kilometers
        :rtype: float
        """
        return gravity.calculate_schwarzschild_radius(self.mass) / 1000


class SolarBody(CelestialBody):
    """subclasses CelestialBody : is a CelestialBody"""

    def __init__(self, mass: float, radius: float, temperature: float):
        """For a solar body, we also require temperature as an initializing
        parameter, as this allows the luminosity to be calculated.

        :param float mass: the mass of the solar body in kilograms
        :param float radius: the radius of the solar body in kilometers
        :param float temperature: the surface temperature of the solar body
        in degrees Kelvin
        """
        self.temperature = temperature
        super().__init__(mass, radius)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mass}, {self.radius}, " \
               f"{self.temperature})"

    @property
    def additional_stats(self) -> str:
        """Returns additional (i.e., subclass-specific) statistics of the
        celestial body.

        :return: subclass-specific statistics of the celestial body
        :rtype: str
        """
        return f"""
    luminosity: {self.luminosity} {self.default_unit['luminosity']}"""

    @property
    def luminosity(self) -> float:
        return luminosity.calculate_stefan_boltzmann_luminosity(
            self.radius, self.temperature)


class PlanetaryBody(CelestialBody):
    """subclasses CelestialBody : is a CelestialBody

    PlanetaryBody allows for calculation of weights of objects on its
    surface, which makes little sense for a SolarBody or a BlackHole.
    """

    def calculate_weight_on_surface(self, mass_of_object: float = 70) -> \
            float:
        """Estimates the weight, in kilograms, of an object on the surface of
        the planetary body. If no mass is provided, default is 70 kg,
        a decent enough approximation of the mass of an average person.

        Assumptions:
            - Gravity is the only force affecting weight.

        :param float mass_of_object: the mass (in kilograms) of the object
        :return: the weight (in kilograms) of the object on the surface of
        the planetary body
        :rtype: float
        """
        weight_in_newtons = \
            gravity.calculate_gravitational_force_between_two_objects(
                self.mass, mass_of_object, self.radius)
        return basic_math.convert_weight_in_newtons_to_kilograms(
            weight_in_newtons, self.gravitational_acceleration)


# Checks
from facts.fact_sheets import planetary_facts, sun_facts
earth = PlanetaryBody(planetary_facts["Earth"]["mass"],
                      planetary_facts["Earth"]["radius"])
earth.calculate_weight_on_surface()
print(earth)
repr(earth)

sag_a = BlackHole(sun_facts["mass"] * 4000000)
print(sag_a)

sol = SolarBody(sun_facts["mass"], sun_facts["radius"],
                sun_facts["mean temperature"])
print(sol)
