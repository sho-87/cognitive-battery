import os
import sys

from PyQt5 import QtWidgets
from interface import battery_window


def main():
    # Get current directory
    cur_directory = os.path.dirname(os.path.realpath(__file__))

    # Check if settings file exists. If not, this is a first run
    first_run = not os.path.isfile(os.path.join(cur_directory, "settings.ini"))

    # Create main app window
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()

    main_window = battery_window.BatteryWindow(cur_directory,
                                   first_run,
                                   screen_resolution.width(),
                                   screen_resolution.height())
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
