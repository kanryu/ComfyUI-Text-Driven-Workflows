##  Join Strings (Text-Driven)

Concatenates multiple string inputs into a single text block using a custom defined delimiter.

* **Inputs:**
* `delimiter` (String, Default: `""`): The string used to separate the text fragments (e.g., `, ` or `\n`).
* `string_inputs` (Autogrow Input): Dynamically expanding input slots.


* **Behavior:** Fully compliant with ComfyUI V3's native 0-indexed Autogrow behavior (`string0`, `string1`, etc.). Connecting a line from another node to an input pin automatically generates and increments a new input pin. You can connect as many input pins as you need. It extracts the index markers via regular expressions, sorts them numerically to maintain strict structural ordering, and joins them into a unified prompt block.
