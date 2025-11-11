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

API_KEY=os.environ["FOR_JAPAN_API_KEY"]

TEXT_TRANS="""你是一个专业的翻译官，精通将日语翻译为中文。现在，用户将会给你发送一句日语，你需要回复对应的中文。注意：你的回复里*只能*包含翻译之后的文本而不能包含任何的其他结果。"""


def one_time_LLM(prompt,user_input):
    client = OpenAI(
        api_key=API_KEY, # 
        base_url="https://api.moonshot.cn/v1",
    )
    completion = client.chat.completions.create(
        model = "kimi-k2-turbo-preview",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
    )
    resp=completion.choices[0].message.content
    return resp

def LLM_trans(user_input):
    return one_time_LLM(TEXT_TRANS, user_input)






