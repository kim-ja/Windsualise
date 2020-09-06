#v6  wind rose plotting integrated + decimal points fixed


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Frame, Checkbutton
from tkinter import BooleanVar, BOTH

import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from matplotlib.ticker import NullFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from functools import partial
from datetime import datetime
import datetime

from windrose import plot_windrose
from windrose import WindroseAxes
import matplotlib.cm as cm





# %d/%m/%Y %H:%M is the format if input file is called TTimeStampLocal



scada_data = None #initially

global flag_time_range  # activates the first time Apply is pressed and time frame / frequency is changed
                        # before Apply is pressed, scada_data (original dataframe with default freq.) is used to plot all time series and scatter plots
                        # after Apply is pressed (flag_time_range --> 1), scada_data_2 is created as a copy of scada_data, followed by resample or timeframe modifications
                        # every time Apply is pressed, new scada_data_2 is created from original scada_data, so resampling would always be done on the raw dataset
                       
flag_time_range = 0

global freq_string 


HUGE_FONT= ("Verdana", 16)
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)





def popupmsg(msg): #to add a popup message
    popup = tk.Tk()
    popup.wm_title("Pop-up Message")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.attributes("-topmost", True)
    popup.mainloop()
  
  
    
    
def alert(frame,var,entry1,entry2):
    global scada_data
    global time
    if var is None: # var is .csv being loaded, by default at the start scada_data is 'None'
        popup = tk.Tk()
        popup.wm_title("Pop-up Message")
        label = ttk.Label(popup, text="You have not selected a file! Please do not leave the program while a .csv or .xlsx file has not been selected.", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.attributes("-topmost", True)
        #popup._root_window.focus_force() 
        popup.mainloop()
    
         
    
    else:
        getstring(entry1)  #dataframe format
        getindex(entry2)    #header (Index) column title
        time = scada_data[index_string].tolist()
        time = pd.to_datetime(time, format=format_string)
        #"%d/%m/%Y %H:%M" unput for gui testtable

        scada_data = scada_data.set_index(index_string)
        scada_data.index = pd.to_datetime(scada_data.index)
        
        
        frame.destroy()
       
    


    
def getstring(entry):
    global format_string
    format_string=entry.get()
    
def getindex(entry):
    global index_string
    index_string=entry.get()




def shutProgram(self):
         self.destroy()
         



def plot_1var_vs_time(array_element): #plots one variable vs time
    
    global scada_data_2
    global time
    
    if flag_time_range == 0:
        fig,ax = plt.subplots(figsize=(12, 7))
        ax.plot(scada_data.index,scada_data[array_element],marker='o', markersize=5, c='black', markerfacecolor = 'teal')
        
        ax.set_title('Time Series of ' + str(array_element))
        ax.set_ylabel(str(array_element))
        ax.set_xlabel('Time')
        fig.tight_layout()
        plt.show()

        
    else: #flag_time_range == 1
        fig,ax = plt.subplots(figsize=(12, 7))
        ax.plot(scada_data_2.index,scada_data_2[array_element],marker='o', markersize=5, c='black', markerfacecolor = 'teal')
        
        ax.set_title(' Time Series of ' + str(array_element) + '   from   ' + str(time2[0]) + '   to   ' + str(time2[-1]) + "    (sampling freq. = " + freqstamp + " )")
        ax.set_ylabel(str(array_element))
        ax.set_xlabel('Time')
        fig.tight_layout()
        plt.show()
        
    
    
    
    
def setX(array_element,global_array):
    global_array [0] = array_element

def setY(array_element,global_array):
    global_array [1] = array_element
    




def plot_scatter(global_array): #plots two variables
    
    if (global_array[0] is None) or (global_array[1] is None):
        popup = tk.Tk()
        popup.wm_title("Pop-up Message")
        label = ttk.Label(popup, text="You have not selected both variables. Please select two variables before pressing the PLOT button!", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.attributes("-topmost", True)
        #popup._root_window.focus_force() 
        popup.mainloop()
   
    else:
        
        if flag_time_range == 0:
        
            fig, ax = plt.subplots(figsize=(12, 7))
            ax.scatter(scada_data[global_array[0]],scada_data[global_array[1]],marker='o',c='coral',edgecolor='black')
            ax.set_title(str(global_array[1])+' vs '+str(global_array[0]))
            ax.set_ylabel(str(global_array[1]))
            ax.set_xlabel(str(global_array[0]))
            fig.tight_layout()
            plt.show()

        else: #flag_time_range == 1
            
            fig, ax = plt.subplots(figsize=(12, 7))
            ax.scatter(scada_data_2[global_array[0]],scada_data_2[global_array[1]],marker='o',c='coral',edgecolor='black')
            ax.set_title(str(global_array[1])+' vs '+str(global_array[0]) + '    from   ' + str(time2[0]) + '   to   ' + str(time2[-1]) + "    (sampling freq. = " + freqstamp + " )")
            ax.set_ylabel(str(global_array[1]))
            ax.set_xlabel(str(global_array[0]))
            fig.tight_layout()
            plt.show()




def plot_wind_rose(global_array): #plots wind rose funct.
    
    if (global_array[0] is None) or (global_array[1] is None):
        popup = tk.Tk()
        popup.wm_title("Pop-up Message")
        label = ttk.Label(popup, text="You have not selected both variables. Please select two variables before pressing the PLOT button!", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.attributes("-topmost", True)
        #popup._root_window.focus_force() 
        popup.mainloop()
   
    else:
        
        if flag_time_range == 0:
                
            df = pd.DataFrame({'speed': scada_data[global_array[0]], 'direction': scada_data[global_array[1]]})
            
            
            upper_lim_legend = max(df['speed'])//10*10
            if upper_lim_legend > 40:
                upper_lim_legend = 40
                
        
            #bins = np.arange(0.01, 16, 1)
            bins = np.arange(0,upper_lim_legend+5,5)

            
            plot_windrose(df, kind="bar", bins=bins, cmap=cm.Reds, lw=3)
            plt.show()
        
            bins = 50
        
            ax, params = plot_windrose(df, kind="pdf", bins=bins)
            ax.set_title("Weibull Distribution  -  parameters: "+ "shape factor: " +str(round(params[1],2)) +  "  scale factor: " +str(round(params[3],2)))
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Windspeed  "+str([global_array[0]]))
            #print("Weibull parameters:")
            #print(params)
            plt.show()
            
            
        else: #flag_time_range == 1
            
            df = pd.DataFrame({'speed': scada_data_2[global_array[0]], 'direction': scada_data_2[global_array[1]]})
                  
        
            upper_lim_legend = max(df['speed'])//10*10
            if upper_lim_legend > 40:
                upper_lim_legend = 40
            
            bins = np.arange(0,upper_lim_legend+5,5)
            
            plot_windrose(df, kind="bar", bins=bins, cmap=cm.Reds, lw=3)
            plt.show()
        
            bins = 50
            
            ax, params = plot_windrose(df, kind="pdf", bins=bins)
            ax.set_title("Weibull Distribution  -  parameters: "+ "shape factor: " +str(round(params[1],2)) +  "  scale factor: " +str(round(params[3],2)))
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Windspeed  "+str([global_array[0]]))
            #print("Weibull parameters:")
            #print(params)
            plt.show()




    
    
    
def change_time_and_resample(entry1,entry2,entry3): #(start date, end date, resampling freq)

    global flag_time_range
    flag_time_range = 1
    
    global d1
    global d2
    
    global startdate
    global enddate
    global scada_data_2
    global scada_data
    global time
    global time2
    global freq_string
    global freqstamp
    
    startdate = entry1.get()
    enddate = entry2.get()
    
    
    if (startdate == "default") or (startdate == "") or (startdate == " "):
        startdate = str(time[0])
    
    if (enddate == "default") or (enddate == "") or (enddate == " "):
        enddate = str(time[-1])
    
    
    #YYYY-MM-DD hh:mm:ss
    sYYYY = int(startdate[0:4])
    sMM = int(startdate[5:7])
    sDD = int(startdate[8:10])
    shh = int(startdate[11:13])
    smm = int(startdate[14:16])
    sss = int(startdate[17:19])
    
    eYYYY = int(enddate[0:4])
    eMM = int(enddate[5:7])
    eDD = int(enddate[8:10])
    ehh = int(enddate[11:13])
    emm = int(enddate[14:16])
    ess = int(enddate[17:19])
    

    d1 = datetime.datetime(sYYYY, sMM, sDD, shh, smm, sss) 
    d2 = datetime.datetime(eYYYY, eMM, eDD, ehh, emm, ess)
    
    if (d1>d2) or (d1<time[0]) or (d2>time[-1]):
        popupmsg("  Dates selected are out of range!\n Select new dates and press Apply  ")
        
    else: #dates selected are in the range
            
        start_idx = int(np.where(time == np.datetime64(datetime.datetime(sYYYY, sMM, sDD, shh, smm, sss)))[0])
    
        end_idx = int(np.where(time == np.datetime64(datetime.datetime(eYYYY, eMM, eDD, ehh, emm, ess)))[0])  #end instance not included
    
    
        scada_data_2 = scada_data.iloc[start_idx:end_idx].copy()
        time2 = time[start_idx:end_idx]
        
        freq_string = entry3.get()
        
        if (freq_string == "default") or (freq_string == "") or (freq_string == " "):
            freq_string = time[1]-time[0] #original sampling freq
    
        scada_data_2 = scada_data_2.resample(freq_string).mean()  
    
    if type(freq_string) is str:
        freqstamp = freq_string
    else:
         freqstamp = "default" 
    
    
    
    
    
 
def plot_histogram(array_element):
    global e_bins
    entry = e_bins
    num_bins = int(entry.get())
    
    
    
    if flag_time_range == 0:
        
        mu = scada_data[array_element].mean()
        sigma = scada_data[array_element].std()
        x = scada_data[array_element]
        
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # the histogram of the data
        n, bins, patches = ax.hist(x[~np.isnan(x)], num_bins, density=1, linewidth = 1.2, color = 'darkseagreen', edgecolor = 'black')
        
        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y, '--')
        ax.set_xlabel(str(array_element))
        ax.set_ylabel('Frequency')
        ax.set_title('$\mu = $' + str(round(mu,2)) + '\t$\sigma = $' + str(round(sigma,2)))
        
        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()

        
        
    else: #flag_time_range == 1
        
        mu = scada_data_2[array_element].mean()
        sigma = scada_data_2[array_element].std()
        x = scada_data_2[array_element]
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # the histogram of the data
        n, bins, patches = ax.hist(x[~np.isnan(x)], num_bins, density=1, linewidth = 1.2, color = 'darkseagreen', edgecolor = 'black')
        
        # add a 'best fit' line
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y, '--')
        ax.set_xlabel(str(array_element) + '   from   ' + str(time2[0]) + '   to   ' + str(time2[-1]) )
        ax.set_ylabel('Frequency')
        ax.set_title('$\mu = $' + str(round(mu,2)) + '\t$\sigma = $' + str(round(sigma,2))+ "    (sampling freq. = " + freqstamp + " )")
        
        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()

        
        
    
    
    
    

    
def exportCSV():
    global scada_data_2
    
    
    if flag_time_range == 0:
        popupmsg("  Original file has not been modified!  ")
         
    else:
    
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        scada_data_2.to_csv(export_file_path)


def exportExcel():
    global scada_data_2
    
    if flag_time_range == 0:
        popupmsg("  Original file has not been modified!  ")
         
    else:    
        export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        scada_data_2.to_excel(export_file_path)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
 # WINDOW THAT BROWSES AND LOADS FILE:
 # ================================================================================================   
from tkinter import filedialog
 

 
class BROWSE_FILE(tk.Tk):
    
        
    def __init__(self):
                
        super(BROWSE_FILE, self).__init__()
        self.title("Wind Turbine Data Visualisation - File Import")
        self.minsize(600, 275)
        
 
        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.pack(padx = 20, pady = 20)
 
        self.button()
 
       
         
 
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
        
        self.button2 = ttk.Button(self,text="Load File",
                            command=lambda: alert(root,scada_data,self.e,self.e2))
        self.button2.pack()
        
        
        self.label = tk.Label(self,text="\nEnter the timestamp format\nExample: 2009-12-31 20:53:45 would be %Y-%m-%d %H:%M:%S ", font=SMALL_FONT)
        self.label.pack(pady=0,padx=10)
        
        self.e = ttk.Entry()
        self.e.pack(pady=5,padx=10)
        self.e.focus_set()
        self.e.insert(1, "%Y-%m-%d %H:%M:%S") #default format_string
        
        self.label2 = tk.Label(self,text="\nEnter the name of the first (Index) column\nExample: TimeStamp, TTimeStampLocal ... ", font=SMALL_FONT)
        self.label2.pack(pady=0,padx=10)
        
        self.e2 = ttk.Entry()
        self.e2.pack(pady=5,padx=10)
        self.e2.focus_set()
        self.e2.insert(1, "TimeStamp") #default index_string

        
        
         
 
    def fileDialog(self):
 
        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("all files","*.*"), ("csv files","*.csv"), ("excel","*.xlsx")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)
               
        
        # load the file:        
        global scada_data
        global fig
        global time
        
        if self.filename.endswith('.csv'):
            scada_data = pd.read_csv(self.filename)
        else:
            scada_data = pd.read_excel(self.filename)
        
     

          

    
                 
 
root = BROWSE_FILE()
root.attributes("-topmost", True)
root.mainloop()    
   
 



 # SCROLLBAR:
 # ================================================================================================   

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="right", expand="false")
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill=BOTH, expand="true")
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor="nw")
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.interior.bind_all("<MouseWheel>", _on_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

 # ================================================================================================   





class WindTurbineData(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Wind Turbine Data Visualisation")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        
    
        filemenu.add_command(label="Exit", command=lambda:shutProgram(self))
        filemenu.add_command(label="About", command= lambda: popupmsg("This GUI was developed at The University of Strathclyde, Technology and Innovation Centre. \n\n\nCreated by Kim Janovski, under supervision of Sofia Koukoura and Alan Turnbull. July 2019."))
        menubar.add_cascade(label="File", menu=filemenu)
        

        tk.Tk.config(self, menu=menubar)
        
   
        

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        
    global list_of_headers
    list_of_headers=scada_data.columns.tolist()
     


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
               
        
        
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Wind Turbine Data Visualisation Interface v.6\nUniversity of Strathclyde, Technology and Innnovation Centre", font=LARGE_FONT)
        label.pack(pady=70,padx=20)
        label = tk.Label(self, text="Start Menu", font=HUGE_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Choose plot type:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        


        button1 = ttk.Button(self, text="Time Series",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="Scatter Plot",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button4 = ttk.Button(self, text="Histogram",
                            command=lambda: controller.show_frame(PageFour))
        button4.pack()
        
        button5 = ttk.Button(self, text="Wind Rose",
                            command=lambda: controller.show_frame(PageFive))
        button5.pack()


        button3 = ttk.Button(self, text="Time Frame Settings",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack(pady = 30)
        
       

     
        

class PageOne(tk.Frame):  #time series plot

    def __init__(self, parent, controller):
        
        
        tk.Frame.__init__(self, parent)
                
        col=0
        row=0
        
        col,row = self.grid_size()
        
        self.grid_columnconfigure(col, minsize=180)

        self.grid_rowconfigure(row, minsize=20)
        
        
        
        label = tk.Label(self, text="Time Series", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
        label.grid(row=0,column=1)


        button1 = ttk.Button(self, text="Start Menu",
                            command=lambda: controller.show_frame(StartPage))
        #button1.pack()
        button1.grid(row=1,column=1)


        button2 = ttk.Button(self, text="Scatter Plot",
                            command=lambda: controller.show_frame(PageTwo))
        #button2.pack()
        button2.grid(row=2,column=1)
        
        
        button3 = ttk.Button(self, text="Time Frame",
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=4, column=2, padx = 45)
        
        button4 = ttk.Button(self, text="Histogram",
                            command=lambda: controller.show_frame(PageFour))
        button4.grid(row=3,column=1)
        
        button5 = ttk.Button(self, text="Wind Rose",
                            command=lambda: controller.show_frame(PageFive))
        button5.grid(row=4,column=1)
      
        
        label2 = tk.Label(self, text="\n\nSelect a variable to plot against time", font=NORM_FONT)
        #label2.pack(pady=10,padx=10)
        label2.grid(row=5,column=1)

        self.frame = VerticalScrolledFrame(self)
        self.frame.grid(column=1, sticky="we")

        buttons = dict()
        for k in range(len(list_of_headers)):
            buttons=ttk.Button(self.frame.interior, text = [list_of_headers[k]], command = partial(plot_1var_vs_time,list_of_headers[k]))  #because lambda: plot_1var vs time(list of headers ...) did not work in a for loop
                      
            #buttons.pack(expand=1, fill=tk.BOTH, side=tk.BOTTOM, padx=200, ipady = 20)
            buttons.grid(column=1, sticky="we")






class PageTwo(tk.Frame):   #scatter plot

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        
        
        self.grid_columnconfigure(4, minsize=20)
        self.grid_columnconfigure(0, minsize=25)
        
        
        
        label = tk.Label(self, text="Scatter Plot", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
        label.grid(row=0,column=2)


        button1 = ttk.Button(self, text="Start Menu",
                            command=lambda: controller.show_frame(StartPage))
        #button1.pack()
        button1.grid(row=1,column=2)


        button2 = ttk.Button(self, text="Time Series",
                            command=lambda: controller.show_frame(PageOne))
        #button2.pack()
        button2.grid(row=2,column=2)
        
        button3 = ttk.Button(self, text="Time Frame",
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=4, column=3)
        
        button4 = ttk.Button(self, text="Histogram",
                            command=lambda: controller.show_frame(PageFour))
        button4.grid(row=3, column=2)
        
        button5 = ttk.Button(self, text="Wind Rose",
                            command=lambda: controller.show_frame(PageFive))
        button5.grid(row=4, column=2)
        
        
        label2 = tk.Label(self, text="\n\nSelect one variable from each row", font=NORM_FONT)
        #label2.pack(pady=10,padx=10)
        label2.grid(row=5,column=2)

            
        plotButton = ttk.Button(self, text="PLOT",
                            command=lambda: plot_scatter(two_var_to_plot))
        #plotButton.pack() 
        plotButton.grid(row=6,column=2)
        
        
        label3 = tk.Label(self, text="x-axis\t\ty-axis", font=LARGE_FONT)
        label3.grid(row=7,column=2)
        
            
        global two_var_to_plot
        two_var_to_plot=[None,None] #empty array, will host 2 variables for scatter plot

        
        self.frame1 = VerticalScrolledFrame(self)
        self.frame1.grid(row=8, column=1, sticky="we")
        
        self.frame2 = VerticalScrolledFrame(self)
        self.frame2.grid(row=8, column=3, sticky="we")
            
        buttonsX = dict()
        for k in range(len(list_of_headers)):
            buttonsX=ttk.Button(self.frame1.interior, text = [list_of_headers[k]], command = partial(setX,list_of_headers[k],two_var_to_plot))
                      
            #buttonsX.pack(expand=1, fill=tk.BOTH, side=tk.TOP, padx=200)
            buttonsX.grid(row=k+8,column=1, sticky="we")
        
        buttonsY = dict()
        for k in range(len(list_of_headers)):
            buttonsY=ttk.Button(self.frame2.interior, text = [list_of_headers[k]], command = partial(setY,list_of_headers[k],two_var_to_plot))
                      
            #buttonsY.pack(expand=1, fill=tk.BOTH, side=tk.BOTTOM, padx=200)
            buttonsY.grid(row=k+8,column=3, sticky="we")
        
        
        
        
        



class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
    
        
        
        label = tk.Label(self, text="Time Frame Settings", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
       

        button1 = ttk.Button(self, text="Start Menu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Time Series",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
        button3 = ttk.Button(self, text="Scatter Plot",
                            command=lambda: controller.show_frame(PageTwo))
        button3.pack()
        
        button4 = ttk.Button(self, text="Histogram",
                            command=lambda: controller.show_frame(PageFour))
        button4.pack()
        
        button5 = ttk.Button(self, text="Wind Rose",
                            command=lambda: controller.show_frame(PageFive))
        button5.pack()
        
        
        a = time[0]
        b = time[-1]
        c = time[1]-time[0]
        self.label_date = tk.Label(self,text="Imported data ranges from   "+str(a)+"   to   "+str(b), font=NORM_FONT)
        self.label_date.pack(pady=10,padx=10)
        
        self.label_freq = tk.Label(self,text="Default data sampling frequency is   "+ str(c) +"   (hh:mm:ss)", font=NORM_FONT)
        self.label_freq.pack(pady=10,padx=10)
        
        self.label_startdate = tk.Label(self,text="\n\nStart date:\tYYYY-MM-DD(space)hh:mm:ss", font=SMALL_FONT)
        self.label_startdate.pack(pady=5,padx=10)
        
        e_startdate = ttk.Entry(self)
        e_startdate.pack(pady=0,padx=10)
        e_startdate.focus_set()
        e_startdate.insert(1, "default") #default
        
        self.label_enddate = tk.Label(self,text="\nEnd date:\t\tYYYY-MM-DD(space)hh:mm:ss", font=SMALL_FONT)
        self.label_enddate.pack(pady=5,padx=10)
        
        e_enddate = ttk.Entry(self)
        e_enddate.pack(pady=0,padx=10)
        e_enddate.focus_set()
        e_enddate.insert(1, "default") #default
        
        self.label_freq = tk.Label(self,text="\n\nSampling frequency:\tdefault, 10 min, 30 min, 1 h, w, m ...", font=SMALL_FONT)
        self.label_freq.pack(pady=5,padx=10)
        
        
        e_freq = ttk.Entry(self)
        e_freq.pack(pady=5,padx=10)
        e_freq.focus_set()
        e_freq.insert(1, "default") #imported sampling
        
        
        button2 = ttk.Button(self, text="Apply",
                            command=lambda: change_time_and_resample(e_startdate,e_enddate,e_freq))
        button2.pack(pady=10)
        
  
        saveAsButton_CSV = ttk.Button(self, text="Export .csv",
                                      command= exportCSV)
        saveAsButton_CSV.pack(pady=5)
        
        saveAsButton_excel = ttk.Button(self, text="Export .xlsx",
                                      command= exportExcel)
        saveAsButton_excel.pack(pady=5)




class PageFour(tk.Frame): #historgam plot

    def __init__(self, parent, controller):
        
       tk.Frame.__init__(self, parent)
                
       col=0
       row=0
        
       col,row = self.grid_size()
        
       self.grid_columnconfigure(col, minsize=180)

       self.grid_rowconfigure(row, minsize=20)
        
        
        
       label = tk.Label(self, text="Histogram", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
       label.grid(row=0,column=1)


       button1 = ttk.Button(self, text="Start Menu",
                            command=lambda: controller.show_frame(StartPage))
        #button1.pack()
       button1.grid(row=1,column=1)

       button2 = ttk.Button(self, text="Time Series",
                                    command=lambda: controller.show_frame(PageOne))
       button2.grid(row=2,column=1)
                
       button3 = ttk.Button(self, text="Scatter Plot",
                                    command=lambda: controller.show_frame(PageTwo))
       button3.grid(row=3,column=1)
                     
        
       button5 = ttk.Button(self, text="Wind Rose",
                                    command=lambda: controller.show_frame(PageFive))
       button5.grid(row=4,column=1)
       
       button4 = ttk.Button(self, text="Time Frame",
                            command=lambda: controller.show_frame(PageThree))
       button4.grid(row=4, column=2, padx = 45)
      
       label = tk.Label(self, text="Bins Value: ", font=SMALL_FONT)
        #label.pack(pady=10,padx=10)
       label.grid(row=5,column=1,pady=15,padx=10)
       
       global e_bins
       e_bins = ttk.Entry(self)
       e_bins.grid(row=6,column=1)
       e_bins.focus_set()
       e_bins.insert(1, "50") #default
       
       label2 = tk.Label(self, text="\n\nSelect a variable to plot", font=NORM_FONT)
        #label2.pack(pady=10,padx=10)
       label2.grid(row=7,column=1)

       self.frame = VerticalScrolledFrame(self)
       self.frame.grid(column=1, sticky="we")

       buttons = dict()
       for k in range(len(list_of_headers)):
           buttons=ttk.Button(self.frame.interior, text = [list_of_headers[k]], command = partial(plot_histogram,(list_of_headers[k]))) #because lambda: plot_histogram(list of headers ...) did not work in a for loop
                      
            #buttons.pack(expand=1, fill=tk.BOTH, side=tk.BOTTOM, padx=200, ipady = 20)
           buttons.grid(column=1, sticky="we")


        
        

class PageFive(tk.Frame):   #wind rose plot

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        
        
        self.grid_columnconfigure(4, minsize=20)
        self.grid_columnconfigure(0, minsize=25)
        
        
        
        label = tk.Label(self, text="Wind Rose", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)
        label.grid(row=0,column=2)


        button1 = ttk.Button(self, text="Start Menu",
                            command=lambda: controller.show_frame(StartPage))
        #button1.pack()
        button1.grid(row=1,column=2)


        button2 = ttk.Button(self, text="Time Series",
                            command=lambda: controller.show_frame(PageOne))
        #button2.pack()
        button2.grid(row=2,column=2)
        
        button3 = ttk.Button(self, text="Time Frame",
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=4, column=3)
        
        button5 = ttk.Button(self, text="Scatter Plot",
                                    command=lambda: controller.show_frame(PageTwo))
        button5.grid(row=3,column=2)
        
        button4 = ttk.Button(self, text="Histogram",
                            command=lambda: controller.show_frame(PageFour))
        button4.grid(row=4, column=2)
        
        
        label2 = tk.Label(self, text="\n\nSelect one variable from each row", font=NORM_FONT)
        #label2.pack(pady=10,padx=10)
        label2.grid(row=5,column=2)

            
        plotButton = ttk.Button(self, text="PLOT",
                            command=lambda: plot_wind_rose(ws_wd))
        #plotButton.pack() 
        plotButton.grid(row=6,column=2)
        
        
        label3 = tk.Label(self, text="wind speed column\t\twind direction column", font=LARGE_FONT)
        label3.grid(row=7,column=2)
        
            
        global ws_wd #wind speed, wind direction
        ws_wd=[None,None] #empty array, will host 2 variables for wind rose plot

        
        self.frame1 = VerticalScrolledFrame(self)
        self.frame1.grid(row=8, column=1, sticky="we")
        
        self.frame2 = VerticalScrolledFrame(self)
        self.frame2.grid(row=8, column=3, sticky="we")
            
        buttonsX = dict()
        for k in range(len(list_of_headers)):
            buttonsX=ttk.Button(self.frame1.interior, text = [list_of_headers[k]], command = partial(setX,list_of_headers[k],ws_wd))
                      
            #buttonsX.pack(expand=1, fill=tk.BOTH, side=tk.TOP, padx=200)
            buttonsX.grid(row=k+8,column=1, sticky="we")
        
        buttonsY = dict()
        for k in range(len(list_of_headers)):
            buttonsY=ttk.Button(self.frame2.interior, text = [list_of_headers[k]], command = partial(setY,list_of_headers[k],ws_wd))
                      
            #buttonsY.pack(expand=1, fill=tk.BOTH, side=tk.BOTTOM, padx=200)
            buttonsY.grid(row=k+8,column=3, sticky="we")
        
        
        




    
        

app = WindTurbineData()
app.lift()
app.mainloop()