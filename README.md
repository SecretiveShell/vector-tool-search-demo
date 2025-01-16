# Tool-DB

Disclaimer that this code is very old (>1 year) at the time of this repo creation and is not maintained. I have not tested the pyproject or have a copy of the original venv on hand. It is provided as a reference for anyone interested in the topic.

## Overview

The Tool DB project is a project based around providing an efficient scalable tool selection system for autonomous agents.

The Goals of the project are to allow small open source local LLMs to select tools with the same accuracy as GPT-3.5 level systems. This project was created before the release of LLAMA-2, and the soloution proposed was based on available resources at the time.

## How it works

The project works by first calculating vector embeddings of the descriptions of the tools available to the AI, and storing the results in an embeddings database. By structuring the prompt in a specific way, we can cause the LLM to generate a description of the perfect tool to complete a task. The embedding vectors for the perfect tool can be calculated, and then matched to the available tools using an algorithm such as cosine similarity.

This approach has considerable benefits such as:
- New tools can be added to the LLM automatically
- Tool descriptions can be extracted from github readme files allowing for a wide selection of open source programs to be used as tools
- If no tools exist we can add the description to a list and then focus dev time on the most requested tools
- An Agentic software soloution would ideally be able to implement tools independently based on this description

## running the software

This example depends on a few different projects:

### llama cpp

Llama cpp is used to run the LLM and generate the description for the required tool

### Chroma DB

Chroma DB is used to store the vector embeddings and calculate cosine similarity

### loop GPT

The tools I used for testing this concept originally came from the loop GPT project.

## Example

Below is an example session running the code. The top part is generic STDOUT logging

```
(.venv) AI $ & c:/Users/root/Documents/AI/.venv/Scripts/python.exe c:/Users/root/Documents/AI/src/tool-db.py
ggml_init_cublas: found 2 CUDA devices:
  Device 0: NVIDIA GeForce GTX 1050
  Device 1: NVIDIA GeForce GTX 1050
llama.cpp: loading model from C:\Users\root\Documents\tiny_tools\orca-mini-3b.ggmlv3.q4_0.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 512
llama_model_load_internal: n_embd     = 3200
llama_model_load_internal: n_mult     = 240
llama_model_load_internal: n_head     = 32
llama_model_load_internal: n_layer    = 26
llama_model_load_internal: n_rot      = 100
llama_model_load_internal: ftype      = 2 (mostly Q4_0)
llama_model_load_internal: n_ff       = 8640
llama_model_load_internal: n_parts    = 1
llama_model_load_internal: model size = 3B
llama_model_load_internal: ggml ctx size =    0.06 MB
llama_model_load_internal: using CUDA for GPU acceleration
ggml_cuda_set_main_device: using device 0 (NVIDIA GeForce GTX 1050) as main device
llama_model_load_internal: mem required  = 2862.72 MB (+  682.00 MB per state)
llama_model_load_internal: offloading 0 repeating layers to GPU
llama_model_load_internal: offloaded 0/29 layers to GPU
llama_model_load_internal: total VRAM used: 512 MB
llama_new_context_with_model: kv self size  =  162.50 MB
AVX = 1 | AVX2 = 1 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 1 | SSE3 = 1 | VSX = 0 |
adding google_search to db
adding browser to db
adding create_agent to db
adding message_agent to db
adding list_agents to db
adding delete_agent to db
adding write_to_file to db
adding read_from_file to db
adding append_to_file to db
adding delete_file to db
adding check_if_file_exists to db
adding list_files to db
adding get_cwd to db
adding make_directory to db
adding review_code to db
adding improve_code to db
adding write_tests to db
adding execute_python_file to db
adding evaluate_math to db
adding ask_user to db
adding shell to db
```

The requests are below


```
task: solve 3x^2=0
model is looking for:
         be able to perform polynomial operations on the given equation, such as factoring and squaring
evaluate_math
improve_code
review_code
task: execute chmod +x script.sh         
model is looking for:
         be able to execute the specified command in combination with the necessary permissions to modify files on the local system
shell
make_directory
write_to_file
task: find the best headphones on amazon
model is looking for:
         be able to search through Amazon's vast selection of headphones, compare multiple models based on criteria such as sound quality, comfort, design, and price, and provide a detailed report with recommendations for the user
google_search
review_code
ask_user
task:
```