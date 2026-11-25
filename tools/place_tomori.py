"""把画压一压，放进 public 里。"""

from pathlib import Path

from PIL import Image

SRC = r"C:\Users\Qxiz\.dsh\attachments\v1\objects\0b\0bbbcdab1970795a3317ffb8867a5599869098d0de52ca0c5fa95584a7ca4903"
OUT = Path(r"C:\Workarea\qinxi-site\public\images\gallery\tomori-birthday.jpg")

OUT.parent.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGB")
print("原始", im.size)
if im.width > 1400:
    h = round(im.height * 1400 / im.width)
    im = im.resize((1400, h), Image.LANCZOS)
im.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
print("写入", OUT, OUT.stat().st_size // 1024, "KB", im.size)
