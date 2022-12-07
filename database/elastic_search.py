from elasticsearch_dsl import connections
from database.es_model import MoocArticle, name2model
import argparse
import os
import json
from tqdm import tqdm


def get_fout(path):
    if os.path.exists(path):
        os.remove(path)
    return open(path, 'a')


def get_answer(dic):
    _type = dic["typetext"]
    answer = ""
    answers = json.loads(dic["answer"])
    options = dic["option"]
    if _type == "单选题" or _type == "判断题":
        try:
            answer = options[answers[0]]
        except:
            print(options)
            print(answers)
    elif _type == "多选题":
        try:
            for a in answers:
                answer += f",{options[a]}"
        except KeyError:
            print(options)
            print(answers)
            answer = options[answers[0]]
    elif _type == "填空题":
        try:
            answer = " ".join(["".join(lst) for lst in answers.values()])
        except AttributeError:
            print(options)
            print(answers)
    elif _type == "主观题":
        # 　没答案
        pass
    return answer


def preprocess(args):
    fout = get_fout(args.data_path)
    # Mooccube的文档资源
    if args.model == 'MoocArticle':
        # 视频字幕
        if 'video' in args.mooc_sources:
            _path = os.path.join(args.data_dir, 'entities', 'video.json')
            with open(_path, 'r') as fin:
                lines = fin.readlines()
                for line in tqdm(lines, total=len(lines)):
                    video_dict = json.loads(line.strip())
                    ccid = video_dict["ccid"]
                    doc_num = 0
                    doc = ""
                    for i, sentence in enumerate(video_dict["text"]):
                        doc += sentence
                        if len(doc) > args.max_ctx_window or i == len(video_dict["text"]) - 1:
                            # output doc
                            res_dict = {
                                "id": f"{ccid}_{doc_num}",
                                "title": video_dict["name"],
                                "body": doc,
                                "tags": []
                            }
                            fout.write(json.dumps(res_dict))
                            fout.write("\n")
                            doc = ""
                            doc_num += 1
        # 习题
        if 'problem' in args.mooc_sources:
            _path = os.path.join(args.data_dir, 'entities', 'problem.json')
            with open(_path, 'r') as fin:
                lines = fin.readlines()
                for line in tqdm(lines, total=len(lines)):
                    problem_dict = json.loads(line.strip())
                    q = problem_dict["content"]
                    a = get_answer(problem_dict)
                    if a:
                        doc = f"{q} {a}"
                        res_dict = {
                            "id": problem_dict["problem_id"],
                            "title": problem_dict["title"],
                            "body": doc,
                            "tags": []
                        }
                        fout.write(json.dumps(res_dict))
                        fout.write("\n")
    elif args.model == 'BaiduArticle':
        pass


def yield_data(args):
    """
    :param args:
    :return: res_lst : list of {"id": str id,
                                "title":str course_name or doc title,
                                "body": str document,
                                "tags": List of str}
    """
    res_lst = []
    with open(args.data_path, 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            res_dict = json.loads(line.strip())
            res_lst.append(res_dict)

    return res_lst


def build_index(args):
    # Define a default Elasticsearch client
    connections.create_connection(hosts=['localhost'])
    # create the mappings in elasticsearch
    Model = name2model[args.model]
    if args.init:
        Model.init()

    # create and save and article
    iters = yield_data(args)
    for iter in tqdm(iters, total=len(iters), desc="build_index"):
        article = MoocArticle(meta={'id': iter['id']}, title=iter['title'],
                              body=iter['body'])
        article.body = iter['body']
        article.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data for searching Open-QA documents on moooccube')
    parser.add_argument('--data_dir', help='数据地址', default='/data/tsq/MOOCCube2')
    parser.add_argument('--task', help='任务类型', default='preprocess',
                        choices=['preprocess', 'build_index'])
    parser.add_argument('--init', action='store_true')
    # 对于建立索引数据的来源
    parser.add_argument('--model', help='索引模型', default='MoocArticle', choices=['MoocArticle', 'BaiduArticle'])
    parser.add_argument('--mooc_sources', help='信息来源', type=str, nargs='+', default=['video', 'problem'])
    parser.add_argument('--max_ctx_window', help='上下文最长', type=int, default=96)

    args = parser.parse_args()
    args.data_path = os.path.join(args.data_dir, 'es', f'{args.model}.json')

    if args.task == 'preprocess':
        preprocess(args)
    elif args.task == 'build_index':
        build_index(args)
