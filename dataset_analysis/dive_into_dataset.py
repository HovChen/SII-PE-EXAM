import json
import pandas as pd

data = []
with open('val.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

records = []
for d in data:
    history_ids    = [itm[0] for itm in d['item_list']]
    candidate_ids  = [itm[0] for itm in d['candidates']]
    target_id      = d['target_item'][0]
    
    overlap = len(set(history_ids) & set(candidate_ids) - {target_id})
    
    pos = candidate_ids.index(target_id) if target_id in candidate_ids else None
    
    records.append({
        'user_id':        d['user_id'],
        'history_len':    len(history_ids),
        'cand_len':       len(candidate_ids),
        'overlap':        overlap,
        'target_id':      target_id,
        'target_pos':     pos,
    })

df = pd.DataFrame(records)

print("=== 基本统计 ===")
print(df[['history_len', 'cand_len', 'overlap', 'target_pos']].describe())

print(df['target_pos'].value_counts(dropna=False).sort_index())

df.to_csv('./dataset_analysis/val_analysis.csv', index=False)
