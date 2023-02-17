import pytest
from pymaterial.materials import OrthotropicMaterial


@pytest.mark.parametrize(
    "Es, nus, Gs, density, ndigits",
    [
        ((3.0, 2.0, 1.0), (0.3, 0.2, 0.1), (0.6, 0.5, 0.4), 1000, [3, 3, 3]),
    ],
)
def test_values(Es, nus, Gs, density, ndigits):
    material = OrthotropicMaterial(*Es, *nus, *Gs, density)
    compliance = material.get_compliance()
    assert len(compliance) == 6
    assert round(compliance[0, 0], ndigits[0]) == round(1 / Es[0], ndigits[0])
    assert round(compliance[0, 1], ndigits[1]) == round(-nus[0] / Es[0], ndigits[1])
    assert round(compliance[4, 4], ndigits[2]) == round(1 / Gs[1], ndigits[2])
