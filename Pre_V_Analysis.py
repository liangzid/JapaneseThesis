"""
======================================================================
PRE_V_ANALYSIS --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 15 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------

import pandas as pd
from tqdm import tqdm
import time
import json

from API import LLM_trans
from API import LLM_V_analysis

"""
前项动词分析（词频+词义+词性）
    - 所使用的前项动词
    - 前项动词在分类语义表中的类别
    - 前项动词在本语料库中出现频次
    - 前项动词自他性【自动词（意志）/自动词（无意志）/他动词】
"""

def run():
    df = pd.read_excel('BCCWJ1313--2.xlsx', sheet_name='bccwj1313')
    # df = pd.read_excel('CHJ376--2.xlsx', sheet_name='chj376')
    # df = pd.read_excel('SHC508--2.xlsx', sheet_name='shc508')

    text_list = df['合并内容'].dropna().tolist()
    # print(text_list[:20])
    temp_ls=text_list[:20]
    print("Overall Length: ", len(temp_ls))
    analysis_ls=[]

    i=0

    for jp_text in tqdm(temp_ls,desc="Analysis Procedure:"):
        i+=1
        try:
            code_after_analysis=LLM_V_analysis(jp_text)

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
    df = pd.DataFrame({
        'Japanese': temp_ls,
        '前项动词-结果': [x["前项动词"]["result"] for x in analysis_ls],
        '前项动词-原因': [x["前项动词"]["reason"] for x in analysis_ls],
        '自他性判断-结果': [x["自他性判断"]["result"] for x in analysis_ls],
        '自他性判断-原因': [x["自他性判断"]["reason"] for x in analysis_ls],
        'IPA辞书官方语义分类-结果': [x["IPA辞书官方语义分类"]["result"] for x in analysis_ls],
        'IPA辞书官方语义分类-原因': [x["IPA辞书官方语义分类"]["reason"] for x in analysis_ls],
        '格助词判断-结果': [x["格助词判断"]["result"] for x in analysis_ls],
        '格助词判断-原因': [x["格助词判断"]["reason"] for x in analysis_ls],
    })

    df.to_excel(f'Analysis-{len(temp_ls)}.xlsx', index=False) 
    print("Export DONE.")
    return None


if __name__=="__main__":
    run()




"""
格助词（が、を、に、へ、から、と、で）
"""
