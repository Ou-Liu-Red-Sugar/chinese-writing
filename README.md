# 中文写作 · Chinese Writing

面向中文教材、技术说明、notebook 和研究报告的写作 skill。先安排思想，再建立段落与句群骨架；经过具体审读和修订，最后填充成稿。

现行版本 **2.6.0** 将主要参考文献的集中研读结果纳入方法：先安排读者依次理解什么，再用材料、次序和详略突出重要关系，并在草图中写定主干、语序与标点。连接词在需要说明关系时使用，内容已经接得上就直接往下写；普通连接词后不自动加逗号。真实阅读范围、来源局限和方法采用见 [文献记录](references/literature.md)。

## 开始使用

在支持本地 skills 的 Codex 中，将本仓库放到 skills 目录下的 `chinese-writing` 文件夹，然后调用：

```text
使用 $chinese-writing，写一篇面向已有基本概率知识读者的中文词条。
先保存第0版思想安排，再形成第1版段落与句群骨架；
按专项反馈修订后生成正文，并保留实际草图、审读和修改入口。
```

macOS / Linux：

```sh
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_dir"
git clone https://github.com/Ou-Liu-Red-Sugar/chinese-writing.git "$skills_dir/chinese-writing"
```

Windows PowerShell：

```powershell
$skillsDirectory = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME 'skills'
} else {
    Join-Path $env:USERPROFILE '.codex/skills'
}
New-Item -ItemType Directory -Path $skillsDirectory -Force | Out-Null
git clone https://github.com/Ou-Liu-Red-Sugar/chinese-writing.git (Join-Path $skillsDirectory 'chinese-writing')
```

目标目录已经存在时，先保存原有修改，再按自己的安装方式更新。`git clone` 不会覆盖现有目录。其他写作助手也可以直接读取 [SKILL.md](SKILL.md) 和所需参考文件；本仓库不包含模型服务或 Chat 连接程序。

## 写作流程

| 阶段 | 实际产物 | 本阶段的工作 |
|---|---|---|
| 第0版 | 思想图、表格或文字安排 | 说明要建立哪些认识，以及用什么材料、实例或推导体现 |
| 第1版 | 段落与句群骨架 | 使用章节、详略和句子组成方法，写定承接对象、必要解释、实际衔接与标点；中间内容暂留明确占位 |
| 后续草图 | 实际修订及原始反馈 | 分别检查篇章内容、段落衔接、句子与标点、必要限定，修正骨架 |
| 最终骨架 | 验收稿与局部填充范围 | 确定结构、句序、关键措辞、标点和内容位置，填充者不再作组织决定 |
| 成稿 | 正文与可查过程 | 补入局部文字，核对内容及固定部分，交付实际草图和修订入口 |

修改次数由问题决定。完整文本复制成几个文件不能充当草图过程，算术正确、文件一致和高评分也不能替代中文审读。详细执行与阶段边界见 [workflow](references/workflow.md)。

## 方法与模板

| 需要做的事 | 入口 |
|---|---|
| 组织篇章、章节、材料及详略 | [编排与句法](references/composition.md) |
| 组织主干、语序、复句及实际停顿 | [句子组成](references/sentence-construction.md) |
| 在第1版调用方法，并安排后续专项 | [方法调用与专项检查](references/specialist-checks.md) |
| 删去防御性表态，保留必要条件 | [限定与防御性措辞](references/qualification.md) |
| 写精简研究报告 | [报告模板](assets/concise-report.md) |
| 保存真实草图与修改 | [分阶段草图工作页](assets/article-sketch.md) |
| 让 Chat 或其他 Agent 协助 | [协作方式](references/chat-collaboration.md)、[交接模板](assets/chat-handoff.md) |
| 查看默认表达偏好 | [写作原则](docs/style-guide.md) |
| 核查方法的文献来源 | [文献与采用范围](references/literature.md) |

文体按任务选择：教材展开定义、实例和推导；研究报告把结果、依据与影响采用的条件直接相接；参考记录服务查询。用户和所在项目的明确要求优先。

## 示例

[独立性与不相关](examples/independence-correlation/article.md)展示一次实际写作过程，包括思想安排、段落骨架、专项原始反馈、修订和最终填充。阅读入口及文件对应见[示例说明](examples/independence-correlation/README.md)。该数学教学示例引用并改编了外部课程材料，目录内单独标明授权。

[句子组织校准材料](assets/sentence-calibration.md)保留创作者的组句示范，以及 Blog 中漏写转折、解释跳步、过度前置对象和连接词后习惯停顿的失败片段。原话、历史改法和当前采用分析分别标明，便于对照。

## Benchmarks

[公开题库](assets/benchmark-cases.json)有 **15道题、45道理解题**，涵盖句序、主干与承担者、标点辖域、详略、数学推导、报告精简、证据身份、必要限定和参考结构。既检查缺少解释，也检查为求通顺补造理由；局部改句题另核主动表达、合理被动、连接词连读及必要的逗号边界。

每题分为 `writer_packet` 与 `reviewer_key`：作者只取得题目材料，审读者在交稿后取得判别依据，独立读者只取得成稿与问题。流程遵守、文本质量、读者任务表现和用户认可分别记录。已公开或已见的材料不称为未见测试；仓库没有发布跨模型排名或经过统计验证的通过阈值。使用方式见[校准方法](references/benchmarks.md)和[结果模板](assets/benchmark-report.md)。

## 验证与贡献

只需 Python 3.10 或更高版本，无第三方依赖：

```sh
python tools/validate.py
```

检查覆盖 skill 元数据、本地链接、题库结构和可能误带的本机路径/凭证形态；它不判断文章是否写得好。GitHub Actions 在推送和 pull request 时运行同一检查。修改方法或增加案例时，保留可重建的具体依据和真实测试身份，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 授权

原创 skill、方法、模板、题库与工具采用 [MIT License](LICENSE)。外部文献链接及第三方内容保留其原有权利；`examples/independence-correlation/` 的课程改编示例按 CC BY-NC-SA 4.0 单独标注，详见 [第三方与示例说明](THIRD_PARTY_NOTICES.md)。仓库不附带第三方书籍、论文全文或模型服务。
