%% MathorCupBigData.cls
%% 2026 MathorCup 数学应用挑战赛——大数据竞赛 论文模板（LaTeX 变体）
%% 依据官方 Word 模板还原：独立封面（编号/赛道/题目）+ 摘要页 + 目录页 + 正文
%% 需求：xelatex 编译，需 ctex 宏包
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{MathorCupBigData}[2026/10/22 v1.0 MathorCup BigData Competition]

\LoadClass[oneside,a4paper,UTF8,linespread=1.25,zihao=-4]{ctexart}

%% ---------- 版式：上下 2.0cm，左右 2.5cm（官方 Word 模板口径） ----------
\RequirePackage[top=2.0cm,bottom=2.0cm,left=2.5cm,right=2.5cm,headheight=0pt]{geometry}

%% ---------- 标题层级：一级四号黑体居中 + 中文数字；二级小四黑体 ----------
\ctexset{
  section={
    format={\zihao{4}\heiti\centering},
    name={,、},
    number=\chinese{section},
    beforeskip=14pt, afterskip=10pt,
  },
  subsection={
    format={\zihao{-4}\heiti\raggedright},
    number={\arabic{section}.\arabic{subsection}},
    beforeskip=10pt, afterskip=6pt,
  },
  subsubsection={
    format={\zihao{-4}\heiti\raggedright},
    number={\arabic{section}.\arabic{subsection}.\arabic{subsubsection}},
  },
}

\setmainfont{Times New Roman}
\setlength{\parindent}{2em}

%% ---------- 页脚：第 X 页 共 Y 页 ----------
\RequirePackage{fancyhdr,lastpage}
\pagestyle{fancy}
\fancyhf{}
\renewcommand\headrulewidth{0pt}
\fancyfoot[C]{第 \thepage{} 页~~共 \pageref{LastPage} 页}

%% ---------- 目录样式：14pt 居中标题，三级，点线 ----------
\RequirePackage{titletoc}
\renewcommand{\contentsname}{\zihao{3}\heiti 目\quad 录}
\titlecontents{section}[0pt]{\addvspace{4pt}\heiti\zihao{-4}}
  {\thecontentslabel\quad}{}{\titlerule*[0.6pc]{.}\contentspage}
\titlecontents{subsection}[1.5em]{\addvspace{2pt}\zihao{-4}}
  {\thecontentslabel\quad}{}{\titlerule*[0.6pc]{.}\contentspage}
\titlecontents{subsubsection}[3em]{\addvspace{1pt}\zihao{-4}}
  {\thecontentslabel\quad}{}{\titlerule*[0.6pc]{.}\contentspage}

%% ---------- 竞赛信息变量 ----------
\def\bianhao#1{\gdef\@bianhao{#1}}
\def\saidao#1{\gdef\@saidao{#1}}      % 赛道 A / B
\def\timu#1{\gdef\@timu{#1}}
\def\keyword#1{\gdef\@keyword{#1}}
\def\@bianhao{\textbf{[队伍编号]}}
\def\@saidao{A}
\def\@timu{[论文题目]}
\def\@keyword{[关键词]}

%% ---------- 封面：编号 / 赛道 / 论文题目 ----------
\newcommand{\makecover}{%
  \begin{titlepage}
    \centering
    \vspace*{2.5cm}
    {\zihao{3}\heiti 2026 年 MathorCup 数学应用挑战赛}\\[6pt]
    {\zihao{3}\heiti ——大数据竞赛}\\[2.2cm]

    {\zihao{4}\heiti 队伍编号}\\[6pt]
    {\zihao{3}\@bianhao}\\[1.2cm]

    {\zihao{4}\heiti 赛道}\\[6pt]
    {\zihao{3}\@saidao}\\[1.8cm]

    {\zihao{4}\heiti 论文题目}\\[8pt]
    {\zihao{3}\heiti \@timu}
    \vfill
  \end{titlepage}%
}

%% ---------- 摘要环境：题目 + 摘要 + 关键词，独立一页 ----------
\renewenvironment{abstract}{%
  \clearpage
  \begin{center}
    {\zihao{4}\heiti \@timu}\\[14pt]
    {\zihao{4}\heiti 摘\quad 要}
  \end{center}\par
  \vspace{6pt}%
}{%
  \par\vspace{12pt}%
  \noindent{\heiti 关键词：}\@keyword
  \clearpage
}

%% ---------- 参考文献 ----------
\renewcommand{\refname}{\zihao{4}\heiti 参考文献}

%% ---------- 浮动体宽松度 ----------
\renewcommand*{\textfraction}{0.05}
\renewcommand*{\topfraction}{0.9}
\renewcommand*{\bottomfraction}{0.8}
\renewcommand*{\floatpagefraction}{0.85}

\endinput
