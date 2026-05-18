# ComfyUI-Text-Driven-Workflows

A smart, modular ComfyUI extension designed to streamline and supercharge text-driven workflows. This extension enables you to systematically organize, aggregate, and switch massive libraries of prompt formulas or character configurations with a single click, allowing you to batch-process multiple staging and direction plans simultaneously without cluttering your workspace.

By decoupling the "Character Core" from the "Scene/Staging Direction", you can build an agile, studio-grade prompt generation pipeline natively within ComfyUI V3.

---

## Key Features

* **Complete Prompt Modularization:** Separate your structural staging (lighting, camera angles, environment) from character prompts and swap them dynamically.
* **Native ComfyUI V3 Engine Support:** Built from the ground up using the latest ComfyUI V3 declarative API (`comfy_api.latest.io`), utilizing native features like safe dynamic `Autogrow` inputs.
* **Smart Batch Processing:** Extract, sequence, and loop string arrays natively to feed batch image generation queues perfectly.
* **Fault-Tolerant Execution:** Handles optional disconnected pins and extreme calculation bounds gracefully without throwing runtime workflow crashes.

---

## Included Nodes

### 1. Single Prompt (Text-Driven)

Manages a single prompt fragment with precision multiplier weighting and master active status control.

* **Inputs:**
* `text` (String, Multiline): The primary prompt fragment.
* `optional_text_in` (String, Force Input, Optional): An upstream text fragment to merge.
* `multiplier` (Float, Default: `1.0`, Range: `0.0` - `10.0`): Weight adjustment factor.
* `active` (Boolean, Default: `True`): Master bypass switch. If `False`, outputs an empty string instantly.


* **Behavior:** Automatically combines `text` and `optional_text_in` with correct spacing. If the multiplier is not `1.0`, it cleanly wraps the final text into standard attention weight syntax: `(combined_text:multiplier)`. Built to handle unlinked optional pins flawlessly.

### 2. Join Strings (Text-Driven)

Concatenates multiple string inputs into a single text block using a custom defined delimiter.

* **Inputs:**
* `delimiter` (String, Default: `""`): The string used to separate the text fragments (e.g., `, ` or `\n`).
* `string_inputs` (Autogrow Input): Dynamically expanding input slots.


* **Behavior:** Fully compliant with ComfyUI V3's native 0-indexed Autogrow behavior (`string0`, `string1`, etc.). Connecting a line from another node to an input pin automatically generates and increments a new input pin. You can connect as many input pins as you need. It extracts the index markers via regular expressions, sorts them numerically to maintain strict structural ordering, and joins them into a unified prompt block.

### 3. Prompt Line (Text-Driven)

Extracts specific lines from a multi-line text block to output as a structured string list, fully supporting batch image generation workflows.

* **Visual Identifiers:** Distinctive dark green design (`color: #225522`, `bgcolor: #33aa33`).
* **Inputs:**
* `prompt` (String, Multiline): The source asset block containing your lines/prompts.
* `start_index` (Int, Default: `0`): The line index to begin extraction.
* `max_rows` (Int, Default: `1000`): Maximum lines to extract.
* `remove_empty_lines` (Boolean, Default: `True`): Automatically cleans up whitespace and dead lines.
* `loops` (Boolean, Default: `False`): Wraparound toggle.


* **Behavior:** This node is specialized for batch image generation. By setting `max_rows` to 2 or more, it outputs multiple prompt lines simultaneously, allowing you to execute two or more prompts at the same time in a single batch generation run. The list output of this node can also be passed to downstream string manipulation nodes for further processing. If `loops` is `True`, it loops back to index `0` when the requested row count exceeds available lines.

### 4. Text Line Selector (Text-Driven)

A studio-grade scenario switch designed to store massive direction and staging plans externally.

* **Behavior:** Allows you to record dozens of rich staging configurations within the node or an external file and recall them instantly via a clean drop-down selector. You can input a label and the custom delimiter **`|-|`** (e.g., `Label|-|Prompt`) for each line of the multi-line text, which makes the options in the combo box much easier to read and select. It seamlessly pipes the chosen scenario prompt into downstream prompt-assembly nodes, completely removing the need to type out repetitive structures manually.

### 5. Resolution Selector (Text-Driven)

A dedicated resolution management utility designed to store preset aspect ratios and target dimensions externally.

* **Behavior:** Allows you to register major resolution pairs and switch between them instantly via a clean drop-down menu. It outputs the width and height dimensions directly into downstream generator or latent nodes, eliminating manual typing and aspect ratio calculation mistakes.
* **Note:** By default, this node lists preset resolutions that are popular for SDXL. You can easily modify the configurations to delete unnecessary rows or add your own preferred landscape resolutions.


```text
                       ┌──► width  ──────► [ Empty Latent Image ]
                       ├──► height ──────►
                       │
[ Resolution Selector ]│
                       ├──► width  ──────► [ CLIP Text Encode SDXL ]
                       │                    (width / target_width)
                       └──► height ──────►  (height / target_height)

```

### 6. Math (Int) (Text-Driven)

An advanced integer arithmetic core designed to calculate loops, steps, dimensions, and indexing logic safely.

* **Inputs:**
* `a` / `b` (Int, Range: `-999,999,999` to `999,999,999`): Supports massive negative and positive integer ranges.
* `operation` (Combo Select): `add`, `subtract`, `multiply`, `divide`, `modulo`, `power`, `shift`.


* **Advanced Logic:**
* `divide` / `modulo`: Allows natural zero-division runtime exceptions to propagate upstream safely.
* `power`: Implements safety range-guards to prevent system-freezing overflow.
* `shift` (Smart Bit-Shift): Intelligently reads the sign of `b`. Performs a standard Left Shift (`a << b`) if `b >= 0`, and automatically switches to a Right Shift (`a >> abs(b)`) if `b < 0` (capped safely at 31 bits).



---

## System Architecture & Workflow Philosophy

The driving philosophy behind this suite is **Modular Prompt Assembly**. Instead of maintaining monolithic, cluttered text nodes for every single prompt variation, this suite allows you to build a clean matrix:

```text
  [ Character Prompt Node ] ──┐
                              ▼
  [ Scene Direction Selector ] ──► [ Join Strings ] ──► [ KSampler ]
                              ▲
  [ Lighting/Style Node ] ────┘

```

By putting your complex environment and staging plans into the **Text Line Selector** or **Prompt Line**, you can pipeline up to dozens of unique cinematic directions, use the **Single Prompt** node to handle dynamic weights or on/off states, and merge them with a fixed character asset block. This results in incredibly organized, scalable, and automated generation grids.

---

## Installation

### Via ComfyUI Manager (Recommended)

1. Open ComfyUI and click on the **Manager** button.
2. Search for `ComfyUI Text-Driven Workflows`.
3. Click **Install**, then restart ComfyUI.

### Manual Git Clone

Navigate to your ComfyUI custom nodes directory and run:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/kanryu/ComfyUI-Text-Driven-Workflows.git

```

Restart your ComfyUI server to load the extension.

* **Note:**  No external Python dependencies required (pure ComfyUI V3 API).
---

## License

This project is licensed under the **GNU GPLv3 License** - see the LICENSE file for details. Developed and maintained by **KATO Kanryu** ([k.kanryu@gmail.com](mailto:k.kanryu@gmail.com)).
