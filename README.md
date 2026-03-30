# 会了 - AI错题识别与讲解系统

**定位**：不是收集错题的工具，是消灭错题的教练。

**核心理念**：错题本的功能是解决错题，不是收集错题。

## 功能模块

| 模块 | 说明 | 状态 |
|------|------|------|
| 图片识别 | 硅基流动 PaddleOCR-VL | ✅ |
| 错因分析 | 本地规则引擎 | ✅ |
| AI讲解 | 引导式对话，3种方式 | ✅ |
| 同类题生成 | 基于错因生成练习题 | ✅ |
| 飞书存储 | 存入多维表格 | ✅ |
| 微信机器人 | 孩子交互界面 | 🔜 |

## 技术架构

- **视觉模型**：硅基流动 `PaddleOCR-VL` / `Qwen2-VL-72B-Instruct`
- **讲解模型**：硅基流动 `Qwen2.5-72B-Instruct`
- **错因分析**：本地规则引擎
- **存储**：飞书多维表格

## 快速开始

```bash
# 克隆
git clone https://github.com/Oooooldbai/hui-le.git
cd hui-le

# 设置API Key
export QWEN_API_KEY="你的硅基流动API_KEY"

# 本地测试
python3 main.py --test

# 演示讲解
python3 main.py --explain

# 完整流程
python3 main.py --workflow
```

## 项目结构

```
hui-le/
├── main.py                 # 主入口
├── config/
│   └── app_config.py       # 配置管理
├── src/
│   ├── error_analysis.py    # 错因分析
│   ├── explanation.py      # AI讲解模块
│   ├── similar_questions.py # 同类题生成
│   ├── qwen_integration.py  # 视觉识别
│   └── feishu_storage.py   # 飞书存储
├── tests/                  # 测试用例
└── data/                   # 数据目录
```

## 产品定位

**核心用户**：小学生家长（特别是出差、没时间辅导的）

**核心价值**：替家长陪伴，不是替代孩子思考

**差异化**：
- vs 喵喵机/试卷宝：我们不止记录，我们帮你讲解
- vs 学习机：我们用引导式对话，不是直接给答案
- vs 搜题App：我们不直接给答案，我们引导思考

## 相关文档

- 产品方案：https://www.feishu.cn/wiki/ZXajwuzdviKQRDkaJ31caBjdnLA
- 飞书多维表格：https://pcnd9j8jcbsd.feishu.cn/base/ODchblduoaOfOTsOrPhcTNwmnZe
