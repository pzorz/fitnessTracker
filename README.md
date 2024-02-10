# Fitness and Health Tracking Program
This project is designed to aid in anyone's fitness journey. It provides a way to assist in analysing data, shoing trends, and keeping the user honest. You cannot make improvements unless you baseline your results. This project helps with that. 

## Features 
### Plotting Lifts
Plot your lift data over time. This will show your max volume each day you lifted. Trend lines are added to help you see if you are lifting more or less weight overtime. 
### Plotting Body Measurements

## How to
### Generating the GUI
    pyuic6 -x fit.ui -o fit.py

### Generating the Executable 
    python3 setup.py py2app -A --packages=PyQt6,pandas,matplotlib