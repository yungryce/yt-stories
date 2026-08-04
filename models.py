from typing import Any

from pydantic import BaseModel, Field


class DualLayerTemplate(BaseModel):
    atmosphere_visual_tone: str = Field(
        ..., description="Visual atmosphere — lighting, colors, mood, time of day"
    )
    foreground_action_detail: str = Field(
        ..., description="What's in the foreground: character expressions, movement, objects that drive the scene"
    )


class NarrativeBeat(BaseModel):
    timestamp_range: str = Field(..., description="Format: [MM:SS - MM:SS]")
    visual_asset_cue: str = Field(
        ..., description="What the viewer sees — lighting, where the camera looks, character expression, setting."
    )
    narration: str = Field(
        ..., description="The narrator's spoken words. Write like a novel read out loud. Drop [VISUAL] every time the camera moves."
    )


class ActScript(BaseModel):
    video_title: str
    video_description: str
    act_number: int
    act_title: str
    dual_layer_visual_template: DualLayerTemplate
    beats: list[NarrativeBeat]


class PipelineConfig(BaseModel):
    pipeline_name: str
    model_target: str
    hyperparameters: dict[str, Any]
