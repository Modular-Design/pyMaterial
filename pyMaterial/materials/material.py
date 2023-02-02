import numpy as np
from ..failure import IFailure
from typing import Optional, List, Union
from numpy import ndarray


class Material(IFailure):
    def __init__(self, attr: dict, failures: Optional[List[IFailure]] = None):
        """
        Parameters
        ----------
        attr : dict
        failures : List[IFailure], optional
        """
        self.attr = attr
        if failures is None:
            failures = []
        self.failures = failures

    def get_compliance(self) -> ndarray:
        raise NotImplementedError

    def get_stiffness(self) -> ndarray:
        return np.linalg.inv(self.get_compliance())

    def get_density(self) -> float:
        return self.attr.get("DENS")

    def get_failures(self) -> List[IFailure]:
        """
        Returns
        -------
        List[IFailure]
            List of possible material failures
        """
        return self.failures

    def get_failure(
        self,
        stresses: Optional[Union[List[float], ndarray]] = None,
        strains: Optional[Union[List[float], ndarray]] = None,
        temperature: Optional[float] = None,
    ) -> dict:
        """
        returns
        {"max_stress": 1.0, "cuntze": 0.5}
        """
        result = dict()
        for failure in self.failures:
            result.update(failure.get_failure(stresses, strains, temperature))
        return result

    def get_plane_stress_stiffness(self):
        """
        Get stiffness tensor for plane stress
        Returns
        -------
        """
        elems = [0, 1, 5]  # ignore the s_zz, s_xy and s_yz row and column
        stiffness = self.get_stiffness()
        return stiffness[elems][:, elems]

    def get_plane_strain_stiffness(self):
        """
        et stiffness tensor for plane strain
        Returns
        -------
        """
        elems = [0, 1, 5]  # ignore the s_zz, s_xy and s_yz row and column
        return np.linalg.inv(self.get_compliance()[elems][:, elems])
