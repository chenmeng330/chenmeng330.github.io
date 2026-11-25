# -*- coding: utf-8 -*-
"""从 docx 提取正文，转成站点 Markdown。"""
from __future__ import annotations

import pathlib
import sys

import docx

OUT = pathlib.Path(r"C:\Workarea\qinxi-site\src\content\texts")

ITEMS = [
    dict(
        src=r"C:\Workarea\以神为衣的凡人：秦河胜_3.docx",
        slug="qin-hesheng",
        kind="longform",
        category="考据",
        date=None,
        summary="秦河胜，一个被神穿过的凡人。从《日本书纪》的记载出发，追一个渡来人如何在神话与史书之间留下痕迹。",
    ),
    dict(
        src=r"C:\OurWork\小说\原创短篇\东方同人\3秦造河胜.docx",
        slug="qinzao-hesheng",
        kind="fiction",
        category="东方同人",
        date=None,
        summary="东方同人长篇。秦造与河胜，两个名字共用一副身体的故事。",
    ),
]


def yaml_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(item: dict) -> str:
    d = docx.Document(item["src"])
    blocks: list[str] = []
    for p in d.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        style = p.style.name if p.style is not None else "Normal"
        if style.lower().startswith("heading"):
            level = "".join(ch for ch in style if ch.isdigit()) or "1"
            blocks.append("#" * min(int(level) + 1, 4) + " " + text)
        else:
            blocks.append(text)

    # 首个块是文章大标题时去掉（标题已在 frontmatter）
    if blocks and blocks[0].startswith("#"):
        blocks.pop(0)

    fm = ["---", f"title: {yaml_str(item['title'])}", f"slug: {yaml_str(item['slug'])}"]
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
    out_path.write_text("\n".join(fm) + "\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    return f"{out_path}  ({sum(len(b) for b in blocks)} 字, {len(blocks)} 块)"


if __name__ == "__main__":
    for it in ITEMS:
        it.setdefault("title", pathlib.Path(it["src"]).stem.split("：")[-1].split("_")[0])
        print(convert(it))
