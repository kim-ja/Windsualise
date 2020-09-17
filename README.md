# Windsualise
## Wind Turbine Data Visualisation Interface developed at University of Strathclyde, Technology &amp; Innovation Centre
###### Developed by Kim Janovski, under supervision of Alan Turnbull and Sofia Koukoura



Aim was to write a graphical user interface that can simplify the process of visualising big sets of raw operational data, and remove the inital scrutiny of tinkering with the code to create quick plots.
Knowledge of coding is not necesarry - app can be utilised by people from different backgrounds - students, researchers, industry.

The application inputs a data file as a .csv or .xlsx and lets user visualise big sets of raw turbine data as time series, scatter plot, wind rose and histogram.

**Application functionalities:**
- Pop-up window notifies the user about wrong input
- Plot Time Series, Scatter Plot, Histogram, Wind Rose
- Zoom/Edit/Export graphs via toolbar
- Change data range (Start/End date)
- Change sampling frequency
- Export the edited file as .csv or .xlsx

## **IMPORTANT**
 **In order to run the app, windrose package needs to be installed - https://github.com/python-windrose/windrose** - To install this package with conda run following:\
conda install -c conda-forge windrose

**To load a csv or Excel file correctly:** first row (row[0]) must contain all the variable names, and first column (column[0]) must contain timestamp/timeseries entries. All extras and inconsistent formatting **must** be deleted prior to loading the file, such as empty columns and rows that are part of the document header, or rows containing data that is not to be plotted.

For an example of how the interface looks like, check About.pdf in the repository.


