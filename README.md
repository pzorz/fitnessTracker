# Fitness and Health Tracking Program
This project is designed to aid in anyone's fitness journey. It provides a way to assist in analysing data, shoing trends, and keeping the user honest. You cannot make improvements unless you baseline your results. This project helps with that. 

## Features 
### Plotting Lifts
Plot your lift data over time. This will show your max volume each day you lifted. Trend lines are added to help you see if you are lifting more or less weight overtime. 

### Plotting Body Measurements
Plot you body measurements over time. This is helpful to keep track of your girth measurements and to see if they are trending up or down.

### Max Volume Report
Generate a report of what your max volume was for each type of lift. This generates a text file. This report can only be run after plotting all the lift data as the report needs to be populated.

## How to
### Generating the GUI
    pyuic6 -x fit.ui -o fit.py

### Generating the Executable 
    python3 setup.py py2app -A --packages=PyQt6,pandas,matplotlib