import os
import numpy as np
import json
import requests
import subprocess
import sys

HTTPS = "https://api-tokyochallenge.odpt.org/api/v4/odpt:Bus?odpt:operator=odpt.Operator:"
KEY = "&acl:consumerKey="

## key名にコロンが入っていると扱いづらいのでkey名を変更する
key_convert_list = {
    "odpt:busNumber": "busNumber", ## バス固有番号
    "odpt:busroutePattern": "busroutePattern", ## 運行中の系統のID
    "odpt:startingBusstopPole": "startingBusstopPole", ## 始発バス停
    "odpt:terminalBusstopPole": "terminalBusstopPole", ## 終点バス停
    "odpt:fromBusstopPole": "fromBusstopPole", ## 直前に通過したバス停
    "odpt:toBusstopPole": "toBusstopPole", ## 直前に通過したバス停
    "geo:lat": "lat", ## バス緯度
    "geo:long": "long", ## バス経度
    "dc:date": "date" ## データ更新日時 
}

def classify_bus_location_by_bus_number(company, token, output_dir, save_key_list):
    bus_location_info_list = requests.get(HTTPS + company + KEY + token).json()
    bus_pattern_list = []

    for bus_location_info in bus_location_info_list:
        bus_number = int(bus_location_info["odpt:busNumber"])
        bus_pattern = bus_location_info["odpt:busroutePattern"].lstrip("odpt.BusroutePattern:%s." % company)
        if not bus_pattern in bus_pattern_list:
            save_param_dict = {}
            for save_key in save_key_list:
                save_param_dict[key_convert_list[save_key]] = bus_location_info[save_key]
            output_file_name = open('%s/bus_location_%s.json' % (output_dir, bus_pattern), 'a')
            json.dump(save_param_dict, output_file_name)
            bus_pattern_list.append(bus_pattern)
    return

if __name__ == "__main__":

    ## === 設定 ===
    token = os.environ["odpt_token"]
    company = "SeibuBus"
    save_key_list = ["odpt:busNumber", "odpt:busroutePattern", "odpt:fromBusstopPole", "odpt:toBusstopPole", "geo:lat", "geo:long", "dc:date"]
    output_dir = "../website/buslocation_data"

    classify_bus_location_by_bus_number(company=company, token=token,
                                        output_dir=output_dir, save_key_list= save_key_list)

