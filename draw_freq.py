"""
======================================================================
DRAW_FREQ --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 17 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager as fm
from matplotlib import rcParams
import matplotlib
import pandas as pd

# def set_cjk_font():
#     # 1. 候选关键词
#     keywords = {'SourceHanSans', 'NotoSansCJK', 'NotoSansJP', 'NotoSansKR', 'NotoSansSC', 'NotoSansTC', "adobe-source-han-sans"}
#     # 2. 扫描系统字体
#     for font in fm.findSystemFonts(fontext='ttf'):
#         try:
#             prop = fm.FontProperties(fname=font)
#             # 3. 只要 PostScript 名称里含关键词就采纳
#             if any(k in prop.get_name() for k in keywords):
#                 # 4. 设为全局默认
#                 matplotlib.rcParams['font.family'] = "adobe-source-han-sans"
#                 print('[✓] 已锁定 CJK 字体：', prop.get_name())
#                 return
#         except Exception:
#             continue
#     raise RuntimeError('未找到任何 Noto/Source Han Sans CJK 字体，请先安装。')
# set_cjk_font()




def parse_excel(fname):
    if fname=="./data_new/5-BCCWJ1313.xlsx":
        sheet_name="bccwj1313"
    elif fname=="./data_new/5-SHC508.xlsx":
        sheet_name="shc508"
    elif fname=="./data_new/5-CHJ376.xlsx":
        sheet_name="chj376"
    df = pd.read_excel(fname,
                       sheet_name=sheet_name)

    v_list=df["所使用的前项动词"].dropna().tolist()
    freq_list=df["前项动词在本语料库中出现频次"].dropna().tolist()

    freq_ls={}
    for i,v in enumerate(v_list):
        freq_ls[v]=freq_list[i]
    return freq_ls

def draw(filename="./data_new/5-BCCWJ1313.xlsx"):
    # --------------- 1. 数据 -----------------
    corpus = parse_excel(filename)

    # --------------- 2. 参数可调 --------------
    TOP_N = 120
    COLOR_MAP = "Set3"
    rcParams["figure.dpi"] = 200
    matplotlib.rcParams['font.family'] = "Source Han Sans CN"

    # --------------- 3. 预处理 ----------------
    df = (pd.Series(corpus, name="freq")
          .sort_values(ascending=False)
          .reset_index()
          .rename(columns={"index": "phrase"}))

    head = df.head(TOP_N)
    other_cnt = df[TOP_N:]["freq"].sum()
    if other_cnt:
        head = pd.concat([head,
                          pd.DataFrame({"phrase": ["その他"], "freq": [other_cnt]})],
                         ignore_index=True)

    save_prefix = filename.replace("./", "_").replace("/", "_")

    # --------------- 4. 条形图（竖条＋扁平） -----------------
    plt.figure(figsize=(20, 4))                       # 宽>>高，直接压扁
    sns.barplot(data=head, x="phrase", y="freq",
                palette=COLOR_MAP, orient="v")
    plt.title("頻出日本語表現（上位{})".format(TOP_N), pad=20)
    plt.ylabel("出現頻度")
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")               # 斜着写避免重叠
    plt.tight_layout()
    plt.savefig(save_prefix + "Bar.png", bbox_inches="tight")
    plt.close()

    # --------------- 5. 饼图（解决标签重叠 + 加描边） -------------------
    labels = head["phrase"]
    sizes  = head["freq"]
    colors = sns.color_palette(COLOR_MAP, n_colors=len(labels))

    total = sizes.sum()
    autopct = lambda pct: ("%1.1f%%" % pct) if pct >= 1 else ""
    explode = [0.05 if s / total < 0.01 else 0 for s in sizes]

    # 关键：给每块扇形加白边，线宽可自己调
    wedgeprops = dict(edgecolor='white', linewidth=1.2)

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=None,
        autopct=autopct,
        startangle=90,
        colors=colors,
        explode=explode,
        wedgeprops=wedgeprops,      # <-- 描边
        textprops={"fontsize": 9}
    )

    # 百分数字体
    for at in autotexts:
        at.set_color("white")
        at.set_weight("bold")

    plt.legend(wedges, labels,
            title="表現",
            loc="center left",
            bbox_to_anchor=(1.02, 0, 0.5, 1),
            ncol=max(1, len(labels) // 20))

    plt.title("頻出日本語表現 割合", pad=20)
    plt.tight_layout()
    plt.savefig(save_prefix + "Pie.png", bbox_inches="tight")
    plt.close()




if __name__=="__main__":
    draw()
    draw("./data_new/5-CHJ376.xlsx")
    draw("./data_new/5-SHC508.xlsx")
