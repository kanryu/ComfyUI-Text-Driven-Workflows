### Prompt Token Counter (Text-Driven)
An input-only visualization node that approximates token counts specifically for Stable Diffusion 1.5 and SDXL workflows.
* **Inputs:**
  * `prompt` (String, Force Input): The incoming combined prompt string from upstream nodes.
* **Behavior:** Utilizing a highly optimized, high-speed estimation algorithm, it dynamically shifts background colors (Green ≤ 65, Yellow 66–75, Red ≥ 76) to visually warn users before prompts breach the critical 75-token CLIP chunk threshold. Tokens forced into the second section or later have a significantly lower probability of being referenced accurately during rendering, potentially leading to image breakdown.
