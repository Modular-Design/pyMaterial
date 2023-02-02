from .material import Material, np, ndarray


class IsotropicMaterial(Material):
    def __init__(self, Em: float, nu: float, density: float, **kwargs):
        """
        Parameters
        ----------
        Em
        nu
        density
        kwargs
        """
        attr = dict(EX=Em, PRXY=nu, DENS=density)
        self.Em = Em
        self.nu = nu
        super().__init__(attr, **kwargs)

    def get_compliance(self) -> ndarray:
        compliance = np.zeros((6, 6))
        compliance[0, 0] = 1 / self.Em
        compliance[1, 1] = 1 / self.Em
        compliance[2, 2] = 1 / self.Em

        compliance[1, 0] = compliance[0, 1] = -self.nu / self.Em
        compliance[2, 0] = compliance[0, 2] = -self.nu / self.Em
        compliance[2, 1] = compliance[1, 2] = -self.nu / self.Em

        compliance[3, 3] = 2 * (1 + self.nu) / self.Em
        compliance[4, 4] = 2 * (1 + self.nu) / self.Em
        compliance[5, 5] = 2 * (1 + self.nu) / self.Em

        return compliance
