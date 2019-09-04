import json
import os
import csv
import glob

def convert_csv_to_json(input_path_list, output_path):

    json_list = []

    # CSV ファイルの読み込み
    for bus_route_index, input_path in enumerate(input_path_list):
        print(input_path)
        with open(input_path, 'r') as f:
            for timestamp_index, row in enumerate(csv.DictReader(f)):
                row['busroute_index'] = bus_route_index
                row['timestamp_index'] = timestamp_index
                print(row)
                json_list.append(row)

    # JSON ファイルへの書き込み
    with open(output_path, 'a') as f:
        json.dump(json_list, f)

if __name__ == "__main__":
    input_dir = "../website/buslocation_data"
    output_path = "../website/buslocation_data/bus_location_all.json"
    if os.path.exists(output_path):
        os.remove(output_path)

    ## csvファイルに対するループ
    csv_file_list = glob.glob("%s/*.csv" % input_dir)
    convert_csv_to_json(csv_file_list, output_path)
