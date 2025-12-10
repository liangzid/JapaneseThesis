"""
======================================================================
KNP_ANALYSIS --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 29 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------

## normal import 
import json
from typing import List,Tuple,Dict
import random
from pprint import pprint as ppp
from pyknp import KNP
import re

def batch_extract_predicate_case(text_list, knp_instance=None):
    """
    批量解析文本列表的用言格解析结果，返回格式化的字符串列表
    
    Args:
        text_list (list[str]): 待解析的日语文本列表
        knp_instance (KNP, optional): 已初始化的KNP实例（避免重复初始化提升效率）
    
    Returns:
        list[str]: 每个文本对应的用言格解析结果字符串（无结果时返回空字符串）
    """
    # 初始化KNP解析器（若未传入）
    if knp_instance is None:
        knp = KNP()
    else:
        knp = knp_instance
    
    # 存储最终结果的字符串列表
    result_str_list = []
    
    # 遍历每个文本进行解析
    for text in text_list:
        # 空文本直接返回空字符串
        if not text.strip():
            result_str_list.append("")
            continue
        
        try:
            # 执行KNP解析（包含格关系分析）
            parse_result = knp.parse(text)
            
            # 提取当前文本的用言格解析结果（结构化数据）
            case_info = _extract_single_text_case(parse_result)
            
            # 将结构化结果格式化为可读字符串
            case_str = _format_case_info(case_info)
            result_str_list.append(case_str)
        
        except Exception as e:
            # 解析失败时返回错误提示（避免批量中断）
            error_str = f"解析失败：{str(e)}"
            result_str_list.append(error_str)
    
    return result_str_list

def _extract_single_text_case(parse_result):
    """
    辅助函数：提取单个文本的用言格解析结构化数据
    
    Args:
        parse_result: knp.parse()返回的解析结果对象
    
    Returns:
        list[dict]: 每个用言的格解析信息（用言原形、基本句、格关系列表）
    """
    case_results = []
    
    # 遍历所有基本句（Tag）定位用言
    for tag in parse_result.tag_list():
        tag_fstring = tag.fstring
        
        # 筛选用言基本句（动词/形容词/形容动词）
        if any(marker in tag_fstring for marker in ["<用言:動>", "<用言:形>", "<用言:形動>"]):
            # 提取用言原形
            predicate_genkei = None
            for mrph in tag.mrph_list():
                if mrph.hinsi in ["動詞", "形容詞", "形容動詞"]:
                    predicate_genkei = mrph.genkei
                    break
            
            # 提取格解析结果
            case_matches = re.findall(r"<格解析結果:(.*?)>", tag_fstring)
            case_relations = []
            
            if case_matches:
                # 拆分格关系（分号分隔多个格）
                for part in case_matches[0].split(";"):
                    fields = part.split(":")
                    if len(fields) >= 5:
                        case_mark = fields[2].split("/")[0]  # 格標識（ガ/ヲ/ニ等）
                        case_element = fields[4]             # 格要素（关联名词）
                        case_relations.append({
                            "格標識": case_mark,
                            "格要素": case_element if case_element != "-" else "無"
                        })
            
            # 收集当前用言信息
            case_results.append({
                "用言原形": predicate_genkei or "不明",
                "用言基本句": "".join([mrph.midasi for mrph in tag.mrph_list()]),
                "格关系列表": case_relations
            })
    
    return case_results

def _format_case_info(case_info):
    """
    辅助函数：将结构化格解析信息格式化为可读字符串
    
    Args:
        case_info (list[dict]): 单个文本的用言格解析结构化数据
    
    Returns:
        str: 格式化后的字符串
    """
    if not case_info:
        return "未检测到用言格解析结果"
    
    # 拼接多个用言的结果
    parts = []
    for idx, item in enumerate(case_info, 1):
        part = [
            f"【用言{idx}】",
            f"  原形：{item['用言原形']}",
            f"  基本句：{item['用言基本句']}",
            f"  格关系：{'; '.join([f'{rel["格標識"]}({rel["格要素"]})' for rel in item['格关系列表']])}"
        ]
        parts.append("\n".join(part))
    
    return "\n".join(parts)

# ------------------- 示例调用 -------------------
if __name__ == "__main__":
    # 测试文本列表
    test_texts = [
        "下鴨神社の参道は暗かった。",
        "私は朝ごはんをパンで食べた。",
        "公園で子供たちが遊んでいる。",
        ""  # 空文本测试
    ]
    
    # 初始化KNP（复用实例提升效率）
    knp = KNP()
    
    # 批量解析
    results = batch_extract_predicate_case(test_texts, knp)
    
    # 打印结果
    for idx, (text, result) in enumerate(zip(test_texts, results), 1):
        print(f"===== 文本{idx} =====")
        print(f"原文：{text}")
        print(f"格解析结果：\n{result}\n")
