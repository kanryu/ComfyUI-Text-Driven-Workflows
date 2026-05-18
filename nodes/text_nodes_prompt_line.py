from comfy_api.latest import io

class PromptLine(io.ComfyNode):
    """
    Part of 'ComfyUI Text-Driven Workflows'.
    Extracts lines from text to output as a string list.
    """

    color = "#225522"
    bgcolor = "#33aa33"

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TextDrivenPromptLine",
            display_name="Prompt Line (Text-Driven)",
            category="Text-Driven Workflows",
            # Registered natively as the hover tooltip text
            description="Extracts specific lines from a multi-line text to output as a list of strings for batch processing. If 'loops' is true, it wraps around to the beginning when max_rows exceeds available lines.",
            inputs=[
                io.String.Input("prompt", multiline=True, default=""),
                io.Int.Input("start_index", default=0, min=0, max=9999),
                io.Int.Input("max_rows", default=1000, min=1, max=9999),
                io.Boolean.Input("remove_empty_lines", default=True),
                io.Boolean.Input("loops", default=False),
            ],
            outputs=[
                io.String.Output("string_out", is_output_list=True),
            ],
        )

    @classmethod
    def execute(cls, prompt, start_index, max_rows, remove_empty_lines, loops, **kwargs) -> io.NodeOutput:
        lines = prompt.split('\n')
        if remove_empty_lines:
            lines = [line.strip() for line in lines if line.strip()]

        total = len(lines)
        if total == 0:
            return io.NodeOutput([])

        results = []
        if not loops:
            start = max(0, min(start_index, total - 1))
            end = min(start + max_rows, total)
            results = lines[start:end]
        else:
            for i in range(max_rows):
                idx = (start_index + i) % total
                results.append(lines[idx])

        return io.NodeOutput(results)