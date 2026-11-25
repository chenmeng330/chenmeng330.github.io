# -*- coding: utf-8 -*-
"""把 C:\\OurWork 里的纯文本稿件导入站点内容目录。

规则：
- 首行视为标题，丢弃（标题写进 frontmatter）
- 空行分段
- 单独一段的「———」（若干破折号）转成 Markdown 分隔线 ***
- 其余原样保留，段落间一个空行
"""
from __future__ import annotations

import pathlib
import re

OUT = pathlib.Path(r"C:\Workarea\qinxi-site\src\content\texts")

ITEMS = [
    # ---------- fiction ----------
    dict(
        src=r"C:\OurWork\秦羲子\作品\关灯.txt",
        slug="guandeng",
        kind="fiction",
        category="原创短篇",
        date="2026-11-20",
        summary="晚自习后留下来关灯锁门的人，和一个总留到最后的人。",
    ),
    dict(
        src=r"C:\OurWork\秦羲子\作品\三婆.txt",
        slug="sanpo",
        kind="fiction",
        category="原创短篇",
        date=None,
        summary="瞎眼的三婆走进院里，闻出这批香里掺了柏木。",
    ),
    dict(
        src=r"C:\OurWork\秦羲子\作品\师父周德顺.txt",
        slug="zhoude-shun",
        kind="fiction",
        category="原创短篇",
        date=None,
        summary="霜降送茅船，师父绕了一条远路，柜里那张愿表写着「未还」。",
    ),
    dict(
        src=r"C:\OurWork\秦羲子\作品\张家媳妇.txt",
        slug="zhangjia-xifu",
        kind="fiction",
        category="原创短篇",
        date=None,
        summary="傩堂里还愿的女人，男人在广东。",
    ),
    dict(
        src=r"C:\OurWork\秦羲子\作品\何姓女人.txt",
        slug="hexing-nvren",
        kind="fiction",
        category="原创短篇",
        date=None,
        summary="陈秀莲，七岁，以身为愿，未还。",
    ),
    dict(
        src=r"C:\OurWork\秦羲子\作品\一百零八道.txt",
        slug="yibailingba-dao",
        kind="fiction",
        category="原创短篇",
        date=None,
        summary="师父死后的第二夜，我还是打开了那只箱子，数面具里的刻痕。",
    ),
    dict(
        src=r"C:\OurWork\小说\原创短篇\东方同人\2短篇\第1章 寻宝鼠.txt",
        slug="xunbaoshu",
        kind="fiction",
        category="东方同人",
        date=None,
        summary="娜兹玲受人所托，去找一件掉了的东西。",
    ),
    dict(
        src=r"C:\OurWork\小说\原创短篇\东方同人\2短篇\第1章 山茶与铃.txt",
        slug="shancha-yu-ling",
        kind="fiction",
        category="东方同人",
        date=None,
        summary=None,
    ),
    # ---------- essays ----------
    dict(
        src=r"C:\OurWork\diary\2026-11-20.txt",
        slug="diary-2026-11-20",
        kind="essay",
        category=None,
        date="2026-11-20",
        summary=None,
    ),
    dict(
        src=r"C:\OurWork\diary\2026-11-22.txt",
        slug="diary-2026-11-22",
        kind="essay",
        category=None,
        date="2026-11-22",
        summary=None,
    ),
]

SEP = re.compile(r"^\s*[—–-]{3,}\s*$")
CN_CHAPTER = re.compile(r"^[一二三四五六七八九十]+$")


def paragraphs(text: str) -> list[str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    # 丢掉首个非空行（标题）
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines:
        lines.pop(0)
    paras: list[str] = []
    buf: list[str] = []
    for line in lines:
        if line.strip() == "":
            if buf:
                paras.append("".join(buf).strip())
                buf = []
            continue
        buf.append(line.rstrip())
    if buf:
        paras.append("".join(buf).strip())
    return [p for p in paras if p]


def yaml_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build(item: dict) -> str:
    src = pathlib.Path(item["src"])
    raw = src.read_text(encoding="utf-8-sig")
    paras = paragraphs(raw)
    title = item.get("title") or raw.replace("\r\n", "\n").split("\n")[0].strip()
    title = title.strip("《》 ").strip()

    body_lines: list[str] = []
    for p in paras:
        if SEP.match(p):
            body_lines.append("***")
            continue
        if CN_CHAPTER.match(p):
            body_lines.append(f"## {p}")
            continue
        body_lines.append(p)

    fm = ["---", f"title: {yaml_str(title)}", f"slug: {yaml_str(item['slug'])}"]
    fm.append(f"kind: {item['kind']}")
    if item.get("category"):
        fm.append(f"category: {yaml_str(item['category'])}")
    if item.get("date"):
        fm.append(f"date: {item['date']}")
    if item.get("summary"):
        fm.append(f"summary: {yaml_str(item['summary'])}")
    fm.append("---")

    out_dir = OUT / item["kind"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{item['slug']}.md"
    out_path.write_text("\n".join(fm) + "\n\n" + "\n\n".join(body_lines) + "\n", encoding="utf-8")
    return f"{out_path}  ({len(''.join(body_lines))} 字)"


if __name__ == "__main__":
    for it in ITEMS:
        try:
            print(build(it))
        except Exception as exc:  # noqa: BLE001
            print("FAILED", it["src"], exc)
