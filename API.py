"""
======================================================================
API --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 11 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------
from openai import OpenAI
import os

from prompts import *


API_KEY=os.environ["FOR_JAPAN_API_KEY"]
# API_KEY=os.environ["DS_JAPAN_API_KEY"]

def one_time_LLM(prompt,user_input):
    client = OpenAI(
        api_key=API_KEY, # 
        base_url="https://api.moonshot.cn/v1",
        # base_url="https://api.deepseek.com",
    )
    completion = client.chat.completions.create(
        # model = "kimi-k2-turbo-preview",
        model = "kimi-k2-0905-preview",
        # model = "deepseek-chat",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
    )
    resp=completion.choices[0].message.content
    return resp

def LLM_trans(user_input):
    return one_time_LLM(TEXT_TRANS, user_input)


def LLM_V_analysis(user_input, version="v1"):
    if version=="v1":
        prompt=TEXT_VV_JAN
    else:
        prompt=TEXT_VV_V2_JAN
    client = OpenAI(
        api_key=API_KEY, # 
        base_url="https://api.moonshot.cn/v1",
        # base_url="https://api.deepseek.com",
    )
    completion = client.chat.completions.create(
        # model = "kimi-k2-turbo-preview",
        model = "kimi-k2-0905-preview",
        # model = "deepseek-chat",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        response_format={"type":"json_object"}
    )
    resp=completion.choices[0].message.content
    print(type(resp))
    print(resp)
    return resp
    

def LLM_V_analysis_withV(user_input):
    prompt=TEXT_V_WITH_V
    client = OpenAI(
        api_key=API_KEY, # 
        base_url="https://api.moonshot.cn/v1",
        # base_url="https://api.deepseek.com",
    )
    completion = client.chat.completions.create(
        # model = "kimi-k2-turbo-preview",
        model = "kimi-k2-0905-preview",
        # model = "deepseek-chat",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        response_format={"type":"json_object"}
    )
    resp=completion.choices[0].message.content
    print(type(resp))
    print(resp)
    return resp



