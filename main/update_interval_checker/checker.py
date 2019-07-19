import requests
import os
import sys

if len(sys.argv) == 1: ## no argument
    data_type = "Bus"
    bus_type = "SeibuBus"
    output_file = "out.txt"
elif len(sys.argv) == 4: ## double arguments
    data_type=sys.argv[1] ## Bus, BusstopPole
    bus_type=sys.argv[2] ## SeibuBus
    output_file = sys.argv[3] ## outpupt.txt
else:
    print("Error. Invalid argument")
    print("Useage: python bus_checker.py Bus SeibuBus")
    sys.exit()

if not os.environ.get("open_data_key"):
    print("Error. Please source env.sh")
    sys.exit()

api_key = os.environ['open_data_key']
url = "https://api-tokyochallenge.odpt.org/api"
api_version = "v4"

params = {'odpt:operator': 'odpt.Operator:%s'%bus_type,
         'acl:consumerKey': api_key}
params_str = "&".join("%s=%s" % (k,v) for k,v in params.items())
#print(params_str)
r = requests.get('%s/%s/odpt:%s'%(url, api_version, data_type), params=params_str)
#print(r.url)
#print(r.status_code)
#print(r.text)

file = open(output_file, "w")
file.write(r.text)
file.close()
