import pytest
from pymaterial.failure import Cuntze


@pytest.mark.parametrize(
    "Em, rs, stresses, strains, result, ndigits",
    [
        (1.0, [2.0, -2.0, 1.0, -1.0, 0.5], [0.0, 0.0, 0.0], [0, 0, 0], 0.0, 2),
    ],
)
def test_values(Em, rs, stresses, strains, result, ndigits):
    failure = Cuntze(Em, rs[0], rs[1], rs[2], rs[3], rs[4])
    res = failure.get_failure(stresses, strains)
    assert round(res["cuntze"], ndigits) == result
