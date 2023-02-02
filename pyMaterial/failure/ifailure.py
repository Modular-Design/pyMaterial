from typing import Optional, List


class IFailure:
    def get_failure(self,
                    stresses: Optional[List[float]] = None,
                    strains: Optional[List[float]] = None,
                    temperature: Optional[float] = None) -> dict:
        """
        Computes the loading dependent failure value.
        Parameters
        ----------
        stresses : List[float], optional
            stress tensor in Voigt notation
        strains : List[float], optional
            strain tensor using the Voigt notation:
        temperature: List[float, optional
            Temperature in [K]
        Notes
        -----
        - **stress** tensor in Voigt notation:
          + 2D: [sigma_11, sigma_22, sigma_12]
          + 3D: [sigma_11, sigma_22, sigma_33, sigma_23, sigma_13, sigma_12]
        - **strain** tensor using the Voigt notation:
          + 2D: [eps_11, eps_22, gamma_12=2*eps_12]
          + 3D: [eps_11, eps_22, eps_33, gamma_12_23, gamma_12_13, gamma_12_12]
        - ****
        Returns
        -------
        dict
            Dictionary of failure id and value.
            Values larger 1.0 a equivalent to a failure of the material.
        """
        raise NotImplementedError