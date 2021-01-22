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
 **In order to run the app, windrose package needs to be installed - https://github.com/python-windrose/windrose** - To install this package with conda run following in Anaconda Prompt:\
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


## **HOW TO USE**

1) To load a csv or Excel file correctly: first row (row[0]) must contain all the variable names, and first column (column[0]) must contain index timestamp/timeseries entries. All extras and inconsistent formatting must be deleted prior to loading the file.

2) The tool can load both Excel and csv files. If your original file is a .csv, do not convert it to .xslx first, Excel can mess up the format during the conversion.

3) You need to specify the timestamp format of your index column (the app gives an example), to specify format that time gets stored in.

4) You need to specify the name of that first, timestamp column

5) Browse the file  (it might take a while to load depending on the file size), and once it is loaded, click on Load File button to proceed

6) If your file takes too long to load, consider making it smaller by only extracting those data columns needed and storing them in a separate, smaller file.

7) Once you have successfully loaded the data file, you will be given options to plot different types of plots, and modify them using an interactive toolbar.

8) If you want to resample or change the time frame of your data, that can be done in the Time Frame settings tab. Once you have defined the new time frame / resampled your values, you MUST press Apply. Then just go back to the plot type buttons, to create the plot you need.

9) If you want to go back to the initial plotting frequency, type **default** into the sampling frequency fill-box and press Apply.

10) If you want to export the dataset, after resampling and modifying time frame, you MUST press Apply. Then you can press the export button.
