"""把「原创短篇」这个分区名改成「“她”的写作」。"""

from pathlib import Path

ROOT = Path(r"C:\Workarea\qinxi-site\src")
OLD = "原创短篇"
NEW = "“她”的写作"

changed = []

for p in (ROOT / "content" / "texts" / "works").glob("*.md"):
    t = p.read_text(encoding="utf-8")
    if f'category: "{OLD}"' not in t:
        continue
    # YAML 用单引号包住，里面的双引号就不用转义
    t = t.replace(f'category: "{OLD}"', f"category: '{NEW}'")
    p.write_text(t, encoding="utf-8")
    changed.append(p.name)

astro = ROOT / "pages" / "works" / "index.astro"
t = astro.read_text(encoding="utf-8")
if OLD in t:
    astro.write_text(t.replace(OLD, NEW), encoding="utf-8")
    changed.append("works/index.astro")

print("改了", len(changed), "处")
for c in changed:
    print(" ", c)
