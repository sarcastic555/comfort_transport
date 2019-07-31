import os
import numpy as np
import json
import requests

HTTPS = "https://api-tokyochallenge.odpt.org/api/v4/odpt:BusstopPole?odpt:operator=odpt.Operator:"
KEY = "&acl:consumerKey="
CONSUMERKEY = os.environ['env_token']

f = lambda x: True if x is None else False


def readout_json_bus_stops(company):
    busstops_in = requests.get(HTTPS + company + KEY + CONSUMERKEY)
    busstops = busstops_in.json()
    list_bus_stops = []
    for busstop in busstops:
        if( f(busstop["geo:lat"]) ):
            continue
        dict_bus_stop = {}
        for component in ["odpt:note", "@id", "geo:lat", "geo:long"]:
            dict_bus_stop[component] = busstop[component]        
        list_bus_stops.append(dict_bus_stop)
    print(len(list_bus_stops))
    file_name = open('./coord_busstops_' + company + '.json', 'w')
    json.dump(list_bus_stops, file_name)


readout_json_bus_stops("Toei")
