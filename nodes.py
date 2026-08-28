import comfy.utils


class GeniusScaleCrop:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),

                # Phase 1: Scale to maximum dimension
                "max_dimension": (
                    "INT",
                    {
                        "default": 864,
                        "min": 64,
                        "max": 8192,
                        "step": 8,
                    },
                ),

                "max_dim_method": (
                    [
                        "area",
                        "nearest-exact",
                        "bilinear",
                        "bicubic",
                        "lanczos",
                    ],
                ),

                # Phase 2: Scale to target size and optionally crop
                "target_width": (
                    "INT",
                    {
                        "default": 480,
                        "min": 64,
                        "max": 8192,
                        "step": 8,
                    },
                ),

                "target_height": (
                    "INT",
                    {
                        "default": 864,
                        "min": 64,
                        "max": 8192,
                        "step": 8,
                    },
                ),

                "scale_method": (
                    [
                        "nearest-exact",
                        "bilinear",
                        "area",
                        "bicubic",
                        "lanczos",
                    ],
                ),

                "crop": (
                    [
                        "center",
                        "disabled",
                    ],
                ),
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE")
    RETURN_NAMES = ("max_dim_image", "final_image")

    FUNCTION = "run"
    CATEGORY = "Genius/Image"

    def run(
        self,
        image,
        max_dimension,
        max_dim_method,
        target_width,
        target_height,
        scale_method,
        crop,
    ):
        # ComfyUI IMAGE format:
        # [batch, height, width, channels]

        original_height = image.shape[1]
        original_width = image.shape[2]

        # --------------------------------------------------
        # PHASE 1
        # Scale the largest dimension to max_dimension
        # while preserving the original aspect ratio.
        # --------------------------------------------------

        scale_factor = max_dimension / max(
            original_width,
            original_height,
        )

        max_dim_width = max(
            1,
            round(original_width * scale_factor),
        )

        max_dim_height = max(
            1,
            round(original_height * scale_factor),
        )

        # ComfyUI scaling functions expect:
        # [batch, channels, height, width]

        tensor = image.movedim(-1, 1)

        tensor = comfy.utils.common_upscale(
            tensor,
            max_dim_width,
            max_dim_height,
            max_dim_method,
            "disabled",
        )

        # First output:
        # image after Max Dimension scaling

        max_dim_image = tensor.movedim(1, -1)

        # --------------------------------------------------
        # PHASE 2
        # Scale to the requested target resolution.
        #
        # crop = center:
        # preserve aspect ratio and center crop
        #
        # crop = disabled:
        # resize directly to target width / height
        # --------------------------------------------------

        tensor = comfy.utils.common_upscale(
            tensor,
            target_width,
            target_height,
            scale_method,
            crop,
        )

        final_image = tensor.movedim(1, -1)

        return (
            max_dim_image,
            final_image,
        )