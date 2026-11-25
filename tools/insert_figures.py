# -*- coding: utf-8 -*-
"""把长文里的「图注：」行替换为 <figure>，并给章节标题加 ##。"""
import io
import re

MD = r"C:\Workarea\qinxi-site\src\content\texts\longform\qin-hesheng.md"

HEADINGS = {
    "序",
    "中国秦？还是日本秦？",
    "飞鸟的秦之首领",
    "是神非神？",
    "似神非神",
    "最后",
    "辅助网站",
}

# 图注关键词 -> (图片, alt)
FIGURES = [
    ("広隆寺楼门", "01-koryuji-romon.jpg", "広隆寺楼门"),
    ("时间轴", "timeline.png", "秦河胜生平时间轴"),
    ("谱系", "genealogy.png", "秦氏家族谱系"),
    ("秦河胜像", "08-kawakatsu.jpg", "秦河胜像"),
    ("弥勒菩萨", "02-miroku.jpg", "弥勒菩萨半跏思惟像"),
    ("梦殿", "05-yumedono.jpg", "法隆寺梦殿"),
    ("大避神社", "04-osake.jpg", "坂越大避神社"),
    ("翁", "07-okina.jpg", "能面「翁」"),
    ("摩多罗神", "06-madarajin.jpg", "摩多罗神及二童子像"),
]

with io.open(MD, encoding="utf-8") as f:
    lines = f.read().split("\n")

out = []
i = 0
used = set()
while i < len(lines):
    line = lines[i]
    s = line.strip()

    if s in HEADINGS:
        out.append("## " + s)
        i += 1
        continue

    if s.startswith("图注："):
        caption = s[len("图注："):]
        img = alt = None
        for key, fn, a in FIGURES:
            if key in caption:
                img, alt = fn, a
                used.add(key)
                break
        if img is None:
            out.append(line)
            i += 1
            continue
        url = ""
        if i + 1 < len(lines) and lines[i + 1].strip().startswith("来源："):
            m = re.search(r"https?://\S+", lines[i + 1])
            if m:
                url = m.group(0).rstrip("）)")
            i += 1
        block = ['<figure>',
                 f'  <img src="/images/qin-hesheng/{img}" alt="{alt}" loading="lazy" />',
                 '  <figcaption>',
                 f'    {caption}']
        if url:
            block.append(f'    <br /><a href="{url}" rel="noopener" target="_blank">来源</a>')
        block += ['  </figcaption>', '</figure>']
        out.append("\n".join(block))
        i += 1
        continue

    if s.startswith("来源："):
        i += 1
        continue

    out.append(line)
    i += 1

with io.open(MD, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))

print("done, figures:", sorted(used))
print("unused:", [k for k, _, _ in FIGURES if k not in used])
