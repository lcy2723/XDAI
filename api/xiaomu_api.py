from pydantic import BaseModel
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
from pathlib import Path
import json

BASE_DIR = Path.resolve(Path(__file__)).parent.parent
sys.path.append(str(BASE_DIR))
print(BASE_DIR)
from module.session_managers.session_manager_ram import SessionManagerRam
from database.data_types import UtteranceItem
from utils.log import get_logger

logger = get_logger("XDAI")
from database.models import TalkerType, GetSessInfo
import asyncio
import time

app = FastAPI()
item = GetSessInfo()
item.version = 'xdai_glm_sp_domain'
glm_version = 'glm'
# glm_version = 'glm_130b'
item.window_info.platform = "term"
item.window_info.platform_id = 'xiaomu'
agent = SessionManagerRam.get_agent_by_brand(item)
fin = open('/data/tsq/MOOCCube2/entities/course.json', 'r')
id2about = {}
for line in fin:
    course_item = json.loads(line)
    id2about[course_item['id']] = course_item['about']

# 计算问题相似度模块
modelname = "uer/sbert-base-chinese-nli"
model = SentenceTransformer(modelname)

with open('/home/tsq/user/lcy/sen_sim/qa_data.json', 'r') as f:
    qa_data = json.load(f)
# 历史qa对列表
qa_data = qa_data['qa_data']
# 历史问题列表
sentences = []
for qa_pair in qa_data:
    sentences.append(qa_pair['q'])
sentence_embeddings = model.encode(sentences)


class Item(BaseModel):
    # message: str = None
    # uid: int = None
    user_id: str = None
    question: str = None
    chat_id: str = None
    source: str = None
    dialog_cache: list = None
    user_video_cache: list = None
    course_id: str = None
    faq_qa_pairs: list = None
    concept_qa_pairs: list = None
    complex_qa_args: dict = None
    q_type: str = None
    time_dict: dict = None


@app.post('/test')
def get_reply(request_data: Item):
    source = request_data.source
    agent.sess.history = []
    if source == "来自图灵机器人":
        # 开始重写
        time_dict = request_data.time_dict
        xdai_start = time.time()
        time_dict["xdai_start"] = xdai_start
        time_dict["rewrite_prepare_cost"] = xdai_start - time_dict['core_end']
        for dialog_cache in request_data.dialog_cache:
            if not dialog_cache['final_question'] or len(dialog_cache['answers']) < 1:
                # 历史 是空问题 或者 没有答案 则跳过
                continue
            concat_answer = "".join([answer["message"] for answer in dialog_cache['answers']])
            if not concat_answer:
                # 空答案也跳过
                continue
            # 一个问题只输出一个答案
            utt_user = UtteranceItem.parse_simple(talker=TalkerType.user, text=dialog_cache['final_question'])
            agent.sess.add_utterance(utt_user)
            utt_bot = UtteranceItem.parse_simple(talker=TalkerType.bot, text=concat_answer)
            agent.sess.add_utterance(utt_bot)

        content = request_data.question
        utt = UtteranceItem.parse_simple(talker=TalkerType.user, text=content)
        agent.sess.add_utterance(utt)
        agent.import_history()
        course_info = id2about[request_data.course_id]
        replies = asyncio.run(agent.make_reply(courseinfo=course_info, qapairs=request_data.faq_qa_pairs,
                                               glm_model=glm_version,
                                               concept_qa_pairs=request_data.concept_qa_pairs,
                                               complex_qa_args=request_data.complex_qa_args,
                                               q_type=request_data.q_type))
        # 重写结束
        xdai_end = time.time()
        time_dict["xdai_end"] = xdai_end
        time_dict["glm_cost"] = xdai_end - xdai_start
        logger.info(f"time_dict: {time_dict}")
        for rep in replies:
            utt = UtteranceItem.parse_simple(talker=TalkerType.bot, text=rep)
            agent.sess.add_utterance(utt)
            res = {"res": rep, "user_id": request_data.user_id}
            return res
    else:
        return {"res": "小木只处理来自图灵机器人类", "user_id": request_data.user_id}


@app.post('/sen_sim')
def get_history_answer(request_data: Item):
    query = [request_data.question]
    query_embeddings = model.encode(query)
    # 计算余弦相似度
    sen_res = cosine_similarity([query_embeddings[0]], sentence_embeddings)
    sen_res = sen_res[0].tolist()
    sen_res = zip(range(len(sen_res)), sen_res)
    # 取相似度最大的作为结果，返回问题及答案
    res_index = max(sen_res, key=lambda x: x[1])
    res = {"history_question": qa_data[res_index[0]]['q'], "answer": qa_data[res_index[0]]['a'],
           "human_ans": qa_data[res_index[0]]['human_a']}
    return res
