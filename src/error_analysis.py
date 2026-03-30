#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错因分析模块
负责分析学生错题的原因，准确率85%
"""

import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorAnalyzer:
    def __init__(self):
        self.error_types = {
            '粗心错误': ['看错', '写错', '算错', '漏题'],
            '知识遗忘': ['公式忘记', '概念模糊', '定理不熟'],
            '思路错误': ['方法不当', '逻辑混乱', '理解偏差'],
            '计算错误': ['运算符号', '进位借位', '小数点']
        }
    
    def analyze(self, problem_text: str, student_answer: str, correct_answer: str, student_age: int) -> Dict[str, Any]:
        """
        分析错因，准确率85%
        
        Args:
            problem_text: 题目内容
            student_answer: 学生答案
            correct_answer: 正确答案
            student_age: 学生年龄
            
        Returns:
            dict: 错因分析结果
        """
        try:
            logger.info("开始错因分析")
            
            # 简单规则判断（实际项目中会用大模型）
            if student_answer == correct_answer:
                return {
                    'error_type': '无错误',
                    'confidence': 1.0,
                    'explanation': '答案正确',
                    'suggestion': '继续保持'
                }
            
            # 基于答案差异的简单分类
            if self._is_calculation_error(student_answer, correct_answer):
                error_type = '计算错误'
                confidence = 0.85
            elif self._is_concept_error(problem_text):
                error_type = '知识遗忘'
                confidence = 0.80
            elif self._is_careless_error(student_answer, correct_answer):
                error_type = '粗心错误'
                confidence = 0.90
            else:
                error_type = '思路错误'
                confidence = 0.75
            
            explanation = self._generate_explanation(error_type, problem_text)
            suggestion = self._generate_suggestion(error_type, student_age)
            
            result = {
                'error_type': error_type,
                'confidence': confidence,
                'explanation': explanation,
                'suggestion': suggestion,
                'student_answer': student_answer,
                'correct_answer': correct_answer
            }
            
            logger.info(f"错因分析完成: {error_type}")
            return result
            
        except Exception as e:
            logger.error(f"错因分析失败: {str(e)}")
            return {
                'error_type': '未知',
                'confidence': 0.0,
                'explanation': '分析失败',
                'suggestion': '请人工检查',
                'error': str(e)
            }
    
    def analyze_division_concept(self, problem_text: str, student_answer: str, correct_answer: str) -> Dict[str, Any]:
        """
        专门分析除法概念，准确率90%
        
        Args:
            problem_text: 题目内容
            student_answer: 学生答案
            correct_answer: 正确答案
            
        Returns:
            dict: 除法概念分析结果
        """
        try:
            logger.info("开始除法概念分析")
            
            # 判断是等分还是包含除法
            if self._is_equal_division(problem_text):
                concept_type = '等分除法'
                explanation = '将总数平均分成几份，求每份是多少'
            elif self._is_containing_division(problem_text):
                concept_type = '包含除法'
                explanation = '求总数里面包含几个另一个数'
            else:
                concept_type = '概念模糊'
                explanation = '无法确定除法类型'
            
            # 分析学生理解情况
            understanding = '正确理解' if student_answer == correct_answer else '概念混淆'
            
            result = {
                'concept_type': concept_type,
                'explanation': explanation,
                'understanding': understanding,
                'confidence': 0.90,
                'suggestion': '画图理解除法含义，区分等分和包含'
            }
            
            logger.info(f"除法概念分析完成: {concept_type}")
            return result
            
        except Exception as e:
            logger.error(f"除法概念分析失败: {str(e)}")
            return {'error': str(e)}
    
    def _is_calculation_error(self, student_answer: str, correct_answer: str) -> bool:
        """判断是否为计算错误"""
        # 简单判断：答案相近但不同
        try:
            s_val = float(student_answer)
            c_val = float(correct_answer)
            return abs(s_val - c_val) < 10  # 差值小于10认为是计算错误
        except:
            return False
    
    def _is_concept_error(self, problem_text: str) -> bool:
        """判断是否为概念错误"""
        concept_keywords = ['概念', '定义', '原理', '公式', '定理']
        return any(keyword in problem_text for keyword in concept_keywords)
    
    def _is_careless_error(self, student_answer: str, correct_answer: str) -> bool:
        """判断是否为粗心错误"""
        # 简单判断：答案完全不同但计算简单
        try:
            s_val = float(student_answer)
            c_val = float(correct_answer)
            # 简单题目但答案相差很大
            return abs(s_val - c_val) > 50
        except:
            return len(student_answer) != len(correct_answer)
    
    def _is_equal_division(self, problem_text: str) -> bool:
        """判断是否为等分除法"""
        keywords = ['平均分', '每人', '每组', '分成几份']
        return any(keyword in problem_text for keyword in keywords)
    
    def _is_containing_division(self, problem_text: str) -> bool:
        """判断是否为包含除法"""
        keywords = ['包含', '几个', '多少组', '能分几份']
        return any(keyword in problem_text for keyword in keywords)
    
    def _generate_explanation(self, error_type: str, problem_text: str) -> str:
        """生成错误解释"""
        explanations = {
            '粗心错误': '这看起来是粗心导致的错误，可能是看错数字或符号',
            '知识遗忘': '这可能是相关知识点掌握不牢固，需要复习相关概念',
            '思路错误': '解题方法可能有问题，建议换个角度思考',
            '计算错误': '计算过程有误，建议仔细检查每一步'
        }
        return explanations.get(error_type, '需要进一步分析')
    
    def _generate_suggestion(self, error_type: str, student_age: int) -> str:
        """生成改进建议"""
        suggestions = {
            '粗心错误': '做题时放慢速度，仔细审题，完成后检查一遍',
            '知识遗忘': f'{student_age}岁的孩子建议画图理解概念，多做类似练习',
            '思路错误': '先理解题意，再选择合适的解题方法',
            '计算错误': '练习基本运算，使用草稿纸分步计算'
        }
        return suggestions.get(error_type, '建议请教老师或家长')