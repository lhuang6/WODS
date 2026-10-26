import tkinter
from tkintermapview import TkinterMapView
import json
from urllib.request import urlopen
import os
from PIL import Image, ImageTk

stationid = []
stationLoc = []
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

markers = []
selected_marker = None

# Get metadata

uri = (
    "https://mesonet.agron.iastate.edu/"
    f"geojson/network/AK_ASOS.geojson"
)
data = urlopen(uri)
jdict = json.load(data)

for site in jdict["features"]:
    stationid.append(site["properties"]["sid"])
    stationLoc.append(site["geometry"]["coordinates"])

root_tk = tkinter.Tk()
root_tk.geometry(f"{600}x{400}")
root_tk.title("Alaska ASOS")

current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
locationIcon = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "circle.png")).resize((10, 10)))
locationIcon2 = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "green.png")).resize((10, 10)))

# create map widget
map_widget = TkinterMapView(root_tk, width=600, height=400, corner_radius=0)
map_widget.set_zoom(3)
map_widget.set_position(53, -117)
map_widget.pack(fill="both", expand=True)

# google normal tile server
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# set current widget position by address
# marker_2 = map_widget.set_marker(70.136, -146.2901, text="Brandenburger Tor")

def onClick(marker):
    global selected_marker

    # reset previous marker back to blue
    if selected_marker is not None:
        selected_marker.change_icon(locationIcon)

    # set new marker to green
    marker.change_icon(locationIcon2)

    # update selected marker
    selected_marker = marker

    print(marker.station_id)

for i in range(len(stationLoc)):
    marker = map_widget.set_marker(stationLoc[i][1], stationLoc[i][0], text_color="green", font=("Helvetica Bold", 12), icon=locationIcon, command=onClick)
    marker.station_id = stationid[i]

    markers.append(marker)

root_tk.mainloop()