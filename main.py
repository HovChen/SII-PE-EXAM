from openai import OpenAI
from template import construct_prompt, parse_output
import json
import math
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

def calculate_ndcg(sorted_ids, target_id, k=10):
    """
    计算 NDCG@K
    参数:
    sorted_ids (list): 模型输出的排序后的电影ID列表
    target_id (int): 实际观看的电影ID
    k (int): 计算NDCG的前K项
    返回:
    float: NDCG@K值
    """
    dcg = 0.0
    for i in range(min(k, len(sorted_ids))):
        if sorted_ids[i] == target_id:
            dcg = 1 / math.log2(i + 2)
            break
    idcg = 1 / math.log2(1 + 1)
    return dcg / idcg

def main():
    # 设置 DeepSeek API 客户端
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    
    # 读取 val.jsonl 文件
    with open('val.jsonl', 'r') as file:
        lines = file.readlines()
    
    # 用于计算平均 NDCG@10
    total_ndcg = 0.0
    count = 0
    
    # 处理每条记录
    for line in lines:
        # 解析 JSON 数据
        data = json.loads(line)
        
        # 构建提示词
        messages = construct_prompt(data)
        
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0,
            stream=False
        )
        
        # 获取模型输出
        output_text = response.choices[0].message.content
        
        # 解析输出
        sorted_movie_ids = parse_output(output_text)
        
        # 计算 NDCG@10
        ndcg_score = calculate_ndcg(sorted_movie_ids, data['target_item'][0], k=10)
        
        # 累加 NDCG 分数
        total_ndcg += ndcg_score
        count += 1
        
        # 打印结果
        print(f"No.{count}, User ID: {data['user_id']}，NDCG@10: {ndcg_score:.4f}")
    
    # 计算并打印平均 NDCG@10
    if count > 0:
        avg_ndcg = total_ndcg / count
        print(f"\nAvg NDCG@10: {avg_ndcg:.4f}")

if __name__ == "__main__":
    main() 
