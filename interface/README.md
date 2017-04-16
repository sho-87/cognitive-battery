# Interface Files

This directory contains class definitions for the different windows and dialog 
boxes. These are imported by the main script as modules and used to 
create/display the different application windows.

Each module here uses the generated Python files (`../designer/*.py`) to
determine the layout for each window

The process as a whole:

1. `.ui` files are created for each window using QT Designer. These can be 
found in `../designer/ui/`
2. `.ui` files are converted to `.py` using `../designer/ui/convertUI.bat`.
These are just Python versions of the `.ui` files and contain the layout and
structure of all window elements. They can be found in `../designer/`
3. The Python modules in this directory define classes for each application 
window, using the layout from files generated in Step #2 and adding the 
logic for each window
4. Finally, these classes are instantiated in the main script to create and
display the windows when needed