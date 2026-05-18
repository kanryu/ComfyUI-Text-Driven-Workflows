import re
from comfy_api.latest import io

class ResolutionSelector(io.ComfyNode):
    """
    Part of 'ComfyUI-Text-Driven-Workflows'.
    Outputs width and height based on a unique dynamic resolution combo box
    supporting intuitive, human-readable aspect ratio labels.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        # Default list layout updated with highly intuitive, human-centered aspect ratio labels
        default_resolutions = [
            "768x1024 (3:4)",
            "832x1216 (13:19)",
            "960x1280 (3:4)",
            "1024x1365 (3:4)",
            "1024x1496 (paper)",
            "1080x1440 (3:4)",
            "1152x1536 (3:4)",
            "1280x1728 (3:4)",
            "1536x1536 (1:1)"
        ]
        default_text = "\n".join(default_resolutions)
        
        # Extract initial values (e.g. "768x1024") by splitting at the space character
        initial_values = [r.split(" ")[0].lower() for r in default_resolutions]

        return io.Schema(
            # 新ブランド名に合わせたユニークIDと表示名
            node_id="TextDrivenResolutionSelector",
            display_name="Resolution Selector (Text-Driven)",
            category="Text-Driven Workflows", # カテゴリーも刷新
            description="Parses a multiline list of resolutions, allows selecting one via a dynamic combo box, and outputs the corresponding width and height.",
            inputs=[
                io.String.Input("resolutions_list", multiline=True, default=default_text),
                io.Combo.Input("selected_resolution", options=initial_values, default=initial_values[0]),
            ],
            outputs=[
                io.Int.Output("width"),
                io.Int.Output("height"),
            ],
        )

    @classmethod
    def validate_inputs(cls, **kwargs) -> bool:
        return True

    @classmethod
    def execute(cls, resolutions_list, selected_resolution, **kwargs) -> io.NodeOutput:
        width, height = 768, 1024
        
        if selected_resolution and "x" in selected_resolution:
            try:
                parts = selected_resolution.lower().split("x")
                width = int(parts[0])
                height = int(parts[1])
            except (ValueError, IndexError):
                pass
                
        return io.NodeOutput(width, height)