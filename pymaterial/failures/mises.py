from .ifailure import IFailure
from typing import Optional, List
from math import sqrt


class VonMisesFailure(IFailure):
    def __init__(self, yield_stress: float):
        """
        con Mises yield criterion
        Parameters
        ----------
        yield_stress: float
            equivalent tensile stress or equivalent von-Mises stress
        Examples
        --------
        Create a Von-Mises-yield criteria
        >>> criteria = VonMises(280)
        >>> crit_loading = [140.0, 0.0, 0.0]
        >>> criteria.get_failure(stresses=crit_loading)
        returns {``max-stress``: 0.5}
        >>> uncrit_loading = [140.0, 0.0, 0.0]
        >>> criteria.get_failure(stresses=crit_loading)
        returns {``max-stress``: 0.5}
        """

        if yield_stress <= 0:
            raise ValueError(
                f"Yield stress has to be greater 0! (recieved: {yield_stress})"
            )

        self.strength = yield_stress

    def get_failure(
        self,
        stresses: Optional[List[float]] = None,
        strains: Optional[List[float]] = None,
        temperature: Optional[float] = None,
    ):
        if stresses is None:
            raise ValueError("Requires a stress tensor in Voigt notation!")
        length = len(stresses)
        allowed_length = [3, 6]
        if length not in allowed_length:
            raise ValueError(
                f"Stresses has to be of length 3 (2D) or 6 (3d stress state). "
                f"Recieved stress vector of length {length}."
            )

        stress = 0

        s11 = stresses[0]
        s22 = stresses[1]

        if length == 3:
            s12 = stresses[2]
            stress = sqrt(s11**2 - s11 * s22 + s22**2 + 3 * s12)
        else:  # length == 6
            s33 = stresses[2]
            s31 = stresses[3]
            s23 = stresses[4]
            s12 = stresses[5]
            stress = sqrt(
                0.5 * ((s11 - s22) ** 2 + (s22 - s33) ** 2 + (s33 - s11) ** 2)
                + 3.0 * (s12**2 + s23**2 + s31**2)
            )

        return {"mises": stress / self.strength}
