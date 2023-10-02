from typing import Dict, List


def gzip_to_json(gzip: str) -> List[Dict]:
    items = gzip.split('~')
    
    json_result = []
    for item in items:
        if item in ['', ' ']: continue
        item_params = item.split('¬')
        item_data = {}
        
        for param in item_params:
            if param in ['', ' ']: continue
            
            try:
                key, value = param.split('÷')
            except Exception:
                key, value = param.split('·')
            
            if item_data.get(key) is None:
                item_data[key] = value
            else:
                item_data[f'{key}_2'] = value
        
        json_result.append(item_data)
    return json_result
