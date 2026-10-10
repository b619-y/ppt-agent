#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_bar_chart.py —— 用原文表格数据重绘“柱状图 + 红色虚线阈值线”的通用脚本

用法：
    python3 make_bar_chart.py bar_example.json

配置文件（JSON）字段说明见 bar_example.json 与《风格规范.md》第 5 节。
所有相对路径都相对于配置文件所在目录。

风格（与本项目统一规范一致）：
  - 白底；去掉上、右边框；浅灰横向网格线 #E6E6E6
  - 超过阈值的柱子橙红 #E4572E，未超过的灰蓝 #8497B0（higher_is_bad=false 时反过来）
  - 柱顶标数值（13pt 常规字重，#222222）
  - 阈值线：红色 #D00000 虚线，线宽 1.8；配红色箭头 + 文字“达标线 20 µg/L”
  - 轴标题 14pt，纵轴刻度 12pt，横轴类别 11pt（类别名长时自动 30° 斜放）
  - 输出 300 dpi PNG；figsize 用“幻灯片上的实际英寸尺寸”，这样字号 = 幻灯片上的磅值
所有新写文字统一使用微软雅黑；所有文字为常规字重。
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

EXCEED = "#E4572E"   # 超标：橙红
OK = "#8497B0"       # 达标：灰蓝
LINE_RED = "#D00000"  # 阈值线与标注
GRID = "#E6E6E6"
TEXT = "#222222"

def setup_font():
    names = {f.name for f in fm.fontManager.ttflist}
    required = {"Microsoft YaHei"}
    missing = sorted(required - names)
    if missing:
        sys.exit("缺少指定字体：%s。请安装字体后重试。" % ", ".join(missing))
    plt.rcParams["font.family"] = ["Microsoft YaHei"]
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["axes.unicode_minus"] = False
    return "所有新写文字：Microsoft YaHei"


def main(cfg_path):
    base = os.path.dirname(os.path.abspath(cfg_path))
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    font = setup_font()

    items = cfg["data"]               # [{"name":..., "value":数值, "label":可选显示文字}, ...]
    if not items:
        sys.exit("请先填入从原文表格核实的数据；不要按图估读或编造数值。")
    names = [d["name"] for d in items]
    vals = [float(d["value"]) for d in items]
    labels = [d.get("label", ("%g" % float(d["value"]))) for d in items]
    thr = cfg.get("threshold")        # 阈值，可为 null（不画线）
    bad_high = cfg.get("higher_is_bad", True)
    W, H = cfg.get("size_in", [5.31, 4.08])   # 幻灯片上的实际尺寸（英寸）
    fs = cfg.get("font_sizes", {})
    fs_val, fs_axis = fs.get("value", 13), fs.get("axis_title", 14)
    fs_ytick, fs_xtick, fs_leg = fs.get("ytick", 12), fs.get("xtick", 11), fs.get("legend", 11)

    fig, ax = plt.subplots(figsize=(W, H), dpi=300)

    def is_exceed(v):
        if thr is None:
            return True
        return v > thr if bad_high else v < thr
    colors = [EXCEED if is_exceed(v) else OK for v in vals]
    bars = ax.bar(range(len(vals)), vals, color=colors, width=cfg.get("bar_width", 0.62), zorder=3)

    ymax = cfg.get("ylim_max") or max(vals) * 1.28
    ax.set_ylim(0, ymax)
    off = ymax * 0.0115
    for b, v, lab in zip(bars, vals, labels):
        low = (thr is not None) and v <= thr
        ax.text(b.get_x() + b.get_width() / 2, v + off, lab, ha="center", va="bottom",
                fontsize=fs_val, fontweight="normal", color=TEXT, zorder=6,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=0.9) if low else None)

    if thr is not None:
        ax.axhline(thr, color=LINE_RED, ls="--", lw=1.8, zorder=4)
        tl = cfg.get("threshold_label", {})
        text = tl.get("text", "达标线 %g" % thr)
        # 默认放在最后两根柱子之间的空隙，文字在 30% 高度处，用箭头指向阈值线
        x = tl.get("x", len(vals) - 1.5)
        y = tl.get("y", ymax * 0.307)
        ax.annotate(text, xy=(x, thr), xytext=(x, y), color=LINE_RED, fontsize=fs_val,
                    fontweight="normal", ha="center", va="bottom", zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=LINE_RED, lw=1.4, shrinkA=2, shrinkB=1))

    ax.set_xticks(range(len(vals)))
    rot = cfg.get("xtick_rotation", 30 if max(len(n) for n in names) > 5 else 0)
    ax.set_xticklabels(names, fontsize=fs_xtick, rotation=rot,
                       ha="right" if rot else "center", rotation_mode="anchor")
    ax.tick_params(axis="y", labelsize=fs_ytick)
    ax.set_xlim(-0.6, len(vals) - 0.4)
    ax.set_ylabel(cfg.get("ylabel", ""), fontsize=fs_axis)
    ax.set_xlabel(cfg.get("xlabel", ""), fontsize=fs_axis, labelpad=2)
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    leg = cfg.get("legend")  # {"exceed": "超标（>20 µg/L）", "ok": "达标（≤20 µg/L）", "loc": "upper right"}
    if leg:
        ax.legend(handles=[Patch(color=EXCEED, label=leg["exceed"]), Patch(color=OK, label=leg["ok"])],
                  fontsize=fs_leg, frameon=False, loc=leg.get("loc", "upper right"),
                  bbox_to_anchor=tuple(leg.get("anchor", [1.03, 1.03])), handlelength=1.2, handletextpad=0.4)

    fig.tight_layout(pad=0.4)
    out = os.path.join(base, cfg.get("output", "bar_chart.png"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=300, facecolor="white")
    print("已生成：%s（字体：%s，%.2f×%.2f in @300dpi）" % (out, font, W, H))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("用法：python3 make_bar_chart.py <配置.json>")
    main(sys.argv[1])
