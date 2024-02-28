# LLM Math Evaluation Harness

A simple toolkit to benchmark LLMs on various math tasks 🧮✨.

Currently supports:

**Models**:
- All HF 🤗 and [vLLM](https://github.com/vllm-project/vllm) supported models

**Datasets**:
- math,gsm8k,gsm-hard,svamp,asdiv,mawps,tabmwp,finqa,theorem-qa,bbh,hungarian_exam

**Prompts**:
- CoT / PAL / [Tool-Integrated Reasoning (ToRA)](https://github.com/microsoft/ToRA)

> This suite has been adopted in projects such as [ToRA](https://github.com/microsoft/ToRA) (ICLR'24) and [DeepSeek-Coder](https://github.com/deepseek-ai/DeepSeek-Coder/tree/main/Evaluation/PAL-Math). Here, we incrementally optimize the eval code and package it for future reuse.

**TODO**:
- [ ] Add support to MIT-OCW, MMLU-STEM, MMLU-MATH


## 🚀 Usage

### ⚙️ Environment Setup

#### Option 1: Conda

```
conda create -n math_eval python=3.10
conda activate math_eval
```

#### Option 2: Docker

We suggest using vLLM docker directly:

```
docker run --network host --cap-add=SYS_ADMIN --privileged -d \
    --entrypoint '' --name vllm \
    --runtime nvidia --gpus all \
    --security-opt apparmor:unconfined \
    --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
    -v /mnt:/mnt \
    -p 8000:8000 \
    vllm/vllm-openai:latest \
    sleep infinity
```

### Install

```
git clone https://github.com/ZubinGou/math-evaluation-harness.git
cd math-evaluation-harness
pip install -r requirements.txt
```

### 🚀 Evaluation Instructions

1. Configure model and data settings in `scripts/run_math_eval.sh`, and set the `PROMPT_TYPE` variable accordingly:
   - For base models, choose from: `direct`, `cot`, `pal`, or `tool-integrated`.
   - For SFT models, your options include: `tora`, `wizard_zs`, `deepseek-math`, etc.
     - To add new models, update the `construct_prompt` function in `utils.py` to include your new prompt template.
  
2. Run the script:

```bash  
bash scripts/run_math_eval.sh
```

## 📊 Results

### Base Models 

| Size     | Model               | gsm8k | math-oai | svamp | asdiv | mawps |  avg  |
|----------|---------------------|:-----:|:--------:|:-----:|:-----:|:-----:|:-----:|
| **1B**   | TinyLlama-1b-3T     |  3.0  |    3.0   | 11.3  | 18.2  | 20.1  | 11.1  |
| **7B**   | Llama-7b            | 13.6  |    4.6   | 38.1  | 52.3  | 63.1  | 34.3  |
|          | CodeLlama-7b        | 12.7  |    6.2   | 43.1  | 49.5  | 64.5  | 35.2  |
|          | LLemma-7b           | 39.2  |   17.6   | 56.3  | 69.6  | 83.0  | 53.1  |
|          | Mistral-7b          | 42.5  |   14.8   | 64.9  | 69.3  | 87.0  | 55.7  |

### SFT Models

| Size     | Model               | gsm8k | math-oai | svamp | asdiv | mawps |  avg  |
|----------|---------------------|:-----:|:--------:|:-----:|:-----:|:-----:|:-----:|
| **7B**   | DeepSeek-Math-RL    | 88.4  |   48.6   | 87.3  | 91.7  | 94.8  | 82.2  | 
 

## 🍀 Contributing

This project is still under active development. We welcome any contributions, including bug reports, feature requests, and pull requests.


## ☕️ References

- https://github.com/microsoft/ToRA
- https://github.com/openai/prm800k

