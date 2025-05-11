import json
import re
from json import JSONDecoder

def construct_prompt(d):
    """
    构造用于大语言模型的提示词
    
    参数:
    d (dict): jsonl数据文件的一行，为字典类型的变量，详细的数据格式见val.jsonl的说明
    
    返回:
    list: OpenAI API的message格式列表，允许设计多轮对话式的prompt
    示例: [{"role": "system", "content": "系统提示内容"}, 
           {"role": "user", "content": "用户提示内容"}]
    """
    system_prompt = (
        "# Movie Reranking Task\n"
        "\n"
        "- You are a **senior movie recommendation expert**.\n"
        "- Goal: **Maximize NDCG@10**.\n"
        "- Internally think step by step, but DO NOT output reasoning.\n"
        "- Final output MUST be exactly:\n\n"
        "  ```\n"
        "  <RESULT>[id1, id2, …]</RESULT>\n"
        "  ```\n"
        "- No extra text outside `<RESULT>` tags.\n"
    )

    messages = [{"role": "system", "content": system_prompt}]

    history = d["item_list"]
    chunk_size = 5
    for i in range(0, len(history), chunk_size):
        chunk = history[i : i + chunk_size]
        messages.append({
            "role": "user",
            "content": f"Here are some of the user's watched movies: {json.dumps(chunk, ensure_ascii=False)}"
        })
        messages.append({
            "role": "assistant",
            "content": "Understood."
        })

    candidate_content = json.dumps(d["candidates"], ensure_ascii=False)
    messages.append({
        "role": "user",
        "content": f"Now rank these candidate movies by relevance:\nCandidates: {candidate_content}"
    })

    return messages

def parse_output(text):
    """
    解析大语言模型的输出文本，提取推荐重排列表
    
    参数:
    text (str): 大语言模型在设计prompt下的输出文本
    
    返回:
    list: 从输出文本解析出的电影ID列表（python列表格式，列表的每个元素是整数，表示编号），表示重排后的推荐顺序
    示例: [1893, 3148, 111, ...]
    """
    m = re.search(r"<RESULT>([\s\S]*?)</RESULT>", text, re.S)
    if not m:
        raise ValueError(f"No <RESULT> block found:\n{text}")
    content = m.group(1).strip()

    decoder = JSONDecoder()
    try:
        ranked_ids, _ = decoder.raw_decode(content)
        return ranked_ids
    except json.JSONDecodeError:
        m2 = re.search(r"\[.*?\]", content, re.S)
        if not m2:
            raise ValueError(f"Cannot parse JSON array from content:\n{content}")
        return json.loads(m2.group(0))