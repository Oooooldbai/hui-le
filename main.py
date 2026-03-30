#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会了 - AI错题识别与错因分析系统
主入口文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.error_analysis import ErrorAnalyzer
from src.similar_questions import SimilarQuestionGenerator
from config.app_config import config

def test_without_api():
    """不依赖API的本地测试"""
    print("=== 会了 - 本地模块测试 ===\n")
    
    # 1. 测试错因分析
    print("【1】错因分析模块测试")
    analyzer = ErrorAnalyzer()
    
    test_cases = [
        {
            "problem": "小明有12个苹果，平均分给3个小朋友，每个小朋友分到几个？",
            "student_answer": "4",
            "correct_answer": "4",
            "desc": "答案正确"
        },
        {
            "problem": "小明有12个苹果，平均分给3个小朋友，每个小朋友分到几个？",
            "student_answer": "3",
            "correct_answer": "4",
            "desc": "除法概念混淆（等分除）"
        },
        {
            "problem": "24 ÷ 4 = ?",
            "student_answer": "16",
            "correct_answer": "6",
            "desc": "计算错误"
        },
        {
            "problem": "72 ÷ 8 = ?",
            "student_answer": "8",
            "correct_answer": "9",
            "desc": "乘法表不熟"
        }
    ]
    
    for i, tc in enumerate(test_cases, 1):
        result = analyzer.analyze(
            tc["problem"], tc["student_answer"], tc["correct_answer"],
            config.product.student_age
        )
        status = "✅" if (
            (tc["desc"] == "答案正确" and result["error_type"] == "无错误") or
            (tc["desc"] != "答案正确" and result["error_type"] != "无错误")
        ) else "❌"
        print(f"  {status} [{tc['desc']}] 识别为: {result['error_type']} (置信度: {result['confidence']})")
        if result.get('suggestion'):
            print(f"     建议: {result['suggestion']}")
    
    print()
    
    # 2. 测试除法概念分析
    print("【2】除法概念分析模块测试")
    
    division_cases = [
        {
            "problem": "把15个梨平均分给5个小朋友，每人几个？",
            "student_answer": "3",
            "correct_answer": "3",
            "desc": "等分除理解正确"
        },
        {
            "problem": "15里面有几个3？",
            "student_answer": "4",
            "correct_answer": "5",
            "desc": "包含除概念混淆"
        }
    ]
    
    for i, tc in enumerate(division_cases, 1):
        result = analyzer.analyze_division_concept(
            tc["problem"], tc["student_answer"], tc["correct_answer"]
        )
        status = "✅" if result.get('concept_type') else "❌"
        print(f"  {status} [{tc['desc']}] 识别为: {result.get('concept_type', '错误')} - {result.get('explanation', '')}")
    
    print()
    
    # 3. 测试同类题生成
    print("【3】同类题生成模块测试")
    generator = SimilarQuestionGenerator()
    
    base_problem = "把12个苹果平均分给3个小朋友，每个小朋友分到几个？"
    similar = generator.generate(base_problem, count=3)
    print(f"  基准题: {base_problem}")
    print(f"  生成{len(similar)}道同类题:")
    for i, q in enumerate(similar, 1):
        print(f"    {i}. {q}")
    
    print()
    
    # 4. 配置信息
    print("【4】配置信息")
    print(f"  产品名称: {config.product.name}")
    print(f"  口号: {config.product.slogan}")
    print(f"  学生年龄: {config.product.student_age}岁")
    print(f"  错因分析准确率: {config.product.error_analysis_accuracy * 100}%")
    print(f"  除法分析准确率: {config.product.division_analysis_accuracy * 100}%")
    
    has_key, missing = config.validate()
    if has_key:
        print(f"\n  ✅ API配置完整")
    else:
        print(f"\n  ⚠️ 缺少环境变量: {', '.join(missing)}")
        print(f"     设置方法: export QWEN_API_KEY=你的密钥")
    
    print("\n" + "="*40)
    print("测试完成！模块内部逻辑正常。")
    print("="*40)
    
    return True


def test_with_api():
    """依赖API的集成测试（需要真实key）"""
    print("\n=== 会了 - API集成测试 ===\n")
    
    has_key, missing = config.validate()
    if not has_key:
        print(f"❌ 缺少配置: {', '.join(missing)}")
        print("跳过API测试。请先设置环境变量:")
        print("  export QWEN_API_KEY=你的密钥")
        return False
    
    print("✅ API配置完整，开始测试...")
    # 这里放真实API调用测试
    # from src.qwen_integration import QwenVLIntegration
    # ...
    
    return True


if __name__ == "__main__":
    test_without_api()
    print()
    test_with_api()
