import pytest
from math import isclose
from orbital_dynamics.orbital_calculations import *
from facts.fact_sheets import planetary_facts
from facts.fact_sheets import sun_facts


@pytest.mark.parametrize("semimajor_axis,eccentricity,expectation", [
    (fact_dict["distance from sun"], fact_dict["orbital eccentricity"],
     fact_dict["semi-minor axis"])
    for fact_dict in planetary_facts.values()
    if "distance from sun" in fact_dict.keys()
       and "semi-minor axis" in fact_dict.keys()
])
def test_calculate_semiminor_axis_of_ellipse(semimajor_axis, eccentricity,
                                             expectation):
    semi_minor_axis = calculate_semiminor_axis_of_ellipse(semimajor_axis,
                                                          eccentricity)
    assert isclose(semi_minor_axis, expectation, rel_tol=0.01)


@pytest.mark.parametrize("semimajor_axis,eccentricity", [
    ("hello", 1000),
    (1000, "world"),
    ("hello", "world"),
    ([1, 2, 3], 1000)
])
def test_type_error_calculate_semiminor_axis_of_ellipse(semimajor_axis,
                                                        eccentricity):
    with pytest.raises(TypeError):
        calculate_semiminor_axis_of_ellipse(semimajor_axis, eccentricity)


@pytest.mark.parametrize("semimajor_axis,eccentricity", [
    (0, 1000),
    (-1, 1000),
    (1000, -1),
    (1000, 1),
    (1000, 2),
    (0, 1)
])
def test_value_error_calculate_semiminor_axis_of_ellipse(semimajor_axis,
                                                         eccentricity):
    with pytest.raises(ValueError):
        calculate_semiminor_axis_of_ellipse(semimajor_axis, eccentricity)


@pytest.mark.parametrize("semimajor_axis,eccentricity,expectation", [
    (fact_dict["distance from sun"], fact_dict["orbital eccentricity"],
     fact_dict["perihelion"])
    for fact_dict in planetary_facts.values()
    if "distance from sun" in fact_dict.keys()
])
def test_calculate_perihelion_of_ellipse(semimajor_axis, eccentricity,
                                         expectation):
    perihelion = calculate_perihelion_of_ellipse(semimajor_axis, eccentricity)
    assert isclose(perihelion, expectation, rel_tol=0.01)


@pytest.mark.parametrize("semimajor_axis,eccentricity", [
    ("hello", 1000),
    (1000, "world"),
    ("hello", "world"),
    ([1, 2, 3], 1000)
])
def test_type_error_calculate_perihelion_of_ellipse(semimajor_axis,
                                                    eccentricity):
    with pytest.raises(TypeError):
        calculate_perihelion_of_ellipse(semimajor_axis, eccentricity)


@pytest.mark.parametrize("semimajor_axis,eccentricity", [
    (0, 1000),
    (-1, 1000),
    (1000, -1),
    (1000, 1),
    (1000, 2),
    (0, 1)
])
def test_value_error_calculate_perihelion_of_ellipse(semimajor_axis,
                                                     eccentricity):
    with pytest.raises(ValueError):
        calculate_perihelion_of_ellipse(semimajor_axis, eccentricity)


@pytest.mark.parametrize("semimajor_axis,eccentricity,expectation", [
    (fact_dict["distance from sun"], fact_dict["orbital eccentricity"],
     fact_dict["aphelion"])
    for fact_dict in planetary_facts.values()
    if "distance from sun" in fact_dict.keys()
])
def test_calculate_aphelion_of_ellipse(semimajor_axis, eccentricity,
                                       expectation):
    aphelion = calculate_aphelion_of_ellipse(semimajor_axis, eccentricity)
    assert isclose(aphelion, expectation, rel_tol=0.01)


@pytest.mark.parametrize("semimajor_axis,eccentricity", [
    ("hello", 1000),
    (1000, "world"),
    ("hello", "world"),
    ([1, 2, 3], 1000)
])
def test_type_error_calculate_aphelion_of_ellipse(semimajor_axis,
                                                  eccentricity):
    with pytest.raises(TypeError):
        calculate_aphelion_of_ellipse(semimajor_axis, eccentricity)


@pytest.mark.parametrize("semimajor_axis,eccentricity", [
    (0, 1000),
    (-1, 1000),
    (1000, -1),
    (1000, 1),
    (1000, 2),
    (0, 1)
])
def test_value_error_calculate_aphelion_of_ellipse(semimajor_axis,
                                                   eccentricity):
    with pytest.raises(ValueError):
        calculate_aphelion_of_ellipse(semimajor_axis, eccentricity)


@pytest.mark.parametrize(
    "semimajor_axis,primary_body_mass,orbiting_body_mass,expectation", [
        (fact_dict["distance from sun"], sun_facts["mass"], fact_dict["mass"],
         fact_dict["orbital period"])
        for fact_dict in planetary_facts.values()
        if "distance from sun" in fact_dict.keys()
    ])
def test_calculate_orbital_period(semimajor_axis, primary_body_mass,
                                  orbiting_body_mass, expectation):
    orbital_period = calculate_orbital_period(
        semimajor_axis, primary_body_mass, orbiting_body_mass)
    assert isclose(orbital_period, expectation, rel_tol=0.01)


@pytest.mark.parametrize(
    "semimajor_axis,primary_body_mass,orbiting_body_mass", [
        (0, 1000, 1000),
        (-1, 1000, 1000),
        (1000, 0, 1000),
        (1000, -1, 1000),
        (1000, 1000, 0),
        (1000, 1000, -1),
        (0, 0, 0)
    ])
def test_value_error_calculate_orbital_period(
        semimajor_axis, primary_body_mass, orbiting_body_mass):
    with pytest.raises(ValueError):
        calculate_orbital_period(semimajor_axis, primary_body_mass,
                                 orbiting_body_mass)


@pytest.mark.parametrize(
    "semimajor_axis,primary_body_mass,orbiting_body_mass", [
        ("hello", 1000, 1000),
        (1000, "hello", 1000),
        (1000, 1000, "hello"),
        ([1, 2, 3], 1000, 1000)
    ])
def test_type_error_calculate_orbital_period(
        semimajor_axis, primary_body_mass, orbiting_body_mass):
    with pytest.raises(TypeError):
        calculate_orbital_period(semimajor_axis, primary_body_mass,
                                 orbiting_body_mass)


@pytest.mark.parametrize(
    "semimajor_axis,solar_radius,solar_temperature,expectation", [
        (planetary_facts["Earth"]["distance from sun"], sun_facts["radius"],
         sun_facts["mean temperature"], 279)
    ])
def test_calculate_planetary_surface_temperature(
        semimajor_axis, solar_radius, solar_temperature, expectation):
    planet_temperature = calculate_planetary_surface_temperature(
        semimajor_axis, solar_radius, solar_temperature)
    assert isclose(planet_temperature, expectation, rel_tol=0.01)


@pytest.mark.parametrize("semimajor_axis,solar_radius,solar_temperature", [
    ("hello", 1000, 1000),
    (1000, "world", 1000),
    (1000, 1000, "again"),
    ("hello", "world", "again"),
    ([1, 2, 3], 1000, 1000)
])
def test_type_error_calculate_planetary_surface_temperature(
        semimajor_axis, solar_radius, solar_temperature):
    with pytest.raises(TypeError):
        calculate_planetary_surface_temperature(
            semimajor_axis, solar_radius, solar_temperature)


@pytest.mark.parametrize("semimajor_axis,solar_radius,solar_temperature", [
    (-1, 1000, 1000),
    (1000, -1, 1000),
    (1000, 1000, -1),
    (0, 0, 0)
])
def test_value_error_calculate_planetary_surface_temperature(
        semimajor_axis, solar_radius, solar_temperature):
    with pytest.raises(ValueError):
        calculate_planetary_surface_temperature(
            semimajor_axis, solar_radius, solar_temperature)
