#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crop_pdf_figure.py —— 从论文/报告 PDF 高清重渲染某一页，并只裁出“图体”（去掉原图题和正文）

第 1 步：先出带网格的缩略图，确定裁剪范围（网格线按页面宽/高的 5% 画，标注百分比）
    python3 crop_pdf_figure.py 论文.pdf 33 --grid
    → 生成 论文_p33_grid.png，用眼睛看图体大约在页面的哪个百分比范围

第 2 步：按比例裁剪（left top right bottom，均为 0–1 的页面比例），默认 300 dpi
    python3 crop_pdf_figure.py 论文.pdf 33 --box 0.11 0.227 0.95 0.591 --dpi 300 -o 右图_xxx_p33.png

说明：
  - 页码是 PDF 的物理页码（从 1 开始），不是印刷页码；记录来源时两者都写。
  - 原 PDF 里如果是低分辨率位图，提高 dpi 也不会更清楚（只会更大）。
  - 裁完务必打开 PNG 检查：不要留下原图题（Figure X...）和正文文字。
依赖：poppler（pdftoppm）、Pillow。
"""
import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def render(pdf, page, dpi):
    tmp = tempfile.mkdtemp()
    stem = os.path.join(tmp, "p")
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi), "-png",
                    "-singlefile", pdf, stem], check=True)
    return Image.open(stem + ".png").convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("page", type=int)
    ap.add_argument("--grid", action="store_true", help="输出带 5% 网格的缩略图")
    ap.add_argument("--box", type=float, nargs=4, metavar=("L", "T", "R", "B"), help="裁剪框（页面比例 0–1）")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("-o", "--output")
    a = ap.parse_args()
    stem = os.path.splitext(os.path.basename(a.pdf))[0]
    if a.grid:
        im = render(a.pdf, a.page, 100)
        d = ImageDraw.Draw(im); w, h = im.size
        for k in range(1, 20):
            c = (255, 0, 0) if k % 2 == 0 else (255, 170, 170)
            d.line([(w * k / 20, 0), (w * k / 20, h)], fill=c, width=1)
            d.line([(0, h * k / 20), (w, h * k / 20)], fill=c, width=1)
            if k % 2 == 0:
                d.text((w * k / 20 + 2, 2), "%d%%" % (k * 5), fill=(200, 0, 0))
                d.text((2, h * k / 20 + 2), "%d%%" % (k * 5), fill=(200, 0, 0))
        out = a.output or "%s_p%d_grid.png" % (stem, a.page)
        im.save(out); print("网格缩略图：%s" % out); return
    if not a.box:
        sys.exit("请指定 --grid 或 --box L T R B")
    im = render(a.pdf, a.page, a.dpi)
    w, h = im.size
    L, T, R, B = a.box
    crop = im.crop((int(L * w), int(T * h), int(R * w), int(B * h)))
    out = a.output or "%s_p%d_crop_%ddpi.png" % (stem, a.page, a.dpi)
    crop.save(out)
    print("已裁剪：%s（%d×%d px，%d dpi）" % (out, crop.width, crop.height, a.dpi))


if __name__ == "__main__":
    main()
