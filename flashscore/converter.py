def gzip_to_json(gzip: str):
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
            item_data[key] = value
        
        json_result.append(item_data)
    return json_result
