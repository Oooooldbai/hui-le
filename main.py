#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会了 - AI错题识别与讲解系统
主入口文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.error_analysis import ErrorAnalyzer
from src.similar_questions import SimilarQuestionGenerator
from src.explanation import ExplanationModule
from config.app_config import config


def test_local_modules():
    """不依赖API的本地模块测试"""
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
    print("本地模块测试完成！")
    print("="*40)


def explain_problem(problem: str, student_answer: str, correct_answer: str,
                   error_type: str, student_age: int = 8):
    """讲解一道错题"""
    print(f"\n{'='*50}")
    print(f"📚 开始讲解")
    print(f"{'='*50}")
    print(f"题目: {problem}")
    print(f"学生答案: {student_answer} | 正确答案: {correct_answer}")
    print(f"错因: {error_type}")
    print()

    explainer = ExplanationModule()
    result = explainer.explain(problem, student_answer, correct_answer, error_type, student_age)

    if result['status'] == 'success':
        print(result['explanation'])
        return result
    else:
        print(f"❌ 讲解生成失败: {result.get('explanation')}")
        return None


def full_workflow(image_path: str = None):
    """
    完整工作流：
    1. 图片识别（OCR）
    2. 错因分析
    3. AI讲解
    4. 同类题生成
    5. 存入飞书（待集成）
    """
    print("\n" + "="*60)
    print("🎯 会了 - 完整工作流")
    print("="*60)

    # 如果有图片，先OCR识别
    if image_path:
        print("\n【Step 1】图片识别...")
        # from src.qwen_integration import SiliconFlowVision
        # vision = SiliconFlowVision()
        # ocr_result = vision.recognize_problem(image_path)
        print(f"  图片: {image_path}")
        print("  (OCR功能需要图片路径)")

    # 示例：讲解一道真实错题
    print("\n【Step 2】AI讲解演示")
    result = explain_problem(
        problem="45 - 3 = ?",
        student_answer="37",
        correct_answer="42",
        error_type="退位减法错误",
        student_age=8
    )

    print("\n【Step 3】同类题生成")
    generator = SimilarQuestionGenerator()
    similar = generator.generate("45 - 3 = ?", count=3)
    print(f"  生成3道同类练习题:")
    for i, q in enumerate(similar, 1):
        print(f"    {i}. {q}")

    print("\n" + "="*60)
    print("✅ 完整流程演示结束")
    print("="*60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='会了 - AI错题讲解系统')
    parser.add_argument('--test', action='store_true', help='运行本地测试')
    parser.add_argument('--explain', action='store_true', help='演示讲解功能')
    parser.add_argument('--workflow', action='store_true', help='运行完整工作流')
    parser.add_argument('--image', type=str, help='图片路径')

    args = parser.parse_args()

    if args.test:
        test_local_modules()
    elif args.explain:
        explain_problem("45 - 3 = ?", "37", "42", "退位减法错误")
    elif args.workflow:
        full_workflow(args.image)
    else:
        print("会了 - AI错题讲解系统")
        print()
        print("用法:")
        print("  python3 main.py --test      # 本地模块测试")
        print("  python3 main.py --explain   # 演示讲解功能")
        print("  python3 main.py --workflow  # 完整工作流")
        print("  python3 main.py --image /path/to/image.jpg  # 图片识别+讲解")
        print()
        test_local_modules()
