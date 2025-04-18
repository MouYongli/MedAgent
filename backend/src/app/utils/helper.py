from typing import Any, Dict
import re

class DotDict(dict):
    def __getattr__(self, item):
        value = self.get(item)
        if isinstance(value, dict):
            return DotDict(value)
        return value
    def __getitem__(self, item):
        if '.' in item:
            parts = item.split('.')
            value = self
            for part in parts:
                value = dict.__getitem__(value, part) if isinstance(value, dict) else getattr(value, part)
            return value
        return dict.__getitem__(self, item)

def expand_dotted_keys(d: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, value in d.items():
        parts = key.split(".")
        current = result
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result

def merge_dicts(primary: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(fallback)
    for k, v in primary.items():
        if isinstance(v, dict) and k in result and isinstance(result[k], dict):
            result[k] = merge_dicts(v, result[k])
        else:
            result[k] = v
    return result

def to_dotdict(obj):
    if isinstance(obj, dict):
        return DotDict({k: to_dotdict(v) for k, v in obj.items()})
    return obj

def resolve_template(template: str, context: Dict[str, Any]) -> Any:
    expanded = expand_dotted_keys({k: v for k, v in context.items() if '.' in k})
    base = {k: v for k, v in context.items() if '.' not in k}
    merged_context = to_dotdict(merge_dicts(expanded, base))

    if re.fullmatch(r"\{.*\}", template.strip()):
        inner_expr = template.strip()[1:-1]
        return eval(inner_expr, {}, merged_context)

    if template.strip().startswith("f'") or template.strip().startswith('f"'):
        fstring_content = template.strip()[2:-1]
        return eval(f"f'{fstring_content}'", {}, merged_context)

    if "{" in template and "}" in template:
        def replacer(match):
            expr = match.group(1)
            return str(eval(expr, {}, merged_context))
        return re.sub(r"\{(.*?)\}", replacer, template)

    return template
