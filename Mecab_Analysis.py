"""
======================================================================
MECAB_ANALYSIS --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2025, ZiLiang, all rights reserved.
    Created: 16 November 2025
======================================================================
"""


# ------------------------ Code --------------------------------------

import subprocess
import platform
from typing import List, Dict, Optional

class MeCabJapaneseAnalyzer:
    def __init__(self, mecab_path: Optional[str] = None):
        """
        初始化 MeCab 分析器
        :param mecab_path: MeCab 可执行文件路径（Windows 需指定，如 "C:\\Program Files\\MeCab\\bin\\mecab.exe"）
        """
        # 自动适配系统的 MeCab 路径
        self.mecab_cmd = "mecab"

        # 1. 自他性规则库（基于 IPA 辞書高频动词，可根据需求扩展）
        self.transitivity_dict = {
            # 他动词（需搭配を+宾语）
            "読む": "他动词", "書く": "他动词", "食べる": "他动词", "見る": "他动词", 
            "作る": "他动词", "買う": "他动词", "売る": "他动词", "送る": "他动词",
            "受け取る": "他动词", "渡す": "他动词", "開ける": "他动词", "閉める": "他动词",
            # 自动词-意志（可主动控制）
            "走る": "自动词（意志）", "歩く": "自动词（意志）", "話す": "自动词（意志）", 
            "起きる": "自动词（意志）", "寝る": "自动词（意志）", "行く": "自动词（意志）",
            "来る": "自动词（意志）", "帰る": "自动词（意志）", "登る": "自动词（意志）",
            # 自动词-无意志（不可主动控制，多为自然现象/状态变化）
            "降る": "自动词（无意志）", "吹く": "自动词（无意志）", "晴れる": "自动词（无意志）",
            "雨が降る": "自动词（无意志）", "風が吹く": "自动词（无意志）", "壊れる": "自动词（无意志）",
            "届く": "自动词（无意志）", "忘れる": "自动词（无意志）", "覚める": "自动词（无意志）"
        }

        # 2. 目标格助词列表（需分析的7类格助词）
        self.target_particles = {"が", "を", "に", "へ", "から", "と", "で"}

    def _parse_mecab_output(self, text: str) -> List[Dict]:
        """
        调用 MeCab 命令行，解析日语文本并返回结构化结果
        :param text: 待分析的日语句子（如「昨日、本を読んだ」）
        :return: 结构化列表，每个元素为一个词的属性字典
        """
        # 调用 MeCab 命令，指定输出格式为 IPA 辞書标准格式（表層形\t品詞,品詞細分類1,...）
        result = subprocess.run(
            [self.mecab_cmd, "-O", "chasen"],  # -O chasen 确保输出包含完整品词信息
            input=text.strip(),
            capture_output=True,
            encoding="utf-8",
            errors="ignore"
        )

        # 处理 MeCab 输出（排除 EOS 行和空行）
        parsed_data = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line or line == "EOS":
                continue
            
            # 拆分 MeCab 输出字段（格式：表層形\t読み\t発音\t品詞\t品詞細分類1\t品詞細分類2\t品詞細分類3\t活用型\t活用形\t原形）
            parts = line.split("\t")
            if len(parts) < 10:
                continue  # 跳过格式异常的行
            
            # 提取核心属性
            word_attr = {
                "surface": parts[0],          # 表層形（句子中实际出现的形式，如「読んだ」）
                "base_form": parts[9],       # 原形（动词原形，如「読む」）
                "pos": parts[3],             # 品詞（如「動詞」「助詞」）
                "pos_sub1": parts[4],        # 品詞細分類1（如「自立」「格助詞」）
                "pos_sub2": parts[5],        # 品詞細分類2（如「五段・ヨ行」「一般」）
                "conjugation_type": parts[7],# 活用型（如「五段・ヨ行」「サ変・スル」）
                "conjugation_form": parts[8] # 活用形（如「連用タ接続」「基本形」）
            }
            parsed_data.append(word_attr)
        
        return parsed_data

    def extract_main_verb(self, parsed_data: List[Dict]) -> Optional[Dict]:
        """
        从解析结果中提取前项动词（核心动词，排除伴随动词、补助动词）
        :param parsed_data: MeCab 结构化解析结果
        :return: 前项动词的属性字典（无则返回 None）
        """
        # 筛选所有动词（品詞为「動詞」），优先选择句末、自立性动词（排除补助动词）
        verbs = [
            word for word in parsed_data 
            if word["pos"] == "動詞" 
            and word["pos_sub1"] == "自立"  # 排除「ている」「てある」等非自立补助动词
            and "基本形" in word["conjugation_form"] or "連用タ接続" in word["conjugation_form"]  # 常见核心动词活用形
        ]

        # 日语核心动词多位于句末，取最后一个符合条件的动词作为前项动词
        if verbs:
            return verbs[-1]  # 句末动词优先
        return None

    def judge_transitivity(self, verb_base: str) -> str:
        """
        判断动词自他性（基于规则库，无则返回「需手动确认」）
        :param verb_base: 动词原形（如「読む」）
        :return: 自他性分类（「自动词（意志）」「自动词（无意志）」「他动词」「需手动确认」）
        """
        return self.transitivity_dict.get(verb_base, "需手动确认")

    def analyze_case_particles(self, parsed_data: List[Dict]) -> List[Dict]:
        """
        分析句子中的格助词，识别其依存关系（直接依存词、最终依存动词）
        :param parsed_data: MeCab 结构化解析结果
        :return: 格助词分析列表，每个元素包含格助词属性和依存关系
        """
        particle_analysis = []
        main_verb = self.extract_main_verb(parsed_data)  # 核心动词（格助词最终依存目标）
        main_verb_base = main_verb["base_form"] if main_verb else "未识别核心动词"

        # 遍历解析结果，定位目标格助词并分析依存
        for idx, word in enumerate(parsed_data):
            # 筛选目标格助词（品詞为「助詞」且品詞細分類1为「格助詞」，且表層形在目标列表中）
            if word["pos"] == "助詞" and word["pos_sub1"] == "格助詞" and word["surface"] in self.target_particles:
                # 1. 直接依存词：格助词前的名词（如「本を」中「を」的直接依存词是「本」）
                dependent_noun = None
                if idx > 0:  # 向前查找最近的名词
                    for prev_word in reversed(parsed_data[:idx]):
                        if prev_word["pos"].startswith("名詞"):  # 匹配名词（一般/固有名詞等）
                            dependent_noun = prev_word["surface"]
                            break

                # 2. 构建格助词分析结果
                particle_info = {
                    "particle": word["surface"],          # 格助词（如「を」）
                    "direct_dependent": dependent_noun or "未识别名词",  # 直接依存名词
                    "final_dependent_verb": main_verb_base,  # 最终依存动词（核心动词）
                    "particle_function": self._get_particle_function(word["surface"], dependent_noun, main_verb_base)  # 格助词功能
                }
                particle_analysis.append(particle_info)
        
        return particle_analysis

    def _get_particle_function(self, particle: str, dependent_noun: Optional[str], main_verb: str) -> str:
        """
        辅助函数：根据格助词、依存名词、核心动词推断语法功能
        :param particle: 格助词（如「に」）
        :param dependent_noun: 直接依存名词（如「東京」）
        :param main_verb: 核心动词（如「行く」）
        :return: 格助词功能说明（如「目的地」）
        """
        function_map = {
            "が": "主格（动作主体，如「誰が～する」）",
            "を": "宾格（动作对象，如「何を～する」）",
            "に": self._get_ni_function(dependent_noun, main_verb),  # 「に」多义，单独处理
            "へ": "方向格（目的地，如「どこへ～行く」）",
            "から": "起点格（时间/地点起点，如「何時から～する」）",
            "と": self._get_to_function(dependent_noun, main_verb),  # 「と」多义，单独处理
            "で": self._get_de_function(dependent_noun, main_verb)   # 「で」多义，单独处理
        }
        return function_map.get(particle, "未明确功能")

    # 以下为「に」「と」「で」的多义功能推断（基于名词和动词语义）
    def _get_ni_function(self, noun: Optional[str], verb: str) -> str:
        if "行く" in verb or "来る" in verb:
            return "方向格（目的地，如「東京に行く」）"
        elif "会う" in verb or "電話する" in verb:
            return "对象格（动作对象，如「友達に会う」）"
        elif "3時" in noun or "明日" in noun:
            return "时间格（动作时间，如「3時に始まる」）"
        else:
            return "对象格/时间格（需结合语境，如「本に書く」）"

    def _get_to_function(self, noun: Optional[str], verb: str) -> str:
        if "友達" in noun or "家族" in noun:
            return "共同格（共同动作对象，如「友達と遊ぶ」）"
        elif "「" in noun or "言う" in verb:
            return "引用格（引用内容，如「こんにちはと言う」）"
        else:
            return "共同格/引用格（需结合语境）"

    def _get_de_function(self, noun: Optional[str], verb: str) -> str:
        if "学校" in noun or "公園" in noun:
            return "场所格（动作场所，如「公園で遊ぶ」）"
        elif "バス" in noun or "ペン" in noun:
            return "工具格（动作工具，如「バスで行く」）"
        else:
            return "场所格/工具格（需结合语境）"

    def full_analysis(self, text: str) -> Dict:
        """
        完整分析流程：解析文本 → 提取前项动词 → 判断自他性 → 格助词分析
        :param text: 待分析的日语句子
        :return: 完整分析结果字典
        """
        # 1. MeCab 解析
        parsed_data = self._parse_mecab_output(text)
        if not parsed_data:
            return {"error": "MeCab 解析失败，可能是句子为空或格式异常"}

        # 2. 提取前项动词
        main_verb = self.extract_main_verb(parsed_data)
        if main_verb:
            verb_surface = main_verb["surface"]  # 句子中出现的形态（如「読んだ」）
            verb_base = main_verb["base_form"]   # 动词原形（如「読む」）
            # 获取 IPA 辞書语义分类（品詞→細分類1→細分類2→活用型）
            ipa_category = f"品詞→{main_verb['pos']} → 品詞細分類1→{main_verb['pos_sub1']} → 品詞細分類2→{main_verb['pos_sub2']} → 活用型→{main_verb['conjugation_type']}"
            # 判断自他性
            transitivity = self.judge_transitivity(verb_base)
        else:
            verb_surface = verb_base = ipa_category = transitivity = "未识别前项动词"

        # 3. 格助词分析
        particle_analysis = self.analyze_case_particles(parsed_data)
        # 统计未出现的格助词
        used_particles = {p["particle"] for p in particle_analysis}
        unused_particles = [p for p in self.target_particles if p not in used_particles]

        # 4. 整理最终结果
        return {
            "input_sentence": text,
            "main_verb_analysis": {
                "surface_form": verb_surface,    # 出现形态
                "base_form": verb_base,          # 原形
                "ipa_semantic_category": ipa_category,  # IPA 语义分类
                "transitivity": transitivity     # 自他性
            },
            "case_particle_analysis": particle_analysis,  # 格助词分析
            "unused_case_particles": unused_particles     # 未出现的格助词
        }


# ------------------- 示例：使用脚本进行分析 -------------------
if __name__ == "__main__":
    # 1. 初始化分析器（Windows 若自定义 MeCab 路径，需传入 mecab_path 参数，如：
    # analyzer = MeCabJapaneseAnalyzer(mecab_path="C:\\Program Files\\MeCab\\bin\\mecab.exe")
    analyzer = MeCabJapaneseAnalyzer()

    # 2. 待分析的日语句子（可替换为任意句子）
    japanese_sentence = """彼は計算ずくで子供たちをサドマゾの世界に引きずりこもうとしているばかりか、強制収容所的文化をまき散らしているのです。"""
    # 3. 执行完整分析
    result = analyzer.full_analysis(japanese_sentence)

    # 4. 打印结构化结果（美观格式）
    print("=" * 50)
    print(result)
    print(f"待分析句子：{result['input_sentence']}")
    print
