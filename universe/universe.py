from typing import List, Dict
from orbital_dynamics.orbit import *
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle


class Universe:
    """Defines a container for celestial bodies and their orbits.

    To Do List:
    [ ] str (pretty print)
    [ ] add collision detection against other orbits
    """
    __celestial_bodies: Dict[str, CelestialBody]
    __orbits: List[Orbit]
    __orbital_graph: Dict[CelestialBody, dict]
    __unnamed_id: int

    def __init__(self, name: str = None) -> None:
        """Initializes a Universe, a container for CelestialBodies and their
        Orbits.

        :param str name: the name of the Universe
        :return: None
        """
        if name is None:
            self.name = "Unnamed Universe"
        else:
            self.name = name
        self.__celestial_bodies = {}
        self.__orbits = []
        self.__orbital_graph = {}
        self.__unnamed_id = 1

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def untethered_planets(self) -> Dict[str, CelestialBody]:
        """Returns a dictionary of the untethered CelestialBodies in the
        Universe (i.e., any CelestialBody which does not orbit around
        another body). Ignores the CelestialBody at the root of all orbits.

        :return: dictionary of untethered CelestialBodies
        :rtype: Dict[str, CelestialBody]
        """
        orbiting_bodies = [x.orbiting_body for x in self.__orbits]
        untethered = {k: cb for k, cb in self.__celestial_bodies.items()
                      if cb not in orbiting_bodies
                      and cb not in self.__orbital_graph}
        return untethered

    @property
    def celestial_bodies(self) -> Dict[str, CelestialBody]:
        """Simple getter for the dictionary of the names and CelestialBodies
        that exist in the Universe. Note that the user is barred from
        directly assigning, and should use the add_celestial_body() method
        for assignment.

        :return: dictionary of CelestialBodies in the Universe
        :rtype: Dict[str, CelestialBody]
        """
        return self.__celestial_bodies

    @property
    def orbits(self) -> List[Orbit]:
        """Simple getter for the list of Orbits in the Universe. Note that
        the user is barred from directly assigning, and should use the
        add_orbit() method for assignment.

        :return: list of Orbits in the Universe
        :rtype: List[Orbit]
        """
        return self.__orbits

    def alter_celestial_body_name(
            self, current_name: str, new_name: str) -> None:
        """Alters the name of a celestial body that is already part of a
        Universe class.

        :param str current_name: the current name of the CelestialBody
        :param str new_name: the new, desired name of the Celestial Body
        :return: None
        """
        if current_name not in self.__celestial_bodies:
            raise KeyError(f"No celestial body with the name {current_name} "
                           f"exists in {self.name}")
        if new_name in self.__celestial_bodies:
            raise ValueError(f"A celestial body with the name {new_name} "
                             f"already exist in {self.name}.")
        setattr(self.__celestial_bodies[current_name], "__name", new_name)
        self.__celestial_bodies[new_name] = self.__celestial_bodies.pop(
            current_name)

    def _ensure_celestial_body_exists_in_universe(
            self, celestial_body: CelestialBody) -> None:
        """Raises AttributeError if the CelestialBody has not been added to
        the Universe.

        :param CelestialBody celestial_body: celestial body in question
        :return:None
        :raises: AttributeError
        """
        if celestial_body.name not in self.__celestial_bodies:
            raise AttributeError(f"{celestial_body.name} does not exist in "
                                 f"{self.name}. To add, use the "
                                 f"add_celestial_body() method.")

    def add_celestial_body(self, celestial_body: CelestialBody) -> None:
        """Adds a celestial body to the universe. The name of the celestial
        body must be unique to the universe. If no name is provided, a unique
        ID will be assigned.

        :param CelestialBody celestial_body: the celestial body to add
        :return: None
        """
        if celestial_body.name == "Unnamed Celestial Body":
            setattr(celestial_body, "__name",
                    f"Unnamed Celestial Body {self.__unnamed_id}")
            self.__unnamed_id += 1
        if celestial_body.name in self.__celestial_bodies:
            raise ValueError(f"A celestial body with the name "
                             f"{celestial_body.name} already exist in "
                             f"this universe.")
        self.__celestial_bodies[celestial_body.name] = celestial_body

    def __recursive_orbit_get_name(self, edges, return_list, level):
        """Recursively walks through a nested dictionary of orbits, returning
        the name of each celestial body offset by its relative ranking
        (e.g., moons should be below planets).

        :param edges:
        :param return_list:
        :param level:
        :return:
        """
        for root, edge in edges.items():
            margin = "\t" * level
            return_list.append(f"\n{margin}-{root.name}")
            if len(edge) == 0:
                continue
            else:
                self.__recursive_orbit_get_name(edge, return_list, level + 1)

    def print_celestial_bodies_by_orbit(self) -> None:
        """Prints the acyclic graph representing the orbits in the Universe.

        Example:
            -Black Hole
                -Sun A
                    -Planet A
                        -Moon A
                        -Moon B
                    -Planet B
                    -Planet C
                -Sun B
                    -Planet D
                        -Moon C

        :return: None
        """
        return_list = [f"{self.name}:"]
        if len(self.__orbital_graph) == 0:
            print(f"No orbits detected in {self.name}")
        else:
            for root, edges in self.__orbital_graph.items():
                level = 1
                margin = "\t" * level
                return_list.append(f"\n{margin}-{root.name}")
                self.__recursive_orbit_get_name(
                    edges, return_list, level + 1)
        print("".join(return_list))

    def __recursive_graph_sort(
            self, root: CelestialBody) -> Dict[CelestialBody: dict]:
        """Recursively walks through orbits to return the edges between
        vertices.

        :param CelestialBody root: CelestialBody at the root of the graph
        :return: a dictionary of key: Celestial Body, value: dict
        :rtype: Dict[CelestialBody: dict]
        """
        edges = [x.orbiting_body for x in self.__orbits
                 if x.primary_body == root]
        if len(edges) == 0:
            return {}
        else:
            return {edge: self.__recursive_graph_sort(edge) for edge in edges}

    def _build_acyclic_graph_of_orbits(self) -> None:
        """Builds an acyclic graph of orbits, represented as a nested
        dictionary. If multiple celestial bodies are in orbit, they will be
        presented in order of the nearest celestial body (as measured by
        semi-major axis).

        :return: None
        """
        graph = {}
        self.__orbits = sorted(self.__orbits, key=lambda o: o.semimajor_axis)
        primary_bodies = {x.primary_body for x in self.__orbits}
        if len(primary_bodies) == 0:
            self.__orbital_graph = {}
        orbiting_bodies = {x.orbiting_body for x in self.__orbits}
        roots = primary_bodies - orbiting_bodies
        for root in roots:
            graph[root] = self.__recursive_graph_sort(root)
        self.__orbital_graph = graph

    def add_orbit(self, orbit: Orbit) -> None:
        """Adds an orbit to the universe. Checks are made to ensure that:
            A) both celestial bodies already exist in the universe
            B) the orbiting body has not already been defined as being in
            orbit around a different primary body

        :param Orbit orbit: the orbit to add to the universe
        :return: None
        """
        self._ensure_celestial_body_exists_in_universe(orbit.primary_body)
        self._ensure_celestial_body_exists_in_universe(orbit.orbiting_body)
        try:
            orbit_idx = [x.orbiting_body for x in self.__orbits].index(
                orbit.orbiting_body)
            primary_body = self.__orbits[orbit_idx].primary_body.name
            raise AttributeError(f"{orbit.orbiting_body.name} already orbits "
                                 f"{primary_body}")
        except ValueError:
            # Celestial body is not already in orbit
            self.__orbits.append(orbit)
            self._build_acyclic_graph_of_orbits()

    def plot_orbits(self, primary_body: str,
                    simulate_three_dimensions: float = True):
        """Plots the orbits around a chosen primary body.

        Scaling Notes:
        The size of the celestial bodies will be greatly exaggerated
        relative to their orbits for the purpose of being able to see them.
        Planet sizes are to-scale, but note that there is an absolute
        minimum defined for visibility purposes. Because of the much greater
        size of most primary bodies, this will tend to make all orbiting
        bodies look about the same size.

        In addition, by default the semi-minor axis of every orbit will be
        squashed to simulate a three-dimensional effect.

        The distance from the origin of the primary body to the origin of
        the orbiting bodies is always to scale, with an absolute minimum
        defined so as to be greater than the size of the primary body.

        To Do List:
        [ ] color of sun based on chromaticity
        [ ] temperature of planet indicated on a secondary subplot
        [ ] colors of planets based on a "color" attribute?

        :param str primary_body: the name of the primary body (must be a
        celestial body that has been added to the universe)
        :param bool simulate_three_dimensions: whether or not to simulate a 3D
        effect by squashing the semi-minor axis
        :return: None
        """
        if primary_body not in self.__celestial_bodies:
            raise KeyError(f"{primary_body} is not recognized as the name of "
                           f"a celestial body that has been added to this "
                           f"universe.")
        if simulate_three_dimensions is True:
            three_dim_val = 0.1
        else:
            three_dim_val = 1.0
        background_orbits = []
        foreground_orbits = []
        celestial_bodies = []
        # Gather orbits around primary body
        orbits = [o for o in self.__orbits
                  if o.primary_body == self.__celestial_bodies[primary_body]]
        # Set origin and scaling values
        origin = (0, 0)
        figure_width = 16
        figure_height = 9
        min_orbit = orbits[0].semimajor_axis
        max_orbit = orbits[-1].semimajor_axis
        planet_radii = [o.orbiting_body.radius for o in orbits]
        planet_radii = planet_radii + [orbits[0].primary_body.radius]
        min_radius = min(planet_radii)
        max_radius = max(planet_radii)

        def scale_orbit(value, max_val=figure_width,
                        min_val=figure_width * 0.15):
            scaled = (value - min_orbit) / (max_orbit - min_orbit)
            return scaled * (max_val - min_val) + min_val

        def scale_planet(value, max_val=figure_width * 0.08,
                         min_val=figure_width * 0.005):
            scaled = (value - min_radius) / (max_radius - min_radius)
            return scaled * (max_val - min_val) + min_val

        # Add primary body
        celestial_bodies.append(Circle(
            origin,
            scale_planet(self.__celestial_bodies[primary_body].radius),
            facecolor="yellow",
            edgecolor="black",
            label=primary_body
        ))
        # Add orbiting bodies and their orbital paths
        for orbit in orbits:
            color = "blue"
            name = orbit.orbiting_body.name
            legend_name = f"{name}: p = {orbit.period:0,.0f} days"
            radius = scale_planet(orbit.orbiting_body.radius)
            width = scale_orbit(orbit.semimajor_axis) * 2
            height = scale_orbit(orbit.semiminor_axis) * 2 * \
                three_dim_val
            background_orbits.append(Arc(
                origin,
                width,
                height,
                theta1=0.0,
                theta2=180.0,
                facecolor=color,
                edgecolor="black",
                fill=False,
                label=legend_name
            ))
            foreground_orbits.append(Arc(
                origin,
                width,
                height,
                theta1=180.0,
                theta2=0.0,
                facecolor=color,
                edgecolor="black",
                fill=False,
                label=legend_name
            ))
            celestial_bodies.append(Circle(
                ((width / 2), 0),
                radius,
                facecolor=color,
                edgecolor="black",
                label=legend_name
            ))
        # Plot
        fig, ax = plt.subplots(
            subplot_kw={"aspect": "equal"},
            figsize=(figure_width, figure_height),
            dpi=180
        )
        for arc in background_orbits:
            ax.add_artist(arc)
            arc.set_clip_box(ax.bbox)
        for circle in celestial_bodies:
            ax.add_artist(circle)
            circle.set_clip_box(ax.bbox)
        for arc in foreground_orbits:
            ax.add_artist(arc)
            arc.set_clip_box(ax.bbox)
        ax.set_xlim(-(figure_width + figure_width * 0.1),
                    figure_width + figure_width * 0.1)
        ax.set_ylim(-figure_height, figure_height)
        # Set x_ticks to be scaled
        x_ticks = [-figure_width, -(figure_width / 2), 0.0, figure_width / 2,
                   figure_width]
        ax.set_xticks(x_ticks)
        x_tick_labels = [f"{item * max_orbit:.2E} km" for item in x_ticks]
        ax.set_xticklabels(x_tick_labels)
        # Remove y_axis
        ax.get_yaxis().set_visible(False)
        ax.set_title(f"Orbiting Bodies around {primary_body}")
        plt.tick_params(axis='both', which='major', labelsize=10)
        plt.legend(handles=celestial_bodies, loc=2, prop={'size': 10},
                   title="Orbiting Bodies and Orbital Period")
        plt.show()
