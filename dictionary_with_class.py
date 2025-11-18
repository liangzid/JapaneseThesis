"""
======================================================================
DICTIONARY_WITH_CLASS --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 18 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------


from utils_cls_parse import read_cjk_text,construct_a_dict
import pandas as pd


def SupplyCLS():
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

    export_key_name="前项动词在分类语义表中的类别"

    # read the dict
    dic=construct_a_dict("./data_cls/SAKUIN.txt")
    print(dic)
    assert "引き摺る" in dic

    cls_ls=[]
    for v in v_ls:
        if v in dic:
            cls_ls.append(dic[v])
        else:
            print(f"Verb {v} Not Found.")
            cls_ls.append("404NotFound")
    # Export to Excel.
    df = pd.DataFrame({
        'Japanese': temp_ls,
        export_key_name: cls_ls
    })

    df.to_excel(f'Verb-CLS-{len(temp_ls)}.xlsx', index=False) 
    print("Export DONE.")
    return None


if __name__=="__main__":
    SupplyCLS()

