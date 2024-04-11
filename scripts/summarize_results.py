import json
import glob
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_dir", type=str)
    parser.add_argument("--data_names", type=str, default="gsm8k,minerva_math,svamp,asdiv,mawps")
    parser.add_argument("--split", type=str, default="test")
    args = parser.parse_args()
    summarize_results(args.result_dir, args.data_names, args.split)


def summarize_results(result_dir, data_names, split):
    data_list = data_names.split(',')

    # read the result
    results = []
    for data_name in data_list:
        files = glob.glob(f"{result_dir}/{data_name}/{split}*metrics.json")
        assert len(files) == 1, f"Found {len(files)} files for {data_name}"
        with open(files[0], 'r') as f:
            metrics = json.load(f)
            results.append(metrics)
    
    data_list.append("avg")
    results.append({
        "acc": sum([result["acc"] for result in results]) / len(results),
    })
    
    # print all results
    pad = max([len(data_name) for data_name in data_list])
    print("\t".join(data_name.ljust(pad, " ") for data_name in data_list))
    print("\t".join([f"{result['acc']:.1f}".ljust(pad, " ") for result in results]))
    print(" & ".join([f"{result['acc']:.1f}" for result in results]))


if __name__ == "__main__":
    main()
