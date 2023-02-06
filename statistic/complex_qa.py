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
                        choices=['time_distribution', 'human_acc', 'course_distribution', 'user_involve'])
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
    save_path = os.path.join(args.pic_dir, f"{args.pic_name}.pdf")
    # 　设置字体
    sns.set_theme(style="whitegrid", font='Times New Roman')
    model_names = ['GPT3', '130B', 'CPM', 'GLM', 'Cdi.', 'PLA.', 'EVA', 'L.L.M.', 'L.M.', 'X.M.']
    times = [3.79, 15.14, 1.07, 0.9, 1.5, 3, 2.1, 10.6, 1.3, 0.12]
    Type = ['General Language Model'] * 4 + ['Open-domain Dialogue Model'] * 3 + ['Virtual Teaching Assistant'] * 3
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
    ax.grid(False)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close('all')
    print(f"finish at {save_path}")


def draw_courses_distribution(args):
    save_path = os.path.join(args.pic_dir, f"{args.pic_name}.pdf")
    # 　设置字体
    sns.set_theme(style="whitegrid", font='Times New Roman')

    course_names = ['Engineering', 'Natural Sci.', 'Arts', 'Social Sci.', 'Others'] * 3

    scores = [
                 1.539583333,
                 1.6875,
                 1.544791667,
                 1.409853249,
                 1.259631491
             ] + [1.536390102, 1.426622419, 1.328899083, 1.430223285, 1.352787456] + [0.929166667, 1.023958333,
                                                                                      0.792361111,
                                                                                      1.409853249,
                                                                                      0.860897436]
    Type = ['LittleMu(130B)'] * 5 + ['GLM-130B'] * 5 + ['PLATO-XL'] * 5
    type_score = {"courses": course_names, "scores": scores, "model": Type}
    df_data = pd.DataFrame(type_score)
    ax = sns.barplot(x="courses", y="scores", hue="model", data=df_data)
    # Set these based on your column counts
    # newwidth = 0.5
    # for bar in ax.patches:
    #     x = bar.get_x()
    #     width = bar.get_width()
    #     centre = x + width / 2.
    #
    #     bar.set_x(centre - newwidth / 2.)
    #     bar.set_width(newwidth)
    # ax.set_xticks(range(len(sort_df)), labels=range(2011, 2019))
    ax.set_xlabel("Course Category")
    ax.set_ylabel("Average Score")
    ax.grid(False)
    plt.ylim(0.6, 1.8)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close('all')
    print(f"finish at {save_path}")


def draw_user_involve(args):
    save_path = os.path.join(args.pic_dir, f"{args.pic_name}.pdf")
    # 　设置字体
    sns.set_theme(style="whitegrid", font='Times New Roman')
    times = ['20-07', '20-10', '21-01', '21-04', '21-07', '21-10', '22-01', '22-04', '22-07',
             '22-10']
    satisfaction = [51.34, 61.5, 59.37, 61.12, 60.24, 60.31, 61.15, 62.15, 65.44, 66.97]
    rounds = [2.78, 2.61, 2.82, 2.53, 2.23, 2.25, 2.36, 2.18, 2.45, 3.08]

    _df1 = {"times": times, "satisfaction_rate": satisfaction}
    _df2 = {"times": times, "#rounds": rounds}
    df1 = pd.DataFrame(_df1)
    df2 = pd.DataFrame(_df2)
    # 轴1
    # ax2 = sns.lineplot(data=df1, x="times", y="satisfaction_rate", color="g", marker="v")
    # ax.set_xlabel("Period (Year-Month)")
    # ax.set_ylabel("Satisfaction Rate (%)")
    # ax.grid(False)
    # plt.legend(labels=["satisfaction rate"])
    # 输出2
    # ax2 = ax.twinx()
    ax2 = sns.lineplot(data=df2, x="times", y="#rounds", color="b", marker="o")
    ax2.set_ylabel("#rounds")
    ax2.set_xlabel("Period (Year-Month)")
    ax2.grid(False)
    plt.legend(labels=["#rounds"])

    # 保存
    plt.savefig(save_path, bbox_inches='tight')
    plt.close('all')
    print(f"finish at {save_path}")


if __name__ == '__main__':
    args = prepare_args()
    if args.task == 'human_acc':
        draw_acc(args)
    elif args.task == 'time_distribution':
        draw_time_distribution(args)
    elif args.task == 'course_distribution':
        draw_courses_distribution(args)
    elif args.task == "user_involve":
        draw_user_involve(args)
