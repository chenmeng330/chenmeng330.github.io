"""段落里的硬换行会被 markdown 变成空格，中文里就多出一个洞。把同段的行接起来。"""

import re
from pathlib import Path

ROOT = Path(r"C:\Workarea\qinxi-site\src\content\texts\works")
ASCII_TAIL = re.compile(r"[A-Za-z0-9]$")
ASCII_HEAD = re.compile(r"^[A-Za-z0-9]")


def join(buf: str, line: str) -> str:
    if not buf:
        return line
    if ASCII_TAIL.search(buf) and ASCII_HEAD.search(line):
        return buf + " " + line
    return buf + line


for name in ("shu.md", "wa.md"):
    p = ROOT / name
    lines = p.read_text(encoding="utf-8").split("\n")

    out, buf, merged, in_fm = [], "", 0, False
    fence = 0
    for ln in lines:
        s = ln.strip()
        if s == "---":
            fence += 1
            in_fm = fence < 2
            out.append(ln)
            continue
        if in_fm:
            out.append(ln)
            continue

        structured = (
            not s
            or s.startswith("#")
            or s.startswith(">")
            or s.startswith("- ")
            or s.startswith("* ")
            or s.startswith("![")
            or s.startswith("|")
        )
        if structured:
            if buf:
                out.append(buf)
                buf = ""
            out.append(ln)
        else:
            if buf:
                merged += 1
            buf = join(buf, s)

    if buf:
        out.append(buf)

    p.write_text("\n".join(out), encoding="utf-8")
    print(f"{name} 接回 {merged} 行")
