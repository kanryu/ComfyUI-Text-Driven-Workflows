from comfy_api.latest import io
import re
from server import PromptServer

class PromptTokenCounterTextDriven(io.ComfyNode):
    # Enforce this node as an execution terminal endpoint
    OUTPUT_NODE = True

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TextDrivenPromptTokenCounter",
            display_name="Prompt Token Counter (Text-Driven)",
            category="Text-Driven Workflows",
            description=(
                "A prompt token counter node designed for Stable Diffusion 1.5 and SDXL. "
                "Executing this node or running the project calculates an approximate token count "
                "for the generation prompt. Because a strictly accurate calculation requires a massive dictionary, "
                "the algorithm is simplified, making this count a close estimate for reference only.\n\n"
                "- 65 tokens or fewer: Background turns Green.\n"
                "- 66 to 75 tokens: Background turns Yellow.\n"
                "- 76 tokens or more: Background turns Red.\n\n"
                "Tokens beyond 76 are pushed into the second chunk (section) or later. "
                "These tokens have a significantly lower probability of being referenced during rendering, "
                "potentially causing image degradation or generation breakdown."
            ),
            is_output_node=True,
            inputs=[
                io.String.Input("prompt", force_input=True),
            ],
            hidden=[
                io.Hidden.unique_id
            ],
            outputs=[]
        )

    @classmethod
    def execute(cls, prompt) -> tuple:
        unique_id = cls.hidden.unique_id
        
        if not prompt:
            count = 2
        else:
            text_lower = prompt.lower()
            t = re.sub(r'[\r\n\t]', ' ', text_lower)
            t = t.replace('\\(', ' a ').replace('\\)', ' a ')
            t = re.sub(r':\d+(?:\.\d+)?', ' a ', t)
            t = t.replace(')', ' a ').replace(',', ' a ').replace("'", ' a ')
            
            suffixes = [
                'ment ', 'tion ', 'ness ', 'able ', 'ible ', 'less ', 'full ', 'fully ',
                'ing ', 'est ', 'ive ', 'ted ', 'sed ', 'red ', 'ped ', 'lly ',
                'ed ', 'ly ', 'ry ', 'es ', 'al ', 'ic ', 'er ', 's '
            ]
            
            for suffix in suffixes:
                t = t.replace(suffix, ' a ')
                
            t = re.sub(r'\s+', ' ', t).strip()
            
            if not t:
                count = 2
            else:
                base_count = t.count(' ') + 1
                count = base_count + 2
        
        cls._send_to_ui(unique_id, count)
        return ()

    @classmethod
    def _send_to_ui(cls, node_id, count):
        if node_id is not None:
            PromptServer.instance.send_sync(
                "text_driven_token_count_update", 
                {"node_id": str(node_id), "count": str(count)}
            )