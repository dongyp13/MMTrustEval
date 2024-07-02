source activate mllm-dev

if [ $# -eq 0 ]; then
    echo "Usage: $0 <model_id>"
    exit 1
fi

model_id=$1

dataset_ids=(
    "vispr-recognition-pri-query"
)

for dataset_id in "${dataset_ids[@]}";
do
    CUDA_VISIBLE_DEVICES=3 python run_task.py --config mmte/configs/task/privacy/p2-vqa-recognition-vispr.yaml --cfg-options \
        dataset_id=${dataset_id} \
        model_id=${model_id} \
        log_file="logs/privacy/p2-vqa-recognition-vispr/${model_id}/${dataset_id}.json"
done
