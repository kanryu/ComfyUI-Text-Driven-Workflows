##  Resolution Selector (Text-Driven)

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
