from comfy_api.latest import io
import re

class TextLinePromptTextDriven(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        # Condense the sample into exactly 4 lines as initial defaults
        default_text = (
            "1girl, solo, emilia \\(re:zero\\), blonde hair,\n"
            "(abstract background:1.5),\n"
            "three quarter view, speed lines,\n"
            "(by carnelian:0.6),"
        )
        
        # Formatted initial options matching the startup state
        initial_options = [
            "1: 1girl, solo, emilia \\(re:zero\\), blonde hair",
            "2: (abstract background:1.5)",
            "3: three quarter view, speed lines",
            "4: (by carnelian:0.6)"
        ]

        return io.Schema(
            node_id="TextDrivenTextLinePrompt",
            display_name="Text Line Prompt (Text-Driven)",
            category="Text-Driven Workflows",
            description=(
                "An innovative bi-directional editing node that allows intuitive control of extensive prompt assets "
                "or line-separated concepts within a single text area. Selecting a line via the combobox lets you "
                "directly modify its multiplier or active state in real-time, rewriting the text content. "
                "Deactivated lines are commented out with '//' on the fly and automatically skipped during execution "
                "to yield a clean, concatenated string output."
            ),
            inputs=[
                io.String.Input("text", multiline=True, default=default_text),
                io.Combo.Input("selected_line", options=initial_options, default=initial_options[0]),
                io.Float.Input("multiplier", default=1.0, min=0.0, max=10.0, step=0.1),
                io.Boolean.Input("active", default=True),
                io.String.Input("optional_text_in", optional=True, force_input=True),
            ],
            outputs=[io.String.Output("string_out")]
        )

    @classmethod
    def validate_inputs(cls, **kwargs) -> bool:
        # Bypass strict backend list check to allow any dynamic string from JavaScript frontend
        return True

    @classmethod
    def execute(cls, text, selected_line, multiplier, active, **kwargs) -> tuple:
        prompts = []
        
        # Prepend optional text input if provided
        optional_text_in = kwargs.get("optional_text_in")
        if optional_text_in and isinstance(optional_text_in, str) and optional_text_in.strip():
            prompts.append(optional_text_in.strip())

        if text:
            lines = text.splitlines()
            for line in lines:
                cleaned = line.strip()
                if not cleaned:
                    continue
                
                # Check active status based on comment prefix '//'
                is_comment = cleaned.startswith("//")
                if is_comment:
                    cleaned = cleaned[2:].strip()
                
                if not cleaned:
                    continue
                
                # Strip trailing commas and surrounding spaces from the end of the line
                cleaned = re.sub(r',\s*$', '', cleaned).strip()
                
                # Skip commented-out lines for the final prompt string output
                if is_comment:
                    continue
                
                # Separate label if custom delimiter '|-|' exists
                if "|-|" in cleaned:
                    _, prompt_part = cleaned.split("|-|", 1)
                    prompt_part = prompt_part.strip()
                else:
                    prompt_part = cleaned
                
                if not prompt_part:
                    continue
                
                # Count only UNESCAPED open parentheses using lookbehind regex
                unescaped_open_count = len(re.findall(r'(?<!\\)\(', prompt_part))
                
                if unescaped_open_count >= 2:
                    # Multiple unescaped parentheses case - turn off multiplier logic, treat as 1.0
                    prompts.append(prompt_part)
                else:
                    # Try to extract global multiplier wrapper like (prompt:weight)
                    match = re.match(r'^\((.*):(\d+(?:\.\d+)?)\)$', prompt_part)
                    if match:
                        inner_content = match.group(1)
                        weight = float(match.group(2))
                        inner_unescaped_count = len(re.findall(r'(?<!\\)\(', inner_content))
                        if inner_unescaped_count == 0:
                            # Round and strip trailing zeros for output string (e.g., 1.10 -> 1.1)
                            formatted_weight = f"{round(weight, 2):g}"
                            prompts.append(inner_content if weight == 1.0 else f"({inner_content}:{formatted_weight})")
                        else:
                            prompts.append(prompt_part)
                    else:
                        prompts.append(prompt_part)
                    
        # Concatenate valid prompts into a unified comma-separated block
        result_text = ",".join(prompts)
        
        # Rigorously trim spaces around core punctuation marks
        result_text = result_text.replace(" ,", ",").replace(", ", ",")
        result_text = result_text.replace(" .", ".").replace(". ", ".")
        
        return (result_text,)