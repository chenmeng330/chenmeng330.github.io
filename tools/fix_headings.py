"""把两篇用 # 当章节标题的文章改成 ##，顺手清掉全角空格占的空行。"""

from pathlib import Path

ROOT = Path(r"C:\Workarea\qinxi-site\src\content\texts\works")

for name in ("shu.md", "wa.md"):
    p = ROOT / name
    lines = p.read_text(encoding="utf-8").split("\n")
    out, heads, blanks = [], 0, 0
    for ln in lines:
        if ln.startswith("# "):
            ln = "## " + ln[2:]
            heads += 1
        elif ln.strip() == "" and ln != "":
            # 只有全角空格的行，markdown 不认它是空行，只会把上下段粘在一起
            ln = ""
            blanks += 1
        out.append(ln)
    p.write_text("\n".join(out), encoding="utf-8")
    print(f"{name} 标题 {heads} 个，清掉全角空行 {blanks} 个")
