from tkinter import messagebox
from tkintermapview import TkinterMapView
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

import json
from urllib.request import urlopen
import os
from PIL import Image, ImageTk
import sys
from src.wods.database import Database
from pathlib import Path

IMAGE_DIR = Path(__file__).resolve().parents[2] / "images"

class Gui:
    #------------------File -> Exit Method------------------#
    def exit(self):

        # message box that asks if they really want to quit the program or not
        self.exitWin = messagebox.askyesno("Are you sure?", "Are you sure you want to exit?")

        # if they clicked yes then it quits tkinter
        if(self.exitWin):
            self.main.destroy()

    #------------------Help -> About Method------------------#
    def aboutWindow(self):

        # show info message box that gives the info about the program
        self.aboutMsg = messagebox.showinfo("About", "Weather Observations Database v1.0\nCreated by Lucas Huang")

    #------------------Update Debug Label------------------#
    def updateDebug(self):

        # changes the string variable to the database debug variable and updates label
        self.varDebug.set(value=self.db.debug)
        self.lblDebug.config(fg=self.db.debugColor)

    #------------------Updates Entries that Show the Records------------------#
    def showDb(self, type):
        
        # checks if button can be used (not disconnected or adding a record)
        if (self.boolButton):

            try:
                # puts the entire database from select into "values" variable)
                self.values = self.db.select()

                # changes the id based on which button they pressed (forward, backward, etc.), i didnt want to make 6 different methods
                if (type == "fwd"):
                    if (self.id < len(self.values) - 1):
                        self.id += 1
                
                if (type == "bck"):
                    if (self.id > 0):
                        self.id -= 1

                if (type == "fwd2"):
                    if (self.id + 2 < len(self.values) - 1):
                        self.id += 2
                    else: 
                        self.id = len(self.values) - 1

                if (type == "bck2"):
                    if (self.id - 2 >= 0):
                        self.id -= 2
                    else: 
                        self.id = 0
                
                if (type == "end"):
                    self.id = len(self.values) - 1

                if (type == "start"):
                    self.id = 0

                # variable for the record and updates DATABASE id variable
                data = self.values[self.id]
                self.idDb = data[0]

                # updates id string variable to id for the label, changes background so there isnt a... 
                # ...random box before connecting (which first calls the method)
                self.idVar.set(self.idDb)
                self.lblId.config(bg=self.frameBtnBG)

                # splits "DATE" datatype in sqlite into 2 strings, if it doesnt work then it makes the data and time nothing
                try:
                    day, time = data[1].split(" ")
                except:
                    day = ""
                    time = ""
                
                # changes all the string variables and updates the entries
                self.varTemp.set(data[2])
                self.varDewp.set(data[3])
                self.varDrct.set(data[4])
                self.varWspd.set(data[5])
                self.varGust.set(data[6])
                self.varMslp.set(data[7])
                self.varDay.set(day)
                self.varTime.set(time)

                self.entryTemp.config()
                self.entryDewp.config()
                self.entryDrct.config()
                self.entryWspd.config()
                self.entryGust.config()
                self.entryMslp.config()
                self.entryDay.config()
                self.entryTime.config()
            
            # in case of a random python error
            except Exception as error:
                print(error)
                print(sys.exc_info()[-1].tb_lineno)
            
            # updates debug message
            self.updateDebug()

    #------------------Reset Entries------------------#
    def resetEntry(self):

        # sets all entries and string variables to nothing
        self.varTemp.set("")
        self.varDewp.set("")
        self.varDrct.set("")
        self.varWspd.set("")
        self.varGust.set("")
        self.varMslp.set("")
        self.varDay.set("")
        self.varTime.set("")
        self.idVar.set("")

        self.entryTemp.config()
        self.entryDewp.config()
        self.entryDrct.config()
        self.entryWspd.config()
        self.entryGust.config()
        self.entryMslp.config()
        self.entryDay.config()
        self.entryTime.config()
    
    #------------------Connect to Database------------------#
    def connectDb(self):
        
        # turns on the rest of the buttons
        self.boolButton = True

        # calls connect method from database, updates debug, and shows the first record
        self.db.connect()
        self.updateDebug()

        self.dropdownTables.config(values=self.db.tables)

        # changes connect button to disconnect butto
        self.btnConnect = tk.Button(self.frame, text="Disconnect", height=1, width=10, bg="#368B3A", 
                                    fg=self.frameBtnFG, command=self.disconnectDb)
        self.btnConnect.place(x=150, y=self.crudY, anchor=tk.CENTER)

    #------------------Select Table------------------#
    def selectTb(self):
        
        # once the table is selected, the records will be shown
        self.db.table = self.dropdownTables.get()
        self.showDb(None)
        self.updateDebug()

    #------------------Disconnect from Database------------------#
    def disconnectDb(self):

        # calls connect method from database, updates debug, and shows the first record
        self.db.disconnect()
        self.updateDebug()

        # changes the entries back to nothing
        self.resetEntry()

        # changes connect button to disconnect button
        self.btnConnect = tk.Button(self.frame, text="Connect", height=1, width=10, bg="#368B3A", 
                                    fg=self.frameBtnFG, command=self.connectDb)
        self.btnConnect.place(x=150, y=self.crudY, anchor=tk.CENTER)

        # turns off rest of the buttons
        self.boolButton = False

    #------------------Add to Database (Add Button)------------------#
    def addRec(self):

        # checks if button can be used (not disconnected or adding a record)
        if (self.boolButton):

            # sets entries to nothing to type in
            self.resetEntry()

            # changes the button into the save button
            self.btnInsert = tk.Button(self.frame, text="Save", height=1, width=10, bg="#8B8A36", 
                                    fg=self.frameBtnFG, command=lambda: self.insertDb("add"))
            self.btnInsert.place(x=250, y=self.crudY, anchor=tk.CENTER)

            # changes update button to cancel
            self.btnCancel = tk.Button(self.frame, text="Cancel", height=1, width=10, bg=self.frameBtnBG, 
                                    fg=self.frameBtnFG, command=lambda: self.insertDb(None))
            self.btnCancel.place(x=450, y=self.crudY, anchor=tk.CENTER)

            # turns off rest of the buttons
            self.boolButton = False

    #------------------Insert to Database (Save Button)------------------#
    def insertDb(self, type):

        # turns on the rest of the buttons
        self.boolButton = True
        
        # if the button is the "add" button
        if (type == "add"):
            # sets tuple for inserting record
            self.db.insRec = [self.entryDay.get() + " " + self.entryDay.get(), self.entryTemp.get(), self.entryDewp.get(), 
                              self.entryDrct.get(), self.entryWspd.get(), self.entryGust.get(), self.entryMslp.get()]

            # calls insert method from database, and updates record and debug
            self.id = self.db.insert(self.idDb, self.values) - 1

        # updates entries and debug message
        self.showDb(None)
        self.updateDebug()

        # changes save back to add
        self.btnInsert = tk.Button(self.frame, text="Add", height=1, width=10, bg="#8B8A36", 
                                   fg=self.frameBtnFG, command=self.addRec)
        self.btnInsert.place(x=250, y=self.crudY, anchor=tk.CENTER)

        # changes cancel back to update
        self.btnUpdate = tk.Button(self.frame, text="Update", height=1, width=10, bg=self.frameBtnBG, 
                                   fg=self.frameBtnFG, command=self.updateDb)
        self.btnUpdate.place(x=450, y=self.crudY, anchor=tk.CENTER)
    
    #------------------Update Record------------------#
    def updateDb(self):
        
        # checks if button can be used (not disconnected or adding a record)
        if (self.boolButton):

            # updates the update record tuple and runs the update method, then it updates debug
            self.db.upRec = [self.entryDay.get() + " " + self.entryTime.get(), self.entryTemp.get(), self.entryDewp.get(), 
                             self.entryDrct.get(), self.entryWspd.get(), self.entryGust.get(), self.entryMslp.get(), self.idDb]
            self.db.update()
            self.updateDebug()
    
    #------------------Delete Record------------------#
    def deleteDb(self):

        # checks if button can be used (not disconnected or adding a record)
        if (self.boolButton):

            # first shows a pop up on if they really want to delete the record
            self.deleteAns = messagebox.askyesno("Are you sure?", "Are you sure you want to delete this?")
            
            # if they click yes, then it deletes the record, updates the debug, and shows the next available record
            if (self.deleteAns):
                self.id = self.db.delete(self.idDb, self.values) 
                self.updateDebug()
                self.showDb(None)
    
    #------------------Select a State------------------#
    def selectNetwork(self, dropdown):
        
        # delets all previous markers and resets the dropdown text
        self.map_widget.delete_all_marker()
        self.dropdownStation.set("Select a Station")

        # creates new empty lists for the station id, location, and each marker for each station
        self.stationid = []
        self.stationLoc = []
        self.markers = []

        # creates ImageTk image (TkinterMapView only allows this type)
        self.locationIcon = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "circle.png")).resize((10, 10)))
        self.locationIcon2 = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "green.png")).resize((10, 10)))

        # gets the state selected in the dropdown and converts it to the network code
        state = dropdown.get()
        self.network = self.states[state]

        # opens json file with all the stations on it from a website
        url = f"https://mesonet.agron.iastate.edu/geojson/network/{self.network}.geojson"
        jdict = json.load(urlopen(url))

        # adds each station id and coordinates to the empty lists
        for site in jdict["features"]:
            self.stationid.append(site["properties"]["sid"])
            self.stationLoc.append(site["geometry"]["coordinates"])

        # places a marker for each station on the map
        for i in range(len(self.stationLoc)):
            marker = self.map_widget.set_marker(self.stationLoc[i][1], self.stationLoc[i][0], text_color="green", font=("Helvetica Bold", 12), icon=self.locationIcon, command=self.onClick)
            marker.stationid = self.stationid[i]

            self.markers.append(marker)

        # changes the values in the dropdown of the station
        self.dropdownStation.config(values=self.stationid)

    #------------------Station Clicked Method-----------------#
    def onClick(self, marker):
        
        # checks if a station had already been selected previously, and changes it back to the default
        if self.selectedMarker is not None:
            self.selectedMarker.change_icon(self.locationIcon)

        # changes the clicked station green
        marker.change_icon(self.locationIcon2)
        self.selectedMarker = marker

        # changes the dropdown text to the id of station
        self.dropdownStation.set(marker.stationid)

    #------------------Download Data Method-----------------#
    def retrieveData(self):

        # error if the user did not put a name
        if (self.entryDataName.get() == ""):
            messagebox.showerror(title="An Error Occured", message="The table must have a name!")

        # error if the user put a space as the table name
        if (" " in self.entryDataName.get()):
            messagebox.showerror(title="An Error Occured", message="The table name cannot have a space")

        else:
            
            # gets ASOS data from database class
            self.db.getAsos(self.network, self.dropdownStation.get(), self.entryHours.get(), self.entryDataName.get())
            
            # updates the tables and the dropdown
            self.db.getTables()
            self.dropdownTables.config(values=self.db.tables)

    #------------------"Get Data" Popup Window------------------#
    def getData(self):
        
        if (self.db.connected):
            # variable used to store the marker (station) that was last clicked
            self.selectedMarker = None

            # making a popup and a frame
            self.dataWin = tk.Toplevel()
            self.frameData = tk.Frame(self.dataWin, width=800, height=80, bg=self.frameBG)
            self.frameData.grid(row=0, column=0)

            # labels for the window
            self.lblDataState = tk.Label(self.frameData, text="State:", bg=self.frameBG)
            self.lblDataStation = tk.Label(self.frameData, text="Station:", bg=self.frameBG)
            self.lblDataPast = tk.Label(self.frameData, text="Past:", bg=self.frameBG)
            self.lblDataHour = tk.Label(self.frameData, text="Hours", bg=self.frameBG)
            self.lblDataName = tk.Label(self.frameData, text="Table Name", bg=self.frameBG)

            # entries for the window
            self.entryDataName = tk.Entry(self.frameData, bd=2, width=15, relief="sunken")
            self.entryHours = tk.Entry(self.frameData, bd=2, width=15, relief="sunken")
            self.btnStateSubmit = tk.Button(self.frameData, text="Select", height=1, width=5, bg=self.frameBtnBG, 
                                    fg=self.frameBtnFG, command=lambda: self.selectNetwork(self.dropdownState))
            self.btnDataSubmit = tk.Button(self.frameData, text="Submit", height=1, width=5, bg=self.frameBtnBG, 
                                    fg=self.frameBtnFG, command=self.retrieveData)

            # list for all 50 states in the US
            # specific list called a "dictionary", the left is what is displayed in the dropdown, right is the network id for the state
            self.states = {"Alaska": "AK_ASOS", "Alabama": "AL_ASOS", "Arkansas": "AR_ASOS",
                                "Arizona": "AZ_ASOS", "California": "CA_ASOS", "Colorado": "CO_ASOS",
                                "Connecticut": "CT_ASOS", "Delaware": "DE_ASOS", "Florida": "FL_ASOS",
                                "Georgia": "GA_ASOS", "Hawaii": "HI_ASOS", "Iowa": "IA_ASOS",
                                "Idaho": "ID_ASOS", "Illinois": "IL_ASOS", "Indiana": "IN_ASOS",
                                "Kansas": "KS_ASOS", "Kentucky": "KY_ASOS", "Louisiana": "LA_ASOS",
                                "Massachusetts": "MA_ASOS", "Maryland": "MD_ASOS", "Maine": "ME_ASOS",
                                "Michigan": "MI_ASOS", "Minnesota": "MN_ASOS", "Mississippi": "MS_ASOS",
                                "Missouri": "MO_ASOS", "Montana": "MT_ASOS", "North Carolina": "NC_ASOS",
                                "North Dakota": "ND_ASOS", "Nebraska": "NE_ASOS", "New Hampshire": "NH_ASOS",
                                "New Jersey": "NJ_ASOS", "New Mexico": "NM_ASOS", "Nevada": "NV_ASOS",
                                "New York": "NY_ASOS", "Ohio": "OH_ASOS", "Oklahoma": "OK_ASOS",
                                "Oregon": "OR_ASOS", "Pennsylvania": "PA_ASOS", "Rhode Island": "RI_ASOS",
                                "South Carolina": "SC_ASOS", "South Dakota": "SD_ASOS", "Tennessee": "TN_ASOS",
                                "Texas": "TX_ASOS", "Utah": "UT_ASOS", "Virginia": "VA_ASOS",
                                "Vermont": "VT_ASOS", "Washington": "WA_ASOS", "Wisconsin": "WI_ASOS",
                                "West Virginia": "WV_ASOS", "Wyoming": "WY_ASOS"}
            
            # defining variable for a list of station id's for each state
            self.stationid = []

            # dropdown for selecting a state
            self.dropdownState = ttk.Combobox(self.dataWin, values=list(self.states.keys()), state="readonly")
            self.dropdownState.set("Select a State")
            self.dropdownState.place(x=60, y=10)

            # dropdown for selecting a station
            self.dropdownStation = ttk.Combobox(self.dataWin, values=self.stationid, state="readonly")
            self.dropdownStation.set("Select a Station")
            self.dropdownStation.place(x=350, y=10)
            
            # placing each label
            self.lblDataState.place(x=20, y=10)
            self.lblDataStation.place(x=300, y=10)
            self.lblDataPast.place(x=20, y=40)
            self.lblDataHour.place(x=165, y=40)
            self.lblDataName.place(x=520, y=10)
            
            # placing each entry
            self.entryHours.place(x=60, y=40)
            self.entryDataName.place(x=610, y=10)

            # placing each button
            self.btnStateSubmit.place(x=215, y=8)
            self.btnDataSubmit.place(x=215, y=38)
            
            # creates a map using tkintermapview library
            # sets the zoom and the latitude and longitude where it is centered
            self.map_widget = TkinterMapView(self.dataWin, width=800, height=700, corner_radius=0)
            self.map_widget.set_zoom(3)
            self.map_widget.set_position(53, -117)
            self.map_widget.grid(row=1, column=0)

            # sets the map to be from google maps
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # error if not connected to database
        else:
            messagebox.showerror(title="An Error Occured", message="Not connected to database!")
    
    #------------------Graph Popup Window------------------#
    def graph(self, option):
        
        if (self.db.connected):
            if (self.db.table is not None):
                try:
                    # makes a popup for the graph
                    self.graphWin = tk.Toplevel()

                    # creates a figure with a size, and adds a plot to it
                    fig = plt.Figure(figsize=(14, 8))
                    plot = fig.add_subplot(111)

                    # t for temperature plot
                    if (option == "t"):
                        
                        # list that removes all None
                        filtered = [row for row in self.values if row[2] is not None]

                        # creates a list of each column using the filtered list
                        T = [row[2] for row in filtered]
                        Td = [row[3] for row in filtered]
                        valid = [row[1] for row in filtered]

                        # turns SQL time into pandas datetime
                        time = pd.to_datetime(valid)

                        # plots each column with matplotlib into the subplot
                        plot.plot(time, T, color="red", lw=3)
                        plot.plot(time, Td, color="green", lw=3)

                        # places a marker at the end of the line
                        plot.plot(time[-1], T[-1], color="black", marker="o", ms=10)
                        plot.plot(time[-1], Td[-1], color="black", marker="o", ms=10)

                        # labels the marker with the temperature and dewpoint
                        plot.annotate(str(T[-1]) + "F", (time[-1], T[-1]), textcoords="offset points", xytext=(-10, 10), fontweight="bold")
                        plot.annotate(str(Td[-1]) + "F", (time[-1], Td[-1]), textcoords="offset points", xytext=(-10, 10), fontweight="bold")

                        # shades between each line
                        plot.fill_between(time, T, Td, color="#212338", alpha=0.25)

                        # sets title and label of the plot
                        plot.set_title("Temperature and Dewpoint", fontweight="bold", fontsize="xx-large")
                        plot.set_ylabel("Temperature (F)", fontweight="bold", fontsize="large")

                    # mslp for pressure plot
                    if (option == "mslp"):
                        
                        # list that removes all None
                        filtered = [row for row in self.values if row[7] is not None]

                        # creates a list of each column with the filtered list
                        mslp = [row[7] for row in filtered]
                        valid = [row[1] for row in filtered]

                        # turns SQL time into pandas datetime
                        time = pd.to_datetime(valid)

                        # plots pressure and marker
                        plot.plot(time, mslp, color="#0E113F", lw=3)
                        plot.plot(time[-1], mslp[-1], color="black", marker="o", ms=10)

                        # places a marker at the end of the line
                        plot.annotate(str(mslp[-1]) + " hPa", (time[-1], mslp[-1]), textcoords="offset points", xytext=(-30, 10), fontweight="bold")

                        # sets title and labels
                        plot.set_title("Pressure", fontweight="bold", fontsize="xx-large")
                        plot.set_ylabel("Pressure (hPa)", fontweight="bold", fontsize="large")

                # creates error message and prints out error in terminal
                except Exception as error:
                    messagebox.showerror(title="An Error Occured", message="Unable to create a graph")
                    print(error)

            # error message for no table
            else:
                messagebox.showerror(title="An Error Occured", message="No table selected")

        # error message for not connecting
        else:
            messagebox.showerror(title="An Error Occured", message="Not connected to database!")

        # wspd for windspeed plot
        if (option == "wspd"):

            # list that removes all None
            filtered = [row for row in self.values if row[5] is not None]

            # creates a list of each column with the filtered list
            wspd = [row[5] for row in filtered]
            valid = [row[1] for row in filtered]

            # turns SQL time into pandas datetime
            time = pd.to_datetime(valid)

            # smoothed out windspeed with scipy "savgol filter"
            smooth_wspd = savgol_filter(wspd, 32, 2)

            # plots each column and the marker
            plot.plot(time, wspd, color="gray", lw=1)
            plot.plot(time, smooth_wspd, color="#0E113F", lw=3)
            plot.plot(time[-1], wspd[-1], color="black", marker="o", ms=10)
            plot.annotate(str(wspd[-1]) + " mph", (time[-1], wspd[-1]), textcoords="offset points", xytext=(-30, 10), fontweight="bold")
            
            # sets title and label of plot
            plot.set_title("Windspeed", fontweight="bold", fontsize="xx-large")
            plot.set_ylabel("Windspeed (mph)", fontweight="bold", fontsize="large")

        # adds x and y grid to the graph with a dotted line
        plot.grid(True, linestyle='--', lw=1, alpha=0.5)

        # title of the plot
        plot.set_xlabel("Time (UTC)", fontweight="bold", fontsize="large")

        # FigureCanvasTkAgg connects matplotlib canvas to tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graphWin)
        canvas.draw()

        canvas.get_tk_widget().pack()

    #------------------Interpolate Method------------------#
    def interpolate(self):
        messagebox.showinfo(title="Coming Soon", message="Interpolate Coming Soon")

    #------------------Constructor Method------------------#
    def __init__(self):
        
        # new database class
        self.db = Database()

        # main tkinter window
        self.main = tk.Tk()

        # sets all string variables
        self.varTemp = tk.StringVar()
        self.varDewp = tk.StringVar()
        self.varDrct = tk.StringVar()
        self.varWspd = tk.StringVar()
        self.varGust = tk.StringVar()
        self.varMslp = tk.StringVar()
        self.varDay = tk.StringVar()
        self.varTime = tk.StringVar()
        self.varDebug = tk.StringVar(value=self.db.debug)

        # id is the TUPLE id for going between values, used in case one id is missing
        self.id = 0

        # seperate variable for the id in the database
        self.idDb = 1

        # string variable for id that shows what id the program is on
        self.idVar = tk.StringVar()
        self.values = None

        # boolean for whether the buttons are active or not
        # they are not active when disconnected or adding a record
        self.boolButton = False

        # title of main window
        self.main.title("Weather Obs")

        # sets icon of application
        self.icon = tk.PhotoImage(file=os.path.join(IMAGE_DIR, "4834585.png"))
        self.main.iconphoto(False, self.icon)

        #------------------MAIN FRAME CODE------------------# 

        # sets color variables
        self.frameBG = "#BBE7F0"
        self.frameBtnBG = "#36708B"
        self.frameBtnFG = "white"

        # main frame variable
        self.frame = tk.Frame(self.main, width=600, height=420, bg=self.frameBG)

        # makes a menubar
        self.menubar = tk.Menu(self.frame)

        # makes the menu for file
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Get Data", command=self.getData)
        self.fileMenu.add_command(label="Interpolate", command=self.interpolate)
        self.fileMenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        # makes menu for graphing
        self.graphMenu = tk.Menu(self.menubar, tearoff=0)
        self.graphMenu.add_command(label="Temp and Dewp", command=lambda: self.graph("t"))
        self.graphMenu.add_command(label="Pressure", command=lambda: self.graph("mslp"))
        self.graphMenu.add_command(label="Windspeed", command=lambda: self.graph("wspd"))
        self.menubar.add_cascade(label="Graph", menu=self.graphMenu)

        # makes the menu for exit
        self.exitMenu = tk.Menu(self.menubar, tearoff=0)
        self.exitMenu.add_command(label="About", command=self.aboutWindow)
        self.menubar.add_cascade(label="Help", menu=self.exitMenu)

        # connect, update, delete buttons (bottom buttons)
        self.btnConnect = tk.Button(self.frame, text="Connect", height=1, width=10, bg="#368B3A", 
                                    fg=self.frameBtnFG, command=self.connectDb)
        self.btnUpdate = tk.Button(self.frame, text="Update", height=1, width=10, bg=self.frameBtnBG, 
                                   fg=self.frameBtnFG, command=self.updateDb)
        self.btnDelete = tk.Button(self.frame, text="Delete", height=1, width=10, bg="#8B5136", 
                                   fg=self.frameBtnFG, command=self.deleteDb)
        self.btnSelectTable = tk.Button(self.frame, text="Select", height=1, width=10, bg=self.frameBtnBG, 
                                    fg=self.frameBtnFG, command=self.selectTb)
        self.btnInsert = tk.Button(self.frame, text="Add", height=1, width=10, bg="#8B8A36", 
                                   fg=self.frameBtnFG, command=self.addRec)

        # changing record buttons (top buttons)
        self.btnForward = tk.Button(self.frame, text=">", height=1, width=5, bg=self.frameBtnBG, 
                                    fg=self.frameBtnFG, command=lambda: self.showDb("fwd"))
        self.btnForwardTwo = tk.Button(self.frame, text=">>", height=1, width=5, bg=self.frameBtnBG, 
                                    fg=self.frameBtnFG, command=lambda: self.showDb("fwd2"))
        self.btnEnd = tk.Button(self.frame, text="->|", height=1, width=5, bg=self.frameBtnBG, 
                                fg=self.frameBtnFG, command=lambda: self.showDb("end"))
        self.btnBackward = tk.Button(self.frame, text="<", height=1, width=5, bg=self.frameBtnBG, 
                                     fg=self.frameBtnFG, command=lambda: self.showDb("bck"))
        self.btnBackwardTwo = tk.Button(self.frame, text="<<", height=1, width=5, bg=self.frameBtnBG, 
                                     fg=self.frameBtnFG, command=lambda: self.showDb("bck2"))
        self.btnStart = tk.Button(self.frame, text="|<-", height=1, width=5, bg=self.frameBtnBG, 
                                  fg=self.frameBtnFG, command=lambda: self.showDb("start"))

        # Label for the entries
        self.lblTemp = tk.Label(self.frame, text="Temperature (F)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblDewp = tk.Label(self.frame, text="Dewpoint (F)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblDrct = tk.Label(self.frame, text="Wind Direction (Deg)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblWspd = tk.Label(self.frame, text="Wind Speed (mph)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblGust = tk.Label(self.frame, text="Wind Gust (mph)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblMslp = tk.Label(self.frame, text="Pressure (hPa)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblDay = tk.Label(self.frame, text="Day (YYYY-MM-DD)", bg=self.frameBG, font=("Helvetica", 10))
        self.lblTime = tk.Label(self.frame, text="Time (HH:MM:SS)", bg=self.frameBG, font=("Helvetica", 10))

        # Entries that show data of records
        self.entryTemp = tk.Entry(self.frame, textvariable=self.varTemp)
        self.entryDewp = tk.Entry(self.frame, textvariable=self.varDewp)
        self.entryDrct = tk.Entry(self.frame, textvariable=self.varDrct)
        self.entryWspd = tk.Entry(self.frame, textvariable=self.varWspd)
        self.entryGust = tk.Entry(self.frame, textvariable=self.varGust)
        self.entryMslp = tk.Entry(self.frame, textvariable=self.varMslp)
        self.entryDay = tk.Entry(self.frame, textvariable=self.varDay)
        self.entryTime = tk.Entry(self.frame, textvariable=self.varTime)

        # Debug and Id labels
        self.lblDebug = tk.Label(self.frame, textvariable=self.varDebug, bg=self.frameBG, fg=self.db.debugColor)
        self.lblId = tk.Label(self.frame, textvariable=self.idVar, bg=self.frameBG, fg=self.frameBtnFG)

        self.dropdownTables = ttk.Combobox(self.frame, values=self.db.tables, state='readonly')
        self.dropdownTables.set("Select a Table")

        # placing Debug and Id
        self.lblDebug.place(x=5, y=5)
        self.lblId.place(x=595, y=5, anchor="ne")

        # placing all the top buttons from left to right
        indexbtnY = 380
        self.btnStart.place(x=175, y=indexbtnY, anchor=tk.CENTER)
        self.btnBackwardTwo.place(x=225, y=indexbtnY, anchor=tk.CENTER)
        self.btnBackward.place(x=275, y=indexbtnY, anchor=tk.CENTER)
        self.btnForward.place(x=325, y=indexbtnY, anchor=tk.CENTER)
        self.btnForwardTwo.place(x=375, y=indexbtnY, anchor=tk.CENTER)
        self.btnEnd.place(x=425, y=indexbtnY, anchor=tk.CENTER)

        # placing all the labels for entries from top to bottom
        valuesY = 70
        self.lblTemp.place(x=130, y=valuesY)
        self.lblDewp.place(x=130, y=valuesY + 30)
        self.lblDrct.place(x=130, y=valuesY + 60)
        self.lblWspd.place(x=130, y=valuesY + 90)
        self.lblGust.place(x=130, y=valuesY + 120)
        self.lblMslp.place(x=130, y=valuesY + 150)
        self.lblDay.place(x=130, y=valuesY + 180)
        self.lblTime.place(x=130, y=valuesY + 210)
        
        # placing all entries of records from top to bottom
        self.entryTemp.place(x=330, y=valuesY)
        self.entryDewp.place(x=330, y=valuesY + 30)
        self.entryDrct.place(x=330, y=valuesY + 60)
        self.entryWspd.place(x=330, y=valuesY + 90)
        self.entryGust.place(x=330, y=valuesY + 120)
        self.entryMslp.place(x=330, y=valuesY + 150)
        self.entryDay.place(x=330, y=valuesY + 180)
        self.entryTime.place(x=330, y=valuesY + 210)

        # placing all the bottom buttons from left to right
        self.crudY = indexbtnY - 35
        self.btnConnect.place(x=150, y=self.crudY, anchor=tk.CENTER)
        self.btnInsert.place(x=250, y=self.crudY, anchor=tk.CENTER)
        self.btnDelete.place(x=350, y=self.crudY, anchor=tk.CENTER)
        self.btnUpdate.place(x=450, y=self.crudY, anchor=tk.CENTER)

        self.tableY = 40
        self.dropdownTables.place(x=250, y=self.tableY, anchor=tk.CENTER)
        self.btnSelectTable.place(x=380, y=self.tableY, anchor=tk.CENTER)

        # puts the frame on the bottom row
        self.frame.grid(row=0, column=0)
        
        # adds the menubar to the main window
        self.main.config(menu=self.menubar)
        self.main.mainloop()

        # prints connection closed after mainloop is closed
        print("Connection Closed")
