import argparse
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def prepare_args():
    parser = argparse.ArgumentParser(description='Draw statistics for complex QA on xiaomu')
    parser.add_argument('--data_dir', help='Where to load', default='/data/tsq/xiaomu/complex/')
    parser.add_argument('--input_files', help='Where to load',
                        default=['result_20220912_fix_prompt_原因类.csv', 'result_20220912_fix_prompt_比较类.csv'])
    parser.add_argument('--pic_dir', help='Where to save', default='/data/tsq/xiaomu/complex/pic/')
    parser.add_argument('--pic_name', help='Where to save', default='cot_v1_fix_prompt')
    args = parser.parse_args()
    return args


def get_type2score(data_dir, input_file, setting_type_score):
    csv_path = os.path.join(data_dir, input_file)
    qa_df = pd.read_csv(csv_path)
    qa_type2score = {}
    for index, row in qa_df.iterrows():
        q_type = row['q_type']
        answer_str = row['回答是否正确']
        answer_score = 1
        if answer_str == '否':
            answer_score = 0
        # print(answer_score)
        try:
            qa_type2score[q_type].append(answer_score)
        except KeyError:
            qa_type2score[q_type] = [answer_score]
    setting_file = input_file
    setting = setting_file.split(".")[0]
    print(f"settings: {setting}")
    print("The type and score is:")
    print(qa_type2score)
    for k, scores in qa_type2score.items():
        acc = sum(scores) / len(scores)
        # add to log dict
        setting_type_score["setting"].append(setting)
        setting_type_score["acc"].append(acc)
        setting_type_score["q_type"].append(k)
    # print(setting_type_score)
    print("#" * 16)
    return setting_type_score


def draw_acc(args):
    save_path = os.path.join(args.pic_dir, args.pic_name)
    setting_type_score = {"setting": [], "acc": [], "q_type": []}
    for input_file in args.input_files:
        setting_type_score = get_type2score(args.data_dir, input_file, setting_type_score)
    hits_data = pd.DataFrame(setting_type_score)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
    sns.set(font='SimHei', font_scale=0.8)  # 解决Seaborn中文显示问题
    sns.lineplot(x="q_type", y="acc", hue="setting", markers="o", data=hits_data)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close('all')
    print(f"finish at {save_path}")


if __name__ == '__main__':
    args = prepare_args()
    draw_acc(args)
