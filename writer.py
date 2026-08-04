from pathlib import Path

from models import ActScript


def escape_narration(text: str) -> str:
    """Escape double-quotes so they don't break markdown inline quoting."""
    return text.replace('"', "'")


def write_output(script_package: ActScript, output_path: Path) -> None:
    """ Write the script package to a markdown file at the specified output path.
    Args:
        script_package (ActScript): The script package to write.
        output_path (Path): The path to the output markdown file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as out:
        out.write(f"# {script_package.video_title}\n\n")
        out.write(f"## Metadata Description:\n>{script_package.video_description}\n\n")
        out.write("### VISUAL TONE:\n")
        out.write(
            f"* **Atmosphere/Lighting:** {script_package.dual_layer_visual_template.atmosphere_visual_tone}\n"
        )
        out.write(
            f"* **Foreground Action:** {script_package.dual_layer_visual_template.foreground_action_detail}\n\n"
        )
        out.write("---\n\n")
        out.write(
            f"### ACT {script_package.act_number}: {script_package.act_title}\n\n"
        )

        for beat in script_package.beats:
            out.write(f"**{beat.timestamp_range} - Scene**:\n{beat.visual_asset_cue}\n\n")
            out.write(f"**Narration**: \"{escape_narration(beat.narration)}\"\n\n")
            out.write("───\n\n")

