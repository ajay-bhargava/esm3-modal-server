"""Modal Endpoint for the ESM3 model."""

import modal

###
# Modal Setup
###

# Container to execute the model
ESM3_IMAGE = (modal
              .Image
              .from_registry("nvidia/cuda:12.1.1-devel-ubuntu22.04", add_python="3.11")
              .pip_install("esm==3.0.0", "huggingface-hub", "torch", "pytz", "rich")
            )

# Time Constants
MINUTES = 60 # seconds

# Define the App
app = modal.App("example-esm3-inference-endpoint")

@app.cls(
    image=ESM3_IMAGE,
    timeout=5 * MINUTES,
    gpu="any",
    allow_concurrent_inputs=100,
)

#####
# Model Class
#####

class Model:
    """Model class for the ESM3 model."""

    @modal.enter()
    def warmup(self):
        """Instantiate the model."""
        from rich import print
        try:
            from datetime import datetime

            import pytz
            import torch
            from esm.models.esm3 import ESM3
            from huggingface_hub import login

        except ImportError as err:
            raise ImportError("Please install huggingface-hub and esm to download the model.") from err

        login(token="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")
        self.model = ESM3.from_pretrained("esm3_sm_open_v1", device=torch.device("cuda"))
        self.start_time = datetime.now(tz=pytz.timezone("UTC"))
        print("🏁 Starting up!")

    @modal.web_endpoint(method="POST", docs = True)
    def predict(self, sequence: str):
        """Run a prediction."""
        from datetime import datetime

        import pytz
        from esm.sdk.api import ESMProtein, GenerationConfig

        current_time = datetime.now(tz=pytz.timezone("UTC"))

        return {
            "sequence": sequence,
            "time": {"start": self.start_time,
                     "invoke": current_time,
                     "completion": current_time},
        }
