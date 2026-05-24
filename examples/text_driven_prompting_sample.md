# Text-Driven Prompting Workflow Guide

This workflow streamlines prompt management and eliminates manual weight tweaking by utilizing dedicated custom nodes for layered control and real-time validation.

## Node Overview

### 1. Text Line Prompt (Text-Driven)
Manages a list of prompt assets or concepts line by line.
- **Bi-directional Sync**: Select a line via the dropdown menu to modify its multiplier or active state. The raw text area updates automatically in real-time.
- **Muting Function**: Deactivating a line prepends `//` to comment it out. These lines are completely skipped during backend execution.

### 2. Multi Prompts (Text-Driven)
Allows managing multiple independent prompt blocks simultaneously within a single node.
- **Layered Control**: Each prompt block can be independently weighted with a multiplier or toggled active/inactive, streamlining the blending of styles, characters, and environments.

### 3. Prompt Token Counter (Text-Driven)
An input-only visualization node designed specifically for Stable Diffusion 1.5 and SDXL to estimate the total token count of the incoming combined prompt.
- **Real-time Color Signals**: 
  - **Green (≤ 65 tokens)**: Safe zone. The entire prompt fits comfortably within the primary context chunk.
  - **Yellow (66–75 tokens)**: Warning zone. Approaching the absolute hardware limit of a single CLIP text encoder chunk.
  - **Red (≥ 76 tokens)**: Danger zone. The prompt will be sliced into multiple chunks (sections).
- **Chunk Slicing Risk**: Tokens forced into the second section or later have a significantly lower probability of being referenced accurately during rendering, which can dilute attention weights, skew character concepts, or lead to image breakdown.
- **Approximation Note**: Since a strictly exact calculation requires a massive dictionary (~49k words), this node utilizes a highly optimized, high-speed approximation algorithm. The displayed count serves as a close reference estimate.

### 4. Join Strings (Text-Driven)
Concatenates strings from multiple text-driven nodes using a customizable delimiter (e.g., a comma), serving as the bridge to consolidate your structured prompt layers into a single continuous stream.