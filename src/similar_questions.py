#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同类题生成模块
根据错题生成相似的练习题
"""

import logging
import random
from typing import Dict, Any, List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarQuestionGenerator:
    def __init__(self):
        self.question_templates = {
            '加法': [
                "小明有{num1}个苹果，小红有{num2}个苹果，他们一共有多少个苹果？",
                "停车场原来有{num1}辆车，又开来了{num2}辆车，现在有多少辆车？",
                "{num1}只小鸟在树上，又飞来了{num2}只，树上共有多少只小鸟？"
            ],
            '减法': [
                "小明有{num1}个糖果，吃了{num2}个，还剩多少个？",
                "树上有{num1}只鸟，飞走了{num2}只，还剩多少只？",
                "书包里有{num1}本书，拿出了{num2}本，还剩多少本？"
            ],
            '乘法': [
                "每个盒子有{num1}个苹果，{num2}个盒子一共有多少个苹果？",
                "一支铅笔{num1}元，买{num2}支需要多少钱？",
                "每行种{num1}棵树，{num2}行一共种多少棵树？"
            ],
            '除法': [
                "{num1}个苹果平均分给{num2}个小朋友，每人分到几个？",
                "{num1}块糖，每人分{num2}块，可以分给几个人？",
                "{num1}米长的绳子，每段长{num2}米，可以分成几段？"
            ]
        }
    
    def generate(self, original_problem: str, error_type: str = None, count: int = 3) -> List[Dict[str, Any]]:
        """
        生成同类题
        
        Args:
            original_problem: 原题内容
            error_type: 错误类型
            count: 生成数量
            
        Returns:
            list: 同类题列表
        """
        try:
            logger.info(f"开始生成同类题，错误类型: {error_type}")
            
            # 根据原题判断题型
            problem_type = self._identify_problem_type(original_problem)
            
            similar_questions = []
            for i in range(count):
                question = self._generate_single_question(problem_type, i + 1)
                similar_questions.append({
                    'id': i + 1,
                    'question': question['text'],
                    'answer': question['answer'],
                    'type': problem_type,
                    'difficulty': self._calculate_difficulty(question['text'])
                })
            
            logger.info(f"生成{len(similar_questions)}道同类题")
            return similar_questions
            
        except Exception as e:
            logger.error(f"生成同类题失败: {str(e)}")
            return []
    
    def _identify_problem_type(self, problem_text: str) -> str:
        """识别题目类型"""
        if any(word in problem_text for word in ['+', '加', '一共', '总共']):
            return '加法'
        elif any(word in problem_text for word in ['-', '减', '剩下', '还剩']):
            return '减法'
        elif any(word in problem_text for word in ['×', '*', '乘', '倍']):
            return '乘法'
        elif any(word in problem_text for word in ['÷', '/', '除', '平均', '分给']):
            return '除法'
        else:
            return '混合运算'
    
    def _generate_single_question(self, problem_type: str, index: int) -> Dict[str, str]:
        """生成单道题目"""
        templates = self.question_templates.get(problem_type, self.question_templates['加法'])
        template = random.choice(templates)
        
        # 生成合适的数字
        if problem_type == '加法':
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
            answer = num1 + num2
        elif problem_type == '减法':
            num1 = random.randint(20, 60)
            num2 = random.randint(5, 20)
            answer = num1 - num2
        elif problem_type == '乘法':
            num1 = random.randint(2, 9)
            num2 = random.randint(2, 9)
            answer = num1 * num2
        elif problem_type == '除法':
            answer = random.randint(2, 8)
            num2 = random.randint(2, 6)
            num1 = answer * num2
        else:
            num1 = random.randint(10, 30)
            num2 = random.randint(5, 15)
            answer = num1 + num2
        
        question_text = template.format(num1=num1, num2=num2)
        
        return {
            'text': question_text,
            'answer': str(answer)
        }
    
    def _calculate_difficulty(self, question_text: str) -> str:
        """计算题目难度"""
        # 简单规则判断
        if any(word in question_text for word in ['÷', '/', '除', '平均']):
            return '中等'
        elif any(word in question_text for word in ['×', '*', '乘']):
            return '简单'
        elif any(word in question_text for word in ['+', '-']):
            return '简单'
        else:
            return '中等'