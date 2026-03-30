#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生评估模块 - 在讲解前评估孩子的理解力和表达力
目的是找到最适合孩子的讲解方式
"""

import requests
import logging
import os
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssessmentModule:
    """学生评估模块 - 评估理解力和表达力"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('QWEN_API_KEY')
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model = "Qwen/Qwen2.5-72B-Instruct"

        # 评估问题
        self.assessment_questions = [
            {
                "id": "q1",
                "question": "宝贝你好！你叫什么名字呀？",
                "type": "icebreaker",
                "purpose": "破冰，建立信任感"
            },
            {
                "id": "q2",
                "question": "你喜欢玩什么游戏呀？能教教我怎么玩吗？",
                "type": "language",
                "purpose": "评估语言复杂度和表达流畅度"
            },
            {
                "id": "q3",
                "question": "如果有12颗糖果要平均分给3个小朋友，每个人能分到几颗？你会怎么分？",
                "type": "concrete",
                "purpose": "评估具象思维能力（需不需要举例说明）"
            },
            {
                "id": "q4",
                "question": "25加17等于多少？你是怎么算出来的？",
                "type": "abstract",
                "purpose": "评估抽象思维能力（直接计算 vs 需要举例）"
            },
            {
                "id": "q5",
                "question": "妈妈买了30块钱的菜，花了18块，还剩多少？你能想到几种算法？",
                "type": "depth",
                "purpose": "评估理解深度和多角度思考能力"
            }
        ]

    def get_assessment_questions(self) -> List[Dict]:
        """获取评估问题列表"""
        return self.assessment_questions

    def generate_assessment_intro(self, student_age: int = 8) -> str:
        """生成评估开场白"""
        prompt = f"""
你是一位友好的小学数学陪练AI，现在要和一个大约{student_age}岁的小朋友进行一次小小的"数学小测试"。
这不是考试哦，是老师想认识一下你，看看怎么教你最合适。

【开场白要求】
1. 语气友好、像朋友聊天
2. 告诉小朋友这不是考试，不用紧张
3. 告诉小朋友回答没有对错，想怎么说就怎么说
4. 控制在50字以内

请写一段开场白。
"""
        return self._call_model(prompt)

    def analyze_response(self, question_id: str, question: str, response: str) -> Dict[str, Any]:
        """
        分析孩子对单个问题的回答

        Args:
            question_id: 问题ID
            question: 问题
            response: 孩子回答

        Returns:
            dict: 分析结果
        """
        # 找到问题类型
        q_type = None
        for q in self.assessment_questions:
            if q['id'] == question_id:
                q_type = q['type']
                break

        if not q_type:
            return {"error": "unknown question type"}

        # 构建分析prompt
        prompt = f"""
分析这位小学二三年级孩子的数学回答。

问题：{question}
孩子回答：{response}
问题类型：{q_type}

请从以下维度分析（输出JSON）：
{{
    "language_level": "simple/medium/complex",  // 语言复杂度
    "thinking_style": "concrete/abstract/mixed",  // 思维偏好
    "expression_ability": "poor/fair/good/excellent",  // 表达能力
    "understanding_depth": "shallow/medium/deep",  // 理解深度
    "needs_examples": true/false,  // 是否需要举例说明
    "insights": "1-2句话的关键洞察"
}}

只输出JSON，不要其他文字。
"""
        result = self._call_model(prompt)
        try:
            import json
            return json.loads(result)
        except:
            return {"error": "parse failed", "raw": result}

    def generate_profile(self, responses: List[Dict]) -> Dict[str, Any]:
        """
        综合所有回答，生成孩子画像

        Args:
            responses: [{question_id, question, response, analysis}, ...]

        Returns:
            dict: 孩子画像和推荐讲解策略
        """
        responses_text = "\n".join([
            f"问题{resp['question_id']}: {resp['question']}\n回答: {resp['response']}\n分析: {resp['analysis']}"
            for resp in responses
        ])

        prompt = f"""
基于以下评估对话结果，给这位小学生生成画像和推荐讲解策略。

{responses_text}

请输出JSON：
{{
    "profile": {{
        "name": "孩子昵称（从对话中推断，不确定写'未知'）",
        "age_estimate": "大约年龄",
        "language_level": "简单/中等/复杂",
        "thinking_preference": "具象型/抽象型/混合型",
        "expression_ability": "较弱/一般/良好/优秀",
        "understanding_depth": "浅/中/深",
        "key_strength": "主要优点",
        "key_need": "主要需要"
    }},
    "teaching_strategy": {{
        "preferred_method": "具象化/分步/逆向/混合",
        "explanation_order": ["方式1", "方式2", "方式3"],
        "avoid_method": "应该避免的方式",
        "special_notes": "1-2句话特别注意事项"
    }},
    "assessment_summary": "2-3句话的评估总结"
}}

只输出JSON。
"""
        result = self._call_model(prompt)
        try:
            import json
            profile_data = json.loads(result)

            # 格式化输出
            output = f"""
{'='*50}
📋 评估完成！这是{profile_data['profile']['name']}的小档案：
{'='*50}

🎯 思维偏好：{profile_data['profile']['thinking_preference']}
📝 语言水平：{profile_data['profile']['language_level']}
🗣️ 表达能力：{profile_data['profile']['expression_ability']}
🧠 理解深度：{profile_data['profile']['understanding_depth']}

✨ 优点：{profile_data['profile']['key_strength']}
💡 需要：{profile_data['profile']['key_need']}

{'='*50}
📚 推荐讲解方式（按顺序）：
{'='*50}
1. {profile_data['teaching_strategy']['preferred_method']}
2. {profile_data['teaching_strategy']['explanation_order']}

⚠️ 注意：{profile_data['teaching_strategy']['special_notes']}

{profile_data['assessment_summary']}
"""
            return {
                "status": "success",
                "profile": profile_data['profile'],
                "teaching_strategy": profile_data['teaching_strategy'],
                "summary": profile_data['assessment_summary'],
                "formatted_output": output
            }
        except:
            return {"status": "error", "raw": result}

    def _call_model(self, prompt: str) -> str:
        """调用模型"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': '你是一位专业的小学数学老师，擅长分析孩子的学习特点。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_tokens': 2000
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"评估API调用失败: {e}")
            return f"error: {e}"


if __name__ == "__main__":
    # 测试评估模块
    assessor = AssessmentModule()

    print("=== 学生评估模块测试 ===\n")

    # 测试开场白
    intro = assessor.generate_assessment_intro(8)
    print("开场白:")
    print(intro)
    print()

    # 测试生成画像
    sample_responses = [
        {
            "question_id": "q2",
            "question": "你喜欢玩什么游戏呀？",
            "response": "我喜欢玩我的世界！就是那个搭积木的游戏，我可以搭很大的城堡！",
            "analysis": {"language_level": "medium", "thinking_preference": "concrete", "expression_ability": "good"}
        },
        {
            "question_id": "q3",
            "question": "12颗糖果分给3个小朋友，怎么分？",
            "response": "我会每人先给2颗，再给2颗，再给2颗，这样就是6颗了... 不对，是每人4颗！",
            "analysis": {"thinking_preference": "concrete", "needs_examples": True}
        },
        {
            "question_id": "q4",
            "question": "25+17等于多少？",
            "response": "25+10=35，35+7=42！我先算大数！",
            "analysis": {"thinking_preference": "abstract", "understanding_depth": "deep"}
        }
    ]

    result = assessor.generate_profile(sample_responses)
    if result['status'] == 'success':
        print(result['formatted_output'])
    else:
        print(f"Error: {result}")
