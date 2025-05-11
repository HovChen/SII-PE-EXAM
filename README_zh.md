<h1 align="center">SII-PE 电影推荐重排序任务</h1>

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">中文</a>
</p>

<p align="center">
  基于大语言模型的电影推荐重排序系统，<br>
  针对用户历史观影记录，对候选电影进行个性化排序。
</p>

## 功能特点

- 使用 DeepSeek API 进行电影推荐重排序
- 基于用户历史观影记录进行个性化推荐
- 使用 NDCG@10 评估推荐质量

## 使用方法

1. 创建 `config.py` 文件并设置 API 密钥：
   ```python
   DEEPSEEK_API_KEY = "your_api_key_here"
   DEEPSEEK_BASE_URL = "https://api.deepseek.com"
   ```

2. 运行主程序：
   ```
   python main.py
   ```

## 文件说明

- `main.py`: 主程序，处理数据并调用 API
- `template.py`: 提示词模板构建和输出解析
- `config.py`: API 配置（需自行创建）
- `val.jsonl`: 验证数据集

## 实验结果

- 平均 NDCG@10: 大约 0.65 ~ 0.71