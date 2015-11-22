#Cognitive Battery
A Python based battery of common cognitive psychology tasks. Designed to be modular as each task is contained within a single Python script, the results of which are returned as a dataframe for saving. Pull requests are welcome! Please see the contribution notes below.

![Battery loading screen](/images/load_screen.png)

Some tasks contain copyrighted images (e.g. Mental Rotations Task, Raven's Progressive Matrices) that I cannot include in this repo. In case you have access to the original images, I have included an explanation of how to name/format those items to work with this battery.

**Note**: I created this project as I needed to get some tasks up and running quickly for an experiment. Everything is fully functional as it stands, but I will be refactoring much of the code over time to clean things up. This will include things like code reduction, better handling of different screen resolutions, and improved logic.

##Requirements
You will need to have the following dependencies installed to run the battery, most of which are just Python modules:

* **Python 2.7.x**
  - The easiest way to install Python is using the [Anaconda](https://www.continuum.io/downloads) distribution as it also includes some of the other dependencies listed below.
* **Pandas**
  - Included with Anaconda. Otherwise, install using pip (`pip install pandas`)
* **Numpy**
  - Included with Anaconda. Otherwise, install using pip (`pip install numpy`)
* **Pygame**
  - Downloadable from the [Pygame website](http://www.pygame.org/download.shtml). If you installed 64bit Python, you will need to download the 64bit Pygame binaries from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) and install using pip (`pip install <download filename>`)
* **PyQT4**
  - Full release downloadable from the [PyQT4 website](https://www.riverbankcomputing.com/software/pyqt/download)

##Usage
Using the battery is as simple as running the `run_battery.py` file. This can either be done using the command line (navigate to the directory and `python run_battery.py`), or running it from IDLE.

On the loading screen, all sections are currently mandatory, although some may be irrelevant for your particular experiment. You can place arbitrary values in the irrelevant fields.

Select the tasks you want to include by using the checkboxes. The order of task administration can be set using the `Up` and `Down` buttons. Alternatively, you can set the order to be random using the checkbox.

The task results are saved in the /data directory. Each participant's data is saved as an Excel file, where each task is saved to a separate sheet. I'm considering replacing the use of Excel with .csv files, but that will come later.

##Contribution
Extending the battery is simple.

Each new task you want to add will need to be programmed as a Python module.

Create a Class within the module that returns a Pandas dataframe object.

A new instance of the class is spawned in `run_battery.py`. The Pandas dataframe object gets returned there and saved out to Excel. The code for this is towards the end of the file in the `start()` method, after the UI code.

The UI will also need to be updated in `run_battery.py`. The new task needs to be added to the `taskList` object, which is a QT List widget.

In summary:

1. Program a separate `.py` module for your task
2. Return a Pandas dataframe at the end of your task
3. Import this module in `run_battery.py`
4. Add your task name to the `taskList` widget in `run_battery.py` (within the `retranslateUi()` method)
5. Spawn a new instance of the class in `run_battery.py` within the `start()` method.

##References
