"""
======================================================================
PRE_V_WITHV_ANALYSIS --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 17 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------


import pandas as pd
from tqdm import tqdm
import time
import json

from API import LLM_trans
from API import LLM_V_analysis_withV

"""
前项动词分析（词频+词义+词性）
    - 前项动词自他性【自动词（意志）/自动词（无意志）/他动词】
    - 格助词分析
"""

def run():
    df = pd.read_excel('./data_new/5-BCCWJ1313.xlsx', sheet_name='bccwj1313')
    # df = pd.read_excel('./data_old/CHJ376--2.xlsx', sheet_name='chj376')
    # df = pd.read_excel('./data_old/SHC508--2.xlsx', sheet_name='shc508')

    text_list = df['合并内容'].dropna().tolist()
    v_list=df["所使用的前项动词"].dropna().tolist()
    # print(text_list[:20])
    temp_ls=text_list[:20]
    v_ls=v_list[:20]
    print("Overall Length: ", len(temp_ls))
    analysis_ls=[]

    i=0

    for index, jp_text in enumerate(tqdm(temp_ls,desc="Analysis Procedure:")):
        i+=1
        try:
            jp_text=f"待分析语句：{jp_text}\n前项动词：{v_ls[index]}"
            code_after_analysis=LLM_V_analysis_withV(jp_text)
            code_after_analysis=json.loads(code_after_analysis)

        except Exception as e:
            print("A failed Sample Occured.")
            code_after_analysis={
            "前项动词":{
                "result":"Failed.",
                "reason":"Failed.",
            },
            "自他性判断":{
                "result":"Failed.",
                "reason":"Failed.",
            },
            "IPA辞书官方语义分类":{
                "result":"Failed.",
                "reason":"Failed.",
            },
            "格助词判断":{
                "result":"Failed.",
                "reason":"Failed.",
            },
        }
            
        analysis_ls.append(code_after_analysis)
        time.sleep(0.3)

    assert len(temp_ls)==len(analysis_ls)
    # Export to excel.
    # df = pd.DataFrame({
    #     'Japanese': temp_ls,
    #     '前项动词-结果': [x["前项动词"]["result"] for x in analysis_ls],
    #     '前项动词-原因': [x["前项动词"]["reason"] for x in analysis_ls],
    #     '词汇素-结果': [x["词汇素"]["result"] for x in analysis_ls],
    #     '词汇素-原因': [x["词汇素"]["reason"] for x in analysis_ls],
    #     '自他性判断-结果': [x["自他性判断"]["result"] for x in analysis_ls],
    #     '自他性判断-原因': [x["自他性判断"]["reason"] for x in analysis_ls],
    #     '格助词判断-结果': [x["格助词判断"]["result"] for x in analysis_ls],
    #     '格助词判断-原因': [x["格助词判断"]["reason"] for x in analysis_ls],
    # })
    df = pd.DataFrame({
        'Japanese': temp_ls,
        "前項動詞(語彙素)[Label]": v_ls,
        '自他性判断-结果': [x["自他性判断"]["result"] for x in analysis_ls],
        '自他性判断-原因': [x["自他性判断"]["reason"] for x in analysis_ls],
        '格助词判断-结果': [x["格助词判断"]["result"] for x in analysis_ls],
        '格助词判断-原因': [x["格助词判断"]["reason"] for x in analysis_ls],
    })

    df.to_excel(f'With前项动词Analysis-{len(temp_ls)}.xlsx', index=False) 
    print("Export DONE.")
    return None


if __name__=="__main__":
    run()




"""
格助词（が、を、に、へ、から、と、で）
"""
