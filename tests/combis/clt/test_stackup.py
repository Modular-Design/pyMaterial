import pytest
from pymaterial.materials import TransverselyIsotropicMaterial
from pymaterial.combis.clt import Ply, Stackup
import numpy as np
from math import ceil, log

material = TransverselyIsotropicMaterial(
    E_l=141000.0, E_t=9340.0, nu_lt=0.35, G_lt=4500.0, density=1.7e-9
)


def get_significance(number: float) -> int:
    significance = 0
    if number != 0.0:
        significance = abs(number)  # cant be negative
        significance = log(significance, 10)  #
        significance = abs(significance)  # will be negative
        significance = ceil(significance)  # rund_up
    return significance


@pytest.mark.parametrize(
    "plies, a_mat",
    [
        (
            [Ply(material, 1.0, 0)],
            np.array(
                [[142153.5, 3295.7, 0.0], [3295.7, 9416.4, 0.0], [0.0, 0.0, 4500.0]]
            ),
        ),
        (
            [Ply(material, 1.0, 45.0, degree=True)],
            np.array(
                [
                    [44040.4, 35040.4, 33184.3],
                    [35040.4, 44040.4, 33184.3],
                    [33184.3, 33184.3, 36244.6],
                ]
            ),
        ),
        (
            [Ply(material, 1.0, -45.0, degree=True)],
            np.array(
                [
                    [44040.4, 35040.4, -33184.3],
                    [35040.4, 44040.4, -33184.3],
                    [-33184.3, -33184.3, 36244.6],
                ]
            ),
        ),
    ],
)
def test_abd_a(plies: list, a_mat):
    abd = Stackup(plies).get_abd()
    for i in range(3):
        for j in range(3):
            assert round(abd[i, j], 1) == a_mat[i, j]


@pytest.mark.parametrize(
    "plies, b_mat",
    [
        (
            [Ply(material, 1.0, 0)],
            np.array([[11846.1, 274.6, 0.0], [274.6, 784.7, 0.0], [0.0, 0.0, 375.0]]),
        ),
        (
            [Ply(material, 1.0, 45.0, degree=True)],
            np.array(
                [
                    [3670.0, 2920.0, 2765.4],
                    [2920.0, 3670.0, 2765.4],
                    [2765.4, 2765.4, 3020.4],
                ]
            ),
        ),
        (
            [Ply(material, 1.0, -45.0, degree=True)],
            np.array(
                [
                    [3670.0, 2920.0, -2765.4],
                    [2920.0, 3670.0, -2765.4],
                    [-2765.4, -2765.4, 3020.4],
                ]
            ),
        ),
    ],
)
def test_abd_b(plies: list, b_mat):
    abd = Stackup(plies).get_abd()
    for i in range(3):
        for j in range(3):
            assert round(abd[i + 3, j + 3], 1) == b_mat[i, j]


@pytest.mark.parametrize(
    "plies, loading, deformations",
    [
        (
            [Ply(material, 1.0, 45.0, degree=True)],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            (0.000083, -0.000028, -0.00005, 0.0, 0.0, 0.0),
        ),
        (
            [Ply(material, 1.0, -45.0, degree=True)],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            (0.000083, -0.000028, 0.00005, 0.0, 0.0, 0.0),
        ),
    ],
)
def test_deformations(plies: list, loading, deformations):
    deform = Stackup(plies).apply_load(np.array(loading))
    assert len(deform) == len(deformations)
    for i in range(len(deformations)):
        significance = get_significance(deformations[i])
        assert round(deform[i], significance + 1) == deformations[i]


@pytest.mark.parametrize(
    "plies, loading, strains",
    [
        (
            [Ply(material, 1.0, 45.0, degree=True)],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [([2.3e-06, 5.2e-05, -1.1e-04], [2.3e-06, 5.2e-05, -1.1e-04])],
        ),
        (
            [Ply(material, 1.0, -45.0, degree=True)],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [([2.3e-06, 5.2e-05, 1.1e-04], [2.3e-06, 5.2e-05, 1.1e-04])],
        ),
    ],
)
def test_strains(plies: list, loading, strains):
    stackup = Stackup(plies)
    deform = stackup.apply_load(np.array(loading))
    layer_strains = stackup.get_strains(deform)
    assert len(layer_strains) == len(strains)
    for i in range(len(strains)):
        # bottom
        stress = strains[i][0]
        for j in range(len(stress)):
            significance = get_significance(stress[j])
            assert round(layer_strains[i][0][j], significance + 1) == stress[j]

        # top
        stress = strains[i][1]
        for j in range(len(stress)):
            significance = get_significance(stress[j])
            assert round(layer_strains[i][1][j], significance + 1) == stress[j]


@pytest.mark.parametrize(
    "plies, loading, stresses",
    [
        (
            [Ply(material, 1.0, 45.0, degree=True)],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [([0.5, 0.5, -0.5], [0.5, 0.5, -0.5])],
        ),
        (
            [Ply(material, 1.0, -45.0, degree=True)],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])],
        ),
    ],
)
def test_stresses(plies: list, loading, stresses):
    stackup = Stackup(plies)
    deform = stackup.apply_load(np.array(loading))
    layer_strains = stackup.get_strains(deform)
    layer_stresses = stackup.get_stresses(layer_strains)
    assert len(layer_stresses) == len(stresses)
    for i in range(len(stresses)):
        # bottom
        stress = stresses[i][0]
        for j in range(len(stress)):
            significance = get_significance(stress[j])
            assert round(layer_stresses[i][0][j], significance + 1) == stress[j]

        # top
        stress = stresses[i][1]
        for j in range(len(stress)):
            significance = get_significance(stress[j])
            assert round(layer_stresses[i][1][j], significance + 1) == stress[j]
