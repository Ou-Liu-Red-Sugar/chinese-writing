# 中文写作 · Chinese Writing

面向中文教材、技术说明、notebook 和研究报告的写作 skill。先安排思想，再建立段落与句群骨架；经过具体审读和修订，最后填充成稿。

现行版本 **2.12.1** 将[常用衔接表达](references/sentence-construction.md#常用衔接表达)整理为按关系选择的候选，包括“如果／假如／要是／若”等常见说法；替换同时照顾语义、搭配与语气，重复设定也可以通过重组句群处理。中间说明写实或骨架修订后，沿[标点方法](references/sentence-construction.md#7-标点与第1版的交付)重新核顿号、分号和句界，不把早期占位的停顿直接冻结成稿。

[句群重组方法](references/sentence-construction.md#从分句关系重组句群)继续从信息关系和前句留下的阅读期待出发，安排后句、句式和停顿，补足小词承担的情态、动作进展与语气，并通过整段连读把握[完整讲解与适度从容](references/sentence-construction.md#完整讲解与适度从容)。资料工作分为[取材与深挖](references/workflow.md#取材与深挖)：取材服务第0版和第1版草图，第1版正式交出并接收后，再按草图需要深挖原件、数据、条件和计算。

标题仍规定全篇主线，[开篇方法](references/openings.md)负责接题、点题与后文接续。早期把尚待深查的内容留作资料需求，不预写未经核实的结论；深挖发现材料不支持原安排时，修订草图。事实核验在最终定稿前完成。

全篇文气仍在第0版统筹：主体接住疑问、逐步推进，转进有材料与认识上的来由，末尾完成题意。详略、节奏和语气纳入同一安排；第1版再落实段落、衔接与标点。方法见[全篇次序](references/composition.md#3-全篇次序)与[选材详略](references/composition.md#2-选材与详略)。

早期草图保持阶段边界：第0版安排思想，第1版写定起句、衔接和标点，以具体语义占位安排中间内容；首次就写成的全文不能改称第1版草图，须先退回阶段任务。经过实际反馈形成的最终草图才可以没有空缺。具体见[阶段接收检查](references/workflow.md#阶段接收检查)。

两类审查按内容成熟度调用，专业意见处理后由文字角色最后定稿，包括解释层次和数字显示精度。文字首判先读稿件，保存意见后再看作者的安排理由，避免用作者意图补足正文缺口。阶段与分工见[专项检查](references/specialist-checks.md)。

篇章、句法与标点方法沿主要文献的集中研读结果：先安排读者依次理解什么，再用材料、次序和详略突出重要关系。连接词帮助读者把握关系、语气和推进节奏，即使省去仍能理解，也可以保留或补入使行文更自然的连接；普通连接词后不自动加逗号。真实阅读范围、来源局限和方法采用见 [文献记录](references/literature.md)。

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
| 后续草图 | 实际修订及两类原始反馈 | 文字角色先核语言组织；具体内容具备后，专业角色核实际主张与输入，未填内容不提前核算 |
| 最终骨架 | 文字定稿、验收与局部填充范围 | 专业意见处理后由文字角色决定最后措辞、详略和表达精度，Lead核结果，填充者不再作组织决定 |
| 成稿 | 正文与可查过程 | 补入局部文字并完成必要核对，由文字角色最后通读，交付实际草图和修订入口 |

修改次数由问题决定。多篇请求逐篇完成，同一篇内部可分工查资料或审读，前篇定稿后再启动下一篇草图；用户监督的单篇实验按指定阶段交回。完整文本复制成几个文件不能充当草图过程，算术正确、文件一致和高评分也不能替代中文审读。详细执行与阶段边界见 [workflow](references/workflow.md)。

## 方法与模板

| 需要做的事 | 入口 |
|---|---|
| 组织篇章、章节、材料及详略 | [编排与句法](references/composition.md) |
| 承接标题、选择入口、点题与扣题 | [开篇方法与示例](references/openings.md) |
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

[句子组织校准材料](assets/sentence-calibration.md)保留创作者的组句示范，以及 Blog 中漏写转折、解释跳步、过度前置对象和连接词后习惯停顿的失败片段，以及对过度省略连接词的纠偏。原话、历史改法和当前采用分析分别标明，便于对照。

## Benchmarks

[公开题库](assets/benchmark-cases.json)有 **18道题、54道理解题**，涵盖句序、主干与承担者、标点辖域、详略、数学推导、报告精简、证据身份、必要限定和参考结构。开篇题另覆盖独立进入、承接已有前文及报告读者，核点题、读者需要与后文接续，不将题目数量当作已运行成绩。

每题分为 `writer_packet` 与 `reviewer_key`：作者取得题目材料；文字首判取得稿件、读者先修与任务，不接收作者意图或答案；专业审查在内容具备后取得判别依据；独立读者只取得成稿、先修与问题。流程遵守、文本质量、读者任务表现和用户认可分别记录。已公开或已见的材料不称为未见测试；仓库没有发布跨模型排名或经过统计验证的通过阈值。使用方式见[校准方法](references/benchmarks.md)和[结果模板](assets/benchmark-report.md)。

## 验证与贡献

只需 Python 3.10 或更高版本，无第三方依赖：

```sh
python tools/validate.py
```

检查覆盖 skill 元数据、本地链接、题库结构和可能误带的本机路径/凭证形态；它不判断文章是否写得好。GitHub Actions 在推送和 pull request 时运行同一检查。修改方法或增加案例时，保留可重建的具体依据和真实测试身份，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 授权

原创 skill、方法、模板、题库与工具采用 [MIT License](LICENSE)。外部文献链接及第三方内容保留其原有权利；`examples/independence-correlation/` 的课程改编示例按 CC BY-NC-SA 4.0 单独标注，详见 [第三方与示例说明](THIRD_PARTY_NOTICES.md)。仓库不附带第三方书籍、论文全文或模型服务。
