from pydantic import BaseModel
from fastapi import FastAPI
import sys
from pathlib import Path
import json

BASE_DIR = Path.resolve(Path(__file__)).parent.parent
sys.path.append(str(BASE_DIR))
print(BASE_DIR)
from module.session_managers.session_manager_ram import SessionManagerRam
from database.data_types import UtteranceItem
from database.models import TalkerType, GetSessInfo
import asyncio

import argparse

app = FastAPI()
item = GetSessInfo()
item.version = 'xdai_glm_sp_domain'
item.window_info.platform = "term"
item.window_info.platform_id = 'xiaomu'
agent = SessionManagerRam.get_agent_by_brand(item)


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


@app.post('/test')
def get_reply(request_data: Item):
    source = request_data.source
    agent.sess.history = []
    if source == "来自图灵机器人":
        for dialog_cache in request_data.dialog_cache:
            if not dialog_cache['final_question']:
                # 是空字符
                continue
            utt_user = UtteranceItem.parse_simple(talker=TalkerType.user, text=dialog_cache['final_question'])
            agent.sess.add_utterance(utt_user)
            for answer in dialog_cache['answers']:
                utt_bot = UtteranceItem.parse_simple(talker=TalkerType.bot, text=answer['message'])
                agent.sess.add_utterance(utt_bot)
                # 一个问题只输出一个答案
                break
        content = request_data.question
        utt = UtteranceItem.parse_simple(talker=TalkerType.user, text=content)
        agent.sess.add_utterance(utt)
        agent.import_history()
        course_info = ''
        with open('/data/tsq/MOOCCube2/entities/course.json', 'r') as f:
            for line in f:
                course_item = json.loads(line)
                if course_item['id'] == request_data.course_id:
                    course_info = course_item['about']
        replies = asyncio.run(agent.make_reply(courseinfo=course_info, qapairs=request_data.faq_qa_pairs))
        for rep in replies:
            utt = UtteranceItem.parse_simple(talker=TalkerType.bot, text=rep)
            agent.sess.add_utterance(utt)
            res = {"res": rep, "user_id": request_data.user_id}
            return res
    else:
        return {"res": "小木只处理来自图灵机器人类", "user_id": request_data.user_id}
