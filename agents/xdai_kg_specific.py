### GLM + specific domain knowledge injected (Using concept-expansion & faq matching mechanism with mongodb)
### For better performance, you can add more components like preprocess and check-result-and-regenerate.
### version = "xdai_glm_sp_domain"
### set the topic
import random

from agents import AgentBase
from module.use_plm import getGeneratedText
from utils.processor import filter_glm
from utils.log import get_logger
from database.models import UtterranceMode
from module.internal_api import get_similarity_scores_query, get_faq_pairs_api
from module.qa_t5 import answer_QA
from database.persona import personas, persona2qa_lst, persona2background
from database.complex_qa_expamples import complex_type2qa_examples
import math

logger = get_logger("XDAI")


class ChatAgent_SP(AgentBase):
    botname = "A"
    username = "Q"
    close_kw = ["bye"]
    byemsg = ["和你聊天很愉快，再见~"]
    version = "xdai_glm_sp_domain"
    activate_kw = version
    concat_turns = 6
    background = [
        ("你好", "你好, 我是你的智能学习助理小木~"),
        ("最近怎么样", "还是老样子"),
        ("你有什么功能", "我可以为你解释知识点概念、查询课程资源、回答平台使用常见问题，推荐学术资源，还可以为你作诗哦～")
    ]
    model = "glm"
    topic = "self-defined-topic"  # the same you use for concept expansion
    description = "self-defined-description of the topic"  #
    faq_qapairs = []
    concept_qapairs = []
    complex_qa_args = {}
    q_type = ""
    persona = ""

    def __init__(self, sess_mgr=None, talkername="Q"):
        logger.info(f"init class: {self.version}, talker's name:{talkername}")
        super().__init__(sess_mgr=sess_mgr)
        self.username = talkername

    async def make_reply(self, mode="normal", **kwargs):
        self.description = kwargs.get('courseinfo', "self-defined-description of the topic")
        self.faq_qapairs = kwargs.get('qapairs', [])
        self.concept_qapairs = kwargs.get('concept_qa_pairs', [])
        self.complex_qa_args = kwargs.get('complex_qa_args', {})
        self.q_type = kwargs.get('q_type', '')
        self.model = kwargs.get('glm_model', 'glm')
        if mode in [UtterranceMode.normal, UtterranceMode.activate]:
            num = self.concat_turns
            prompt, concept_text = self.get_concat_history(num)
            logger.info(f"[selected prompt]:\n{prompt}")
            raw_generated_contents = await getGeneratedText(prompt, limit=30, batchsize=1, model=self.model)
            # logger.info(f"130b raw_generated_contents is {raw_generated_contents}")
            reply = ""
            if self.model == "glm":
                for text in raw_generated_contents:
                    reply = filter_glm(text, split="|", prefix=f"({self.botname}:|{self.username}:)")
            else:
                # glm-130b
                for text in raw_generated_contents:
                    logger.info(f"130b text is {text}")
                    _reply = filter_glm(text[0] + "|A:不知道", split="|", prefix=f"({self.botname}:|{self.username}:)")
                    logger.info(f"130b _reply is {_reply}")
                    reply = ''.join(_reply.split())
                    # logger.info(f"130b reply is {reply}")
            reply = reply.strip(",:，：")
            if len(concept_text) > 0:
                reply = reply + "\n答案解析:" + concept_text
            logger.info(f"reply:{reply}")
            return [reply]

        elif mode == UtterranceMode.close:
            return self.byemsg

    def get_concat_history(self, num=None):
        query = self.history[-1]
        history_utts = self.get_chatlog_utterances(num=num)
        imported_qapairs = self.get_external_retrieved_qapairs()
        all_candidates = history_utts + imported_qapairs
        logger.info("history_utts:{}".format(history_utts))
        # logger.info("all_candidates:{}".format(all_candidates))
        if all_candidates:
            sim_res = self.score_prompt_sim(target=query.get("text"), prompt_list=all_candidates)
            candidates_ranking = [
                (c.get("text"), c.get("weight", 0.5) * sim * max(30, len(c.get("text"))) / 30)
                for c, sim in zip(all_candidates, sim_res)
            ]
            sorted_prompts = sorted(candidates_ranking, key=lambda x: x[-1])
            sorted_prompts = [i[0] for i in sorted_prompts][-12:]
        else:
            sorted_prompts = []
        logger.info("sorted_prompts:{}".format(sorted_prompts))
        # sorted_prompts.append("{username}" + ":{}".format(query.get("text")))
        # sorted_prompts.append("{botname}:")
        concat_text = "|".join(sorted_prompts)
        concat_text = concat_text.format(botname=self.botname, username=self.username)
        concat_text = self.description + " " + concat_text
        # shorten the context
        shorten_concat_text = concat_text[:900]
        concept_text = ""
        if self.complex_qa_args:
            # we will preset the answer's start words with concept definition
            concept_qapairs = self.__get_concept_qa()
            if concept_qapairs:
                concept_text = " ".join([concept_qapair['a'] for concept_qapair in concept_qapairs])
                _concept_text = "{}所以,{}? 答案是".format(concept_text, query.get("text"))
                concat_text = shorten_concat_text + "|{}:{}|{}:{}".format(self.username, query.get("text"),
                                                                          self.botname,
                                                                          _concept_text)
            else:
                concat_text = shorten_concat_text + "|{}:{}|{}:".format(self.username, query.get("text"), self.botname)
        else:
            concat_text = shorten_concat_text + "|{}:{}|{}:".format(self.username, query.get("text"), self.botname)

        return concat_text, concept_text

    def score_prompt_sim(self, target="", prompt_list=[]):
        ### prompt_list = [(q,a)]
        if not target:
            target = self.history[-1].get("text")
        target = target.replace("{botname}:", "").replace("{username}:", "")
        text_list = []
        logger.info("prompt_list: {}".format(prompt_list))
        for item in prompt_list:
            if isinstance(item, dict):
                q = item.get("q", "")
                a = item.get("a", "")
                text = q + a
            elif isinstance(item, str):
                text = item
            elif isinstance(item, tuple):
                try:
                    q = item[0]
                    a = item[1]
                    text = q + a
                except:
                    text = ""
            text = text.replace("{botname}:", "").replace("{username}:", "")
            text_list.append(text)

        res = get_similarity_scores_query(target=target, candidates=text_list)
        return res

    def get_chatlog_utterances(self, num, max_history_turns=8):
        query_lst = self.history[::-2][:max_history_turns]

        def get_persona_intention(query):
            for _persona in personas:
                if _persona in query["text"]:
                    return _persona
            return None

        # consider the persona
        # logger.info(f"query_lst is: {query_lst}")
        # logger.info(f"personas is: {personas}")
        candidate_history = self.history
        for _query in query_lst:
            persona = get_persona_intention(_query)
            # logger.info(f"persona is: {persona}")
            if persona:
                # add persona qa in history
                persona_qa = persona2qa_lst[persona]
                logger.info(f"persona is: {persona}")
                logger.info(f"persona_qa is: {persona_qa}")
                candidate_history = persona_qa + self.history[-3:]
                num += len(persona_qa)
                self.persona = persona
                break
        logger.info(f"candidate_history is: {candidate_history}")
        history_selected = candidate_history[-num - 1:-1][::-1]
        # logger.info(f"history_selected is: {history_selected}")
        his_turn = len(history_selected) // 2
        history_utts = []
        for i in range(his_turn):
            try:
                if history_selected[i * 2]['is_bot'] and not history_selected[i * 2 + 1]['is_bot']:
                    question = history_selected[i * 2 + 1].get("text")
                    talker_1 = history_selected[i * 2 + 1].get("talker")
                    talker_1_str = "{botname}" if talker_1 == "bot" else "{username}"
                    answer = history_selected[i * 2].get("text")
                    talker_2 = history_selected[i * 2].get("talker")
                    talker_2_str = "{botname}" if talker_2 == "bot" else "{username}"
                    w = 1 + math.exp(-0.2 * i)
                    if talker_2_str == "{botname}":
                        text = f"{talker_1_str}:{question}|{talker_2_str}:{answer}"
                    else:
                        text = f"{talker_2_str}:{answer}|{talker_1_str}:{question}"
                    res = {
                        "text": text,
                        "q": question,
                        "a": answer,
                        "weight": w
                    }
                    logger.info(f"res {res}")
                    history_utts.append(res)
            except KeyError:
                continue
        return history_utts

    def __get_conversational_cold_start(self):
        if self.persona:
            try:
                self.background = persona2background[self.persona]
            except KeyError:
                self.background = [("你好", f"同学你好, 我是你的{self.persona}小木~")]
        qapairs = [{"q": i[0], "a": i[1]} for i in self.background]
        return qapairs

    def __get_faq_qa(self):
        # if len(self.history) >= 3:
        #     utts = [self.history[-1], self.history[-3]]
        # else:
        #     utts = self.history[::-1]

        # if len(self.history) >= 1:
        #     questions = [doc.get("text", "") for doc in utts]
        # else:
        #     return None
        # logger.info("question:{}".format(questions))
        # qapairs = []
        # for i, text in enumerate(questions):
        #     # cur_qapairs = get_faq_pairs_api(query=text, topic=self.topic, topk=3)
        #     cur_qapairs = []
        #     for pair in cur_qapairs:
        #         qapair = answer_QA.QAgeneration(method="template", doc={"name":pair.get("q"),"summary":pair.get("a")})
        #         qapairs.append(qapair)
        #     if cur_qapairs:
        #         break
        # qapairs =  qapairs[:3]
        qapairs = []
        for qapair in self.faq_qapairs:
            _qapair = {'q': qapair.pop('question'), 'a': qapair.pop('answer')}
            # if self.complex_qa_args:
            #     For complex_qa, we only need concepts
            # if '\n' in qapair['a']:
            #     pure_explain = qapair['a'].split('\n')[0]
            #     qapair['a'] = pure_explain
            # else:
            #     continue
            qapairs.append(_qapair)
        logger.info("faq result:{}".format(qapairs))
        return qapairs

    def __get_concept_qa(self, max_concept_num=2):
        qapairs = []
        logger.info("raw concepts:{}".format(self.concept_qapairs))
        for qapair in self.concept_qapairs:
            if len(qapairs) >= max_concept_num:
                break
            _qapair = {'q': qapair.pop('question'), 'a': qapair.pop('answer').strip()}
            # We need concept explanation
            tmp = _qapair['a'].split('；')
            # logger.info("tmp:{}".format(tmp))
            if len(tmp) < 2:
                continue
            elif len(tmp[1]) < 5:
                continue
            # Domain information is separated by \n
            # if '\n属于' in _qapair['a']:
            #     pure_explain = _qapair['a'].split('\n')[0]
            #     _qapair['a'] = pure_explain
            qapairs.append(_qapair)
        logger.info("concept result:{}".format(qapairs))
        return qapairs

    def __get_cot_qa(self):
        qapairs = []
        if self.complex_qa_args:
            complex_type = self.complex_qa_args.get("fix_prompt_type")
            if complex_type:
                qa_examples = complex_type2qa_examples[complex_type]
                qapairs = qa_examples[:4]
            else:
                # dynamic choose type
                # TODO
                qa_examples = complex_type2qa_examples[self.q_type]
                qapairs = qa_examples[:4]
        logger.info("CoT result:{}".format(qapairs))
        return qapairs

    def get_external_retrieved_qapairs(self):
        ###

        if self.complex_qa_args:
            SourceDict = {
                "coldstart": (self.__get_conversational_cold_start, 0.1),
                "CoT": (self.__get_cot_qa, 0.8),
            }
        else:
            SourceDict = {
                "coldstart": (self.__get_conversational_cold_start, 0.1),
                "xlore": (self.__get_faq_qa, 0.5),
                "CoT": (self.__get_cot_qa, 0.8),
            }
        all_pairs = []

        def merged(item, weight):
            q = item.get("q")
            a = item.get("a")
            text = "|".join(["{username}:" + q, "{botname}:" + a])
            return {"q": q, "text": text, "weight": weight}

        for k, v in SourceDict.items():
            func, w = v[0], v[1]
            qapirs = func()
            qapirs = [merged(item, w) for item in qapirs]
            all_pairs.extend(qapirs)
            # print(k, v, qapirs)

        return all_pairs


if __name__ == "__main__":
    pass
