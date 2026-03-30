#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会了 - 错题集配置管理系统
"""

import os
from dataclasses import dataclass

@dataclass
class QwenConfig:
    """Qwen/Moonshot API配置"""
    api_key: str = ""
    base_url: str = "https://api.moonshot.cn/v1/chat/completions"
    model: str = "moonshot-vl-32k"  # 或 qwen-vl-max
    image_model: str = "qwen-vl-max"  # 视觉用 Qwen-VL-Max
    max_tokens: int = 2000
    temperature: float = 0.1

@dataclass
class FeishuConfig:
    """飞书配置"""
    app_token: str = "ODchblduoaOfOTsOrPhcTNwmnZe"
    app_secret: str = ""
    table_id: str = ""

@dataclass
class WeChatConfig:
    """微信机器人配置"""
    enabled: bool = False
    token: str = ""
    encoding_aes_key: str = ""
    app_id: str = ""
    app_secret: str = ""

@dataclass
class ProductConfig:
    """产品配置"""
    name: str = "会了"
    slogan: str = "错题本的功能是解决错题，不是收集错题"
    student_age: int = 8
    error_analysis_accuracy: float = 0.85
    division_analysis_accuracy: float = 0.90

class AppConfig:
    """应用配置管理器"""
    
    def __init__(self, env: str = "development"):
        self.env = env
        self.qwen = QwenConfig()
        self.feishu = FeishuConfig()
        self.wechat = WeChatConfig()
        self.product = ProductConfig()
        
        self._load_from_env()
        
    def _load_from_env(self):
        """从环境变量加载配置"""
        if os.getenv("QWEN_API_KEY"):
            self.qwen.api_key = os.getenv("QWEN_API_KEY")
        if os.getenv("FEISHU_APP_TOKEN"):
            self.feishu.app_token = os.getenv("FEISHU_APP_TOKEN")
        if os.getenv("FEISHU_APP_SECRET"):
            self.feishu.app_secret = os.getenv("FEISHU_APP_SECRET")
        if os.getenv("FEISHU_TABLE_ID"):
            self.feishu.table_id = os.getenv("FEISHU_TABLE_ID")
            
    def validate(self) -> bool:
        """验证必需配置"""
        errors = []
        if not self.qwen.api_key:
            errors.append("QWEN_API_KEY")
        if not self.feishu.app_token:
            errors.append("FEISHU_APP_TOKEN")
        return len(errors) == 0, errors

# 全局配置
config = AppConfig()
