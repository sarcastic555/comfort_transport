import os
import numpy as np
import json
import requests
import subprocess
import sys

HTTPS = "https://api-tokyochallenge.odpt.org/api/v4/odpt:BusstopPole?odpt:operator=odpt.Operator:"
KEY = "&acl:consumerKey="

f = lambda x: True if x is None else False
key_orig_list=["dc:title", "odpt:kana", "@id", "geo:lat", "geo:long", "odpt:busroutePattern"]
key_replaced_list=["name_kanji", "name_kana", "id", "lat", "lon", "busroutePattern"]

def readout_json_bus_stops(company, token):
    busstops_in = requests.get(HTTPS + company + KEY + token)
    busstops = busstops_in.json()
    list_bus_stops = []
    for busstop in busstops:
        if( f(busstop["geo:lat"]) ):
            continue
        dict_bus_stop = {}
        for key_orig, key_replaced in zip(key_orig_list, key_replaced_list):
            dict_bus_stop[key_replaced] = busstop[key_orig]
        list_bus_stops.append(dict_bus_stop)
    print("Valid data size: %d" % len(list_bus_stops))
    file_name = open('../website/busstop_data/coord_busstops_' + company + '.json', 'w')
    json.dump(list_bus_stops, file_name, ensure_ascii=False)



def main():
    companies = ["Toei", "SeibuBus", "NishiTokyoBus", "KokusaiKogyoBus", "KantoBus", "TokyuBus"]
    if os.environ.get("env_defined") != "True":
        print("Error. $odpt_token not defined.")
        print("Please execute source env.sh command")
        sys.exit()
    token = os.environ['odpt_token']
    subprocess.call(['mkdir', '-p', '../website/busstop_data'])

    for company in companies:
        readout_json_bus_stops(company=company, token=token)

if __name__ == "__main__":
    main()
