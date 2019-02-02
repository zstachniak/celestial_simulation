import pytest
from math import isclose
from gravity.gravity import *
from facts.fact_sheets import schwarzschild_facts, planetary_facts


@pytest.mark.parametrize("mass,expected", [
    (fact_dict["mass"], fact_dict["radius"])
    for fact_dict in schwarzschild_facts.values()
])
def test_calculate_schwarzschild_radius(mass, expected):
    radius = calculate_schwarzschild_radius(mass)
    assert isclose(radius, expected, rel_tol=0.02)


@pytest.mark.parametrize("mass", [
    -1000,
    -1,
    0,
])
def test_value_error_calculate_schwarzschild_radius(mass):
    with pytest.raises(ValueError):
        calculate_schwarzschild_radius(mass)


@pytest.mark.parametrize("mass", [
    "hello",
    "world",
    [1, 2, 3],
])
def test_type_error_calculate_schwarzschild_radius(mass):
    with pytest.raises(TypeError):
        calculate_schwarzschild_radius(mass)


@pytest.mark.parametrize("mass,radius,expected", [
    (fact_dict["mass"], fact_dict["radius"], fact_dict["gravity"])
    for fact_dict in planetary_facts.values()
])
def test_calculate_gravitational_acceleration(mass, radius, expected):
    gravity = calculate_gravitational_acceleration(mass, radius)
    assert isclose(gravity, expected, rel_tol=0.2)


@pytest.mark.parametrize("mass,radius", [
    (-1000, 1000),
    (1000, -1000),
    (0, 1000),
    (1000, 0),
    (-1000, 0),
    (0, -1000),
    (-1000, -1000),
    (0, 0)
])
def test_value_error_calculate_gravitational_acceleration(mass, radius):
    with pytest.raises(ValueError):
        calculate_gravitational_acceleration(mass, radius)


@pytest.mark.parametrize("mass, radius", [
    ("hello", 1000),
    (1000, "world"),
    ("hello", "world"),
    ([1, 2, 3], 1000),
    (1000, [1, 2, 3])
])
def test_type_error_calculate_gravitational_acceleration(mass, radius):
    with pytest.raises(TypeError):
        calculate_gravitational_acceleration(mass, radius)


@pytest.mark.parametrize("mass_one,mass_two,distance,expected", [
    (100, 5.98e+24, 6.38e+03, 980),
    (40, 5.98e+24, 6.38e+03, 392),
    (70, 5.98e+24, 6.60e+03, 641),
    (70, 70, 0.001, 3.27e-07),
    (70, 70, 0.0002, 8.17e-06),
    (70, 1, 0.001, 4.67e-09),
    (70, 7.34e+22, 1.71e+03, 117),
    (70, 1.901e+27, 6.98e+04, 1823)
])
def test_calculate_gravitational_force_between_two_objects(
        mass_one, mass_two, distance, expected):
    """Gravity Examples
    Credit: https://www.physicsclassroom.com/class/circles/Lesson-3
    /Newton-s-Law-of-Universal-Gravitation
    """
    gravity = calculate_gravitational_force_between_two_objects(
        mass_one, mass_two, distance)
    assert isclose(gravity, expected, rel_tol=0.005)


@pytest.mark.parametrize("mass_one,mass_two,distance", [
    (-1000, 1000, 1000),
    (1000, -1000, 1000),
    (1000, 1000, -1000),
    (-1000, -1000, 1000),
    (-1000, -1000, -1000),
    (0, 1000, 1000),
    (1000, 0, 1000),
    (1000, 1000, 0),
    (0, 0, 1000),
    (0, 0, 0),
    (-1000, 0, 1000),
    (0, -1000, 1000),
])
def test_value_error_calculate_gravitational_force_between_two_objects(
        mass_one, mass_two, distance):
    with pytest.raises(ValueError):
        calculate_gravitational_force_between_two_objects(
            mass_one, mass_two, distance)


@pytest.mark.parametrize("mass_one,mass_two,distance", [
    ("hello", 1000, 1000),
    (1000, "world", 1000),
    (1000, 1000, "again"),
    ("hello", "world", "again"),
    ([1, 2, 3], 1000, 1000),
    (1000, [1, 2, 3], 1000),
    (1000, 1000, [1, 2, 3])
])
def test_type_error_calculate_gravitational_force_between_two_objects(
        mass_one, mass_two, distance):
    with pytest.raises(TypeError):
        calculate_gravitational_force_between_two_objects(
            mass_one, mass_two, distance)
