# LLM Math Evaluation Harness

A simple toolkit to benchmark LLMs on various math tasks 🧮✨.

Currently supports:

**Models**:
- All HF 🤗 and [vLLM](https://github.com/vllm-project/vllm) supported models

**Datasets**:
- math,gsm8k,gsm-hard,svamp,asdiv,mawps,tabmwp,finqa,theorem-qa,bbh,hungarian_exam

**Prompts**:
- CoT / PAL / [ToRA](https://github.com/microsoft/ToRA)

## 🚀 Usage

### ⚙️ Enviorment Setup

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

```
bash scritpts/run_math_eval.sh
```

Enjoy 🍻!


## 🍀 Contributing

This project is still under active development. We welcome any contributions, including bug reports, feature requests, and pull requests.


## ☕️ References

- https://github.com/microsoft/ToRA
- https://github.com/openai/prm800k


<!-- ## Cite -->


