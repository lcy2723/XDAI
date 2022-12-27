import os
import re
import torch
import pandas as pd
from tqdm import tqdm
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


class DataProcessor(object):
    def __init__(self, tokenizer, max_sequence_length,
                 use_course_name=False, use_history_answer=False, max_history_turns=4):
        """
        :arg
         - tokenizer: 分词器
         - max_sequence_length: 拼接后句子的最长长度
         - truncation_strategy: 如果句子超过max_sequence_length,截断的策略
         - use_course_name: 是否在历史开头加上课程名
         - use_history_answer: 是否使用历史中的回复
         - max_history_turns: 最多能用的历史轮数
        """
        # params for tokenizer
        self.tokenizer = tokenizer
        self.max_sequence_length = max_sequence_length
        self.truncation_strategy = 'longest_first'
        # strategy for utilizing the input information
        self.use_course_name = use_course_name
        self.use_history_answer = use_history_answer
        self.max_history_turns = max_history_turns
        # transform str to class id
        self.label2id = {'简单问题': 0, '复杂问题': 1, '平台、课程问题': 2, '情绪闲聊': 3, '其他闲聊': 4, '其他': 5}
        self.label2binary_id = {'简单问题': 0, '复杂问题': 0, '平台、课程问题': 0, '情绪闲聊': 1, '其他闲聊': 1, '其他': 1}

    def _convert_to_transformer_inputs(self, history, query):
        """
        Converts tokenized input to ids, masks and segments for transformer (including bert)
        :arg
         - text: 文本

        :return
         - input_ids: 记录句子里每个词对应在词表里的 id
         - input_masks: 列表中， 1的部分代表句子单词，而后面0的部分代表paddig，只是用于保持输入整齐，没有实际意义。
           相当于告诉BertModel不要利用后面0的部分
        - segments: 列表用来指定哪个是第一个句子，哪个是第二个句子，0的部分代表句子一, 1的部分代表句子二
        """

        inputs = self.tokenizer.encode_plus(history, query,
                                            add_special_tokens=True,
                                            max_length=self.max_sequence_length,
                                            truncation_strategy=self.truncation_strategy,
                                            # truncation=True
                                            )

        input_ids = inputs["input_ids"]
        input_segments = inputs["token_type_ids"]
        input_masks = [1] * len(input_ids)
        padding_length = self.max_sequence_length - len(input_ids)
        padding_id = self.tokenizer.pad_token_id
        input_ids = input_ids + ([padding_id] * padding_length)
        input_masks = input_masks + ([0] * padding_length)
        input_segments = input_segments + ([0] * padding_length)

        return input_ids, input_masks, input_segments

    def process_ans(self, _answer):
        max_ans_len = self.max_sequence_length // self.max_history_turns
        # filter some html tags
        if type(_answer) != str:
            print("process_ans")
            print(_answer)
            print(type(_answer))
            return _answer
        message = re.sub(r'<.*?>', "", _answer)
        message = re.sub(r'\n', "", message)
        message = re.sub(r'答案解析.*', "", message)
        return message[:max_ans_len]

    def get_history(self, session_qa_lst, course_name):
        if self.use_course_name:
            history = f"当前的课程是{course_name}，有同学问"
        else:
            history = "在一个慕课网站上，有同学问"
        for qa_pair in session_qa_lst[-self.max_history_turns:]:
            history += f"|Q:{qa_pair[0]}"
            if self.use_history_answer:
                history += f"|A:{qa_pair[1]}"

        return history

    def get_input(self, df):
        """
        :param
         - df: 数据集集的dataFrame

        :return
            3个处理好的tensor,形状都是[数据总数,max_sequence_length],它们的含义请看_convert_to_transformer_inputs
         - tokens_tensor: (tensor) [数据总数,max_sequence_length]
         - input_masks_tensors: (tensor) [数据总数,max_sequence_length]
         - segments: 列表用来指定哪个是第一个句子，哪个是第二个句子，0的部分代表句子一, 1的部分代表句子二
        """
        token_ids, masks, input_segments = [], [], []
        # 每一条数据
        previous_id = -1
        session_qa_lst = []
        for i in tqdm(range(len(df))):
            course_name = df.iloc[i]['course_name']
            question = df.iloc[i]['question']
            answer = self.process_ans(df.iloc[i]['answer'])
            session_id = df.iloc[i]['session_id']
            if previous_id != session_id:
                # new session
                session_qa_lst = []
                previous_id = session_id
            # concat the qa pairs
            history = self.get_history(session_qa_lst, course_name)
            input_ids, input_masks, input_segment = self._convert_to_transformer_inputs(history, question)
            token_ids.append(input_ids)
            masks.append(input_masks)
            input_segments.append(input_segment)
            # log the session's qa
            session_qa_lst.append((question, answer))

        tokens_tensor = torch.tensor(token_ids)
        input_masks_tensors = torch.tensor(masks)
        input_segments_tensors = torch.tensor(input_segments)

        return [tokens_tensor, input_masks_tensors, input_segments_tensors]

    def get_output(self, df_train):
        """
        :param df_train: 训练集的dataFrame
        :return: (tensor) [num_vocab] 数据的标注,只有0和1,1代表这个reply回答了query
        """
        labels = df_train['问题类型']
        id_labels = []
        for label in tqdm(labels):
            id_label = self.label2id[label]
            id_labels.append(id_label)
        # return torch.tensor(np.array(id_labels)).unsqueeze(1)
        return torch.tensor(np.array(id_labels))

    def transform_to_binary_intention(self, raw_data_path, out_data_path):
        df = pd.read_csv(raw_data_path)
        res_lst = []
        for i in tqdm(range(len(df))):
            question = df.iloc[i]['question']
            if type(question) != str:
                question = "null1"
            label = df.iloc[i]['问题类型']
            id_label = self.label2binary_id[label]
            res = {"question": question, "label": id_label}
            res_lst.append(res)
        res_df = pd.DataFrame(res_lst)
        res_df.to_csv(out_data_path)

    def transform_splits_to_binary_intention(self, data_dir):
        splits = ['train', 'valid', 'test']
        real_intention_dir = os.path.join(data_dir, 'real')
        bin_intention_dir = os.path.join(data_dir, 'binary')
        for sp in splits:
            input_path = os.path.join(real_intention_dir, f'{sp}.csv')
            output_path = os.path.join(bin_intention_dir, f'{sp}.csv')
            df = pd.read_csv(input_path)
            res_lst = []
            for i in tqdm(range(len(df))):
                label = df.iloc[i]['问题类型']
                id_label = self.label2binary_id[label]
                res = dict(df.iloc[i])
                res['问题类型'] = id_label
                res_lst.append(res)
            res_df = pd.DataFrame(res_lst)
            res_df.to_csv(output_path)


if __name__ == '__main__':
    processor = DataProcessor(None, None)
    # raw_data_path = '/data/tsq/xiaomu/intention/real_intention_4002.csv'
    # out_data_path = '/data/tsq/xiaomu/intention/binary_intention_4002.csv'
    # processor.transform_to_binary_intention(raw_data_path, out_data_path)
    processor.transform_splits_to_binary_intention('/data/tsq/xiaomu/intention/')
