# -*- coding: utf-8 -*-
"""压缩配图并复制到 public/images/qin-hesheng/。"""
import os
from PIL import Image

SRC_DIR = r"C:\Workarea\秦河胜配图"
SRC_EXTRA = r"C:\Workarea"
OUT_DIR = r"C:\Workarea\qinxi-site\public\images\qin-hesheng"

JPG_MAP = [
    ("01_koryuji_romon.jpg", "01-koryuji-romon.jpg"),
    ("02_miroku.jpg", "02-miroku.jpg"),
    ("03_matsunoo.jpg", "03-matsunoo.jpg"),
    ("04_osake.jpg", "04-osake.jpg"),
    ("05_yumedono.jpg", "05-yumedono.jpg"),
    ("06_madarajin.jpg", "06-madarajin.jpg"),
    ("07_okina.jpg", "07-okina.jpg"),
    ("08_kawakatsu.jpg", "08-kawakatsu.jpg"),
]
PNG_MAP = [
    ("秦河胜_时间轴.png", "timeline.png"),
    ("秦氏谱系图.png", "genealogy.png"),
]

MAX_W = 1500
os.makedirs(OUT_DIR, exist_ok=True)


def compress(src, dst, max_w=MAX_W, quality=84):
    im = Image.open(src)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    w, h = im.size
    if w > max_w:
        im = im.resize((max_w, round(h * max_w / w)), Image.LANCZOS)
    if dst.lower().endswith(".png"):
        im.save(dst, "PNG", optimize=True)
    else:
        im.save(dst, "JPEG", quality=quality, progressive=True, optimize=True)
    print(f"{os.path.basename(src)} {w}x{h} -> {os.path.basename(dst)} {im.size[0]}x{im.size[1]} {os.path.getsize(dst)//1024}KB")


for src_name, dst_name in JPG_MAP:
    compress(os.path.join(SRC_DIR, src_name), os.path.join(OUT_DIR, dst_name))

for src_name, dst_name in PNG_MAP:
    compress(os.path.join(SRC_EXTRA, src_name), os.path.join(OUT_DIR, dst_name), max_w=1800)
