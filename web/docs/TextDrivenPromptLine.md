##  Prompt Line (Text-Driven)

Extracts specific lines from a multi-line text block to output as a structured string list, fully supporting batch image generation workflows.

* **Visual Identifiers:** Distinctive dark green design (`color: #225522`, `bgcolor: #33aa33`).
* **Inputs:**
* `prompt` (String, Multiline): The source asset block containing your lines/prompts.
* `start_index` (Int, Default: `0`): The line index to begin extraction.
* `max_rows` (Int, Default: `1000`): Maximum lines to extract.
* `remove_empty_lines` (Boolean, Default: `True`): Automatically cleans up whitespace and dead lines.
* `loops` (Boolean, Default: `False`): Wraparound toggle.


* **Behavior:** This node is specialized for batch image generation. By setting `max_rows` to 2 or more, it outputs multiple prompt lines simultaneously, allowing you to execute two or more prompts at the same time in a single batch generation run. The list output of this node can also be passed to downstream string manipulation nodes for further processing. If `loops` is `True`, it loops back to index `0` when the requested row count exceeds available lines.
