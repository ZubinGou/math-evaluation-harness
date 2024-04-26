"""
This scripts is deprecated.
"""
import os
import time
import torch
import subprocess
import argparse
from multiprocessing import Pool

from summarize_results import summarize_results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", default="gpt-4", type=str)
    parser.add_argument("--data_names", default="gsm8k,minerva_math,math,gsm_hard,svamp,tabmwp,asdiv,mawps", type=str)
    parser.add_argument("--output_dir", default="/mnt/project/tora/outputs", type=str)
    parser.add_argument("--prompt_type", default="tool-integrated", type=str, choices=["direct", "cot", "pal", "tool-integrated", "self-instruct", "self-instruct-boxed", "tora", "pal", "cot", "wizard_zs", "platypus_fs", "deepseek-math", "kpmath"])
    parser.add_argument("--split", default="test", type=str)
    parser.add_argument("--num_test_sample", default=-1, type=int) # -1 for full data_name
    parser.add_argument("--seed", default=0, type=int)
    parser.add_argument("--start", default=0, type=int)
    parser.add_argument("--end", default=-1, type=int)
    parser.add_argument("--temperature", default=0, type=float)
    parser.add_argument("--n_sampling", default=1, type=int)
    parser.add_argument("--top_p", default=1, type=float)
    parser.add_argument("--gpus_per_model", default=1, type=int) # 2 for 70b
    parser.add_argument("--available_gpus", default=None, type=str)
    parser.add_argument("--split_data_over_gpus", action="store_true")
    parser.add_argument("--use_vllm", action="store_true")
    parser.add_argument("--save_outputs", action="store_true")
    parser.add_argument("--use_safetensors", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    return args

args = parse_args()

if not os.path.exists(args.model_name_or_path):
    raise FileNotFoundError(args.model_name_or_path)

data_list = args.data_names.split(',')

if args.available_gpus:
    available_gpus = args.available_gpus.split(',')
else:
    available_gpus = [str(i) for i in range(torch.cuda.device_count())]

start_end_list = [(args.start, args.end) for _ in range(len(data_list))]

if args.split_data_over_gpus:
    assert len(data_list) == 1
    assert args.num_test_sample != -1
    num_gpus = len(available_gpus)
    data_list = [data_list[0] for _ in range(num_gpus)]
    num_test_sample_per_gpu = args.num_test_sample // num_gpus
    start_end_list = [(i * num_test_sample_per_gpu, (i+1) * num_test_sample_per_gpu if i != (num_gpus - 1 ) else args.num_test_sample) for i in range(num_gpus)]


gpu_idx = 0
scripts = []
for i, data_name in enumerate(data_list):
    if gpu_idx + args.gpus_per_model > len(available_gpus):
        print("No enough GPUs!")
        break

    start, end = start_end_list[i]
    cmd = f"sleep {gpu_idx * 3} && " \
        f"CUDA_VISIBLE_DEVICES={','.join(available_gpus[gpu_idx:gpu_idx+args.gpus_per_model])} TOKENIZERS_PARALLELISM=false "\
        "python3 -u math_eval.py " \
        f"--model_name_or_path {args.model_name_or_path} " \
        f"--data_name {data_name} " \
        f"--output_dir {args.output_dir} " \
        f"--split {args.split} " \
        f"--prompt_type {args.prompt_type} " \
        f"--num_test_sample {args.num_test_sample} " \
        f"--seed {args.seed} " \
        f"--temperature {args.temperature} " \
        f"--n_sampling {args.n_sampling} " \
        f"--top_p {args.top_p} " \
        f"--start {start} " \
        f"--end {end} " \

    if args.use_vllm:
        cmd += "--use_vllm "
    if args.save_outputs:
        cmd += "--save_outputs "
    if args.use_safetensors:
        cmd += "--use_safetensors "
    if args.overwrite:
        cmd += "--overwrite"

    # cmd += " & "
    # print(cmd)
    # os.system(cmd)

    scripts.append(cmd)
    gpu_idx += args.gpus_per_model


def run_process(cmd):  
    os.system(cmd)  


if __name__ == "__main__":

    for i, script in enumerate(scripts):
        print(f"Script {i}: {script}")

    pool = Pool()
    pool.map(run_process, scripts) 

    pool.close()

    summarize_results(args.output_dir, args.data_names, args.split)


# Usage:
# model_name_or_path=./mistral/Mistral-7B-v0.1
# python3 scripts/run_eval_multi_gpus.py \
#     --model_name_or_path $model_name_or_path \
#     --prompt_type "cot" \
#     --save_outputs \
#     --available_gpus 0,1,2,3 \
#     --data_names gsm8k,minerva_math,svamp,asdiv \
#     --use_vllm \
#     --gpus_per_model 1 \
#     --overwrite
