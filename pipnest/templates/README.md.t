# %%NAME%%

%%DESCRIPTION%%

## Installation instructions

### Using pip

When installed through pip the module is built for you with CMake outside of the python
package folder, this means that pip cannot track the real installation status. To
uninstall and reinstall see [Uninstallation](Uninstallation).

0. Install NEST following the instructions provided here (https://www.nest-simulator.org/)

1. Install using pip

```
pip install %%NAME%% --no-cache-dir
```

3. Load the module after importing nest:

```
import nest
nest.Install("%%NAME%%module")
```

## Uninstallation

To uninstall this module use `pip uninstall %%NAME%%` and remove the
`(lib)%%NAME%%module.so` files from the `lib/nest/` directory in your nest installation.
