import json
import argparse
import os


def observe(args, results):
    num_meaningful_questions = 0
    for i, result in enumerate(results):
        question = result[1]
        answer = result[2]
        course_name = result[3]
        source = result[4]
        sense_commit = result[5]
        new_answer = result[6]
        if i < args.show_num:
            print(f"Q:{question},A:{answer},C:{course_name},S:{source},意义:{sense_commit},New:{new_answer}")

        if sense_commit == "有意义":
            num_meaningful_questions += 1
    print(f"有意义的问题有{num_meaningful_questions}个,无意义的问题有{len(results) - num_meaningful_questions}个")


def draw_distribution(args, results):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data for checked QA history on xiaomu')
    parser.add_argument('--size', help='原始数据数量', default=300000)
    parser.add_argument('--show_num', help='打印数据数量', default=5)
    parser.add_argument('--data_dir', help='数据地址', default='/data/tsq/xiaomu')
    parser.add_argument('--task', help='任务类型', default='observe',
                        choices=['observe', 'draw_distribution'])
    args = parser.parse_args()
    raw_data_path = os.path.join(args.data_dir, f'qa_history_{args.size}.json')
    with open(raw_data_path, 'r') as fin:
        json_dict = json.load(fin)
    results = json_dict["json_dict"]
    print(f"Total checked QA history num is {len(results)}")

    if args.task == 'observe':
        observe(args, results)
    elif args.task == 'draw_distribution':
        draw_distribution(args, results)
