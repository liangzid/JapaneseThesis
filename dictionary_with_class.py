"""
======================================================================
DICTIONARY_WITH_CLASS --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 18 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------


from utils_cls_parse import read_cjk_text,construct_a_dict, construct_cls_map_dict
import pandas as pd


def SupplyCLS():
    df = pd.read_excel('./data_new/5-BCCWJ1313.xlsx', sheet_name='bccwj1313')
    # df = pd.read_excel('./data_new/5-CHJ376.xlsx', sheet_name='chj376')
    # df = pd.read_excel('./data_new/5-SHC508.xlsx', sheet_name='shc508')

    text_list = df['合并内容'].dropna().tolist()
    v_list=df["所使用的前项动词"].dropna().tolist()
    # print(text_list[:20])
    temp_ls=text_list[:]
    v_ls=v_list[:]
    print("Overall Length: ", len(temp_ls))
    analysis_ls=[]

    export_key_name="前项动词在分类语义表中的类别"
    export_type_name2="前项动词含义"

    # read the dict
    dic=construct_a_dict("./data_cls/SAKUIN.txt")
    dic2=construct_cls_map_dict("./data_cls/KOUMOKU.txt")
    # dic={**dic1, **dic2}

    # print(dic)
    # assert "引き摺る" in dic
    words_cannot_found=[]

    cls_ls=[]
    for v in v_ls:
        if v in dic:
            cls_ls.append(dic[v])
        else:
            print(f"Verb {v} Not Found.")
            cls_ls.append("Not Found.")
            words_cannot_found.append(v)

    meaning_ls=[]
    for cls in cls_ls:
        if cls in dic2:
            meaning_ls.append(dic2[cls])
        else:
            meaning_ls.append(["NotFound", "NotFound", "NotFound"])

    v1_ls=[x[0] for x in meaning_ls]
    v2_ls=[x[1] for x in meaning_ls]
    v3_ls=[x[2] for x in meaning_ls]
            
    # Export to Excel.
    print(len(temp_ls),len(v_ls),len(cls_ls),len(meaning_ls))
    df = pd.DataFrame({
        'Japanese': temp_ls,
        '所使用的前项动词': v_ls,
        export_key_name: cls_ls,
        "Meaning": v1_ls,
        "Function": v2_ls,
        "XXXXXXX": v3_ls,
    })

    # with open("WordsCannotFound.txt", "w", encoding='utf8') as f:
    #     f.write("\n".join(list(set(words_cannot_found))))

    df.to_excel(f'Verb-CLS-{len(temp_ls)}.xlsx', index=False) 
    print("Export DONE.")
    return None


if __name__=="__main__":
    SupplyCLS()

