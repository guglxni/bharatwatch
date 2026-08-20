from typing import List, Dict, Any
import json
from pydantic import BaseModel, create_model

def build_validator(schema: Dict[str, Any]) -> type[BaseModel]:
    fields = {}
    for key, value in schema.items():
        if isinstance(value, str):
            fields[key] = (str, ...)
        elif isinstance(value, int):
            fields[key] = (int, ...)
        elif isinstance(value, bool):
            fields[key] = (bool, ...)
        elif isinstance(value, float):
            fields[key] = (float, ...)
        else:
            fields[key] = (str, ...)
    return create_model("Item", **fields)

def validate_items(items: List[Dict[str, Any]], sample: Dict[str, Any]) -> tuple[bool, List[Dict[str, Any]]]:
    if not items:
        return False, []
    Validator = build_validator(sample)
    valid = []
    for item in items:
        try:
            valid.append(Validator(**item).model_dump())
        except Exception:
            pass
    return len(valid) > 0, valid
