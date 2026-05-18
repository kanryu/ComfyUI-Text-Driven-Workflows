## Single Prompt (Text-Driven)

Manages a single prompt fragment with precision multiplier weighting and master active status control.

* **Inputs:**
* `text` (String, Multiline): The primary prompt fragment.
* `optional_text_in` (String, Force Input, Optional): An upstream text fragment to merge.
* `multiplier` (Float, Default: `1.0`, Range: `0.0` - `10.0`): Weight adjustment factor.
* `active` (Boolean, Default: `True`): Master bypass switch. If `False`, outputs an empty string instantly.


* **Behavior:** Automatically combines `text` and `optional_text_in` with correct spacing. If the multiplier is not `1.0`, it cleanly wraps the final text into standard attention weight syntax: `(combined_text:multiplier)`. Built to handle unlinked optional pins flawlessly.
