from comfy_api.latest import io

class TextLineSelector(io.ComfyNode):
    """
    Part of 'ComfyUI Text-Driven Workflows'.
    Selects a line from a multiline text field. Supports '|-|' separator 
    to split UI display label (left) from the actual output string value (right).
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        # 【更新】キャラクター名とLoRAタグ入りプロンプトをセパレータ '|-|' で繋いだデフォルト値
        default_entries = [
            "Character A (Standard)|-|<lora:char_a_v1:1.0>, character_a, blue hair, school uniform",
            "Character B (Paper-Ratio Style)|-|<lora:char_b_v2:0.8>, character_b, red dress, long hair",
            "Character C (Cinematic)|-|<lora:char_c_fantasy:1.2>, character_c, armor, holding sword"
        ]
        default_text = "\n".join(default_entries)
        
        # Establish initial backend fallback options from new presets
        initial_options = []
        for line in default_entries:
            line = line.strip()
            if not line:
                continue
            if "|-|" in line:
                parts = line.split("|-|")
                initial_options.append(parts[1].strip())
            else:
                initial_options.append(line)

        return io.Schema(
            # 新ブランド名に合わせたユニークIDと表示名
            node_id="TextDrivenTextLineSelector",
            display_name="Text Line Selector (Text-Driven)",
            category="Text-Driven Workflows", # カテゴリーも刷新
            description="Parses a multiline text field into a combo box. Uses '|-|' to separate the UI display label (left) from the actual output text (right).",
            inputs=[
                io.String.Input("text_list", multiline=True, default=default_text),
                io.Combo.Input("selected_line", options=initial_options, default=initial_options[0]),
            ],
            outputs=[
                io.String.Output("string"),
            ],
        )

    @classmethod
    def validate_inputs(cls, **kwargs) -> bool:
        return True

    @classmethod
    def execute(cls, text_list, selected_line, **kwargs) -> io.NodeOutput:
        return io.NodeOutput(selected_line or "")