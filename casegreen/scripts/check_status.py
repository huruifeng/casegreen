import json
import os

import pandas as pd
case_status_df = pd.read_csv("../../mycase/data/case_status.csv", header=0, index_col=0, sep=",")
status_ls = case_status_df.index.tolist()

IOE_status = []
folder = "E:/OneDrive - Mass General Brigham/personal/Temp/CaseCrawlerIOE/ubuntu/saved_dataPanda"
for file_i in os.listdir(folder):
    print(file_i)
    with open(folder + "/" + file_i) as json_file:
        data_ioe = json.load(json_file)
    for rn in data_ioe:
        status_x = data_ioe[rn][2]
        if status_x not in IOE_status:
            IOE_status.append(status_x)

folder = "E:/OneDrive - Mass General Brigham/personal/Temp/CaseCrawlerIOE/ubuntu/saved_dataERISOne"
for file_i in os.listdir(folder):
    print(file_i)
    with open(folder + "/" + file_i) as json_file:
        data_ioe = json.load(json_file)
    for rn in data_ioe:
        status_x = data_ioe[rn][2]
        if status_x not in IOE_status:
            IOE_status.append(status_x)

x = [i for i in IOE_status if i not in status_ls]
print(x)
