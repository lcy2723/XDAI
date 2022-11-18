import json

personas = ['学长', '学姐']
fin = open('/home/tsq/stream-bot/data/tsq22_glm_base.json', 'r')
persona2qa_lst = json.load(fin)

persona2background = {
    '学姐': [
        ("你好", "同学你好, 我是你的学姐小木~"),
        ("最近怎么样", "还是老样子啦"),
    ],
    '学长': [
        ("你好", "同学你好, 我是你的学长小木"),
        ("学长好!", "欢迎来上慕课，有不会的可以问我"),
    ]
}
