import pytest
from math import isclose
from luminosity.luminosity import *
from facts.fact_sheets import sun_facts


@pytest.mark.parametrize("radius,temperature,expected", [
    (sun_facts["radius"], sun_facts["mean temperature"],
     sun_facts["luminosity"])
])
def test_calculate_stefan_boltzmann_luminosity(radius, temperature, expected):
    luminosity = calculate_stefan_boltzmann_luminosity(radius, temperature)
    assert isclose(luminosity, expected, rel_tol=0.005)


@pytest.mark.parametrize("radius,temperature", [
    (-1000, 1000),
    (1000, -1000),
    (-1000, -1000),
    (0, 1000),
    (1000, 0),
    (0, 0),
    (0, -1000)
])
def test_value_error_calculate_stefan_boltzmann_luminosity(radius,
                                                           temperature):
    with pytest.raises(ValueError):
        calculate_stefan_boltzmann_luminosity(radius, temperature)


@pytest.mark.parametrize("radius,temperature", [
    ("hello", 1000),
    (1000, "world"),
    ("hello", "world"),
    ([1, 2, 3], 1000),
    (1000, [1, 2, 3])
])
def test_type_error_calculate_stefan_boltzmann_luminosity(radius, temperature):
    with pytest.raises(TypeError):
        calculate_stefan_boltzmann_luminosity(radius, temperature)


@pytest.mark.parametrize("solar_temperature,expectation", [
    (sun_facts["mean temperature"], ["G", "yellowish white"])
])
def test_classify_harvard_spectral_classification(solar_temperature,
                                                  expectation):
    classification, chromaticity = classify_harvard_spectral_classification(
        solar_temperature)
    assert classification == expectation[0]
    assert chromaticity == expectation[1]


@pytest.mark.parametrize("solar_temperature", [
    ("hello", ),
    ([1, 2, 3], )
])
def test_type_error_classify_harvard_spectral_classification(
        solar_temperature):
    with pytest.raises(TypeError):
        classify_harvard_spectral_classification(solar_temperature)


@pytest.mark.parametrize("solar_temperature", [
    1000,
    -5555555
])
def test_value_error_classify_harvard_spectral_classification(
        solar_temperature):
    with pytest.raises(ValueError):
        classify_harvard_spectral_classification(solar_temperature)
