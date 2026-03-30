#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen-VL-Max模型集成模块
负责题目识别、OCR识别、答案计算
"""

import base64
import requests
import json
import logging
import os
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QwenVLIntegration:
    def __init__(self, api_key: str = None):
        """
        初始化Qwen-VL-Max集成
        
        Args:
            api_key: ModelScope API密钥
        """
        self.api_key = api_key or os.getenv('QWEN_API_KEY')
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model = "Qwen/Qwen2-VL-7B-Instruct"
        
    def recognize_problem(self, image_path: str) -> Dict[str, Any]:
        """
        识别题目内容、学生答案、计算正确答案
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            dict: 识别结果
        """
        try:
            logger.info(f"开始识别题目: {image_path}")
            
            # 读取图片并转为base64
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # 构建提示词
            prompt = """
请分析这张小学数学题图片，提取以下信息：
1. 完整的题目描述
2. 学生的答案（如果有的话）
3. 正确答案（请计算出结果）
4. 题目类型（计算、应用、几何等）

请用中文回答，格式如下：
题目：{题目描述}
学生答案：{学生写的答案}
正确答案：{正确计算结果}
题目类型：{类型}
"""
            
            # 调用Qwen-VL-Max API
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': prompt},
                            {'type': 'image_url', 'image_url': {
                                'url': f'data:image/jpeg;base64,{image_data}'
                            }}
                        ]
                    }
                ],
                'max_tokens': 1000,
                'temperature': 0.1
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 解析返回的内容
            parsed_result = self._parse_qwen_response(content)
            parsed_result['success'] = True
            
            logger.info("题目识别成功")
            return parsed_result
            
        except Exception as e:
            logger.error(f"题目识别失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _parse_qwen_response(self, content: str) -> Dict[str, Any]:
        """解析Qwen返回的内容"""
        lines = content.split('\n')
        result = {}
        
        for line in lines:
            if line.startswith('题目：'):
                result['problem_text'] = line.replace('题目：', '').strip()
            elif line.startswith('学生答案：'):
                result['student_answer'] = line.replace('学生答案：', '').strip()
            elif line.startswith('正确答案：'):
                result['correct_answer'] = line.replace('正确答案：', '').strip()
            elif line.startswith('题目类型：'):
                result['problem_type'] = line.replace('题目类型：', '').strip()
        
        # 如果解析失败，返回原始内容
        if 'problem_text' not in result:
            result['problem_text'] = content
            result['student_answer'] = ''
            result['correct_answer'] = ''
            result['problem_type'] = '未知'
        
        return result
    
    def calculate_answer(self, expression: str) -> str:
        """
        计算数学表达式答案
        
        Args:
            expression: 数学表达式
            
        Returns:
            str: 计算结果
        """
        try:
            # 简单的数学表达式计算
            # 生产环境中可以用更安全的方式
            expression = expression.replace('×', '*').replace('÷', '/')
            return str(eval(expression))
        except:
            return "无法计算"

# 测试代码
if __name__ == "__main__":
    client = QwenVLIntegration()
    result = client.recognize_problem("test_image.jpg")
    print(result)