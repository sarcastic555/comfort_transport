import json
import os
import csv
import glob

def convert_csv_to_json(input_path, output_path):

    json_list = []

    # CSV ファイルの読み込み
    with open(input_path, 'r') as f:
        for row in csv.DictReader(f):
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
    for csv_file in glob.glob("%s/*.csv" % input_dir):
        print(csv_file)
        convert_csv_to_json(csv_file, output_path)
