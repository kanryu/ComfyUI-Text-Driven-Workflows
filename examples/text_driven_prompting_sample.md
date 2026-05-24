# Text-Driven Prompting Workflow Guide

This workflow streamlines prompt management and eliminates manual weight tweaking by utilizing two custom nodes for layered control.

---

## Node Overview

### 1. Text Line Prompt (Text-Driven)
Manages a list of prompt assets or concepts line by line.
* **Bi-directional Sync:** Select a line via the dropdown menu to modify its multiplier or active state. The raw text area updates automatically in real-time.
* **Muting Function:** Deactivating a line prepends `//` to comment it out. These lines are completely skipped during backend execution to output a clean string.
* **Regex Parsing:** Properly handles character LoRA escaped brackets `\( \)` and safely bypasses rows containing multiple unescaped brackets.

### 2. Multi Prompts (Text-Driven)
Provides centralized layer-control for multiple modifiers.
* **Dynamic UI Layout:** Input fields dynamically hide or show based on the "num_prompts" value (up to 10 slots) to keep the canvas clean.
* **Granular Controls:** Allows you to adjust individual multipliers and toggle the active state of each prompt fragment with a single click.

---

## Workflow Pipeline

The nodes are connected in a relay structure to compile the final prompt:

1. **Base Generation:** [Text Line Prompt] manages base characters, core concepts, or specific styles.
2. **Modifier Stacking:** The selected base prompt is fed into [Multi Prompts] via the hidden `optional_text_in` input pin.
3. **Final Output:** [Multi Prompts] appends aesthetic modifiers (lighting, attire, quality tokens), then sends the fully combined string directly to the SDXL CLIP Text Encode.

### Quick Start
1. Choose a row in **Text Line Prompt** using the dropdown menu.
2. Tweak individual weights or toggle active states in **Multi Prompts**.
3. Click **Queue Prompt** to execute.