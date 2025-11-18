"""
======================================================================
UTILS_CLS_PARSE --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 18 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------

from io import StringIO
import pandas as pd   # 或 csv 标准库
from pathlib import Path
from typing import List, Optional

# 1. 暴力试码表（覆盖 99% 中日韩文本）
_CJK_ENCODINGS: List[str] = [
    "utf-8",                 # 带/不带 BOM 都能处理
    "gbk",                   # 简体 Win-936
    "gb18030",               # 国标最新版，向下兼容 GBK
    "big5",                  # 繁体
    "big5hkscs",             # 香港增补
    "shift_jis",             # 日文 Shift-JIS
    "euc-jp",                # 日文 EUC
    "euc-kr",                # 韩文 EUC
    "iso2022-jp",            # 古老的 JIS（邮件里偶尔出现）
]

def read_cjk_text(path: str | Path,
                  encoding: Optional[str] = None,
                  errors: str = "ignore") -> str:
    """
    自动识别 CJK 编码并读取文本文件。

    参数
    ----
    path : 文件路径
    encoding : 如果显式给出，则直接采用；为 None 时自动检测
    errors : 解码失败时的处理方式，同 open() 的同名参数

    返回
    ----
    str : 解码后的文本

    异常
    ----
    最终仍无法解码时抛出 UnicodeDecodeError
    """
    path = Path(path)

    # 1. 用户给了编码就直接读
    if encoding:
        return path.read_text(encoding=encoding, errors=errors)

    # 2. 先试试 chardet（如果装了）
    try:
        import chardet
        raw = path.read_bytes()
        det = chardet.detect(raw)
        print(det)
        if det and det["encoding"]:
            return raw.decode(det["encoding"], errors=errors)
    except ImportError:  # 没装 chardet 就跳过
        print("Using chardet failed.")
        pass

    # 3. 暴力试码表
    for enc in _CJK_ENCODINGS:
        try:
            print(enc)
            return path.read_text(encoding=enc, errors="strict")
        except UnicodeDecodeError:
            print("Using CJK Encodings failed.")
            continue

    # 4. 最后一搏：用 utf-8 带 ignore 保底
    return path.read_text(encoding="utf-8", errors=errors)

def construct_a_dict(fname):
    stra=read_cjk_text(fname)
    # 用 StringIO 把字符串包成“文件”
    return pd.read_csv(
        StringIO(stra),
        header=None,
        dtype=str,
    ).set_index(1)[2].to_dict()


# ----------------- 使用示例 -----------------
if __name__ == "__main__":
    astr=read_cjk_text("./data_cls/SAKUIN.txt")
    astr=astr[:32]
    print("==========================================================")
    print(astr)
