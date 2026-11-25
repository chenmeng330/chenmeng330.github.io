# -*- coding: utf-8 -*-
"""重排导入的 txt：qinzao 每行成段并识别章节号；xunbaoshu/shancha 按对话断段。"""
import io
import re

BASE = r"C:\Workarea\qinxi-site\src\content\texts\fiction"

CN_NUM = "序壹贰叁肆伍陆柒捌玖拾终"


def split_front(s):
    parts = s.split("---", 2)
    return "---" + parts[1] + "---\n\n", parts[2]


def join_front(front, body):
    return front + body


def reflow_qinzao(body):
    out = []
    for raw in body.split("\n"):
        t = raw.strip("\u3000 \t\r")
        if not t:
            continue
        m = re.fullmatch(r"([%s])、" % CN_NUM, t)
        if m:
            out.append("## " + m.group(1))
        else:
            out.append(t)
        out.append("")
    return "\n".join(out).strip("\n") + "\n"


def reflow_dialogue(body):
    text = body.strip("\n")
    text = re.sub(r"”\s*(?=“)", "”\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text + "\n"


for fn, mode in [
    ("qinzao-hesheng.md", "qinzao"),
    ("xunbaoshu.md", "dialogue"),
    ("shancha-yu-ling.md", "dialogue"),
]:
    p = BASE + "\\" + fn
    s = io.open(p, encoding="utf-8").read()
    front, body = split_front(s)
    before = len([l for l in body.split("\n") if l.strip()])
    new = reflow_qinzao(body) if mode == "qinzao" else reflow_dialogue(body)
    io.open(p, "w", encoding="utf-8", newline="\n").write(front + new)
    after = len([l for l in new.split("\n") if l.strip()])
    print(f"{fn}: {before} -> {after} paragraphs")
