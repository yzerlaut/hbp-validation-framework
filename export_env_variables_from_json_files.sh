#! /bin/bash

output=$(python -c '
import json, os
file1 = os.path.join(os.path.expanduser("~"), "Downloads", "HBP.json")
if os.path.isfile(file1):
   data1=json.load(open(file1))
else:
   print("echo ** /!\ ", file1, "not found **")
file2 = os.path.join(os.path.expanduser("~"), "Downloads", "config.json")
if os.path.isfile(file2):
   data2=json.load(open(file2))
else:
   print("echo ** /!\ ", file2, "not found **")

magic=""
magic+="export HBP_token=\""+str(data1["access_token"])+"\"\n";
magic+="export HBP_STORAGE_TOKEN=\""+str(data2["auth"]["token"]["access_token"])+"\"" ; 
print(magic)')

eval "$output"

