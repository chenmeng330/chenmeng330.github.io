"""把日记 txt 转成网站的 markdown。首行当标题，其余当正文。"""

import re
from pathlib import Path

DIARY = Path(r"C:\OurWork\diary")
OUT = Path(r"C:\Workarea\qinxi-site\src\content\texts\essay")

DATES = [
    "2026-11-17",
    "2026-11-18",
    "2026-11-19",
    "2026-11-21",
    "2026-11-23",
    "2026-11-24",
]

for d in DATES:
    src = DIARY / f"{d}.txt"
    if not src.exists():
        print(f"跳过 {src} 不存在")
        continue
    text = src.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    lines = text.split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    out = OUT / f"diary-{d}.md"
    text_out = (
        "---\n"
        f'title: "{title}"\n'
        f'slug: "diary-{d}"\n'
        "kind: essay\n"
        f"date: {d}\n"
        "---\n\n"
        f"{body}\n"
    )
    out.write_text(text_out, encoding="utf-8")
    print(f"{out.name} <- {len(body)} 字")
