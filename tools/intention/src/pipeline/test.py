# coding=UTF-8
import torch
import torch.utils.data as Data
import argparse
from transformers import AutoModel, BertTokenizer
from tqdm import tqdm
import os
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
import tools.intention.src.models.albert
from tools.intention.src.models.albert import AlbertClassifierModel
from tools.intention.src.pipeline.preprocess import DataProcessor

classes = ['简单问题', '复杂问题', '平台、课程问题', '情绪闲聊', '其他闲聊', '其他']


def work(args):
    """
    :param args: 一堆 运行前 规定好的 参数
    :return: 在测试集上输出结束(会输出到args.output_dir),
    记录在args.output_dir/scores.txt
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 加载test数据
    tokenizer = BertTokenizer.from_pretrained(args.pretrained_model)
    df_test = pd.read_csv(args.df_test_path)
    processor = DataProcessor(tokenizer, args.max_input_len,
                              args.use_course_name, args.use_history_answer, args.max_history_turns)
    inputs = processor.get_input(df_test)
    labels = processor.get_output(df_test)
    # 加载ckpt
    loaded = torch.load(args.ckpt)
    model_kwargs = loaded['kwargs']
    for k in model_kwargs:
        # 如果现有的args里有和训练时冲突的,就把加载进来的ckpt的参数覆盖掉
        if hasattr(args, k) and getattr(args, k) is not None:
            model_kwargs[k] = getattr(args, k)
    args.fout.write("state_dict raw")
    print(loaded['state_dict'])
    for k, v in model_kwargs.items():
        args.fout.write("k {}, v{}".format(k, v))
        print(k, v)

    # 加载模型
    model = AlbertClassifierModel(**model_kwargs)
    model.load_state_dict(loaded['state_dict'])
    model.eval()
    model = model.to(device)
    # 预测
    with torch.no_grad():
        predict_on_testset(model, inputs, labels, device, args)


def predict_on_testset(model, inputs, labels, device, args):
    """
    :param model: 模型对象
    :param inputs: (list) 作为输入的tensor, 它是由get_input处理得的
    :param labels: test集原始数据的 labels
    :param device: cuda 或 cpu
    :param args:一堆 运行前 规定好的 参数
    :return: 测试集输出结束
    """
    torch_dataset = Data.TensorDataset(inputs[0], inputs[1], inputs[2])
    # 这是test集,不要打乱,故shuffle=False
    loader = Data.DataLoader(dataset=torch_dataset, batch_size=args.batch_size, shuffle=False)
    pred_probs = []
    for batch_iter, (input_ids, attention_mask, input_segments) in tqdm(enumerate(loader)):
        pred_prob = model(input_ids.to(device),
                          segment_ids=input_segments.to(device),
                          attention_mask=attention_mask.to(device))
        pred_probs.append(pred_prob)

    merged_pred_probs = torch.cat(pred_probs).cpu().numpy()
    print(merged_pred_probs.shape)
    pred_y_list = np.argmax(merged_pred_probs, axis=1).tolist()
    # 计算分数
    df_labels = pd.DataFrame(labels.cpu().numpy())
    df_preds = pd.DataFrame(np.argmax(merged_pred_probs, axis=1))
    f1 = f1_score(df_labels, df_preds, average="macro")
    acc = accuracy_score(df_labels, df_preds)
    # 存
    args.fout.write("### test scores ###\n")
    args.fout.write(f"f1 {f1}\n")
    args.fout.write(f"acc {acc}\n")
    # 保存预测的类
    with open(args.output_txt_path, 'w') as fout:
        for pred_y in pred_y_list:
            # print(pred_y)
            fout.write("{}\n".format(classes[pred_y]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # path parameters
    parser.add_argument('--data-dir', type=str, default='/data/tsq/xiaomu/intention/binary')
    parser.add_argument('--save-dir', type=str, default='/data/tsq/xiaomu/intention/binary/ckpt')
    parser.add_argument('--pretrained-model', type=str, default='/data/tsq/xiaomu/intention/albert_chinese_base')
    parser.add_argument('--ckpt', required=True)
    # Data Process parameters
    parser.add_argument("--use_course_name", action='store_true', default=False)
    parser.add_argument("--use_history_answer", action='store_true', default=False)
    parser.add_argument('--max_history_turns', type=int, default=4)
    # model parameters
    parser.add_argument('--max-input-len', type=int, default=100)
    # mini-batch 保证每一条test都有输出
    parser.add_argument('--batch_size', type=int, default=1)

    args = parser.parse_args()
    # test集的路径
    args.df_test_path = os.path.join(args.data_dir, "test.csv")

    # write the output [id,sub_id,pred_y]
    ckpt_base = os.path.splitext(os.path.basename(args.ckpt))[0]

    output_dir = os.path.join(args.save_dir, "test_output_{}".format(ckpt_base))
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        print('output dir %s exists, be careful that we will overwrite it' % output_dir)
    # 最终结果
    args.output_dir = output_dir
    args.output_txt_path = os.path.join(output_dir, 'submission.txt')
    f = open(os.path.join(output_dir, 'scores.txt'), 'w')
    args.fout = f
    work(args)
