"""把 kind 迁到新栏目，随笔补上 channel。"""

import re
from pathlib import Path

ROOT = Path(r"C:\Workarea\qinxi-site\src\content\texts")

for p in sorted(ROOT.rglob("*.md")):
    t = p.read_text(encoding="utf-8")
    old = t
    t = re.sub(r"^kind: fiction$", "kind: work", t, flags=re.M)
    t = re.sub(r"^kind: longform$", "kind: work", t, flags=re.M)
    if re.search(r"^kind: essay$", t, flags=re.M) and "channel:" not in t:
        t = re.sub(
            r"^kind: essay$",
            'kind: essay\nchannel: "秦羲"',
            t,
            flags=re.M,
        )
    if t != old:
        p.write_text(t, encoding="utf-8")
        print("改了", p.relative_to(ROOT))
