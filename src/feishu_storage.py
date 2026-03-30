#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书存储集成模块
负责将错题记录保存到飞书多维表格
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeishuStorage:
    def __init__(self):
        self.app_token = "XUyzbvWVsaExmFsTBp5cMNMvnEh"  # 从记忆中获取的飞书多维表格token
        self.table_id = "tbl_1234567890"  # 假设的表格ID，实际需要获取
        logger.info("飞书存储模块初始化完成")
    
    def save_error_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存错题记录到飞书多维表格
        
        Args:
            record_data: 错题记录数据
            
        Returns:
            dict: 保存结果
        """
        try:
            logger.info("开始保存错题记录到飞书")
            
            # 构造飞书记录格式
            fields = {
                "题目内容": record_data.get('problem', ''),
                "学生答案": record_data.get('student_answer', ''),
                "正确答案": record_data.get('correct_answer', ''),
                "错因类型": record_data.get('error_analysis', {}).get('error_type', ''),
                "置信度": str(record_data.get('error_analysis', {}).get('confidence', 0)),
                "错因解释": record_data.get('error_analysis', {}).get('explanation', ''),
                "改进建议": record_data.get('error_analysis', {}).get('suggestion', ''),
                "学生年龄": str(record_data.get('student_age', 8)),
                "记录时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "处理状态": "已分析"
            }
            
            # 如果有除法分析，添加到记录
            if 'division_analysis' in record_data.get('error_analysis', {}):
                div_analysis = record_data['error_analysis']['division_analysis']
                fields["除法类型"] = div_analysis.get('concept_type', '')
                fields["除法理解"] = div_analysis.get('understanding', '')
            
            # 模拟保存到飞书（实际项目中需要调用飞书API）
            record_id = f"rec_{int(datetime.now().timestamp())}"
            
            result = {
                'success': True,
                'record_id': record_id,
                'fields': fields,
                'message': '保存成功'
            }
            
            logger.info(f"错题记录保存成功，记录ID: {record_id}")
            return result
            
        except Exception as e:
            logger.error(f"保存错题记录失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': '保存失败'
            }
    
    def get_error_records(self, limit: int = 10) -> Dict[str, Any]:
        """
        获取错题记录
        
        Args:
            limit: 获取数量限制
            
        Returns:
            dict: 记录列表
        """
        try:
            logger.info(f"获取最近{limit}条错题记录")
            
            # 模拟获取记录（实际项目中需要调用飞书API）
            mock_records = [
                {
                    'record_id': 'rec_1234567890',
                    'fields': {
                        '题目内容': '小明有12个苹果，平均分给3个小朋友，每人几个？',
                        '学生答案': '3',
                        '正确答案': '4',
                        '错因类型': '计算错误',
                        '记录时间': '2026-03-25 08:00:00'
                    }
                }
            ]
            
            return {
                'success': True,
                'records': mock_records,
                'total': len(mock_records)
            }
            
        except Exception as e:
            logger.error(f"获取错题记录失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def update_review_status(self, record_id: str, reviewed: bool = True) -> Dict[str, Any]:
        """
        更新复习状态
        
        Args:
            record_id: 记录ID
            reviewed: 是否已复习
            
        Returns:
            dict: 更新结果
        """
        try:
            logger.info(f"更新记录{record_id}的复习状态")
            
            # 模拟更新（实际项目中需要调用飞书API）
            return {
                'success': True,
                'message': '状态更新成功',
                'record_id': record_id,
                'reviewed': reviewed
            }
            
        except Exception as e:
            logger.error(f"更新复习状态失败: {str(e)}")
            return {'success': False, 'error': str(e)}