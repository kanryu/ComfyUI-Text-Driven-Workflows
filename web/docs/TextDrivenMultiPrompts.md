### Multi Prompts (Text-Driven)
Allows simultaneous editing and management of multiple independent prompts within a single node.
* **Inputs:**
  * `num_prompts` (Combo, Options: `1` - `10`, Default: `3`): The number of active visible slots.
  * `optional_text_in` (String, Force Input, Optional): An upstream text fragment to merge.
  * `text_1` to `text_10` (String, Multiline): Individual prompt fragment slots.
  * `multiplier_1` to `multiplier_10` (Float, Default: `1.0`, Range: `0.0` - `10.0`): Weight factors for each slot.
  * `active_1` to `active_10` (Boolean, Default: `True`): Toggles the output state of each slot.
* **Behavior:** The text input fields dynamically expand or shrink based on the specified number to keep your workspace clean. You can toggle individual weights and output active states for each slot. All active prompts are automatically joined into a single comma-separated string output. It automatically strips trailing zeros from floating numbers (e.g., `1.10` becomes `1.1`) to ensure clean prompt injection.
