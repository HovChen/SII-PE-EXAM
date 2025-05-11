<h1 align="center">🎬 Movie Recommendation Reranking Task</h1>

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">中文</a>
</p>

<p align="center">
  A movie recommendation reranking system based on large language models,<br>
  which personalizes the ranking of candidate movies based on users' viewing history.
</p>

## ✨ Features

- Uses DeepSeek API for movie recommendation reranking
- Personalizes recommendations based on user viewing history
- Evaluates recommendation quality using NDCG@10

## 🚀 Usage

1. Create a `config.py` file and set your API key:
   ```python
   DEEPSEEK_API_KEY = "your_api_key_here"
   DEEPSEEK_BASE_URL = "https://api.deepseek.com"
   ```

2. Run the main program:
   ```
   python main.py
   ```

## 📁 File Description

- `main.py`: Main program that processes data and calls the API
- `template.py`: Prompt template construction and output parsing
- `config.py`: API configuration (needs to be created)
- `val.jsonl`: Validation dataset

## 📊 Results

- Avg NDCG@10: about 0.65 ~ 0.71
