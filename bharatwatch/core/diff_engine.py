from typing import List, Dict, Any
import hashlib
import json

def item_key(item: Dict[str, Any], key_fields: List[str]) -> str:
    return "|".join(str(item.get(k, "")) for k in key_fields)

def compute_hash(items: List[Dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()

def compute_diff(old_items: List[Dict[str, Any]], new_items: List[Dict[str, Any]], key_fields: List[str]) -> List[Dict[str, Any]]:
    old_map = {item_key(i, key_fields): i for i in old_items}
    new_map = {item_key(i, key_fields): i for i in new_items}
    changes = []
    for k, v in new_map.items():
        if k not in old_map:
            changes.append({"change_type": "created", "before": None, "after": v})
        elif json.dumps(old_map[k], sort_keys=True) != json.dumps(v, sort_keys=True):
            changes.append({"change_type": "updated", "before": old_map[k], "after": v})
    for k, v in old_map.items():
        if k not in new_map:
            changes.append({"change_type": "deleted", "before": v, "after": None})
    return changes
