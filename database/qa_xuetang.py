import json
import argparse
import os
import pandas as pd


def observe(args, results):
    num_meaningful_questions = 0
    num_new_answer = 0
    num_kg = 0
    num_good_ans = 0
    for i, result in enumerate(results):
        question = result[1]
        answer = result[2]
        course_name = result[3]
        source = result[4]
        sense_commit = result[5]
        label_used = result[6]
        type_belong = result[7]
        answer_commit = result[8]
        new_answer = result[9]
        update_time = result[10]
        if args.specific_id:
            if args.specific_id == int(result[0]):
                print(
                    f"Q:{question},A:{answer},C:{course_name},S:{source},意义:{sense_commit},答案:{answer_commit},New:{new_answer}")
        else:
            if i < args.show_num:
                print(f"Q:{question},A:{answer},C:{course_name},S:{source},意义:{sense_commit},New:{new_answer}")
                print("#" * 6)
        if sense_commit == "有意义":
            num_meaningful_questions += 1
        if type_belong == '知识图谱点击':
            num_kg += 1
        if answer_commit == '好':
            num_good_ans += 1
        if new_answer:
            num_new_answer += 1
    print(f"有意义的问题有{num_meaningful_questions}个,无意义的问题有{len(results) - num_meaningful_questions}个")
    print(f"有新答案的问题有{num_new_answer}个,无新答案的回答有{len(results) - num_new_answer}个")
    print(f"好答案的问题有{num_good_ans}个,回答不好的有{len(results) - num_good_ans}个")
    print(f"知识图谱点击的问题有{num_kg}个")


def draw_distribution(args, results):
    pass


def dump_answer_commit(args, results):
    v1_csv_path = os.path.join(args.data_dir, f'xiaomu_v1.csv')
    v1_df = pd.read_csv(v1_csv_path, header=None)
    id_list = []
    for index, row in v1_df.iterrows():
        if index == 0:
            continue
        origin_id = int(row[2])
        id_list.append(origin_id)
    print(f"Total id num is {len(id_list)}")
    print(id_list)
    id_to_answer_label = {}
    for i, result in enumerate(results):
        _id = int(result[0])
        answer_commit = result[8]
        if _id in id_list:
            id_to_answer_label[_id] = answer_commit
    output_path = os.path.join(args.data_dir, f'xiaomu_v1_id_to_answer_label.json')
    json.dump(id_to_answer_label, open(output_path, 'w'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data for checked QA history on xiaomu')
    parser.add_argument('--size', help='原始数据数量', default=302000)
    parser.add_argument('--show_num', help='打印数据数量', default=5)
    parser.add_argument('--specific_id', help='具体的记录id', type=int, default=None)
    parser.add_argument('--data_dir', help='数据地址', default='/data/tsq/xiaomu')
    parser.add_argument('--task', help='任务类型', default='observe',
                        choices=['observe', 'draw_distribution', 'dump_answer_commit'])
    args = parser.parse_args()
    raw_data_path = os.path.join(args.data_dir, f'qa_history_{args.size}.json')
    with open(raw_data_path, 'r') as fin:
        json_dict = json.load(fin)
    results = json_dict["results"]
    print(f"Total checked QA history num is {len(results)}")

    if args.task == 'observe':
        observe(args, results)
    elif args.task == 'draw_distribution':
        draw_distribution(args, results)
    elif args.task == 'dump_answer_commit':
        dump_answer_commit(args, results)
