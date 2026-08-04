import json
from pathlib import Path
from typing import Any

from models import PipelineConfig


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_pipeline_config(config_path: Path) -> PipelineConfig:
    raw = load_json(config_path)
    # Drop unused expected_response_format if present — schema is hardcoded to ActScript
    raw.pop("expected_response_format", None)
    return PipelineConfig.model_validate(raw)


def resolve_global_config_dir() -> Path:
    """Return the global_config/ directory relative to this repo's root.

    How it works: walk up from this file until we find global_config/.
    """
    candidate = Path(__file__).resolve().parent
    while candidate != candidate.parent:
        gc = candidate / "global_config"
        if gc.is_dir():
            return gc
        candidate = candidate.parent
    raise FileNotFoundError("Cannot find global_config/ directory")
