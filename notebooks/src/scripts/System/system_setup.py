# scripts/System/system_setup.py

import json
import os
import re
from typing import Any


def _resolve_env_variables(obj: Any) -> Any:
    """
    Recursively resolve environment variables in a config object.
    Strings like "${ENV_VAR}" will be replaced by os.environ["ENV_VAR"].
    """
    if isinstance(obj, dict):
        return {k: _resolve_env_variables(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_resolve_env_variables(i) for i in obj]
    elif isinstance(obj, str):
        match = re.fullmatch(r"\$\{(\w+)\}", obj)
        if match:
            var_name = match.group(1)
            return os.environ.get(var_name, "")
        return obj
    else:
        return obj


def load_system_json(path: str) -> dict:
    """
    Loads a workflow system JSON from the given path and resolves environment variables.

    Args:
        path (str): Path to a JSON file.

    Returns:
        dict: Parsed and environment-resolved JSON config.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw_config = json.load(f)

    return _resolve_env_variables(raw_config)
