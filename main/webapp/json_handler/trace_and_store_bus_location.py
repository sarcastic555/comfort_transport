import os
import numpy as np
import json
import requests
import subprocess
import pandas as pd
import re
import time
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
bus_pattern_list = {} ## bus_pattern, bus_number

def classify_bus_location_by_bus_number(company, token, output_dir, save_key_list):
    bus_location_info_list = requests.get(HTTPS + company + KEY + token).json()


    for bus_location_info in bus_location_info_list:
        bus_number = bus_location_info["odpt:busNumber"]
        bus_pattern = bus_location_info["odpt:busroutePattern"].lstrip("odpt.BusroutePattern:%s." % company)

        ## バスパターンが登録されていて、かつバス番号が登録したものと異なる場合、以降の処理をスキップ
        if bus_pattern in bus_pattern_list.keys() and bus_pattern_list[bus_pattern] != bus_number:
            continue
        ## バスパターンが登録されていない場合は登録して以降の処理を続ける
        elif not bus_pattern in bus_pattern_list.keys():
            bus_pattern_list[bus_pattern] = bus_number
        ## その他(バスパターンが登録されていてバス番号が登録したものと一致)の場合、以降の処理を続ける
        output_filename = "%s/bus_location_%s.csv" % (output_dir, bus_pattern)
        try:
            df = pd.read_csv(output_filename, index_col=0)
        except:
            df = pd.DataFrame()
        series = pd.Series()
        for save_key in save_key_list:
            ## 先頭の"odpt.BusstopPole:SeibuBus."を削除する
            output = re.sub(r"odpt.*%s."%company, r"", str(bus_location_info[save_key]))
            series[key_convert_list[save_key]] = output
        series['company'] = company ## 会社名も追加しておく
        df = df.append(series, ignore_index=True)
        df.to_csv(output_filename)
    return

if __name__ == "__main__":

    ## === 設定 ===
    token = os.environ["odpt_token"]
    company = "SeibuBus"
    save_key_list = ["odpt:busNumber", "odpt:busroutePattern", "odpt:fromBusstopPole", "odpt:toBusstopPole", "geo:lat", "geo:long", "dc:date"]
    output_dir = "../website/buslocation_data"
    repeat_num = 1000
    sleep_time = 30 ## [s]

    ## === 出力ディレクトリにあるファイルをすべて削除する ===
    subprocess.run("rm %s/*"%output_dir, shell=True)

    ## === 指定した回数バス位置を保存する ===
    for i in range(repeat_num):
        if (i%10 == 0):
            print("Try: %d/%d" % (i+1,repeat_num))
        classify_bus_location_by_bus_number(company=company, token=token,
                                            output_dir=output_dir, save_key_list= save_key_list)
        time.sleep(sleep_time)

