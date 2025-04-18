from typing import Dict, Any

def render_template(template: str, context: Dict[str, Any]) -> str:
    # Helper class to allow dot-access and deep lookup
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

    # Merge and normalize context
    expanded = expand_dotted_keys({k: v for k, v in context.items() if '.' in k})
    base = {k: v for k, v in context.items() if '.' not in k}
    merged_context = to_dotdict(merge_dicts(expanded, base))

    # Evaluate based on prefix
    stripped = template.strip()
    if stripped.startswith(("f'''", 'f"""')):
        fstring_body = stripped[4:-3]
        return eval(f"f'''{fstring_body}'''", {}, merged_context)
    elif stripped.startswith(("f'", 'f"')):
        fstring_body = stripped[2:-1]
        return eval(f"f'{fstring_body}'", {}, merged_context)
    elif stripped.startswith("{") and stripped.endswith("}"):
        return eval(stripped[1:-1], {}, merged_context)
    else:
        return template



def _run_examples():
    examples = [
        # 1 - Direct dict output
        ("{test}", { "test": {"test_obj": 1} }),

        # 2 - Simple f-string with dict access
        ("f'Test: {test[\"test_obj\"]}'", { "test": {"test_obj": 1} }),

        # 3 - Expression evaluation
        ("{a + b}", { "a": 4, "b": 3 }),

        # 4 - Attribute access using dot notation in f-string
        ("f'Test layer: {test.inner}'", {"test.inner": 3, "test": 1}),

        # 5 - Direct attribute access expression
        ("{test.inner}", {"test.inner": 3, "test": 1}),

        # 6 - Comprehension inside raw expression
        (
            "{''.join(f\"<context_item>{r['text']}</context_item>\" for r in retriever.results)}",
            {
                "start.current_user_input": "Hello?",
                "retriever.results":[
                    {"text": "The answer is 42.", "gl": 0},
                    {"text": "The answer is 43.", "gl": 1},
                    {"text": "The answer is 44.", "gl": 2}
                ]
            }
        ),

        # 7 - Complex multiline f-string with embedded comprehension
        (
            "f'''Answer the question provided inside the <question></question> section. "
            "Base your answers in the citations from medical guidelines given in the <context></context> section.\n\n"
            "<question>{start.current_user_input}</question>\n\n"
            "<context>{ \"\".join(f\"<context_item>{r['text']}</context_item>\" for r in retriever.results) }</context>'''",
            {
                "start.current_user_input": "Hello?",
                "retriever.results": [
                    {"text": "The answer is 42.", "gl": 0},
                    {"text": "The answer is 43.", "gl": 1},
                    {"text": "The answer is 44.", "gl": 2}
                ]
            }
        )
    ]

    print("\n=======================")
    print(" Running Test Examples ")
    print("=======================\n")
    for i, (template, context) in enumerate(examples, 1):
        print(f"--- Example #{i} ---")
        print("Template:")
        print(template)
        print("Context:")
        print(context)
        try:
            result = render_template(template, context)
            print("Result:")
            print(result)
        except Exception as e:
            print("❌ Error:", str(e))
        print("\n" + "-"*40 + "\n")

# This will only run the tests when you execute the file directly
if __name__ == "__main__":
    _run_examples()