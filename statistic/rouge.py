import argparse
import os
import pandas as pd
import json


def prepare_args():
    parser = argparse.ArgumentParser(description='Draw statistics for complex QA on xiaomu')
    parser.add_argument('--data_dir', help='Where to load', default='/data/tsq/xiaomu/qa/')
    parser.add_argument('--models', help='model to load',
                        default=['cpm2', 'glm', 'glm130b_base', 'gpt3', 'xiaoshih', 'dpr', 'bm25'])
    # task
    parser.add_argument('--score_key', type=str, default='f',
                        choices=['r', 'p', 'f'])
    parser.add_argument('--task', type=str, default='output_table',
                        choices=['output_table', 'compare'])
    args = parser.parse_args()
    return args


def get_avg(complex_res):
    res = {
    }
    for key, values in complex_res.items():
        res[key] = sum(values) / len(values)
    return res


def get_table_row(avg_simple_res, avg_complex_res, avg_all_res):
    res_lst = [avg_simple_res, avg_complex_res, avg_all_res]
    row_str = ""
    for res in res_lst:
        for score in res.values():
            row_str += "& {:.1f} ".format(score * 100)
    row_str += "\\"
    return row_str


def output_table(args):
    # get simple and complex label
    data_path = '/home/tsq/user/lcy/RocketQA/问题答案标注.xlsx'
    raw_data = pd.read_excel(data_path, sheet_name='Sheet1')
    _labels = raw_data['问题类型']
    answers = raw_data['答案']
    labels = []
    for label, a in zip(_labels, answers):
        if a != 'cannot_answer':
            labels.append(label)
    # simple r1/2/l, complex r1/2/l, all r1/2/l
    model2average = {}
    for model in args.models:
        csv_path = os.path.join(args.data_dir, f"scores_of_{model}.csv")
        df = pd.read_csv(csv_path, delimiter='|')
        assert len(labels) == len(df['rouge-1'])
        data_num = len(labels)
        simple_res = {
            "r1": [],
            "r2": [],
            "rl": [],
        }
        complex_res = {
            "r1": [],
            "r2": [],
            "rl": [],
        }
        # log scores
        for r1, r2, rl, label in zip(df['rouge-1'], df['rouge-2'], df['rouge-l'], labels):
            # print("r1", r1)
            s_r1 = json.loads(r1.replace('\'', '\"'))[args.score_key]
            s_r2 = json.loads(r2.replace('\'', '\"'))[args.score_key]
            s_rl = json.loads(rl.replace('\'', '\"'))[args.score_key]
            if label == '简单问题':
                simple_res['r1'].append(s_r1)
                simple_res['r2'].append(s_r2)
                simple_res['rl'].append(s_rl)
            else:
                complex_res['r1'].append(s_r1)
                complex_res['r2'].append(s_r2)
                complex_res['rl'].append(s_rl)

        # calculate average
        avg_simple_res = get_avg(simple_res)
        avg_complex_res = get_avg(complex_res)
        avg_all_res = {}
        for k, v in avg_simple_res.items():
            assert len(simple_res['r1']) + len(complex_res['r1']) == data_num
            avg_all_res[k] = (v * len(simple_res['r1']) + avg_complex_res[k] * len(complex_res['r1'])) / data_num
        # build the string for latex table
        table_str = get_table_row(avg_simple_res, avg_complex_res, avg_all_res)
        model2average[model] = table_str
    output_path = os.path.join(args.data_dir, f"average_{args.score_key}_of_{len(model2average)}models.json")
    with open(output_path, 'w') as fout:
        json.dump(model2average, fout, indent=4)
    print(f"finish at {output_path}")


if __name__ == '__main__':
    args = prepare_args()
    if args.task == 'output_table':
        output_table(args)
