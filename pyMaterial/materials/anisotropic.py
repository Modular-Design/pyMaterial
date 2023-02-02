from .material import Material, ndarray, np


class AnsiotropicMaterial(Material):
    def __init__(self, stiffness: ndarray, density: float, **kwargs):
        """
        Parameters
        ----------
        stiffness
        density
        kwargs
        """
        self.stiffness = stiffness
        super().__init__(dict(DENS=density), **kwargs)

    def get_stiffness(self) -> ndarray:
        return self.stiffness

    def get_compliance(self) -> ndarray:
        return np.linalg.inv(self.get_stiffness())
