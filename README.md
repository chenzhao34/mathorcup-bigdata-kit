# MathorCup 大数据竞赛工具包

面向 **2026 MathorCup 数学应用挑战赛——大数据竞赛** 的论文模板与语料采集工具。

## 为什么要单独做一套

竞赛主办方有两条不同的赛道产品：

| | 常规赛（春季） | 大数据竞赛 |
|---|---|---|
| 首页 | 编号 + 题号 | 编号 + **赛道 A/B** + 题目 |
| 目录 | 不出目录 | **有目录页** |
| 页边距 | 四周 2.5 cm | 上下 **2.0**、左右 **2.5** cm |

多数开源模板（包括常见的 `MathorCupmodeling.cls`）是常规赛版式，直接用于大数据赛会缺封面赛道、缺目录、页边距不符。

## 内容

```
templates/mathorcup_bigdata/
├── MathorCupBigData.cls      LaTeX 文档类（封面 + 摘要 + 目录 + 页脚页码）
├── main.tex                  正文骨架（八章 + 参考文献 + 附录）
└── 论文模板_空白.docx          Word 骨架（封面/摘要/目录域/章节占位）
tools/
├── make_docx.py              生成 .docx 骨架，可传编号/赛道/题目
└── crawl_mathorcup.py        赛题与附件采集脚本
corpus/
├── 语料清单.md                历届赛题获取情况与缺口
├── manifest.json             官方文件 URL 与本地路径映射
└── 赛题画像示例.md            题型/数据规模/交付物抽取示例
```

## 使用

### LaTeX

```bash
cd templates/mathorcup_bigdata
xelatex main.tex && xelatex main.tex
```

需 TeX Live / MiKTeX，含 `ctex`、`fandol` 或系统宋体/黑体。
填三处：`\bianhao{}`、`\saidao{}`、`\timu{}`。

### Word

```bash
python tools/make_docx.py 论文.docx "MCB260001" "B" "基于××的××预测"
```

生成后在 Word/WPS 里右键目录 → 更新域。

### 采集历年赛题

```bash
python tools/crawl_mathorcup.py
```

脚本从官网公告页与赛氪 CDN 抓取原始压缩包，支持断点续传（CDN 会在中途断流）。
产物不入库，`.gitignore` 已排除 `raw/`、`extracted/`。

## 关于接入 Agent

本仓库的模板是**独立文件**，可直接用于 LaTeX/Word 写作。

若要注入 Modex 一类的桌面 Agent，需要注意：其竞赛技能包为加密胶囊，模板在运行时才落盘到工作区 `_templates/`，**无法通过往安装目录丢文件生效**。可行路径：

1. 等运行时把 `_templates/` 展开后，用同名目录覆盖 `mathorcup/`；
2. 或向厂商提需求，开放自定义技能目录。

## 数据与版权

本仓库**不包含**任何官方赛题、附件数据或获奖论文，仅包含抓取脚本与目录结构说明。
赛题版权归 MathorCup 组委会所有，请仅作学习研究使用，不要二次分发。

获奖论文未被官方公开发布，因此不提供；如需参考，请通过官方答辩材料、本校获奖队伍或作者本人授权的渠道获取。

## License

代码与模板：MIT
