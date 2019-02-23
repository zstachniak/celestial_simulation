from orbital_dynamics.orbit import *


class Universe:
    """Defines a container for celestial bodies and their orbits.

    To Do List:
    [ ] repr
    [ ] str (pretty print)
    [ ] add collision detection against other orbits
    [ ] plot orbits (ellipses)
    [ ] function that checks for planetary bodies that aren't orbiting
    anything (untethered planets)
    """
    __celestial_bodies = {}
    __orbits = []
    __orbital_graph = {}
    __unnamed_id = 1

    def __init__(self, name: str = None):
        """docstring"""
        if name is None:
            self.name = "Unnamed Universe"
        else:
            self.name = name

    def _ensure_celestial_body_exists_in_universe(
            self, celestial_body: CelestialBody):
        """

        :param celestial_body:
        :return:
        """
        if celestial_body.name not in self.__celestial_bodies:
            raise AttributeError(f"{celestial_body.name} does not exist in "
                                 f"this universe. To add, use the "
                                 f"add_celestial_body() method.")

    def add_celestial_body(self, celestial_body: CelestialBody):
        """Adds a celestial body to the universe. The name of the celestial
        body must be unique to the universe. If no name is provided, a unique
        ID will be assigned.

        :param CelestialBody celestial_body: the celestial body to add
        :return: None
        """
        if celestial_body.name == "Unnamed Celestial Body":
            celestial_body.name = f"Unnamed Celestial Body " \
                f"{self.__unnamed_id}"
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

    def print_celestial_bodies_by_orbit(self):
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
            return f"No orbits detected in {self.name}"
        else:
            for root, edges in self.__orbital_graph.items():
                level = 1
                margin = "\t" * level
                return_list.append(f"\n{margin}-{root.name}")
                self.__recursive_orbit_get_name(
                    edges, return_list, level + 1)
        print("".join(return_list))

    def __recursive_graph_sort(self, root):
        """Recursively walks through orbits to return the edges between
        vertices.

        :param root:
        :return:
        """
        edges = [x.orbiting_body for x in self.__orbits
                 if x.primary_body == root]
        if len(edges) == 0:
            return {}
        else:
            return {edge: self.__recursive_graph_sort(edge) for edge in edges}

    def _build_acyclic_graph_of_orbits(self):
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

    def add_orbit(self, orbit: Orbit):
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
