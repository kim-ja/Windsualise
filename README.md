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

The tool can load both Excel and csv files.
If your original file is a .csv, do not convert it to .xslx first, because in rare cases, Excel can mess up the timestamp format during the conversion.

For a preview of the application, check **About.pdf** in the repository.

For any enquiries, feel free to send me an email at kim.janovski.public@gmail.com

There is an executable version (.exe) available upon request, for 64bit Windows systems, that requires no
Anaconda/Spyder. This is a little slower, but might be more convenient for some.
Due to large size of the file, send me an email if you are interested, and I can see if it is possible to share it
via Google Drive/OneDrive.


