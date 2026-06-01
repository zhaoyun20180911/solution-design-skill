# solution-design

`solution-design` 是一个用于算法类、科研类和工程类技术方案设计的 Codex Skill。它不是通用写作模板，而是一个讨论迭代式方案设计工作流。

该 Skill 帮助用户从初始主题出发，逐步完成项目画像、调研资料包、技术路线确认、方案框架冻结、正式 Markdown 方案正文和 Word 导出。

## 适用场景

- 技术方案
- 算法方案
- 工程方案报告
- 科研项目方案框架
- 技术路线比较与选择
- Markdown 初稿确认后的 Word 方案准备

## 不适用场景

- 直接开发算法代码
- 直接写仿真脚本
- 直接生成测试大纲
- 直接生成测试报告
- 编造测试结果
- 自动绘图
- 复杂 docx 版式检查

## 工作流程

1. 检测用户语言并输出对应启动说明。
2. 创建项目画像。
3. 创建调研资料包，整理候选路线和学习资料。
4. 请用户确认技术路线。
5. 创建方案框架和技术框架。
6. 请用户确认方案框架。
7. 创建正式方案 Markdown 源文件。
8. 运行正式方案禁用语检查和 Markdown 数学变量检查。
9. 请用户确认 Markdown 初稿。
10. 使用 pandoc 导出 Word，并明确提示最终 Word 路径。

## 输出模式

默认使用 full mode，因为方案设计需要保留调研、框架和用户确认过程。

```text
{project_name}_solution_design/
├── project_profile.md
├── project_research_pack.md
├── solution_outline.md
├── solution_design.md
├── change_log.md
└── exports/
    └── {project_name}_方案设计.docx
```

如果用户明确表示“只要 Word”“不要中间文件”“最终只输出 docx”，使用 clean mode：

```text
{project_name}_solution_design/
├── exports/
└── .solution-design/
    ├── project_profile.md
    ├── project_research_pack.md
    ├── solution_outline.md
    ├── solution_design.md
    └── change_log.md
```

clean mode 下中间文件仍然保留，只是放入隐藏目录 `.solution-design/`。

## 安装

将 `solution-design/` 文件夹复制或同步到 Codex skills 目录，例如：

```text
~/.codex/skills/solution-design/
```

Skill 本体文件不应复制到每个用户项目目录中。

## 运行依赖

从用户提出需求到确认 Markdown 方案正文，本 Skill 不需要 Codex 之外的额外软件。

如果要运行 Skill 自带的辅助脚本，Codex 需要能访问一个 Python 3 解释器。该解释器可能以 `python`、`python3`、`py`，或运行环境提供的 Python 可执行文件形式存在。脚本只使用 Python standard library（Python 标准库），正常使用不需要安装 PyYAML、python-docx、pypandoc 或其他 Python 包。

如果没有 Python，工作流也不应中断。脚本只是便捷工具，不是硬性运行门槛：Codex 应直接创建或更新项目目录和 Markdown 文件，按 references 中的规则人工检查正文，并在 Markdown 初稿确认后直接运行 pandoc 导出 Word。

最终输出 Word 时，Markdown 转 Word 需要 pandoc。如果没有 pandoc，Skill 应保留已确认的 Markdown 源文件，并提示用户 Word 导出需要等 pandoc 安装后再执行。

## 触发示例

```text
做一个关于某工程系统的方案
写一个某算法模块的技术方案
写一个某科研项目的方案框架
帮我设计某项目的方案框架
我要做一个 XXX 的 Word 方案
```

## 脚本用法

初始化方案项目：

```bash
python scripts/init_solution_project.py "项目名称" --mode full --lang zh
python scripts/init_solution_project.py "Project Name" --mode clean --lang en
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

如果没有 Python 但已安装 pandoc，可直接运行 pandoc 导出：

```bash
pandoc solution_design.md -o exports/项目名称_方案设计.docx
```

Word 导出依赖 pandoc。Windows 可安装 `.msi`，macOS 可安装 `.pkg` 或使用 Homebrew，Linux 可使用系统包管理器。

## 文件生成反馈机制

每次生成或更新关键文件时，必须告知用户：

- 文件名
- 文件路径
- 文件作用
- 是否为最终交付物
- 下一步如何使用

生成 Word 后必须单独、醒目地输出：

```text
最终 Word 文件位置：{project_dir}/exports/{project_name}_方案设计.docx
```
