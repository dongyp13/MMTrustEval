from mmte.tasks.base import BaseTask
from mmte.utils.registry import registry
from mmte.evaluators.metrics import _supported_metrics
from mmte.utils.utils import DictAction, merge_config
import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file path')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    args = parser.parse_args()
    return args

print("models: ", registry.list_chatmodels())
print("datasets: ", registry.list_datasets())
print("methods: ", registry.list_methods())
print("evaluators: ", registry.list_evaluators())
print("metrics: ", list(_supported_metrics.keys()))


if __name__ == '__main__':
    args = parse_args()
    config = args.config

    with open(config, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        if hasattr(args, "cfg_options"):
            cfg = merge_config(cfg, args.cfg_options)
        print(config)
        print(cfg)
        model_id = cfg.get('model_id')
        dataset_id = cfg.get('dataset_id')
        log_file = cfg.get('log_file')
        method_cfg = cfg.get('method_cfg', {})
        dataset_cfg = cfg.get('dataset_cfg', {})
        evaluator_seq_cfgs = cfg.get('evaluator_seq_cfgs', [])
        
        runner = BaseTask(dataset_id=dataset_id, model_id=model_id, method_cfg=method_cfg, dataset_cfg=dataset_cfg, log_file=log_file, evaluator_seq_cfgs=evaluator_seq_cfgs)
        runner.pipeline()