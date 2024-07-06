"""Modal Endpoint for the ESM3 model."""

import modal

###
# Modal Setup
###


def download_model():
    """Download the ESM3 model."""
    try:
        import torch
        from esm.models.esm3 import ESM3
        from huggingface_hub import login

    except ImportError as err:
        raise ImportError("Please install huggingface-hub and esm to download the model.") from err

    login(token="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")
    ESM3.from_pretrained("esm3_sm_open_v1", device=torch.device("cuda"))


# Container to execute the model
ESM3_IMAGE = (
    modal.Image.from_registry("nvidia/cuda:12.1.1-devel-ubuntu22.04", add_python="3.11")
    .pip_install("esm==3.0.0", "huggingface-hub", "torch", "pytz", "rich")
    .run_function(download_model, gpu="any")
)

# Time Constants
MINUTES = 60  # seconds

# Define the App
app = modal.App("example-esm3-inference-endpoint")

#####
# Model Class
#####


@app.cls(
    image=ESM3_IMAGE,
    timeout=20 * MINUTES,
    container_idle_timeout=5 * MINUTES,
    gpu="any",
    mounts=[modal.Mount.from_local_python_packages("src.esm3_hacking.lib.deserializer")],
)
class Model:
    """Model class for the ESM3 model."""

    @modal.enter()
    def warmup(self):
        """Instantiate the model."""
        import torch
        from esm.models.esm3 import ESM3
        from rich import print

        self.model = ESM3.from_pretrained("esm3_sm_open_v1", device=torch.device("cuda"))
        print("🏁 Starting up!")

    @modal.web_endpoint(method="POST", docs=True)
    def predict(self, request: dict):
        """Run a prediction.

        Arguments:
        ---------
            request: A dictionary containing the sequence prompt and structure from the prompt to predict upon.

        """
        try:
            import time

            from esm.sdk.api import ESMProtein, GenerationConfig
            from rich import print
            from src.esm3_hacking.lib.deserializer import deserializer
        except ImportError as err:
            raise ImportError("Please install ESM to run the model.") from err

        # Deserialize the data
        data = deserializer(request)

        # Create the model input (Sequence)
        sequence_prompt = ESMProtein(
            sequence=data["sequence_prompt"],
            coordinates=data["structure_prompt"],
        )

        # Configuration (Sequence)
        sequence_configuration = GenerationConfig(
            track="sequence",
            num_steps=data["sequence_prompt"].count("_") // 2,
            temperature=0.5,
        )

        # Run the Model (Sequence Generation)
        start_time = time.time()
        sequence_prediction = self.model.generate(sequence_prompt, sequence_configuration)
        end_time = time.time()

        # Calculate the inference time
        inference_time = end_time - start_time

        # Configuration (Structure)
        structure_configuration = GenerationConfig(
            track="structure", num_steps=len(sequence_prediction) // 8, temperature=0.7
        )

        # Prompt Preparation (Structure)
        structure_prompt = ESMProtein(
            sequence=sequence_prediction.sequence,
        )

        # Run the Model (Structure Generation)
        start_time = time.time()
        structure_prediction = self.model.generate(structure_prompt, structure_configuration)
        end_time = time.time()

        # Calculate the inference time
        inference_time += end_time - start_time

        print(f"🎉 Prediction Complete! Complete Inference Time: {inference_time:.2f} seconds.")

        prediction_protein_chain = structure_prediction.to_protein_chain()
        pdb_buffer_object = prediction_protein_chain.to_pdb_string()

        return {"pdb": pdb_buffer_object, "inference_time": inference_time}
