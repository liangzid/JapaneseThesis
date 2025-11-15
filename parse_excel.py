"""
======================================================================
PARSE_EXCEL --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 11 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------

import pandas as pd
from tqdm import tqdm
import time

from API import LLM_trans


def run_translate2Chinese():
    # df = pd.read_excel('BCCWJ1313.xlsx', sheet_name='bccwj1313')
    # df = pd.read_excel('CHJ376--2.xlsx', sheet_name='chj376')
    df = pd.read_excel('SHC508--2.xlsx', sheet_name='shc508')

    text_list = df['合并内容'].dropna().tolist()
    # print(text_list[:5])
    temp_ls=text_list[:]
    print("Overall Length: ", len(temp_ls))
    translated_ls=[]
    for jp_text in tqdm(temp_ls,desc="Translation Procedure:"):
        try:
            code_after_trans=LLM_trans(jp_text)
        except Exception as e:
            print("A failed Sample Occured.")
            code_after_trans="Failed to Translate."
            
        translated_ls.append(code_after_trans)
        time.sleep(0.3)

    assert len(temp_ls)==len(translated_ls)
    # Export to excel.
    df = pd.DataFrame({
        'Japanese': temp_ls,
        'Chinese': translated_ls
    })

    df.to_excel(f'Jp-Ch-Translation-{len(temp_ls)}.xlsx', index=False) 
    print("Export DONE.")
    return None


if __name__=="__main__":
    run_translate2Chinese()















