from typing import List, Tuple
import numpy as np
from .ply import Ply
from pyMaterial.materials import TransverselyIsotropicMaterial


class Stackup:
    def __init__(self, plies: List[Ply], bot_to_top=True):
        """
        Stackup or Laminat
        Parameters
        ----------
        plies : List[Ply]
            list of lies that makes the stackup, order is bottom to top
        References
        ----------
        .. [1] J. Ashton and J.M. Whitney, "Theory of Laminated Plates",
           Technomic, vol. 4, 1970
        """

        self.plies = plies
        if not bot_to_top:
            self.plies.reverse()
            self.plies = plies
        self.thickness = self.calc_thickness()
        self.density = self.calc_density()
        self.abd = None

    def get_plies(self, bot_to_top=True) -> List[Ply]:
        """
        Get plies of stackup.
        Returns
        -------
        List[Ply]
            lists of plies, order is bottom to top
        """
        if not bot_to_top:
            copy = self.plies.copy()
            copy.reverse()
            return copy
        else:
            return self.plies

    def calc_thickness(self) -> float:
        """
        Calculate the stackup thickness
        Notes
        -----
        **Calculation** means that that the result will allways computated again.
        Meaning that it will always correct, but might take a little bit longer.
        If you dont want this use **get_thickness()** instead!
        Returns
        -------
        float
            complete thickness of the stackup or sum over all ply thicknesses
        """
        thickness = 0.0
        for ply in self.plies:
            thickness = thickness + ply.thickness
        self.thickness = thickness
        return self.thickness

    def get_thickness(self) -> float:
        """
        Returns the stackup thickness
        Notes
        -----
        The Thickness is calculated at the beginning of the object creation.
        Meaning that later changes will probably not be considered!
        If you dont want this use **calc_thickness()** instead!
        Returns
        -------
        float
            complete thickness of the stackup or sum over all ply thicknesses
        """
        return self.thickness

    def calc_density(self) -> float:
        """
        Calculate the stackup density
        Notes
        -----
        **Calculation** means that that the result will allways computated again.
        Meaning that it will always correct, but might take a little bit longer.
        If you dont want this use **get_density()** instead!
        Returns
        -------
        float
            density of the stackup or mean over the plies
        """
        thick_density = 0.0
        for i in range(len(self.plies)):
            ply = self.plies[i]
            density = ply.get_material().get_density()
            if density is None:
                raise ValueError(f"Density is not defined for Material in Layer {i}.")
            thick_density += ply.thickness * density
        self.density = thick_density / self.get_thickness()
        return self.density

    def get_density(self) -> float:
        """
        Returns the stackup density
        Notes
        -----
        The Density is calculated at the beginning of the object creation.
        Meaning that later changes will probably not be considered!
        If you dont want this use **calc_density()** instead!
        Returns
        -------
        float
            density of the stackup or mean over the plies
        """
        return self.density

    def rotate(self, angle, degree=False) -> "Stackup":
        """
        Rotate Stackup
        Parameters
        ----------
        angle
            angle in [rad] or [deg] when degree is set True
        degree : bool, optional
            changes the measurement system of angle, default is False
        Returns
        -------
        Stackup
            new instance of the rotated Stackup
        Examples
        --------
        >>> stackup = Stackup([ply])
        >>> rot_stackup = stackup.rotate(90, degree=True)
        Be aware, that the stackup is left untouched.
        To change this, use:
        >>> stackup = stackup.rotate(90, degree=True)
        instead.
        """
        if degree:
            angle = angle / 180.0 * np.pi
        plies = []
        for ply in self.plies:
            plies.append(ply.rotate(angle))
        return Stackup(plies)

    def get_abd(self, truncate=True) -> np.ndarray:
        """
        Returns the ABD-Matrix of the stackup.
        Parameters
        ----------
        truncate : bool, optional
            when true: erase values smaller 1e-6. default: True
        Returns
        -------
        array:
            ABD-Matrix, dim=(6,6)
        """
        if self.abd is None:
            h = self.thickness / 2

            # Create empty matricces for A B en D.
            A = np.zeros((3, 3))
            B = np.zeros((3, 3))
            D = np.zeros((3, 3))

            # Loop over all plies
            z_bot = -h
            for ply in self.plies:
                # Calculate the z coordinates of the top and bottom of the ply.
                z_top = z_bot + ply.thickness

                # Rotate the local stiffenss matrix.
                Q_bar = ply.get_stiffness()

                # Calculate the contribution to the A, B and D matrix of this layer.
                Ai = Q_bar * (z_top - z_bot)
                Bi = 1 / 2.0 * Q_bar * (z_top**2 - z_bot**2)
                Di = 1 / 3.0 * Q_bar * (z_top**3 - z_bot**3)

                # Summ this layer to the previous ones.
                A = A + Ai
                B = B + Bi
                D = D + Di
                z_bot = z_top

            # Compile the entirety of the ABD matrix.
            self.abd = np.array(
                [
                    [A[0, 0], A[0, 1], A[0, 2], B[0, 0], B[0, 1], B[0, 2]],
                    [A[1, 0], A[1, 1], A[1, 2], B[1, 0], B[1, 1], B[1, 2]],
                    [A[2, 0], A[2, 1], A[2, 2], B[2, 0], B[2, 1], B[2, 2]],
                    [B[0, 0], B[0, 1], B[0, 2], D[0, 0], D[0, 1], D[0, 2]],
                    [B[1, 0], B[1, 1], B[1, 2], D[1, 0], D[1, 1], D[1, 2]],
                    [B[2, 0], B[2, 1], B[2, 2], D[2, 0], D[2, 1], D[2, 2]],
                ]
            )

        # Truncate very small values.
        if truncate is True:
            return np.array(
                np.where(np.abs(self.abd) < np.max(self.abd) * 1e-6, 0, self.abd)
            )
        return self.abd

    def calc_homogenized(self) -> TransverselyIsotropicMaterial:
        """
        Homogenize the Stackup as a Transversely Isotropic Material.
        Returns
        -------
        TransverselyIsotropicMaterial
            Homogenized Stackup
        """
        scale = 1.0 / self.get_thickness()
        e_1 = scale * (
            self.get_abd()[0, 0] - (self.get_abd()[0, 1]) ** 2 / self.get_abd()[1, 1]
        )
        e_2 = scale * (
            self.get_abd()[1, 1] - (self.get_abd()[0, 1]) ** 2 / self.get_abd()[0, 0]
        )
        g_12 = scale * self.get_abd()[2, 2]
        nu_12 = self.get_abd()[0, 1] / self.get_abd()[1, 1]
        return TransverselyIsotropicMaterial(e_1, e_2, nu_12, g_12, self.get_density())

    def apply_load(self, mech_load: np.ndarray) -> np.ndarray:
        """
        Calculate the strain and curvature of the full plate
        under a given load using Kirchhoff plate theory.
        Parameters
        ----------
        mech_load : vector
            The load vector consits of are
            :math:`(N_x, N_y, N_{xy}, M_x, M_y, M_{xy})^T`
        Returns
        -------
        deformation : vector
            This deformation consists of :math:`(varepsilon_x, varepsilon_y
            varepsilon_{xy},kappa_x, kappa_y, kappa_{xy})^T`
        """
        return np.ravel(np.linalg.inv(self.get_abd()).dot(mech_load))

    def apply_deformation(self, deformation: np.ndarray) -> np.ndarray:
        """
        Calculate the applied load and moment of the plate
        under a given deformation using Kichhoff plate theory.
        Parameters
        ----------
        deformation : vector
            This deformation consists of :math:`(varepsilon_x, varepsilon_y,
            varepsilon_{xy},kappa_x, kappa_y, kappa_{xy})^T`
        Returns
        -------
        load : vector
            The load vector consits of are
            :math:`(N_x, N_y, N_{xy}, M_x, M_y, M_{xy})^T`
        """
        return np.ravel(self.get_abd().dot(deformation))

    def get_strains(
        self, deformation: np.ndarray
    ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Return strains in plies.
        Parameters
        ----------
        deformation : array
            deformation tensor of shape [e_11, e_11, e_12, x_11, x_22, x_12]
            with e being the membrane strain, and x = curvature
        Returns
        -------
        List[Tuple[np.ndarray, np.ndarray]]
            list of strains (bottom to top) with tuple of the lower and upper strain
        Notes
        -----
        Result can be used in get_stress(strains)
        """
        # Calculating total thickness of the layup.
        h = self.thickness / 2

        # Calculate deformation of the midplane of the laminate.
        strain_membrane = deformation[:3]
        curvature = deformation[3:]

        # Create a list for the strains in each ply.
        strains = []
        z_bot = -h

        # Iterate over all plies.
        for ply in self.plies:
            # Calculate the z coordinates of the top and bottom of the ply.
            z_top = z_bot + ply.thickness

            # Caluclate strain in the ply.
            strain_top = strain_membrane + z_top * curvature
            strain_bot = strain_membrane + z_bot * curvature

            # Rotate strain from global to ply axis sytstem.
            strain_lt_top = ply.get_local_strain(strain_top)
            strain_lt_bot = ply.get_local_strain(strain_bot)

            # Store the strain values of this ply.
            strain_ply = (strain_lt_bot, strain_lt_top)
            strains.append(strain_ply)
            z_bot = z_top

        return strains

    def get_stresses(
        self, strains: List[Tuple[np.ndarray, np.ndarray]]
    ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Return stresses in plies.
        Parameters
        ----------
        strains : list
            list of strains in plies
        Returns
        -------
        List[Tuple[np.ndarray, np.ndarray]]
            list of stresses (bottom to top) with tuple of the lower and upper stress
        Notes
        -----
        Result can be used in get_failure(stresses)
        """
        stresses = []

        # Iterate over all plies.
        for i in range(len(self.plies)):
            # Obtain the strains from this ply.
            strain_lt_bot, strain_lt_top = strains[i]

            # Convert strains into stresses.
            stiffness = self.plies[i].get_stiffness(local=True)
            stress_lt_top = stiffness.dot(strain_lt_top)
            stress_lt_bot = stiffness.dot(strain_lt_bot)

            # Store the stress values of this ply.
            stress_ply = (stress_lt_bot, stress_lt_top)
            stresses.append(stress_ply)

        return stresses

    def get_failure(
        self,
        stresses: List[Tuple[np.ndarray, np.ndarray]],
        strains: List[Tuple[np.ndarray, np.ndarray]],
    ) -> List[Tuple[dict, dict]]:
        """
        Return the failures in the plies.
        Parameters
        ----------
        strains : list
            list of strains in plies
        stresses : list
            list of stresses in plies
        Returns
        -------
        List[Tuple[dict, dict]]
            list of failures (bottom to top) with tuple of the lower and upper failure
        """
        failures = []
        for i in range(len(stresses)):
            ply_stress = stresses[i]
            ply_strains = strains[i]
            material = self.plies[i].get_material()
            failures.append(
                (
                    material.get_failure(
                        stresses=ply_stress[0], strains=ply_strains[0]
                    ),
                    material.get_failure(
                        stresses=ply_stress[1], strains=ply_strains[1]
                    ),
                )
            )
        return failures
