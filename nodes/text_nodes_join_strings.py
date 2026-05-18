import re
from comfy_api.latest import io

class JoinStrings(io.ComfyNode):
    """
    Part of 'ComfyUI Text-Driven Workflows'.
    Joins multiple strings together using a defined delimiter.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        # ComfyUI V3 native Autogrow is strictly 0-indexed (string0, string1...) by platform design.
        # No 'start' argument is supported in the TemplatePrefix constructor.
        string_template = io.Autogrow.TemplatePrefix(
            input=io.String.Input("string", force_input=True),
            prefix="string",
            min=1,
            max=100
        )

        return io.Schema(
            node_id="TextDrivenJoinStrings",
            display_name="Join Strings (Text-Driven)",
            category="Text-Driven Workflows",
            description="Concatenates multiple input strings into a single text output using a defined delimiter. Connecting an output to the first string pin automatically generates the next input pin.",
            inputs=[
                io.String.Input("delimiter", default=""),
                io.Autogrow.Input("string_inputs", template=string_template)
            ],
            outputs=[
                io.String.Output("string_out")
            ],
        )

    @classmethod
    def execute(cls, delimiter, string_inputs, **kwargs) -> io.NodeOutput:
        # Extract index numbers from string0, string1, string2... and sort them numerically
        sorted_keys = sorted(
            string_inputs.keys(),
            key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
        )
        
        strings_to_join = []
        for key in sorted_keys:
            val = string_inputs.get(key)
            if val is not None and str(val).strip() != "":
                strings_to_join.append(str(val))
        
        result = delimiter.join(strings_to_join)
        return io.NodeOutput(result)