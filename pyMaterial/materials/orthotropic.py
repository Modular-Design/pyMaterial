from .material import Material, np, ndarray, Optional, List, IFailure


class OrthotropicMaterial(Material):
    def __init__(
        self,
        E_x: float,
        E_y: float,
        E_z: float,
        nu_xy: float,
        nu_xz: float,
        nu_yz: float,
        G_xy: float,
        G_xz: float,
        G_yz: float,
        density: float,
        failures: Optional[List[IFailure]] = None,
    ):
        self.E_x = E_x
        self.E_y = E_y
        self.E_z = E_z
        self.nu_xy = nu_xy
        self.nu_xz = nu_xz
        self.nu_yz = nu_yz
        self.G_xy = G_xy
        self.G_xz = G_xz
        self.G_yz = G_yz
        attr = dict(
            EX=E_x,
            EY=E_y,
            EZ=E_z,
            PRXY=nu_xy,
            PRXZ=nu_xz,
            PRYZ=nu_yz,
            GXY=G_xy,
            GXZ=G_xz,
            GYZ=G_yz,
            DENS=density,
        )
        super().__init__(attr, failures=failures)

    def get_compliance(self) -> ndarray:
        compliance = np.zeros((6, 6))
        compliance[0, 0] = 1 / self.E_x
        compliance[1, 1] = 1 / self.E_y
        compliance[2, 2] = 1 / self.E_z
        compliance[3, 3] = 1 / self.G_yz
        compliance[4, 4] = 1 / self.G_xz
        compliance[5, 5] = 1 / self.G_xy

        compliance[1, 0] = compliance[0, 1] = -self.nu_xy / self.E_x
        compliance[2, 0] = compliance[0, 2] = -self.nu_xz / self.E_x
        compliance[2, 1] = compliance[1, 2] = -self.nu_yz / self.E_y

        return compliance
