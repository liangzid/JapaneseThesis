"""
======================================================================
SHIFTING_WORDCLOUD --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 29 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------


key_name="時代名"

time_ls=[
    "2平安",
    "3鎌倉",
    "5江戸",
    "6明治",
    "7大正",
    "8昭和",
    ]

def extract_corresponding_sets(
    # df = pd.read_excel('./data_old/CHJ376--2.xlsx', sheet_name='chj376')
    df = pd.read_excel('./data_old/SHC508--2.xlsx', sheet_name='shc508')
        ):

    v_key="所使用的前项动词"

    v_ls=df[v_key].dropna().tolist()
    times=df[key_name].dropna().tolist()

    time_vls_dict={}
    for i, time in enumerate(times):
        if time not in time_vls_dict:
            time_vls_dict[time]=[]
        else:
            time_vls_dict[time].append()
            


    pass








## normal import 
import json
from typing import List,Tuple,Dict
import random
from pprint import pprint as ppp



## running entry
if __name__=="__main__":
    main()
    print("EVERYTHING DONE.")


