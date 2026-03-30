#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Explanation Module - 消灭错题核心
使用引导式对话，不是直接给答案
孩子选A/B回应，AI判断对错继续引导
"""

import requests
import logging
import os
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplanationModule:
    """AI讲解模块 - 引导式对话"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('QWEN_API_KEY')
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model = "Qwen/Qwen2.5-72B-Instruct"
        self.conversation_history = []

    def explain(self, problem: str, student_answer: str, correct_answer: str,
                error_type: str, student_age: int = 8,
                teaching_preference: str = None) -> Dict[str, Any]:
        """
        开始讲解流程

        Args:
            problem: 题目
            student_answer: 学生答案
            correct_answer: 正确答案
            error_type: 错因类型
            student_age: 学生年龄
            teaching_preference: 讲解偏好（具象型/抽象型/混合型），从评估模块获取

        Returns:
            dict: 讲解结果
        """
        logger.info(f"开始讲解: {problem}, 偏好: {teaching_preference}")

        result = self._generate_explanation(
            problem, student_answer, correct_answer, error_type, student_age,
            teaching_preference
        )

        return result

    def _generate_explanation(self, problem: str, student_answer: str,
                            correct_answer: str, error_type: str,
                            student_age: int,
                            teaching_preference: str = None) -> Dict[str, Any]:
        """生成引导式讲解对话"""

        # 根据偏好决定讲解顺序
        if teaching_preference == "具象型":
            style_order = "先讲故事、用糖果苹果举例，再过渡到抽象"
            first_method = "具象化讲解"
        elif teaching_preference == "抽象型":
            style_order = "先讲逻辑、直接给方法，再举例验证"
            first_method = "抽象方法讲解"
        elif teaching_preference == "混合型":
            style_order = "交替使用具象和抽象方法"
            first_method = "分步讲解"
        else:
            style_order = "三种方式都尝试，找到最适合的"
            first_method = "具象化讲解"

        preference_note = f"\n\n【讲解偏好】{style_order}。" if teaching_preference else ""

        prompt = f"""
你是一位耐心的小学数学AI陪练，正在帮助一位{student_age}岁的小朋友理解一道做错的数学题。

【重要规则】
1. 不直接告诉答案，而是提问让小朋友选择
2. 语言要简单有趣，像朋友聊天
3. 每道题用2-3个问题引导
4. 小朋友只需要回答 A 或 B
5. 如果答错了，不要批评，而是换一种方式继续引导{preference_note}

【错题信息】
题目: {problem}
小朋友的答案: {student_answer}
正确答案: {correct_answer}
错因类型: {error_type}

【输出要求】
请用Markdown格式输出一个完整的讲解对话，包含3种不同的讲解方式：

## 第1种方式：{first_method}
[这种讲解方式的内容]

问题1: [简单的问题，引导思考]
- A. [选项A]
- B. [选项B]

（如果选错）哦不对哦，我们再想想...

问题2: [继续引导]

...

## 第2种方式：[另一种讲解方式]
...

## 第3种方式：[第三种讲解方式]
...

## 如果都不行
退回到: [基础知识点名称]
练习题1: [1道基础练习]
练习题2: [1道基础练习]

请开始写讲解对话。
"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': '你是一位专业的小学数学陪练，擅长用引导式对话帮助孩子理解数学题。语言生动有趣，像朋友聊天。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 3000
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            logger.info("讲解生成成功")
            return {
                'status': 'success',
                'explanation': content,
                'model': self.model,
                'teaching_preference': teaching_preference
            }
        except Exception as e:
            logger.error(f"讲解生成失败: {e}")
            return {'status': 'error', 'explanation': str(e)}


if __name__ == "__main__":
    # 测试讲解模块（带偏好）
    module = ExplanationModule()

    print("=== 测试：抽象型孩子 ===")
    result = module.explain(
        problem="45 - 3 = ?",
        student_answer="37",
        correct_answer="42",
        error_type="退位减法错误",
        student_age=8,
        teaching_preference="抽象型"
    )
    if result['status'] == 'success':
        print(result['explanation'][:500])
