# Genius Nodes for ComfyUI

Smart and practical custom nodes for ComfyUI.

**Genius Nodes** is a growing collection of compact tools designed to simplify common ComfyUI workflow tasks.

The goal is simple:

> Fewer nodes. Less manual calculation. Cleaner workflows.

---

## Included Nodes

### Genius Scale & Crop

**Genius Scale & Crop** prepares an image for a target output resolution in two connected stages.

1. Scale the image proportionally so its longest side matches the desired maximum dimension.
2. Crop the excess on the shorter side to reach the exact target resolution.

The important part is that the image is **not stretched or distorted**.

The node automatically calculates the proportional intermediate resolution, so there is no need to manually calculate aspect ratios or intermediate pixel dimensions.

---

## How It Works

The basic idea is simple:

The **longest side of the desired output resolution** is used as the `max_dimension`.

This means one dimension of the final output is already established during the first stage.

The other dimension is calculated automatically through proportional scaling.

After that, only the excess on the shorter dimension needs to be cropped.

---

## Portrait Example

Suppose the desired final output is:

```text
480 × 864
```

The longest side of the desired output is:

```text
864
```

Set:

```text
max_dimension = 864
```

The input image is then scaled proportionally until its longest side is exactly 864 pixels.

For example, an input image of:

```text
1024 × 1536
```

becomes:

```text
576 × 864
```

The height is now already correct.

The proportional width of 576 pixels was calculated automatically.

There is no need to calculate it manually.

For the final stage, set:

```text
target_width  = 480
target_height = 864
crop          = center
```

The 864-pixel height remains the intended final dimension.

Only the excess width needs to be removed:

```text
576 × 864
    ↓
480 × 864
```

With a centered crop, the excess width is removed equally from both sides.

The result matches the requested output resolution without stretching the image.

---

## Landscape Example

The same principle works in the opposite direction.

Suppose the desired final output is:

```text
864 × 480
```

The longest side is again:

```text
864
```

Set:

```text
max_dimension = 864
```

After proportional scaling, the intermediate image could for example be:

```text
864 × 576
```

The width is now already correct.

For the final stage, set:

```text
target_width  = 864
target_height = 480
crop          = center
```

The 864-pixel width remains the intended final dimension.

Only the excess height needs to be removed:

```text
864 × 576
    ↓
864 × 480
```

The image reaches the final target resolution without distortion.

---

## The Core Idea

The workflow follows this principle:

```text
Desired Output Resolution
        ↓
Take the Longest Side
        ↓
Use it as Max Dimension
        ↓
Proportional Scaling
        ↓
Automatic Intermediate Resolution
        ↓
Keep the Long Dimension
        ↓
Crop the Excess on the Short Dimension
        ↓
Exact Final Resolution
```

This avoids having to manually calculate the proportional intermediate size.

For example, if the final video resolution is:

```text
480 × 864
```

you already know that:

```text
max_dimension = 864
```

The node calculates the other dimension automatically.

If the result after proportional scaling is:

```text
576 × 864
```

you immediately know how much image area will be removed when cropping to:

```text
480 × 864
```

That intermediate result can also be previewed before the final crop.

---

## Why This Is Useful

Without this workflow, preparing an image for another aspect ratio often requires multiple separate nodes or manual calculations.

You may need to:

- determine the correct proportional intermediate resolution
- calculate the aspect ratio manually
- resize the image without distortion
- inspect the result
- crop the remaining excess
- connect multiple scaling and cropping nodes

**Genius Scale & Crop** combines that process into one compact node.

This helps reduce:

- unnecessary node chains
- manual aspect-ratio calculations
- intermediate resolution calculations
- trial and error
- accidental image distortion

---

## Inputs

### `image`

The input image.

---

### `max_dimension`

Defines the length of the longest side after the first scaling stage.

For the intended workflow, this should normally be the longest side of the desired final output resolution.

Example:

For:

```text
480 × 864
```

use:

```text
max_dimension = 864
```

For:

```text
864 × 480
```

use:

```text
max_dimension = 864
```

---

### `max_dim_method`

Defines the scaling algorithm used during the proportional Max Dimension stage.

Available methods include:

```text
area
nearest-exact
bilinear
bicubic
lanczos
```

---

### `target_width`

Defines the final requested image width.

---

### `target_height`

Defines the final requested image height.

For the intended Scale & Crop workflow, one of the two target dimensions normally remains equal to `max_dimension`.

The other dimension defines the final cropped size.

For example:

```text
max_dimension = 864

target_width  = 480
target_height = 864
```

or:

```text
max_dimension = 864

target_width  = 864
target_height = 480
```

This allows the same node to work naturally with both portrait and landscape formats.

---

### `scale_method`

Defines the scaling method used by the final ComfyUI scaling/cropping operation.

Available methods include:

```text
nearest-exact
bilinear
area
bicubic
lanczos
```

---

### `crop`

Current options:

```text
center
disabled
```

#### `center`

The image is cropped around its center to reach the requested final resolution.

#### `disabled`

Cropping is disabled.

---

## Outputs

### `max_dim_image`

The image after proportional scaling to `max_dimension`.

This output makes it possible to visually inspect the intermediate result before the final crop.

For example:

```text
Original:
1024 × 1536

Max Dimension Result:
576 × 864
```

This helps show how much image information is available before cropping.

---

### `final_image`

The finished image at the requested target resolution.

For example:

```text
480 × 864
```

This is normally the output connected to the next stage of the ComfyUI workflow.

---

## Why Two Outputs?

The two outputs make the transformation easy to inspect visually.

You can preview:

```text
Original Image
      ↓
Max Dimension Result
      ↓
Final Cropped Result
```

This allows you to check two important things:

1. The image quality and available resolution after proportional scaling.
2. The final composition after cropping.

This is especially useful when preparing images for resolution-sensitive workflows such as image-to-video generation.

---

## Installation

### ComfyUI Manager / Registry

Genius Nodes is available through the Comfy Registry and can be installed through ComfyUI Manager.

---

### Manual Installation

Clone this repository into the ComfyUI `custom_nodes` directory:

```bash
git clone https://github.com/GeniusGQ/ComfyUI-Genius-Nodes.git
```

Then restart ComfyUI.

The nodes are available under the Genius category.

---

## Philosophy

Genius Nodes are designed around small workflow problems that should have simple solutions.

Each node should aim to:

- solve a real workflow problem
- reduce unnecessary node chains
- reduce manual calculations
- remain understandable
- stay lightweight
- integrate naturally with ComfyUI
- make repetitive workflow tasks easier

More Genius Nodes are planned.

---

## Planned Improvements

Future versions of **Genius Scale & Crop** may add additional crop positioning controls.

Possible future options include:

```text
center
top
bottom
left
right
```

This would allow users to control which part of an image is removed when the final crop is applied.

Version 1.0 focuses on a simple and reliable centered Scale & Crop workflow.

---

## License

Genius Nodes are free to use in personal and commercial creative workflows.

Images, videos, workflows, and other outputs created with Genius Nodes may be used commercially.

The Genius Nodes software and source code itself may **not** be copied, redistributed, republished, rebranded, sold, incorporated into another distributed node pack, or commercially distributed without prior written permission.

ComfyUI workflow files that reference Genius Nodes may be freely shared.

Users receiving those workflows should obtain Genius Nodes through an official distribution channel.

See [LICENSE.txt](LICENSE.txt) for the complete license terms.

---

## Author

**Genius**

Comfy Registry Publisher:

```text
@genius
```

GitHub:

```text
GeniusGQ
```

---

Copyright © 2026 Genius / GeniusGQ  
All rights reserved.