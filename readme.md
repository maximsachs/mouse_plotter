# Mouse plotter for ubuntu



## Dependencies:

```
conda create -n mouse_plotter
conda activate mouse_plotter
conda install -c conda-forge python-xlib
pip install PyUserInput Pillow numpy
```

## Windows is a pain 

On windows there is strange stuff happening because PyUserInput is kinda old. Some dependencies are no longer maintained. Probably will only work with Python 2 on windows.

 If pyhook is a problem have a look here: https://stackoverflow.com/questions/39876454/can-someone-help-me-installing-pyhook

Also on Windows replace `raise ListenInterrupt("Calibrated.")` with `self.stop()`