# LLM Math Evaluation Harness

A unified, precise, and extensible toolkit to benchmark LLMs on various mathematical tasks 🧮✨.

> 🔴🚀 **Important Notice**: We've identified variances above 5% in results from diverse math evaluation frameworks. To ensure fair and standardized comparisons across research, our toolkit strives to harmonize evaluation methods, promoting consistent and reliable math evaluation.

> 🌟 **In Practice**: Esteemed projects like [ToRA](https://github.com/microsoft/ToRA) (ICLR'24) and [DeepSeek-Coder](https://github.com/deepseek-ai/DeepSeek-Coder/tree/main/Evaluation/PAL-Math) have leveraged this suite!

### Features:

- **Models**: Seamless compatibility with models from Hugging Face 🤗 and [vLLM](https://github.com/vllm-project/vllm).

- **Datasets**: An extensive array of datasets including `math`, `gsm8k`, `gsm-hard`, `svamp`, `asdiv`, `mawps`, `tabmwp`, `finqa`, `theorem-qa`, `bbh`, `hungarian_exam`.

- **Prompts**: Diverse prompting paradigms, from Direct to Chain-of-Thought (CoT), Program-of-Thought (PoT/PAL), and [Tool-Integrated Reasoning (ToRA)](https://github.com/microsoft/ToRA).


- **Coming**:

    - [ ] Add support to MIT-OCW, MMLU-STEM, MMLU-MATH


## 🚀 Getting Started

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

### ⚖️ Evaluation

1. Configure model and data settings in `scripts/run_math_eval.sh`, and set the `PROMPT_TYPE` variable accordingly:
   - For base models, choose from: `direct`, `cot`, `pal`, or `tool-integrated`.
   - For SFT models, your options include: `tora`, `wizard_zs`, `deepseek-math`, etc.
     - To add new models, update the `construct_prompt` function in `utils.py` to include your new prompt template.
  
2. Run the script:

```bash  
bash scripts/run_math_eval.sh
```

## 📊 Results

### Base Models (CoT)

| Size     | Model                  | GSM8k | MATH-OAI | SWAMP | ASDiv | MAWPS |  AVG |
|----------|------------------------|:-----:|:--------:|:-----:|:-----:|:-----:|:-----:|
| **1B**   | TinyLlama-1b-3T        |  3.0  |    3.0   | 11.3  | 18.2  | 20.1  | 11.1  |
| **7B**   | Llama-7b               | 13.6  |    4.6   | 38.1  | 52.3  | 63.1  | 34.3  |
|          | CodeLlama-7b           | 12.7  |    6.2   | 43.1  | 49.5  | 64.5  | 35.2  |
|          | LLemma-7b              | 39.2  |   17.8   | 56.4  | 69.7  | 83.1  | 53.3  |
|          | Mistral-7b             | 42.5  |   14.8   | 64.9  | 69.3  | 87.0  | 55.7  |
|          | InternLM2-Math-Base-7B* | 42.8  |   16.2   | 59.0  | 67.5  | 83.9  | 53.9  |
|          | DeepSeek-Math-7B-Base  | 63.2  |   30.6   | 73.2  | 83.4  | 92.3  | 68.5  |

### SFT Models (CoT)

| Size     | Model                  | GSM8k | MATH-OAI | SWAMP | ASDiv | MAWPS |  AVG |
|----------|------------------------|:-----:|:--------:|:-----:|:-----:|:-----:|:-----:|
| **7B**   | DeepSeek-Math-Instruct* | 72.8  |   36.6   | 72.9  | 85.9  | 93.5  | 72.3  |
|          | DeepSeek-Math-RL       | 88.4  |   48.6   | 87.3  | 91.7  | 94.8  | 82.2  | 

***Note**: The results of `InternLM2-Math-Base-7B` and `DeepSeek-Math-Instruct` may have some bugs. We are working on fixing them.
 

## 🍀 Contributing

This project is still under active development. We welcome any contributions, including bug reports, feature requests, and pull requests.


## ☕️ References

- https://github.com/microsoft/ToRA
- https://github.com/openai/prm800k

