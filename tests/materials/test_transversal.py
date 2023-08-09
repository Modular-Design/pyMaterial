import pytest  # noqa
from pymaterial.materials import TransverselyIsotropicMaterial

"""
# CFK UD(230 GPa) prepreg (source: ANSYS composite engineering data)
CFK_230GPa_prepreg_cuntze = CuntzeFailure(
    E1=121000,  # t/s^2/mm
    R_1t=2231.0,  # t/s^2/mm
    R_1c=1082,  # t/s^2/mm
    R_2t=29,  # t/s^2/mm
    R_2c=100,  # t/s^2/mm
    R_21=60,  # t/s^2/mm
    my_21=0.27,
)
"""
CFK_230GPa_prepreg = TransverselyIsotropicMaterial(
    E_l=121000,  # t/s^2/mm
    E_t=8600,  # t/s^2/mm
    nu_lt=0.27,
    nu_tt=0.4,
    G_lt=4700,  # t/s^2/mm
    density=1.490e-9,  # t/mm^3
    # failures=[CFK_230GPa_prepreg_cuntze],
)  # MPa


CFK_230GPa_prepreg.get_compliance()
