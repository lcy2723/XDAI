import argparse
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def prepare_args():
    parser = argparse.ArgumentParser(description='Draw statistics for complex QA on xiaomu')
    parser.add_argument('--data_dir', help='Where to load', default='/data/tsq/xiaomu/complex/')
    parser.add_argument('--input_files', help='Where to load',
                        default=['result_20220912_fix_prompt_原因类.csv', 'result_20220912_fix_prompt_比较类.csv'])
    parser.add_argument('--pic_dir', help='Where to save', default='/data/tsq/xiaomu/statistic/')
    parser.add_argument('--pic_name', help='Where to save', default='time_v1')
    # task
    parser.add_argument('--task', type=str, default='human_acc',
                        choices=['time_distribution', 'human_acc'])
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


def draw_time_distribution(args):
    save_path = os.path.join(args.pic_dir, args.pic_name)
    # 　设置字体
    sns.set_theme(style="whitegrid", font='Times New Roman')
    model_names = ['GPT3', '130B', 'CPM', 'GLM', 'Cdi.', 'PLA.', 'EVA', 'XDAI', 'L.M.', 'Rule']
    times = [3.79, 15.14, 1.07, 0.9, 1.5, 3, 2, 1.6, 1.3, 0.12]
    Type = ['General Language Model'] * 4 + ['Open-domain Dialogue Model'] * 3 + ['Knowledge-grounded Model'] * 3
    type_score = {"model_names": model_names, "times": times, "Type": Type}
    df_data = pd.DataFrame(type_score)
    sort_df = df_data.sort_values(by=["times"], ascending=[True])
    ax = sns.barplot(x="model_names", y="times", hue="Type", data=sort_df, dodge=False)
    # Set these based on your column counts
    newwidth = 0.5
    for bar in ax.patches:
        x = bar.get_x()
        width = bar.get_width()
        centre = x + width / 2.

        bar.set_x(centre - newwidth / 2.)
        bar.set_width(newwidth)
    # ax.set_xticks(range(len(sort_df)), labels=range(2011, 2019))
    ax.set_xlabel("Model")
    ax.set_ylabel("Response Time(s)")
    plt.savefig(save_path, bbox_inches='tight')
    plt.close('all')
    print(f"finish at {save_path}")


if __name__ == '__main__':
    args = prepare_args()
    if args.task == 'human_acc':
        draw_acc(args)
    elif args.task == 'time_distribution':
        draw_time_distribution(args)
