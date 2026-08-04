from typing import Any

from openai import OpenAI

from models import ActScript


def get_openai_client(api_key: str) -> OpenAI:
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not configured.")
    return OpenAI(api_key=api_key)


def build_messages(
    system_prompt: str,
    raw_research: str,
    creative_override: str = "",
    previous_act: str = "",
) -> list[dict[str, str]]:
    previous_act_block = (
        f"PREVIOUS ACT (for continuity — pick up where this left off):\n{previous_act}\n\n"
        if previous_act
        else ""
    )
    override_block = (
        f"CREATIVE FREEDOM OVERRIDE:\n{creative_override}\n\n"
        if creative_override
        else ""
    )
    user_message = (
        "TASK:\n"
        "Read the raw research below and build the script.\n\n"
        "RULES (DO NOT BREAK THESE):\n"
        "1. BEAT COUNT: You must generate a MINIMUM of 12 to 15 narrative beats "
        "for this Act. Pack every beat with emotion. Make it hit hard.\n"
        "2. NO ROBOT VOICE: The narration must flow like a gripping novel spoken "
        "aloud — natural, emotional, and never mechanical.\n"
        "3. VISUAL TIMING: Place [VISUAL] tags wherever the camera naturally shifts — "
        "sometimes at the start of a sentence, sometimes mid-sentence, sometimes trailing. "
        "Never use the same position twice in a row. The tag must feel like the narrator "
        "pointing at something, not a robot stamp. Examples:\n"
        "  - Lead: \"[VISUAL] The door opened. She didn't move.\"\n"
        "  - Mid-sentence: \"He smiled, [VISUAL] the knife still wet in his hand, and stepped closer.\"\n"
        "  - Trail: \"She finally looked up. Her eyes were gone. [VISUAL]\"\n\n"
        f"{previous_act_block}"
        f"{override_block}"
        f"RAW RESEARCH PAYLOAD:\n{raw_research}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]


def parse_response(response: Any) -> ActScript:
    if not response.choices:
        raise ValueError("OpenAI returned no choices.")
    message = response.choices[0].message
    if message is None:
        raise ValueError("OpenAI returned a choice with no message.")
    parsed = getattr(message, "parsed", None)
    if parsed is None:
        raise ValueError("Response parsing failed or produced no structured output.")
    return ActScript.model_validate(parsed)
