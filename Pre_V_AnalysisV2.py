"""
======================================================================
PRE_V_ANALYSISV2 ---

New version of Pre-V Analysis.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 18 November 2025
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
    df = pd.read_excel('./data_old/BCCWJ1313--2.xlsx', sheet_name='bccwj1313')
    # df = pd.read_excel('./data_old/CHJ376--2.xlsx', sheet_name='chj376')
    # df = pd.read_excel('./data_old/SHC508--2.xlsx', sheet_name='shc508')

    text_list = df['合并内容'].dropna().tolist()
    # print(text_list[:20])
    temp_ls=text_list[:30]
    print("Overall Length: ", len(temp_ls))
    analysis_ls=[]

    i=0

    for jp_text in tqdm(temp_ls,desc="Analysis Procedure:"):
        i+=1
        try:
            code_after_analysis=LLM_V_analysis(jp_text, "v2")

            code_after_analysis=json.loads(code_after_analysis)

            # Do error check:
            if "前項動詞" not in code_after_analysis:
                code_after_analysis["前項動詞"]={
                    "result":"Failed.",
                    "reason":"Failed.",
                    }
            else:
                if "result" not in code_after_analysis["前項動詞"]:
                    code_after_analysis["前項動詞"]["result"]="Failed"
                if "reason" not in code_after_analysis["前項動詞"]:
                    code_after_analysis["前項動詞"]["reason"]="Failed"
            
            if "語彙素" not in code_after_analysis:
                code_after_analysis["語彙素"]={
                    "result":"Failed.",
                    "reason":"Failed.",
                    }
            else:
                if "result" not in code_after_analysis["語彙素"]:
                    code_after_analysis["語彙素"]["result"]="Failed"
                if "reason" not in code_after_analysis["前項動詞"]:
                    code_after_analysis["語彙素"]["reason"]="Failed"
                
            if "自他性判断" not in code_after_analysis:
                code_after_analysis["自他性判断"]={
                    "result1":"Failed.",
                    "result2":"Failed.",
                    "reason":"Failed.",
                    }
            else:
                if "result1" not in code_after_analysis["自他性判断"]:
                    code_after_analysis["自他性判断"]["result1"]="Failed"
                if "result2" not in code_after_analysis["自他性判断"]:
                    code_after_analysis["自他性判断"]["result2"]="Failed"
                if "reason" not in code_after_analysis["自他性判断"]:
                    code_after_analysis["自他性判断"]["reason"]="Failed"
                
            if "格助詞判断" not in code_after_analysis:
                code_after_analysis["格助詞判断"]={
                    "result":"Failed.",
                    "description": "Failed",
                    "reason":"Failed.",
                    }
            else:
                if "result" not in code_after_analysis["格助詞判断"]:
                    code_after_analysis["格助詞判断"]["result"]="Failed"
                if "description" not in code_after_analysis["格助詞判断"]:
                    code_after_analysis["格助詞判断"]["description"]="Failed"
                if "reason" not in code_after_analysis["格助詞判断"]:
                    code_after_analysis["格助詞判断"]["reason"]="Failed"

        except Exception as e:
            print("A failed Sample Occured.")
            print("Error:", e)
            code_after_analysis={
            "前項動詞":{
                "result":"Failed.",
                "reason":"Failed.",
            },
            "語彙素":{
                "result":"Failed.",
                "reason":"Failed.",
            },
            "自他性判断":{
                "result1":"Failed.",
                "result2":"Failed.",
                "reason":"Failed.",
            },
            "格助詞判断":{
                "result":"Failed.",
                "description": "Failed",
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
        '前项动词-结果': [x["前項動詞"]["result"] for x in analysis_ls],
        '前项动词-原因': [x["前項動詞"]["reason"] for x in analysis_ls],
        '词汇素-结果': [x["語彙素"]["result"] for x in analysis_ls],
        '词汇素-原因': [x["語彙素"]["reason"] for x in analysis_ls],
        '自他性判断-结果1': [x["自他性判断"]["result1"] for x in analysis_ls],
        '自他性判断-结果2': [x["自他性判断"]["result2"] for x in analysis_ls],
        '自他性判断-原因': [x["自他性判断"]["reason"] for x in analysis_ls],
        '格助词判断-结果': [x["格助詞判断"]["result"] for x in analysis_ls],
        '格助词判断-描述': [x["格助詞判断"]["description"] for x in analysis_ls],
        '格助词判断-原因': [x["格助詞判断"]["reason"] for x in analysis_ls],
    })

    df.to_excel(f'AnalysisV2-{len(temp_ls)}.xlsx', index=False) 
    print("Export DONE.")
    return None


if __name__=="__main__":
    run()




"""
格助词（が、を、に、へ、から、と、で）
"""
