import json
import argparse
import os
import pandas as pd
from tqdm import tqdm


def observe(args, results):
    num_meaningful_questions = 0
    num_new_answer = 0
    num_kg = 0
    num_good_ans = 0
    csv_results = []
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
        chat_id = result[11]
        if args.specific_id:
            if args.specific_id == int(result[0]):
                print(
                    f"Q:{question},A:{answer},C:{course_name},S:{source},意义:{sense_commit},答案:{answer_commit},New:{new_answer}")
        else:
            if i < args.show_num:
                print(f"Q:{question},A:{answer},C:{course_name},S:{source},意义:{sense_commit},New:{new_answer}")
                print("#" * 6)
        csv_results.append({"question": question, "answer": answer, "course_name": course_name,
                            "source": source, "sense_commit": sense_commit, "label_used": label_used,
                            "type_belong": type_belong, "answer_commit": answer_commit,
                            "new_answer": new_answer, "update_time": update_time, "session_id": chat_id})
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
    df = pd.DataFrame(csv_results)
    df.to_csv(os.path.join(args.data_dir, f'qa_history_{args.size}.csv'))


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


def filter_df(df):
    dfs = []
    questions = []
    # 去除重复的
    for index, row in df.iterrows():
        question = row[1]
        if question not in questions:
            dfs.append(row)
            questions.append(question)
    if len(dfs) == 0:
        return df
    final = pd.DataFrame(dfs, columns=df.columns)
    return final


def sample_intention(args):
    raw_data_path = os.path.join(args.data_dir, f'qa_history_{args.size}.csv')
    df = pd.read_csv(raw_data_path)
    # 去除预设的
    for _type in ['加减乘除', '作诗', '问助教', '脏问题', '助教回答', '预设问答', '视频答案']:
        df = df[df['type_belong'] != _type]
    down_df = df[df["update_time"] >= "2022-09-22"]
    df = df[df["update_time"] >= "2020-07"]
    up_df = df[df["update_time"] <= "2022-09-12"]
    # 去除了非正常时间的记录
    inner_df = pd.concat([up_df, down_df], join="inner")
    print("input data num is", len(inner_df))
    print(inner_df.shape[0])
    print(inner_df)
    chat_id2df = {}
    chat_id2df_len = {}
    # 聚合session_id
    for index, row in tqdm(inner_df.iterrows(), total=len(inner_df)):
        if index == 0:
            continue
        chat_id = row[11]
        if chat_id not in chat_id2df.keys():
            chat_id2df[chat_id] = filter_df(inner_df[inner_df['session_id'] == chat_id])
            chat_id2df_len[chat_id] = chat_id2df[chat_id].shape[0]
    session_num = len(chat_id2df_len)
    avg_session_len = sum(chat_id2df_len.values()) / session_num
    # 平均session长度,与session总数
    print("average len is ", avg_session_len)
    print("Total session is ", session_num)
    # 采样session数
    sample_session_num = int(args.sample_num / avg_session_len)
    # 采样间隔
    interval = int(session_num / sample_session_num)
    print(f"sample_session_num {sample_session_num}, interval {interval}")
    sessions = []
    total_len = 0
    for i, key in enumerate(chat_id2df.keys()):
        if i % interval != 1:
            continue
        session_df = chat_id2df[key]
        df_len = chat_id2df_len[key]
        sessions.append(session_df)
        total_len += df_len
        if total_len > args.sample_num:
            break
    # 导出
    # final_df = filter_df(pd.concat(sessions, join="inner"))
    final_df = pd.concat(sessions, join="inner")
    sample_path = os.path.join(args.data_dir, f'sample_{len(final_df)}_from_{args.size}.csv')
    final_df.to_csv(sample_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data for checked QA history on xiaomu')
    parser.add_argument('--size', help='原始数据数量', default=312000)
    parser.add_argument('--show_num', help='打印数据数量', default=5)
    parser.add_argument('--specific_id', help='具体的记录id', type=int, default=None)
    parser.add_argument('--data_dir', help='数据地址', default='/data/tsq/xiaomu/dump')
    parser.add_argument('--task', help='任务类型', default='observe',
                        choices=['observe', 'sample_intention', 'dump_answer_commit'])
    # 对于准备意图检测数据的采样
    parser.add_argument('--sample_num', help='要采样的数量', type=int, default=4000)

    args = parser.parse_args()

    if args.task != 'sample_intention':
        raw_data_path = os.path.join(args.data_dir, f'qa_history_{args.size}.json')
        with open(raw_data_path, 'r') as fin:
            json_dict = json.load(fin)
        results = json_dict["results"]
        print(f"Total checked QA history num is {len(results)}")

    if args.task == 'observe':
        observe(args, results)
    elif args.task == 'sample_intention':
        sample_intention(args)
    elif args.task == 'dump_answer_commit':
        dump_answer_commit(args, results)
