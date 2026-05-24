from comfy_api.latest import io

class MultiPromptsTextDriven(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        # Define general inputs first
        inputs = [
            io.Combo.Input("num_prompts", options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], default="3"),
            io.String.Input("optional_text_in", optional=True, force_input=True),
        ]
        
        # Append controls sequentially to maintain the layout order (Text -> Multiplier -> Active)
        for i in range(1, 11):
            inputs.append(io.String.Input(f"text_{i}", multiline=True))
            inputs.append(io.Float.Input(f"multiplier_{i}", default=1.0, min=0.0, max=10.0, step=0.1))
            inputs.append(io.Boolean.Input(f"active_{i}", default=True))
            
        return io.Schema(
            node_id="TextDrivenMultiPrompts",
            display_name="Multi Prompts (Text-Driven)",
            category="Text-Driven Workflows",
            description=(
                "Allows simultaneous editing and management of multiple independent prompts within a single node. "
                "The text input fields dynamically expand or shrink based on the specified number, "
                "and you can toggle individual weights and output active states for each slot. "
                "All active prompts are automatically joined into a single comma-separated string output."
            ),
            inputs=inputs,
            outputs=[io.String.Output("string_out")]
        )

    @classmethod
    def execute(cls, num_prompts, **kwargs) -> tuple:
        num = int(num_prompts)
        prompts = []
        
        # Prepend optional text input if provided
        optional_text_in = kwargs.get("optional_text_in")
        if optional_text_in and isinstance(optional_text_in, str) and optional_text_in.strip():
            prompts.append(optional_text_in.strip())

        # Process each active slot up to the selected number
        for i in range(1, num + 1):
            active = kwargs.get(f"active_{i}", True)
            if not active:
                continue
            
            text = kwargs.get(f"text_{i}", "")
            if not isinstance(text, str) or not text.strip():
                continue
                
            text = text.strip()
            multiplier = kwargs.get(f"multiplier_{i}", 1.0)
            
            if multiplier == 1.0:
                prompts.append(text)
            else:
                # Round to 2 decimal places and strip trailing zeros (e.g., 1.10 -> 1.1)
                formatted_multiplier = f"{round(multiplier, 2):g}"
                prompts.append(f"({text}:{formatted_multiplier})")
                
        # Join prompts with a comma
        result_text = ",".join(prompts)
        
        # Remove spaces around punctuation marks
        result_text = result_text.replace(" ,", ",").replace(", ", ",")
        result_text = result_text.replace(" .", ".").replace(". ", ".")
        
        return (result_text,)