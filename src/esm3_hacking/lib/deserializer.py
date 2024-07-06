"""Helper functions for serializing and deserializing data."""

def deserializer(data: dict):
    """Deserialize the sequence."""
    try:
        import base64
        import io

        import torch
    except ImportError as err:
        raise ImportError("You are missing imports.") from err

    if 'structure_prompt' in data:
        tensor_data = base64.b64decode(data['structure_prompt'])
        buffer = io.BytesIO(tensor_data)
        data['structure_prompt'] = torch.load(buffer)

    return data
