# SAMPLE WORKFLOW: Text-Driven Multi-Prompt Batch Generation

* Multi-Prompt Batch Execution:
  Demonstrates how to generate multiple completely distinct scenes in a single 
  execution without increasing the latent batch size.

* Decoupled System Architecture:
  Separates the fixed "Character Asset" (managed via Text Line Selector) from 
  the variable "Action/Staging Plans" (sequenced via Prompt Line).

* The "Batch Size = 1 but 2 Images" Mechanic:
  - "Prompt Line" extracts multiple staging rows simultaneously (via max_rows >= 2).
  - The extracted rows are combined with the character base and fed into "Join Strings".
  - ComfyUI's KSampler detects the multiple text conditioning inputs and automatically 
    generates one unique image per prompt, even with a latent batch_size of 1.

* Native SDXL Resolution Driving:
  "Resolution Selector" simultaneously controls the dimensions for both 
  "Empty Latent Image" and "CLIP Text Encode SDXL" to prevent aspect ratio distortion.