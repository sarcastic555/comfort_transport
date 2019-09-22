import os
import numpy as np
import json
import requests
import subprocess
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

def bus_location_plotter(company, pattern, input_dir):
    try:
        df = pd.read_csv("%s/bus_location_%s.csv" % (input_dir,pattern))
        plt.plot(df["lat"], df["long"], marker="o")
        plt.savefig("aho.png")
        print(df.head(2))
    except:
        print("Error. File %s/bus_location_%s.csv not found" % (input_dir,pattern))

if __name__ == "__main__":
    company = "SeibuBus"
    #pattern = "DoshidaJunkan.8001.1"
    pattern = "yama22.505002.1"
    pattern = "Tatsu72.302003.2"
    input_dir = "../website/buslocation_data"
    bus_location_plotter(company=company, pattern=pattern, input_dir=input_dir)
    
