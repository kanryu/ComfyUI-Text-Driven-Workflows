### Text Line Prompt (Text-Driven)

An innovative editing node that allows intuitive control over long prompts entered with newline separations, enabling you to change attention weights or toggle skip on/off for each line with simple mouse clicks.

* **Inputs:**
  * `text` (String, Multiline): The main text area to enter your line-separated prompt fragments.
  * `selected_line` (Combo Select): Selects a specific line from the multi-line text to edit.
  * `multiplier` (Float, Default: `1.0`): Weight adjustment factor for the selected line.
  * `active` (Boolean, Default: `True`): Toggles the output state for the selected line.
* **Behavior:** Input parts or all of your prompts separated by newlines. By selecting a line via the combobox, you can adjust the weight multiplier or active status for that specific line. Deactivated lines are prepended with `//` and are automatically skipped during execution. The final output string from this node will have all newline characters removed at runtime.
