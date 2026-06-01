# solution-design

`solution-design` 是一个用于算法类、科研类和工程类技术方案设计的 Codex Skill。它不是通用写作模板，而是一个对话优先的方案设计工作流。

该 Skill 必须把足够的信息展示在对话里，让用户不用打开本地 Markdown 文件也能判断方案是否合适。本地文件只作为防遗忘锚点和最终写作依据。

Skill 内置 `assets/reference.docx` 作为默认 pandoc Word 模板。你可以直接用 Word 打开并调整这个文件，以控制标题、正文、表格、页边距和段落间距等最终样式。

## 适用场景

- 技术方案
- 算法方案
- 工程方案报告
- 科研项目方案框架
- 技术路线比较与选择
- Word 方案准备

## 不适用场景

- 直接开发算法代码
- 直接写仿真脚本
- 直接生成测试大纲
- 直接生成测试报告
- 编造测试结果
- 自动绘图
- 用户未明确要求时进行页面 PNG 级视觉 QA

## 工作流程

1. 介绍工作流：深度调研、给出候选方案、讨论方案、确定方案、讨论框架、确定框架、最终输出 Word。
2. 在对话中展示调研结论、候选技术路线、路线取舍、推荐初始方向和关键问题。
3. 在对话展示后，将前期信息保存到 `project_anchor.md` 作为记忆锚点。
4. 方案讨论阶段，每次回答结尾都总结最新整体技术路线和方案，并询问是否开始方案框架设计。
5. 用户同意开始框架设计后，先在对话中生成完整框架。
6. 在对话中持续修改框架，直到用户明确同意最新版框架。
7. 将用户确认后的框架保存到 `confirmed_framework.md`。
8. 用户要求生成最终 Word 方案时，生成 `solution_design.md` 并导出 Word。

## 输出文件

```text
{project_name}_solution_design/
|-- project_anchor.md
|-- confirmed_framework.md
|-- solution_design.md
`-- exports/
    `-- {project_name}_方案设计.docx
```

## Word 输出

Word 导出脚本会尽量应用以下规则：

- 未提供用户自定义 `--reference` 时，优先使用 `assets/reference.docx`
- 所有可见文字为黑色
- 各级标题使用宋体
- 所有表格单元格无底纹，包括表头
- 表格单元格内段落不使用正文首行缩进
- 用户未明确要求时，不做页面 PNG 级视觉渲染 QA

导出后需要在对话中报告：

- 最终 Word 路径
- Markdown 源文件路径
- 可获取时的页数
- 表格数量
- 图位数量
- 图位名称清单

## 安装

将 `solution-design/` 文件夹复制或同步到 Codex skills 目录，例如：

```text
~/.codex/skills/solution-design/
```

Skill 本体文件不应复制到每一个用户项目目录中。

## 运行依赖

从用户提出需求到生成 Markdown 方案源文件，本 Skill 不需要 Codex 之外的额外软件。

如果要运行 Skill 自带的辅助脚本，Codex 需要能访问一个 Python 3 解释器。该解释器可能以 `python`、`python3`、`py`，或运行环境提供的 Python 可执行文件形式存在。脚本只使用 Python 标准库，正常使用不需要安装 PyYAML、python-docx、pypandoc 或其他 Python 包。

如果没有 Python，工作流也不应中断。脚本只是便捷工具，不是硬性运行门槛：Codex 应直接创建或更新项目目录和 Markdown 文件，按 references 中的规则人工检查正文，并在最终 Markdown 源文件生成后直接运行 pandoc 导出 Word。

最终输出 Word 时，Markdown 转 Word 需要 pandoc。如果没有 pandoc，Skill 应保留已生成的 Markdown 源文件，并提示用户 Word 导出需要等 pandoc 安装后再执行。

## 触发示例

```text
写一个技术方案
帮我设计项目方案框架
我要生成一个 Word 方案
设计一个算法方案
准备一份工程技术方案
```

## 脚本用法

初始化方案项目：

```bash
python scripts/init_solution_project.py "项目名称" --lang zh
python scripts/init_solution_project.py "Project Name" --lang en
```

检查正式方案正文禁用语：

```bash
python scripts/check_formal_solution.py solution_design.md --lang zh
```

检查 Markdown 数学变量：

```bash
python scripts/check_markdown_math.py solution_design.md --lang zh
```

导出 Word：

```bash
python scripts/export_docx.py solution_design.md --project-name "项目名称" --lang zh
python scripts/export_docx.py solution_design.md --reference path/to/reference.docx --project-name "项目名称" --lang zh
```

第一条命令会在 `assets/reference.docx` 存在时自动使用该内置模板。

如果没有 Python 但已安装 pandoc，可直接运行：

```bash
pandoc solution_design.md -o exports/项目名称_方案设计.docx
```

Word 导出依赖 pandoc。Windows 可安装 `.msi`，macOS 可安装 `.pkg` 或使用 Homebrew，Linux 可使用系统包管理器。
