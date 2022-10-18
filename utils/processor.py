import time
import pytz
from datetime import datetime
import hashlib
import re


def get_time(stamp=None, form="%Y-%m-%d %H:%M:%S"):
    if not stamp:
        stamp = time.time()
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.fromtimestamp(stamp, tz)
    strt = now.strftime(form)
    return strt, stamp


def set_now_time(obj, is_end=False):
    t, stamp = get_time()
    if not is_end:
        obj.created_t = stamp
        obj.created_time = t
    else:
        obj.closed_t = stamp
        obj.closed_time = t


def hashidx(org_id):
    data_hash = hashlib.new("md5", org_id.encode("utf8"))
    return data_hash.hexdigest()


def remove_replicate_secs(text):
    lis = text.split(",")
    res = []
    for i in lis:
        if i in res or not i:
            continue
        else:
            res.append(i)
    return ",".join(res)


def filter_glm(text, prefix="(BOT:|USER:)", split="|"):
    if split == "|":
        regex_pattern = f"\<\|startofpiece\|\>([^\|]*)\{split}"
        reg = re.compile(regex_pattern)
    t = re.findall(reg, text)
    if not t:
        t = re.findall(f"<\|startofpiece\|>(.+)", text)
    if t and t[0] == '':
        t = re.findall(f"<\|startofpiece\|>(.+)", text)
        t = re.findall(f"\|BOT:(.+)", "" if not t else t[0])
    if not t:
        regex_pattern = f"\[\[gMASK\]\]([^\|]*)\{split}"
        reg = re.compile(regex_pattern)
        t = re.findall(reg, text)
    res = "" if not t else t[0]
    if not t:
        generated = text.split("[[gMASK]]")[1]
        if '、' in generated:
            listed = generated.split('、')[:4]
            res = '、'.join(listed)
    res = res.strip()
    res = re.sub("\[.*\]", "", res)
    prefix = prefix
    reg = re.compile(prefix)
    t = re.split(reg, res)
    for i in t:
        if i and i not in prefix:
            res = i
            break
    else:
        pass

    res = res.strip()
    return res


if __name__ == "__main__":
    text = '小吃 太多了 , 肉 夹 馍 、 凉 皮 、 bian gb iang 面 、 西安 酿 皮 、 水 盆 羊肉 、 泡泡 油 糕 。 | Q : 字符串 ( character string ); 一串 邻 接 的 字符 。  算法 ( algorithm ); 解决 给定 问题的 确定的 计算机 指令 序列 , 用以 系统地 描述 解决问题的 步骤 。 所以 你 知道 什么 字符串 相关的 算法 吗 ? | A : [[gMASK]] [sop] 字符串 相关的 算法 有 : 字符串 的  哈 希 算法 、 字符串 的 分 治 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算 法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、  字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字 符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法  、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串 的 回 文 算法 、 字符串 的 回 文 逆 序 算法 、 字符串'
    filtered = filter_glm(text, prefix="(Q:|A:)")
    print("result is:")
    print(filtered)
