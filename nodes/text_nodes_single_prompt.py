from comfy_api.latest import io

class SinglePrompt(io.ComfyNode):
    """
    Part of 'ComfyUI Text-Driven Workflows'.
    Manages a single prompt fragment with weight adjustment and active status control.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TextDrivenSinglePrompt",
            display_name="Single Prompt (Text-Driven)",
            category="Text-Driven Workflows",
            description="Outputs a prompt fragment combined from a text box and an optional input pin, allowing multiplier adjustment and output toggling via an active flag.",
            inputs=[
                io.String.Input("text", multiline=True, default=""),
                # Strictly changed the pin name to 'optional_text_in' as instructed
                io.String.Input("optional_text_in", force_input=True, default="", optional=True),
                io.Float.Input("multiplier", default=1.0, min=0.0, max=10.0, step=0.1),
                io.Boolean.Input("active", default=True),
            ],
            outputs=[
                io.String.Output("string_out")
            ],
        )

    @classmethod
    def execute(cls, text="", optional_text_in="", multiplier=1.0, active=True, **kwargs) -> io.NodeOutput:
        if not active:
            return io.NodeOutput("")
            
        combined_text = text
        # Evaluate optional_text_in to combine with the main text
        if optional_text_in and optional_text_in.strip():
            if combined_text.strip():
                combined_text += " " + optional_text_in
            else:
                combined_text = optional_text_in

        if multiplier != 1.0 and combined_text.strip():
            combined_text = f"({combined_text}:{multiplier:.2f})"

        return io.NodeOutput(combined_text)