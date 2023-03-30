import pytest
from pymaterial.failures import MaxStressFailure


@pytest.mark.parametrize(
    "strength, stress, result, ndigits",
    [
        ([1.0, 1.0, 1.0], [0.0, 0.0, 0.0], 0.0, 2),
        ([1.0, 1.0, 1.0], [2.0, 1.5, 0.5], 2.0, 2),
        ([1.0, (0.0, 1.0), 1.0], [0.5, 0.5, 0.0], 0.5, 2),
        ([1.0, (0.0, 1.0), 1.0, 0.5, 0.5, 0.5], [0.5, 0.5, 0.0, 0.0, 0.0, 0.0], 0.5, 2),
    ],
)
def test_values(strength, stress, result, ndigits):
    failure = MaxStressFailure(strength)
    res = failure.get_failure(stress)
    assert round(res["max-stress"], ndigits) == result


@pytest.mark.parametrize(
    "val",
    [
        ([1]),
        ([1, 2]),
        ([1, 2, 3, 4]),
        ([1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5, 6, 7]),
    ],
)
def test_wrong_strength_length_exeption(val):
    with pytest.raises(ValueError):
        MaxStressFailure(val)


def test_none_stress():
    failure = MaxStressFailure([1.0, 1.0, 1.0])
    with pytest.raises(ValueError):
        failure.get_failure()


@pytest.mark.parametrize(
    "strength, stresses",
    [
        ([1.0, 1.0, 1.0], [1]),
        ([1.0, 1.0, 1.0], [1, 2]),
        ([1.0, 1.0, 1.0], [1, 2, 3, 4]),
        ([1.0, 1.0, 1.0], [1, 2, 3, 4, 5]),
        ([1.0, 1.0, 1.0], [1, 2, 3, 4, 5, 6]),
        ([1.0, 1.0, 1.0], [1, 2, 3, 4, 5, 6, 7]),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1]),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1, 2]),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1, 2, 3]),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1, 2, 3, 4]),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1, 2, 3, 4, 5]),
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1, 2, 3, 4, 5, 6, 7]),
    ],
)
def test_incorrect_stress_lenght(strength, stresses):
    failure = MaxStressFailure(strength)
    with pytest.raises(ValueError):
        failure.get_failure(stresses)
