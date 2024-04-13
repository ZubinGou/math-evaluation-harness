# LLM Math Evaluation Harness

A unified, precise, and extensible toolkit to benchmark LLMs on various mathematical tasks 🧮✨.

> 🔴🚀 **Important Notice**: We've identified variances above 5% in results from diverse math evaluation frameworks. To ensure fair and standardized comparisons across research, our toolkit strives to harmonize evaluation methods, promoting consistent and reliable math evaluation.

> 🌟 **In Practice**: Esteemed projects like [ToRA](https://github.com/microsoft/ToRA) (ICLR'24) and [DeepSeek-Coder](https://github.com/deepseek-ai/DeepSeek-Coder/tree/main/Evaluation/PAL-Math) have leveraged this suite!

### Features:

- **Models**: Seamless compatibility with models from Hugging Face 🤗 and [vLLM](https://github.com/vllm-project/vllm).

- **Datasets**: An extensive array of datasets including `minerva_math`, `math`, `math_oai`, `gsm8k`, `gsm_hard`, `svamp`, `asdiv`, `mawps`, `tabmwp`, `finqa`, `theorem_qa`, `bbh`, `mmlu_stem`, `sat_math`, `mathqa`, `hungarian_exam`.

- **Prompts**: Diverse prompting paradigms, from Direct to Chain-of-Thought (CoT), Program-of-Thought (PoT/PAL), and [Tool-Integrated Reasoning (ToRA)](https://github.com/microsoft/ToRA).


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
bash scripts/run_eval.sh $PROMPT_TYPE $MODEL_NAME_OR_PATH
```


## 📊 Results

### Base Models (CoT)

> PROMPT_TYPE=cot

| Model                                                         | Size | Data   | Uniq. Token | Train Token | GSM8K | MATH[^1] | SVAMP | ASDiv | MAWPS | TAB[^2]   | MQA  | MMLU STEM | SAT | AVG  |
|---------------------------------------------------------------|--------------------------|--------|--------------|------------|-------|----------------|-------|-------|-------|-------|------|-----------|----------------|------|
| **1-2B Base Models**                                          |                          |        |              |            |       |                |       |       |       |       |      |           |                |      |
| [Tinyllama](https://huggingface.co/Tinyllama/Tinyllama-1.1B-intermediate-step-1431k-3T) | 1.1B                     | -      | -            | -          | 2.9   | 3.2            | 11.0  | 18.1  | 20.4  | 12.5  | 14.6 | 16.1      | 21.9           | 13.4 |
| [Phi-1.5](https://huggingface.co/microsoft/phi-1_5)            | 1.3B                     | -      | -            | -          | 32.4  | 4.2            | 43.4  | 53.1  | 66.2  | 24.4  | 14.3 | 21.8      | 18.8           | 31.0 |
| [Qwen1.5](https://huggingface.co/Qwen/Qwen1.5-1.8B)            | 1.8B                     | -      | -            | -          | 36.1 | 6.8            | 48.5 | 63.6 | 79.0 | 29.2  | 25.1 | 31.3      | 40.6           | 40.0 |
| [Gemma](https://huggingface.co/google/gemma-2b)                | 2.0B                     | -      | -            | -          | 18.8  | 11.4           | 38.0  | 56.6  | 72.5  | **36.9** | 26.8 | **34.4**  | 50.0           | 38.4 |
| DeepSeekLLM                                                   | 1.3B                     | OWM    | 14B          | 150B       | 11.5  | 8.9            | -     | -     | -     | -     | -    | 29.6      | 31.3           | -    |
| DeepSeekMath                                                  | 1.3B                     | -      | 120B         | 150B       | 23.8  | 13.6       | -     | -     | -     | -     | -    | 33.1  | **56.3**      | -    |
| [Rho-Math](https://huggingface.co/microsoft/rho-math-1b-v0.1)                                                 | 1.1B                     | OWM    | 14B          | **30B**    | **36.2** | **15.6**       | **52.1** | **67.0** | **83.9** | 29.0 | **32.5** | 23.3  | 28.1      | **40.9** |
| **>= 7B Base Models**                                      |                          |        |              |            |       |                |       |       |       |       |      |           |                |      |
| [LLaMA-2](https://huggingface.co/meta-llama/Llama-2-7b-hf)    | 7B                       |        | -            | -          | 14.0  | 3.6            | 39.5  | 51.7  | 63.5  | 30.9  | 12.4 | 32.7      | 34.4           | 31.4 |
| [Mistral](https://huggingface.co/mistralai/Mistral-7B-v0.1)  | 7B                       |        | -            | -          | 41.2  | 11.6           | 64.7  | 68.5  | 87.5  | 52.9  | 33.0 | 49.5      | 59.4           | 52.0 |
| Minerva                                                       | 8B                       | -      | 39B          | 164B       | 16.2  | 14.1           | -     | -     | -     | -     | -    | 35.6      | -              | -    |
| Minerva                                                       | 62B                      | -      | 39B          | 109B       | 52.4  | 27.6           | -     | -     | -     | -     | -    | 53.9      | -              | -    |
| Minerva                                                       | 540B                     | -      | 39B          | 26B        | 58.8  | 33.6       | -     | -     | -     | -     | -    | **63.9**  | -              | -    |
| [LLemma](https://huggingface.co/EleutherAI/llemma_7b)         | 7B                       | PPile  | 55B          | 200B       | 38.8  | 17.2           | 56.1  | 69.1  | 82.4  | 48.7  | 41.0 | 45.4      | 59.4           | 50.9 |
| [LLemma](https://huggingface.co/EleutherAI/llemma_34b)        | 34B                      | PPile  | 55B          | 50B        | 54.2  | 23.0           | 67.9  | 75.7 | 90.1 | 57.0  | 49.8 | 54.7      | 68.8           | 60.1 |
| [Intern-Math](https://huggingface.co/internlm/internlm2-math-base-7b)     | 7B                       | -      | 31B          | 125B       | 41.8  | 14.4           | 61.6  | 66.8  | 83.7  | 50.0  | 57.3 | 24.8      | 37.5           | 48.7 |
| [Intern-Math](https://huggingface.co/internlm/internlm2-math-base-20b)    | 20B                      | -      | 31B          | 125B       | 65.4 | 30.0       | 75.7 | 79.3  | **94.0** | 50.9  | 38.5 | 53.1      | 71.9           | 62.1 |
| [DeepSeekMath](https://huggingface.co/deepseek-ai/deepseek-math-7b-base) | 7B                       | -      | 120B         | 500B       | 64.1 | **34.2**       | 74.0 | **83.9** | 92.4 | **63.4** | **62.4** | 56.4      | **84.4**      | **68.4** |
| [Rho-Math](https://huggingface.co/microsoft/rho-math-7b-v0.1)                                                 | 7B                       | OWM    | 14B          | **10.5B**  | **66.9** | 31.0       | **77.8** | 79.0 | 93.9 | 49.9 | 58.7 | 54.6  | **84.4**      | 66.2 |


[^1]: We suggest utilizing the [OpenAI test subset](https://github.com/openai/prm800k) for evaluating MATH performance, since the original `MATH` test set has already been included in public training sets such as PRM800k. We use [minerva_math](/prompts/cot/minerva_math.md) prompt.
[^2]: abbreviations: TAB=tabmwp, MQA = mathqa, SAT = sat_math


### SFT Models (Code Interpreter)

> PROMPT_TYPE=tora

| Model            | Size | SFT Data | GSM8k | MATH | SVAMP | ASDiv | MAWPS | TAB | GSM-Hard | AVG  |
|------------------|------|----------|-------|------|-------|-------|-------|-----|----------|------|
| GPT4-early (PAL) | -    | -        | 94.2  | 51.8 | 94.8  | 92.6  | 97.7  | 95.9| 77.6     | 86.4 |
| MAmmoTH          | 70B           | MI-260k            | 76.9           | 41.8           | 82.4           | -              | -              | -            | -              | -            |
| ToRA             | 7B            | ToRA-69k           | 68.8           | 40.1           | 68.2           | 73.9           | 88.8           | 42.4         | 54.6           | 62.4         |
| ToRA             | 70B           | ToRA-69k           | 84.3           | 49.7           | 82.7           | 86.8           | 93.8           | 74.0         | 67.2           | 76.9         |
| DeepSeekMath     | 7B            | ToRA-69k           | 79.8           | 52.0           | 80.1           | 87.1           | 93.8           | 85.8         | 63.1           | 77.4         |
| Rho-Math    | 1B            | ToRA-69k           | 59.4      | 40.6      | 60.7      | 74.2      | 88.6      | 26.7     | 48.1      | 56.9     |
| Rho-Math    | 7B            | ToRA-69k           | 81.3      | 51.8      | 80.8      | 85.5      | 94.5      | 70.1     | 63.1      | 75.3     |


### SFT Models (CoT)

> PROMPT_TYPE=deepseek-math

| Size     | Model                  | GSM8k | MATH | SWAMP | ASDiv | MAWPS |  AVG |
|----------|------------------------|:-----:|:--------:|:-----:|:-----:|:-----:|:-----:|
| **7B**   | DeepSeek-Math-Instruct | 82.4  |   45.8   | 83.5  | 90.1  | 95.7  | 79.5  |
|          | DeepSeek-Math-RL       | 88.3  |   50.0   | 87.2  | 92.0  | 95.5  | 82.6  |


## 🍀 Contributing

This project is still under active development. We welcome any contributions, including bug reports, feature requests, and pull requests.


## ☕️ References

- https://github.com/microsoft/ToRA
- https://github.com/openai/prm800k
- https://github.com/wellecks/lm-evaluation-harness
- https://github.com/deepseek-ai/DeepSeek-Math
