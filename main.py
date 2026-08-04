import argparse
import logging
import os
from pathlib import Path

from config import load_pipeline_config, load_text, resolve_global_config_dir
from models import ActScript
from pipeline import build_messages, get_openai_client, parse_response
from writer import write_output

logger = logging.getLogger(__name__)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a dramatic video script from raw research."
    )
    parser.add_argument(
        "--topic-dir",
        type=Path,
        required=True,
        help="Target topic directory containing input research and output destination.",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=Path("research.md"),
        help="Raw research markdown file inside the topic directory.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("Act_01_Script.md"),
        help="Output markdown file name inside the topic directory.",
    )
    parser.add_argument(
        "--previous-act",
        type=Path,
        default=None,
        help="Optional path to the previous act's generated script (relative to --topic-dir) for continuity context.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("pipeline_config.json"),
        help="Pipeline configuration JSON file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )
    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    config_path = args.config.resolve()
    topic_dir = args.topic_dir.resolve()
    input_path = topic_dir / args.input_file
    output_path = topic_dir / args.output_file

    try:
        pipeline_config = load_pipeline_config(config_path)
        global_dir = resolve_global_config_dir()
        system_prompt = load_text(global_dir / "System_Prompt.md")
        creative_override = load_text(global_dir / "Creative_Freedom_Override.md")
        raw_research = load_text(input_path)

        previous_act = ""
        if args.previous_act:
            previous_act_path = (topic_dir / args.previous_act).resolve()
            logger.info("Loading previous act from: %s", previous_act_path)
            previous_act = load_text(previous_act_path)

        client = get_openai_client(os.environ.get("OPENAI_API_KEY", ""))

        logger.info("Sending to OpenAI...")
        kwargs: dict = dict(
            model=pipeline_config.model_target,
            messages=build_messages(system_prompt, raw_research, creative_override, previous_act),
            response_format=ActScript,
        )
        temp = pipeline_config.hyperparameters.get("temperature")
        if temp is not None and temp != 0.0:
            kwargs["temperature"] = temp
        seed = pipeline_config.hyperparameters.get("seed")
        if seed is not None:
            kwargs["seed"] = seed

        response = client.beta.chat.completions.parse(**kwargs)

        script_package = parse_response(response)
        write_output(script_package, output_path)

    except FileNotFoundError as exc:
        raise SystemExit(f"ERROR: {exc}")
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc)
        raise SystemExit(1)

    logger.info("Script generated successfully at: %s", output_path)


if __name__ == "__main__":
    main()
