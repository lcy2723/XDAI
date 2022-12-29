import asyncio
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import requests, json
import time
import aiohttp
from config import CONFIG


async def api_async(url="", payload={}, headers={}):
    """
    import aiohttp
    """
    if headers == {}:
        headers = {"Content-Type": "application/json;charset=utf8"}

    async with aiohttp.ClientSession(headers=headers, raise_for_status=True) as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()
            return data


def req_api(url="", payload={}, method="POST", headers={}):
    if headers == {}:
        headers = {"Content-Type": "application/json;charset=utf8"}
    payload = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    response = requests.request(method, url, data=payload, headers=headers)
    result = response.json()
    return result


def test130b(texts, strategy="BaseStrategy", stop=[], regix=""):
    # If TOPK/TOPP are 0 it defaults to greedy sampling, top-k will also override top-p
    data = {
        "prompt": texts,
        "max_tokens": 64,
        "min_tokens": 0,
        "top_k": 1,
        "top_p": 0,
        "temperature": 1,
        "seed": 1453,
        "sampling_strategy": strategy,
        "num_beams": 4,
        "length_penalty": 0.9,
        "no_repeat_ngram_size": 3,
        "regix": regix
    }

    t = time.time()
    res = requests.post("http://180.184.97.60:9624/generate", json=data).content.decode()
    t = time.time() - t

    res = json.loads(res)
    # print(res['text'], end='\n\n')
    text_res = []

    for generate, text in zip(res['text'], texts):
        generate.append('')
        generate = generate[0]
        # generate = "\x1B[4m" + generate.replace("[[gMASK]]", "") + "\x1B[0m"
        if "MASK" in text:
            text_res.append(text.replace("[gMASK]", "[[gMASK]]" + generate).replace("[MASK]", generate))
        else:
            text_res.append(text + generate)
    # print("glm130b", text_res)
    return text_res


async def generate_plm(prompt="", limit=30, url=None, model="glm"):
    if url is None:
        url = CONFIG.default_plm_api
    if model == "glm":
        url = CONFIG.glm_query_api
    # payload = {"content": prompt, "max_length": limit}
    payload = {"query": prompt, "limit": limit}

    if model == "glm_130b":
        # url = "http://103.238.162.37:9622/general"
        # payload = {"contexts": [prompt]}
        return test130b([prompt])
    res = await api_async(url=url, payload=payload)
    if res.get("code") != 0:
        return False
    result = res.get("data")
    return result


async def getGeneratedText(prompt=[], limit=30, batchsize=1, model="ctxl"):
    limits = limit
    if isinstance(prompt, str) and batchsize:
        prompt = [prompt for _ in range(batchsize)]
    if isinstance(limits, int):
        limits = [limits for _ in range(len(prompt))]
    elif isinstance(limits, list):
        assert len(limits) == len(prompt)

    tasks = [
        asyncio.create_task(generate_plm(prompt=p, limit=l, model=model))
        for p, l in zip(prompt, limits)
    ]
    done, pending = await asyncio.wait(tasks, timeout=15)

    results = []
    for p in pending:
        p.cancel()

    for d in done:
        results.append(d.result())
    return results


if __name__ == "__main__":
    st = time.time()
    results = asyncio.run(getGeneratedText(prompt=["你好"], model="glm_130b"))
    print(time.time() - st)
    print(results)
