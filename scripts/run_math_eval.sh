set -ex

MODEL_NAME_OR_PATH=./mistral/Mistral-7B-v0.1

OUTPUT_DIR=${MODEL_NAME_OR_PATH}/math_eval

DATA_NAME="gsm8k,math-oai,svamp,asdiv,mawps"

SPLIT="test"
PROMPT_TYPE="cot"
NUM_TEST_SAMPLE=-1 # for all samples


CUDA_VISIBLE_DEVICES=0 TOKENIZERS_PARALLELISM=false \
python -u math_eval.py \
    --model_name_or_path ${MODEL_NAME_OR_PATH} \
    --data_name ${DATA_NAME} \
    --output_dir ${OUTPUT_DIR} \
    --split ${SPLIT} \
    --prompt_type ${PROMPT_TYPE} \
    --num_test_sample ${NUM_TEST_SAMPLE} \
    --seed 0 \
    --temperature 0 \
    --n_sampling 1 \
    --top_p 1 \
    --start 0 \
    --end -1 \
    --use_vllm \
    --save_outputs \
