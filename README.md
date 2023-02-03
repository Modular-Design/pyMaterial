# pyMaterial

[![Python package](https://github.com/Modular-Design/pyMaterial/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/Modular-Design/pyMaterial/actions/workflows/test.yml)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![codecov](https://codecov.io/github/Modular-Design/pyMaterial/branch/master/graph/badge.svg?token=DMR46WJCVP)](https://codecov.io/github/Modular-Design/pyMaterial)

---

A Python library for material and failure modeling.

Use ``pymaterial`` to create your own materials:
```python
from pymaterial.materials import TransverselyIsotropicMaterial
material = TransverselyIsotropicMaterial(
    E_l=141000.0, E_t=9340.0, nu_lt=0.35, G_lt=4500.0, density=1.7e-9
)
```
Add failure criterias
```python
from pymaterial.failure import CuntzeFailure
c_failure = CuntzeFailure()
material.add_failure(c_failure)
```

or use the material library of pre-exisiting materials
```python
from pymaterial.library import steel

steel.get_failure([256,0.0, 0.0]) # sigma_x, sigma_y, tau_xy
```


## Installation

```sh
pip install pymaterial
```

## Development

### TODOs
