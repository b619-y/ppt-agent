# PPT Agent

一个面向科研汇报的 Codex 项目技能包，保留本地 PPT 智能体的结论页流程、证据追溯规范和生成模板。历史论文、个人参考文件和过往成品不包含在这个仓库中。

## 在网页 Codex 中使用

1. 将此 GitHub 仓库连接到网页 Codex。
2. 在任务中调用 `$ppt-agent`，或直接说明要按仓库里的 PPT 流程制作。项目级规则由 `AGENTS.md` 提供。
3. 上传论文／报告，或将文件放到 `input/`。先确定汇报主线与每页证据，再制作一页样稿供确认。
4. 最终文件放在 `output/<主题>/`，包括 PPTX、逐页预览、图片来源记录、配置和用到的图像素材。

## 风格流程

- 16:9 白底；标题直接写结论，标题下用红色横条。
- 每页通常写 2–3 条简短要点，关键短语标红；按证据安排 2–3 张图。
- 图下用蓝色中文图注和黑色括号来源，右下角放灰色页码。
- 所有新写文字（中文、英文和数字）统一微软雅黑。
- 优先从原始论文或官方报告提取证据。数字必须能追溯到原文，不估读、不编造。裁图记录文档、年份、图号、PDF 页码和印刷页码；重绘图逐项记录数据出处。
- 使用 [`风格规范.md`](风格规范.md) 了解完整版式、引用和自检要求。

## 模板与环境

```bash
pip install -r requirements.txt
python3 模板/crop_pdf_figure.py input/paper.pdf 12 --grid
python3 模板/crop_pdf_figure.py input/paper.pdf 12 --box 0.1 0.2 0.9 0.7 --dpi 300 -o input/figure.png
python3 模板/make_bar_chart.py 模板/bar_template.json
python3 模板/make_slide.py 模板/slide_template.json --preview
```

执行前先把模板 JSON 里的示例文案、图片路径、图表数据和来源改为本项目内容。PDF 裁剪需要 Poppler（`pdftoppm`）；PPTX 转 PDF 预览需要 LibreOffice。所有新文字指定微软雅黑；为获得一致的图表预览，运行环境需安装 Microsoft YaHei。

`input/` 和 `output/` 的文件默认被 Git 忽略，避免论文、数据和成品被误传到仓库。
