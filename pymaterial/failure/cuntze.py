from .ifailure import IFailure
from typing import Optional, List


class CuntzeFailure(IFailure):
    def __init__(
        self,
        E1: float,
        R_1t: float,
        R_1c: float,
        R_2t: float,
        R_2c: float,
        R_21: float,
        my_21: Optional[float] = 0.3,
        interaction: Optional[float] = 2.5,
    ):
        """
        Cuntze failure criterion [1]_

        Parameters
        ----------
        E1 : float
            E-Modulus in fibre direction
        R_1t : float
            tensile strength in fibre direction
        R_1c : float
            compressive strength in fibre direction
        R_2t : float
            tensile strength perpendicular to fibre direction
        R_2c : float
            compressive strength perpendicular to fibre direction
        R_21 : float
            in-plane shear strength
        my_21 : Optional[float], optional
            Reibungs-/Materialparameter 0 < My > 0.3, by default 0.3
        interaction : Optional[float], optional
            Interaktionsfaktor 2,5 < m < 3,1, by default 2.5

        References
        ---------
        .. [1] R.G. Cuntze and A. Freund,
            "The predictive capability of failure mode concept-based strength criteria
            for multidirectional laminates", Composites Science and Technology, vol. 64,
            no. 3, pp. 343-377, 2004
        """

        self.E1 = E1
        self.R_1t = R_1t
        self.R_1c = R_1c
        self.R_2t = R_2t
        self.R_2c = R_2c
        self.R_21 = R_21
        self.my_21 = my_21
        self.interaction = interaction

    def get_failure(
        self,
        stresses: Optional[List[float]] = None,
        strains: Optional[List[float]] = None,
        temperature: Optional[float] = None,
    ):
        # epsilon_xt tensile strain in fibre direction
        # epsilon_xc compressive strain in fibre direction
        # sigma_yt   tensile stress perpendicular to fibre direction
        # sigma_yc   compressive stress perpendicular to fibre direction
        # sigma_y    stress perpendicular to fibre direction
        # tau_yx     in-plane shear stress
        # my_21 (= 0.3)  # Reibungs-/Materialparameter 0 < My > 0.3
        m = self.interaction  # Interaktionsfaktor 2,5 < m < 3,1

        # Reserve factors for single layer according to Cuntze

        epsilon_x = strains[0]
        epsilon_xt = 0.0
        epsilon_xc = 0.0
        if epsilon_x > 0:
            epsilon_xt = epsilon_x
        else:
            epsilon_xc = epsilon_x

        sigma_y = stresses[1]
        sigma_yt = 0.0
        sigma_yc = 0.0
        if sigma_y > 0:
            sigma_yt = sigma_y
        else:
            sigma_yc = sigma_y

        tau_yx = stresses[2]

        eff_1sigma = (epsilon_xt * self.E1) / self.R_1t  # FF1
        eff_1tau = (abs(epsilon_xc) * self.E1) / self.R_1c  # FF2

        eff_2sigma = sigma_yt / self.R_2t  # IFF1
        eff_2tau = abs(sigma_yc) / self.R_2c  # IFF2
        eff_21 = abs(tau_yx) / (self.R_21 - self.my_21 * sigma_y)  # IFF2

        # total Reservefactor
        eff_ges = (
            eff_1sigma**m
            + eff_1tau**m
            + eff_2sigma**m
            + eff_2tau**m
            + eff_21**m
        ) ** (1 / m)

        return {"cuntze": eff_ges}
