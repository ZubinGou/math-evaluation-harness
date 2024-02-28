set -ex

# MODEL_NAME_OR_PATH=${HF_MODEL_DIR}/mistral/Mistral-7B-v0.1
# MODEL_NAME_OR_PATH=${HF_MODEL_DIR}/deepseek/deepseek-math-7b-rl
MODEL_NAME_OR_PATH=${HF_MODEL_DIR}/deepseek/deepseek-math-7b-base

PROMPT_TYPE="cot" # for base models: direct / cot / pal / tool-integrated
# PROMPT_TYPE="deepseek-math" # for sft models: tora / wizard_zs / deepseek-math


OUTPUT_DIR=${MODEL_NAME_OR_PATH}/math_eval
DATA_NAME="gsm8k,math-oai,svamp,asdiv,mawps"
SPLIT="test"
NUM_TEST_SAMPLE=-1



CUDA_VISIBLE_DEVICES=0 TOKENIZERS_PARALLELISM=false \
python3 -u math_eval.py \
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
