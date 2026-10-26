from database import Database
import sqlite3
import pandas as pd
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt


import requests


"""link = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?network=MO_ASOS&station=STL&data=tmpf&data=tmpc&hours=24&missing=null&report_type=3&report_type=4'
response = requests.get(link).text

with open('data.csv', 'w') as f:
    f.write(response)

df = pd.read_csv("data.csv")
df = df.drop(columns=["station"])
df = df.dropna()

print(df)"""

"""connection = sqlite3.connect("test.sqlite")

df.to_sql("records", connection, if_exists="replace")

cursor = connection.cursor()
cursor.execute("SELECT * FROM records;")

print(cursor.fetchall())

connection.close()
"""
"""stationid = []
stationName = []
states = ['AK_ASOS', 'AL_ASOS', 'AR_ASOS', 'AZ_ASOS', 'CA_ASOS', 
          'CO_ASOS', 'CT_ASOS', 'DE_ASOS', 'FL_ASOS', 'GA_ASOS', 
          'HI_ASOS', 'IA_ASOS', 'ID_ASOS', 'IL_ASOS', 'IN_ASOS', 
          'KS_ASOS', 'KY_ASOS', 'LA_ASOS', 'MA_ASOS', 'MD_ASOS', 
          'ME_ASOS', 'MI_ASOS', 'MN_ASOS', 'MO_ASOS', 'MS_ASOS', 
          'MT_ASOS', 'NC_ASOS', 'ND_ASOS', 'NE_ASOS', 'NH_ASOS', 
          'NJ_ASOS', 'NM_ASOS', 'NV_ASOS', 'NY_ASOS', 'OH_ASOS', 
          'OK_ASOS', 'OR_ASOS', 'PA_ASOS', 'RI_ASOS', 'SC_ASOS', 
          'SD_ASOS', 'TN_ASOS', 'TX_ASOS', 'UT_ASOS', 'VA_ASOS', 
          'VT_ASOS', 'WA_ASOS', 'WI_ASOS', 'WV_ASOS', 'WY_ASOS']

# Get metadata
uri = (
    "https://mesonet.agron.iastate.edu/"
    f"geojson/network/AK_ASOS.geojson"
)

data = urlopen(uri)
jdict = json.load(data)
for site in jdict["features"]:
    stationid.append(site["properties"]["sid"])
    stationName.append(site["geometry"]["coordinates"])
print(stationName[0][0])"""

date = pd.to_datetime("2026-04-27 09:51")
print(date.month)
print(date.day)
print(date.hour)
print(date.minute)