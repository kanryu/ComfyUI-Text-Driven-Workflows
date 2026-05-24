import logging
import sys
from comfy_api.latest import ComfyExtension

# Setup logging for the entire package
log = logging.getLogger("ComfyUI-Text-Driven-Workflows")
if not log.handlers:
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("[TextDrivenWorkflows] %(levelname)s: %(message)s"))
    log.addHandler(h)
    log.setLevel(logging.INFO)

_NODES = []
WEB_DIRECTORY = "web"
# Import individual node modules (Snake Case naming convention)
try:
    # Import Join Strings node
    from .nodes import text_nodes_join_strings
    _NODES.append(text_nodes_join_strings.JoinStrings)
    
    # Import Math (Int) node
    from .nodes import math_nodes_int
    _NODES.append(math_nodes_int.MathInt)
    
    # Import Multi Prompts node
    from .nodes import text_nodes_multi_prompts
    _NODES.append(text_nodes_multi_prompts.MultiPromptsTextDriven)
    
    # Import Prompt Line node
    from .nodes import text_nodes_prompt_line
    _NODES.append(text_nodes_prompt_line.PromptLine)
    
    # Import Resolution Selector node
    from .nodes import text_nodes_resolution_selector
    _NODES.append(text_nodes_resolution_selector.ResolutionSelector)
    
    # Import Single Prompt node
    from .nodes import text_nodes_single_prompt
    _NODES.append(text_nodes_single_prompt.SinglePrompt)
    
    # Import Text Line Prompt node
    from .nodes import text_nodes_text_line_prompt
    _NODES.append(text_nodes_text_line_prompt.TextLinePromptTextDriven)
    
    # Import Text Line Selector node
    from .nodes import text_nodes_text_line_selector
    _NODES.append(text_nodes_text_line_selector.TextLineSelector)
    
    log.info(f"Successfully loaded {len(_NODES)} nodes.")
except Exception as e:
    log.error(f"Failed to load nodes: {e}")

class TextDrivenWorkflowsExtension(ComfyExtension):
    """
    Unified extension class for ComfyUI Text-Driven Workflows.
    """
    async def get_node_list(self) -> list:
        return _NODES

async def comfy_entrypoint():
    return TextDrivenWorkflowsExtension()