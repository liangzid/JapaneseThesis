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

TEXT_V="""你是一个专业的日本语言学专家，现在，用户将会发给你一个日语语句。你的目标是找出这个语句中的前项动词（通常只有1个）。随后，你要判断这个前项动词地自他性。你的回答必须是是自动词（意志）、自动词（无意志）、它动词三类当中的一种。随后，你需要给出这个前项动词在整个官方分类语义表中的类别。
"""

TEXT_VV="""你是一个专业的日本语言学专家，现在，用户将会发给你一个日语语句。
请严格按照以下要求处理提供的日语句子，输出结果需包含 *“前项动词提取”*, *“自他性判断”*, *“官方语义分类”*, *"格助词分析"* 四部分核心内容，每部分均需附带明确理由，确保逻辑可追溯.
# 待处理任务规则说明
1. 前项动词定义：指句子中逻辑核心动作动词（通常为句末动词，或能主导句子语义的核心动作词，需排除伴随动词（如「て形」「ながら形」动词）、补助动词（如「ている」「てある」「たい」）等非核心动词）；
2. 自他性判断标准：仅从 “自动词（意志）”“自动词（无意志）”“他动词” 三类中选择，判断需结合 “动作可控性”（意志 / 无意志）和 “是否搭配宾格助词「を」+ 宾语”（自 / 他动词）；
3. 官方语义分类依据：采用 MeCab 默认的「IPA 辞書」品词体系，需输出完整层级（格式：品詞 → 品詞細分類 1 → 品詞細分類 2 → 活用型），例如 “動詞 → 自立 → 五段・ヨ行 → 五段”。
4. 格助词分析： 判断目标词的格助词为何。
# 输出格式要求(A)
请严格按照以下固定格式输出，不添加额外无关内容，理由部分请简洁明确：
## 前项动词提取
结果：[动词原形，如「食べる」]（句子中出现的形态：[如「食べた」]）
理由：[说明为何该动词是核心，排除其他非核心动词的原因，如 “「食事をした」是句末最终动作，「作成した後」为前置伴随动作，故核心为「する」”]
## 自他性判断
结果：[从 “自动词（意志）”“自动词（无意志）”“他动词” 中选择其一]
理由：[结合动作可控性 + 助词搭配，如 “「作成する」需搭配宾语「資料を」，且动作可主动控制，故为他动词”]
## IPA 辞書官方语义分类
结果：品詞 → [如「動詞」] → 品詞細分類 1 → [如「自立」] → 品詞細分類 2 → [如「サ変・スル」] → 活用型 → [如「サ変・スル」]
理由：[对应 IPA 辞書分类规则，如 “「する」属于自立性サ変动词，活用型为サ変・スル，符合 IPA 辞書对该动词的分类定义”]
## 格助词判断
结果： [仅关注「が、を、に、へ、から、と、で」7 类核心格助词]
理由：[进行简单的分析解释]
# 输出格式要求(B)
你的输出可以是一个json格式：
```py
{
    "前项动词":{
        "result":str,
        "reason":str,
    },
    "自他性判断":{
        "result":str,
        "reason":str,
    },
    "IPA辞书官方语义分类":{
        "result":str,
        "reason":str,
    },
    "格助词判断":{
        "result":str,
        "reason":str,
    },
}
```
"""


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


def LLM_V_analysis(user_input):
    prompt=TEXT_VV
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
        response_format={"type":"json_object"}
    )
    resp=completion.choices[0].message.content
    print(type(resp))
    print(resp)
    return resp
    




