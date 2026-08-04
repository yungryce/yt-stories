# Storytelling Script Engine

Converts raw research markdown into structured video scripts via OpenAI structured output, now configured for Folklore / Drama / Thriller content.

## Project
- Python CLI that reads research markdown + editorial config (System_Prompt.md), calls OpenAI `beta.chat.completions.parse` with a Pydantic schema, writes a formatted script.
- Stack: Python 3, `openai`, `pydantic`.
- Entry: `python main.py --topic-dir <dir> --input-file <md> --output-file <md> [--previous-act <md>]`.

## Commands
- Act 1: `python main.py --topic-dir Stream/Your_Story --input-file research.md --output-file Act_01_Script.md`
- Act 2: `python main.py --topic-dir Stream/Your_Story --input-file research.md --output-file Act_02_Script.md --previous-act Act_01_Script.md`
- Act 3: `python main.py --topic-dir Stream/Your_Story --input-file research.md --output-file Act_03_Script.md --previous-act Act_02_Script.md`
- Lint: `python -m py_compile models.py config.py pipeline.py writer.py main.py`
- Install deps: `pip install -r requirements.txt`

## Architecture
- `models.py` — Pydantic v2 schemas: `DualLayerTemplate` (atmosphere_visual_tone, foreground_action_detail), `NarrativeBeat`, `ActScript`, `PipelineConfig`
- `config.py` — JSON/text file loading, `load_pipeline_config()`, `resolve_global_config_dir()` (walks up from `__file__`)
- `pipeline.py` — `build_messages()`, `get_openai_client()`, `parse_response()` (with null-guard on `response.choices[0].message`)
- `writer.py` — `write_output()` with `escape_narration()` for markdown safety
- `main.py` — CLI (argparse) + orchestration; wires `seed` from config into the API call
- `pipeline_config.json` — model target, hyperparameters (seed)
- `global_config/` — `System_Prompt.md` (editorial voice), `Language_Ban_List.md` (banned words), `Creative_Freedom_Override.md` (anti-conservatism directive)
- `Stream/` — story directories; each contains `research.md` (input) and `Act_XX_Script.md` (generated output)

## Conventions
- Use `model_validate()` not `parse_obj()` (Pydantic v2)
- Global config paths resolved via `resolve_global_config_dir()`, never hardcoded CWD-relative
- Narration text escaped through `escape_narration()` before writing to markdown
- `pipeline_config.json` controls only model + hyperparameters; schema is hardcoded to `ActScript`
- Field naming: `DualLayerTemplate` uses `atmosphere_visual_tone` / `foreground_action_detail` (story-agnostic)
