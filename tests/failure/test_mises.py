import pytest
from pymaterial.failure import VonMises


@pytest.mark.parametrize(
    "strength, stress, result, ndigits",
    [
        (200, [0, 0, 0], 0.0, 2),
        (200, [100, 0, 0], 0.5, 1),
        (200, [200, 0, 0], 1.0, 1),
        (200, [100, 0, 0, 0, 0, 0], 0.5, 1),
        (200, [200, 0, 0, 0, 0, 0], 1.0, 1),
    ],
)
def test_values(strength, stress, result, ndigits):
    failure = VonMises(strength)
    res = failure.get_failure(stress)
    assert round(res["mises"], ndigits) == result


@pytest.mark.parametrize(
    "val",
    [
        (0),
        (-0.001),
        (-1),
    ],
)
def test_negative_strength_exeption(val):
    with pytest.raises(ValueError):
        VonMises(val)


def test_none_stress():
    failure = VonMises(1)
    with pytest.raises(ValueError):
        failure.get_failure()


@pytest.mark.parametrize(
    "stresses",
    [
        ([1]),
        ([1, 2]),
        ([1, 2, 3, 4]),
        ([1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5, 6, 7]),
    ],
)
def test_incorrect_stress_lenght(stresses):
    failure = VonMises(1)
    with pytest.raises(ValueError):
        failure.get_failure(stresses)
