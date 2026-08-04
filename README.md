# Storytelling Script Engine

This repository converts raw research markdown into structured video scripts using the OpenAI Python SDK and a configurable pipeline. Configured for Folklore, Drama, and Thriller content.

## What it does

- loads editorial voice from `global_config/System_Prompt.md`
- reads raw research from a topic directory
- sends a structured prompt to OpenAI
- validates the model output against a Pydantic schema
- writes a generated video script markdown file

## Setup

```bash
python3 -m pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key"
```

## Run

Generate one act at a time. For Acts 2 and 3, pipe in the previous act to maintain continuity:

```bash
# Act 1
python main.py \
  --topic-dir Stream/Your_Story \
  --input-file research.md \
  --output-file Act_01_Script.md

# Act 2 (carries forward Act 1 for continuity)
python main.py \
  --topic-dir Stream/Your_Story \
  --input-file research.md \
  --output-file Act_02_Script.md \
  --previous-act Act_01_Script.md

# Act 3
python main.py \
  --topic-dir Stream/Your_Story \
  --input-file research.md \
  --output-file Act_03_Script.md \
  --previous-act Act_02_Script.md
```

## Configuration

The pipeline is driven by `pipeline_config.json` which controls:

- `model_target` — the OpenAI model to use
- `hyperparameters` — `seed`, etc.

The output schema is hardcoded as the `ActScript` Pydantic model in `models.py`.

## Architecture

The pipeline is split into focused modules:

| Module | Role |
|---|---|
| `models.py` | Pydantic v2 schemas (`ActScript`, `NarrativeBeat`, etc.) |
| `config.py` | JSON/text loading, path resolution (walks up from `__file__`) |
| `pipeline.py` | Message building, OpenAI client, response parsing |
| `writer.py` | Markdown output with narration escaping |
| `main.py` | CLI argument parsing and orchestration |

See `AGENTS.md` for a full reference.

## Notes

- Output files are written inside the selected topic directory.
- Generate acts sequentially (Act 1 → Act 2 → Act 3) — each act's output becomes the `--previous-act` for the next.
- A manual editorial QA checklist lives in `Editorial_Pass_Protocol.md`.
