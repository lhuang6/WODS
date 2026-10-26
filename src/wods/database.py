import sqlite3
import tkinter as tk
import requests
import pandas as pd
import numpy as np
import sys
from pathlib import Path

class Database:
    
    #------------------Database Class Constructor------------------#
    def __init__(self):
        self.projectRoot = Path(__file__).resolve().parents[2]
        self.dataDir = self.projectRoot / "data"

        # tuples for inserting and updating records
        self.insRec = ["", "", "", "", "", "", ""]
        self.upRec = ["", "", "", "", "", "", "", 0]
        self.table = None
        self.database = self.dataDir / "asos.sqlite"
        self.tables = []
        self.connected = False

        # debug variables for GUI class
        self.debug = "Not Connected"
        self.debugColor = "black"

        # variable for the sqlite queries
        self.query = ""
    
    #------------------Connect to the Database------------------#
    def connect(self):

        # try to connect to database
        try:
            
            # connecting to sqlite and setting a cursor
            self.sqlConnection = sqlite3.connect(self.database)
            self.cursor = self.sqlConnection.cursor()
            self.connected = True

            # retrieves tables from database
            self.getTables()
            
            # changes to a successful debug code
            self.debug = "Connection Successful"
            self.debugColor = "green"
            print(self.debug)
            
        # changes to error code if connection fails
        except Exception as error:
            self.debugColor = "red"
            self.debug = "Error Connecting to Database"
            print(str(error))

    #------------------Retrieve Tables------------------#
    def getTables(self):

        try:
            
            # query statement that selects all tables 
            self.query = "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            self.cursor.execute(self.query)

            self.tables = [tables[0] for tables in self.cursor.fetchall()]
            print(self.tables)

        # changes to error code if it fails
        except Exception as error:
            self.debugColor = "red"
            self.debug = "Error Retrieving Tables"
            print(str(error))
    
    #------------------Disconnect into Database------------------#
    def disconnect(self):

        try:
            # Closes Cursor and Connection
            self.cursor.close()
            self.sqlConnection.close()
            self.connected = False

            # changes to a successful debug code
            self.debug = "Not Connected"
            self.debugColor = "black"
            print(self.debug)
        
        # changes to error code if disconnection fails
        except Exception as error:
            self.debugColor = "red"
            self.debug = "Error Connecting to Database"
            print(str(error))

    #------------------Insert into Database------------------#
    def insert(self, id, values):

        # try to put in insert query
        try:
            
            # changes query for inserting and executes the values in the tuple
            self.query = "INSERT INTO " + self.table + " (valid, tmpf, dwpf, drct, sped, mslp, gust_mph) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.cursor.execute(self.query, self.insRec)
            self.sqlConnection.commit()

            # print(self.query)
            # changes id to the new id at the end
            id = len(values) + 1
            
            # changes to a successful debug code
            self.debug = "Insertion Complete"
            self.debugColor = "green"
            print(self.debug)

        # changes to error code if connection fails
        except Exception as error:
            self.debugColor = "red"
            self.debug = "Error Inserting Record"
            print(str(error))

        # returns new id
        return id
        
    #------------------Select All------------------#
    def select(self):

        # try to select all from the database to store in a variable in the gui class
        try:
            
            # executes selecting all, doesn't need a tuple
            self.query = "SELECT * FROM " + self.table + " ORDER BY valid ASC;"
            self.cursor.execute(self.query)

            # no need for explicit success debug code because it's not a specific button
            return self.cursor.fetchall()
        
        # changes to error code if connection fails
        except Exception as error:
            print(str(error))


    #------------------Update Database------------------#
    def update(self):
        
        # try to put in query to update and executes values in tuple
        try:
            self.query = 'UPDATE ' + self.table + ' SET valid = ?, tmpf = ?, dwpf = ?, drct = ?, sped = ?, gust_mph = ?, mslp = ? WHERE "index" = ?'
            self.cursor.execute(self.query, self.upRec)
            self.sqlConnection.commit()

            # changes to a successful debug code
            self.debug = "Updated Record"
            self.debugColor = "green"
            print(self.debug)

        # changes to error code if connection fails
        except Exception as error:
            self.debugColor = "red"
            self.debug = "Error Updating Database"
            print(str(error))

    #------------------Delete Database Record------------------#
    def delete(self, id, values):
        
        # try to delete a record from database by inputting the id
        try:
            self.query = "DELETE FROM " + self.table + " WHERE 'index' = ?;"
            self.cursor.execute(self.query, str(id))
            self.sqlConnection.commit()

            # change id to the one before if deleted the last record
            print(id)
            if (id == len(values)):
                id = len(values) - 2
                print("here")

            # changes to a successful debug code
            self.debug = "Deleted Record"
            self.debugColor = "green"
            print(self.debug)

        # changes to error code if connection fails
        except Exception as error:
            self.debugColor = "red"
            self.debug = "Error Deleting Record"
            print(str(error))

        # returns new id for indexing
        return id

    #------------------Converting ASOS CSV into SQL Table------------------#
    def readAsos(self, file, name):
        
        try:
            # first creates a new table with all of the columns
            self.query = f"""
                CREATE TABLE {name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    valid DATETIME,
                    tmpf FLOAT,
                    dwpf FLOAT,
                    drct FLOAT,
                    sped FLOAT,
                    gust_mph FLOAT,
                    mslp FLOAT
                );
                """
            
            # commits and executes the query
            self.cursor.execute(self.query)
            self.sqlConnection.commit()

            # pandas reads the csv as a dataframe object
            df = pd.read_csv(file)

            # new query to insert every datapoint from CSV into the table
            self.query = "INSERT INTO " + name + " (valid, tmpf, dwpf, drct, sped, mslp, gust_mph) VALUES (?, ?, ?, ?, ?, ?, ?)"

            # for loop to insert each row in the pandas dataframe as a new record in the table
            for index, row in df.iterrows():
                self.insRec = [row['valid'], row['tmpf'], row['dwpf'], row['drct'], row['sped'], row['mslp'], row['gust_mph']]
                self.cursor.execute(self.query, self.insRec)
                print(row['valid'])

            self.sqlConnection.commit()

        # prints error
        except Exception as error:
            print(sys.exc_info()[-1].tb_lineno)
            print(str(error))

    #------------------Getting Data from Internet------------------#
    def getAsos(self, network, station, hours, name):

        try:
            # link to website that gets the data
            link = (
                f'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?network={network}&station={station}'
                f'&data=tmpf&data=dwpf&data=drct&data=sped&data=gust_mph&data=mslp&hours={hours}&missing=null'
                )
            
            # turns website data into a string
            response = requests.get(link).text

            # turns the website text into a csv
            # uses a with loop to ensure the file is closed when it is done writing
            with open('data.csv', 'w') as f:
                f.write(response)

            # calls its own readAsos function to turn csv into an SQL table
            self.readAsos('data.csv', name)
        
        # prints error
        except Exception as error:
            print(str(error))