# Running an ESM3 Inference Server

>[!NOTE]
> This is strictly for personal and educational exploration uses. Evolutionary Scale AI's ESM3 [terms of service](https://github.com/evolutionaryscale/esm?tab=readme-ov-file#license) strictly prohibits the commercial production of an API that uses ESM3. Please review their terms and conditions before using this code.

This guide will walk you through the process of setting up an ESM3 Inference Server. This server will allow you to interact with the ESM3 model through a REST API. This guide will cover the following steps:

1. Getting [Hugging Face Transformers](https://huggingface.co/transformers/) access token for the model.

2. Modal

3. Running the `.ipynb` file to send a request to the server.


# What is ESM3?

ESM3 is a protein language model developed by [Evolutionary Scale AI](https://evolutionaryscale-public.s3.us-east-2.amazonaws.com/research/esm3.pdf). It is able to reason protein structures. It is trained on a combination of structure, function and seqeuence data. As a generative masked model, you can present partial sequences to the model and it will generate the rest of the sequence given a set of blanks. The general model architecture is presented below. 

![ESM3 Architecture](./docs/ESM3%20Architecture.png)

# Environment Setup

Ensure you have `uv` installed as your package manager. Use:

```bash
uv pip install -r requirements.txt
```

to install the required packages.

Then run the following command to start your envrionment:

```bash
source .venv/bin/activate
```

# How to Run the ESM3 Inference Server
### Step 1: Getting Hugging Face Transformers Access Token
---

[Hugging Face](https://huggingface.co/EvolutionaryScale/esm3-sm-open-v1) hosts the ESM3 model. You will need to get an access token and accept the terms of service laid out on Hugging Face for this model.



### Step 2: Storing the HF secrets for the Inference Server (Modal)
---

You will need to store an `.env` variable for your hugging face token. This is stored on the [Modal Dashboard](https://modal.com/). 


### Step 3a: Running your Modal Server
---

To run the Modal Server ephermerally, use the following command:

```bash
modal serve src/esm3_hacking/endpoint.py
```

You are now able to make inference requests to the ephemeral server.


### Step 3b: Running the `.ipynb` file
---

This is self-explanatory. You will need to run the `.ipynb` file to send a request to the server.


