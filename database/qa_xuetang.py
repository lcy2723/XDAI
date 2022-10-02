import json
import argparse
import os


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
            print(f"Q:{question},A:{answer},C:{course_name},S:{source},意义:{sense_commit},New:{new_answer}")
            print("#" * 6)
    print(f"有意义的问题有{num_meaningful_questions}个,无意义的问题有{len(results) - num_meaningful_questions}个")
    print(f"有新答案的问题有{num_new_answer}个,无新答案的回答有{len(results) - num_new_answer}个")
    print(f"好答案的问题有{num_good_ans}个,回答不好的有{len(results) - num_good_ans}个")
    print(f"知识图谱点击的问题有{num_kg}个")


def draw_distribution(args, results):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data for checked QA history on xiaomu')
    parser.add_argument('--size', help='原始数据数量', default=302000)
    parser.add_argument('--show_num', help='打印数据数量', default=5)
    parser.add_argument('--data_dir', help='数据地址', default='/data/tsq/xiaomu')
    parser.add_argument('--task', help='任务类型', default='observe',
                        choices=['observe', 'draw_distribution'])
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
