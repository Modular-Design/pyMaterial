import pytest
from pymaterial.materials import IsotropicMaterial


@pytest.mark.parametrize(
    "Em, nu, density, ndigits",
    [
        (2.0e5, 0.3, 1000, [3, 3, 3]),
    ],
)
def test_values(Em, nu, density, ndigits):
    material = IsotropicMaterial(Em, nu, density)
    compliance = material.get_compliance()
    assert len(compliance) == 6
    assert round(compliance[0, 0], ndigits[0]) == round(1 / Em, ndigits[0])
    assert round(compliance[0, 1], ndigits[1]) == round(-nu / Em, ndigits[1])
    assert round(compliance[3, 3], ndigits[2]) == round(2 * (1 + nu) / Em, ndigits[2])


def test_plane_stress_stiffness():
    material = IsotropicMaterial(2.0e5, 0.3, 1000)
    stiff = material.get_plane_stress_stiffness()
    assert stiff.shape == (3, 3)


def test_plane_strain_stiffness():
    material = IsotropicMaterial(2.0e5, 0.3, 1000)
    stiff = material.get_plane_strain_stiffness()
    assert stiff.shape == (3, 3)
