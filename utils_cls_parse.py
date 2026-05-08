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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from pathlib import Path
import re

def construct_cls_map_dict(txt_path: str | Path) -> dict[str, list[str]]:
    # 高层语义
    L0_MAP = {'1': '体の類', '2': '用の類', '3': '相の類', '4': 'その他の類'}
    
    # L1 映射规则（简化版）
    def get_l1(major: str, minor_num: int) -> str:
        if major == '1':
            if (100 <= minor_num <= 199) or (1100 <= minor_num <= 1999):
                return '抽象的関係'
            elif (200 <= minor_num <= 299) or (2300 <= minor_num <= 2399):
                return '人間活動の主体'
            elif (300 <= minor_num <= 399) or (3000 <= minor_num <= 3999):
                return '人間活動－精神および行為'
            elif 400 <= minor_num <= 499:
                return '生産物および用具'
            elif 500 <= minor_num <= 599:
                return '自然物および自然現象'
        elif major == '2':
            if (100 <= minor_num <= 199) or (1500 <= minor_num <= 1999):
                return '抽象的関係'
            elif (300 <= minor_num <= 399) or (3000 <= minor_num <= 3999):
                return '精神および行為'
            elif 500 <= minor_num <= 599:
                return '自然現象'
        elif major == '3':
            if 100 <= minor_num <= 199:
                return '抽象的関係'
            elif 300 <= minor_num <= 399:
                return '精神および行為'
            elif 500 <= minor_num <= 599:
                return '自然現象'
        return ''

    txt = read_cjk_text(txt_path)
    
    # 两种正则：
    # 1. 带点的绝对/相对编号
    pattern1 = re.compile(r'^(?P<prefix>\s*)(?P<code>(?:\d+\.\d+(?:\.\d+)*|\.\d+))[ \u3000]+(?P<term>[^ \u3000].*?)(?=[ \u3000]*$|\.+$)')
    # 2. 纯数字子编号（必须有前导空白）
    pattern2 = re.compile(r'^(?P<prefix>\s+)(?P<code>\d+)[ \u3000]+(?P<term>[^ \u3000].*?)(?=[ \u3000]*$)')

    stack: list[tuple[str, int]] = []  # (full_code, indent_len)
    code_to_term: dict[str, str] = {}

    for line in txt.splitlines():
        clean_line = line.rstrip()
        if not clean_line:
            continue

        m1 = pattern1.search(clean_line)
        m2 = None
        full_code = None
        term = None
        indent_len = 0

        if m1:
            prefix = m1['prefix']
            indent_len = len(prefix)
            code_str = m1['code']
            term = m1['term'].strip()
            # 处理相对编号
            if code_str.startswith('.'):
                if stack:
                    parent_code, _ = stack[-1]
                    full_code = parent_code + code_str
                else:
                    continue
            else:
                full_code = code_str
        else:
            m2 = pattern2.search(clean_line)
            if m2:
                prefix = m2['prefix']
                indent_len = len(prefix)
                code_str = m2['code']
                term = m2['term'].strip()
                # 视为相对编号 .{code_str}
                if stack:
                    parent_code, parent_indent = stack[-1]
                    if indent_len > parent_indent:  # 确保是子项
                        full_code = parent_code + '.' + code_str
                    else:
                        continue
                else:
                    continue
            else:
                continue

        # 更新 stack
        # 找到父级位置
        while stack and stack[-1][1] >= indent_len:
            stack.pop()
        stack.append((full_code, indent_len))
        code_to_term[full_code] = term

    # 构建最终结果
    result = {}
    for full_code, term in code_to_term.items():
        parts = full_code.split('.')
        major = parts[0]
        l0 = L0_MAP.get(major, '')
        l1 = ''

        # 确定 L1：找第二段（如果是 1.4150，则第二段是 4150）
        if len(parts) >= 2:
            try:
                minor_num = int(parts[1])
                l1 = get_l1(major, minor_num)
            except:
                pass

        result[full_code] = [l0, l1, term]

    return result
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__=="__main__":
    d = construct_cls_map_dict('./data_cls/KOUMOKU.txt')
    from pprint import pprint
    pprint(d)
    print('1.100  ->', d.get('1.100'))
    print('1.101  ->', d.get('1.101'))   # 来自 .101
    print('1.1240 ->', d.get('1.1240'))
    print('1.1560 ->', d.get('1.1560'))
    print('2.1560 ->', d.get('2.1560'))
    print('1      ->', d.get('1'))
    print('1.1    ->', d.get('1.1'))     # 如果存在



# # ----------------- 使用示例 -----------------
# if __name__ == "__main__":
#     astr=read_cjk_text("./data_cls/SAKUIN.txt")
#     astr=astr[:32]
#     print("==========================================================")
#     print(astr)
