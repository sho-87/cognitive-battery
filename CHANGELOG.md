# Change Log

## [2.0.0](https://github.com/sho-87/cognitive-battery/releases/tag/2.0.0) *(2017-07-xx)*

## [1.1.0](https://github.com/sho-87/cognitive-battery/releases/tag/1.1.0) *(2016-10-09)*

**General**
- Moved a number of text, image and background display functions into their own package (`utils`)

**User Interface**
- Created separate class for UI layout and import into main script
- Changed UI base class to `QTMainWindow`
- Created conversion script for building a Python module from UI file
- Added Menu and Status bar to UI
- Added application icons
- Added global Settings window
- Application now stores (and restores) the size and position of windows

**Tasks**
- All tasks (and their images) moved to separate directory
- Improved integration with pygame
- SART timing has been fine tuned to better match the original publication
- Added the Sternberg Task
- Short version of the ANT has been removed

**Bug Fixes**
- Up/Down buttons now correctly disable if random order is selected
- Pygame window now closes if the main battery UI is closed
- CPU time and memory were being used up needlessly in certain tasks. This has been improved
- Error now correctly displays if no tasks have been chosen
- Pygame windows and backgrounds are now passed around the different tasks correctly
- User input is no longer (pre)registered in digit span during digit display

## [1.0.0](https://github.com/sho-87/cognitive-battery/releases/tag/1.0) *(2015-11-21)*
- Initial release
