# LLM Math Evaluation Harness

A simple toolkit to benchmark LLMs on various math tasks 🧮✨.

Currently supports:

**Models**:
- All HF 🤗 and [vLLM](https://github.com/vllm-project/vllm) supported models

**Datasets**:
- math,gsm8k,gsm-hard,svamp,asdiv,mawps,tabmwp,finqa,theorem-qa,bbh,hungarian_exam

**Prompts**:
- CoT / PAL / [ToRA](https://github.com/microsoft/ToRA)

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

### ⚖️ Run Evaluation

> For tests on fine-tuned models, adjust the `construct_prompt` function in `utils.py` to add prompt template first.

```
bash scritpts/run_math_eval.sh
```

Enjoy 🍻!


## 📊 Results

  
| Size     | Model               | gsm8k | math-oai | svamp | asdiv | mawps |  avg  |  
|----------|---------------------|:-----:|:--------:|:-----:|:-----:|:-----:|:-----:|  
| **1B**   | TinyLlama-1b-3T     |  3.00 |    3.00  | 11.30 | 18.20 | 20.10 | 11.12 |  
| **7B**   | Llama-7b            | 13.60 |    4.60  | 38.10 | 52.30 | 63.10 | 34.34 |  
|          | CodeLlama-7b        | 12.70 |    6.20  | 43.10 | 49.50 | 64.50 | 35.20 |  
|          | LLemma-7b           | 39.20 |   17.60  | 56.30 | 69.60 | 83.00 | 53.14 |  
|          | Mistral-7b          | 42.50 |   14.80  | 64.90 | 69.30 | 87.00 | 55.70 |  


## 🍀 Contributing

This project is still under active development. We welcome any contributions, including bug reports, feature requests, and pull requests.


## ☕️ References

- https://github.com/microsoft/ToRA
- https://github.com/openai/prm800k

