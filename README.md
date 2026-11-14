# 自主实习工程管理仓库 | Independent Internship Engineering Repository

本仓库记录 2026 年暑期在中国科学院近代物理研究所高功率束流室开展的生产实习，包括工程继承、热工仿真、数据验证、实验记录、文献材料与最终交付。

This repository documents the 2026 summer production internship in the High-Power Beam Hall of the Institute of Modern Physics, Chinese Academy of Sciences. It covers engineering handover, thermal simulation, data validation, experimental records, literature, and final deliverables.

> **状态：2026-08-29，现场实习已结束，仓库进入成果整理与工程交接状态。**
>
> **Status: As of 2026-08-29, the on-site internship has ended. The repository is now in the results consolidation and engineering handover phase.**

## 项目主线与职责边界 | Project Workflow and Responsibility Boundaries

本项目属于协作型科研工程。上游 FLUKA 粒子输运计算由团队其他成员负责，本人在其结果基础上重点承担数据接口、Fluent 热工链继承与验证、CAD / Fluent Meshing 排障，以及部分热物性实验。

This is a collaborative research-engineering project. Other team members were responsible for the upstream FLUKA particle-transport calculations. Based on their results, my main responsibilities included data interfaces, inheriting and validating the Fluent thermal-analysis workflow, troubleshooting CAD / Fluent Meshing, and conducting selected thermophysical experiments.

以下流程概括了主要工程链路：

The following diagram summarizes the main engineering workflow:

```text
论文与既有工程基线
→ 上游 FLUKA 能量沉积结果
→ 数据完整性 / 单位 / 坐标 / 功率验证
→ Fluent UDF 热源加载
→ CAD / SpaceClaim / Fluent Meshing
→ Capping / Region / Volume Mesh
→ Solver 温度场
→ Mechanical 热应力
```

实习结束时，最后四个下游节点尚未全部闭环；对应执行状态已写入 `10-handoff/ansys-fluent/`。

At the end of the internship, the final four downstream stages had not all been completed. Their execution status is documented in `10-handoff/ansys-fluent/`.

## 已形成的关键成果 | Key Results

- 完成旧 `.29 → Python/C → UDF → Fluent` 热源链恢复；
  Restored the legacy `.29 → Python/C → UDF → Fluent` heat-source pipeline.
- 将旧模型 **18.422%** 功率缺口分解到几何覆盖差异与 cell-centroid 映射欠/过填充，而非简单“漏网格”；
  Traced the legacy model's **18.422%** power deficit to geometric coverage differences and under-/over-filling in cell-centroid mapping, rather than attributing it simply to “missing mesh cells.”
- 确认新 `.30.lis` 仅含 **14,786,930 / 34,560,000 = 42.786%** 数据，并改由原始 `fort.30` 完成完整二进制读取；
  Confirmed that the new `.30.lis` contains only **14,786,930 / 34,560,000 = 42.786%** of the data, and switched to the original `fort.30` for complete binary reading.
- Python 与 Fluent UDF 对 34.56M 数据、峰值与总量完成独立交叉验证，5 mA 全域积分功率约 **31.035 kW**；
  Independently cross-validated the 34.56-million data points, peak values, and totals between Python and the Fluent UDF. The full-domain integrated power at 5 mA is approximately **31.035 kW**.
- 将长期 Share Topology 故障从“继续加密网格”追溯到局部冷却管—主体 CAD 拓扑，并通过健康对照与删除问题管 A/B 试验获得强证据；
  Traced the persistent Share Topology failure beyond the “refine the mesh further” hypothesis to the local cooling-pipe/main-body CAD topology, supported by healthy controls and A/B tests that removed the problematic pipe.
- DRPL-V 实验完成重复性与环境边界的阶段性评价；短期重复性总体较好，绝对准确度、凝露影响和厚度读数漂移仍未闭环；
  Completed an interim assessment of repeatability and environmental boundaries for the DRPL-V experiment. Short-term repeatability was generally good, while absolute accuracy, condensation effects, and thickness-reading drift remain unresolved.
- 形成每日事实日志、周报、最终报告、PPT 信息架构及 ANSYS / Fluent 正式交接包；运行资产并非全部进入 GitHub，外部资产与缺失 RAW30 UDF 源码已在交接清单中显式标记。
  Produced daily factual logs, weekly reports, the final report, a presentation information architecture, and a formal ANSYS / Fluent handover package. Not all runtime assets are stored in GitHub; external assets and missing RAW30 UDF source code are explicitly identified in the handover checklist.

## 当前仓库结构 | Repository Structure

```text
monte-carlo-particle-transport-internship-2026/
├── 00-admin/                 # 原始任务、计划、当前状态与规则 / Tasks, plans, status, and rules
├── 01-daily-log/             # 终版日志与周报 / Final daily logs and weekly reports
├── 02-meetings/              # 实际组会记录 / Meeting records
├── 04-literature/            # 文献证据、精读、结构化笔记与专题综合 / Literature evidence and reviews
├── 05-software/              # 软件学习记录；正式续接入口不在这里 / Software learning notes; not the handover entry point
├── 06-cases/                 # Ansys / Fluent 算例与运行记录 / Ansys / Fluent cases and run records
├── 07-reports/               # 技术总盘点与最终实习报告 / Technical review and final internship report
├── 08-presentation/          # 最终答辩 PPT 信息架构与历史组会材料 / Final presentation structure and historical meeting materials
├── 09-archive/               # 已退出现役区但仍有参考价值的历史材料 / Historical reference materials
├── 10-handoff/               # 正式工程交接包 / Formal engineering handover package
└── fluka_to_c_translation/   # 旧 .29 回归链的代码与数据基线 / Code and data baseline for the legacy .29 regression pipeline
```

`03-notes/` 原先只有通用占位 README，没有形成独立事实笔记，已在实习收尾清理；目录编号不重排，以避免大量历史链接失效。

`03-notes/` previously contained only a generic placeholder README and no independent factual notes. It was removed during internship closeout. Directory numbering was not changed to avoid breaking numerous historical links.

## 推荐读取顺序 | Recommended Reading Order

### 看实习成果 | To Review Internship Results

1. `07-reports/final-internship-report.md`
2. `07-reports/internship-content-review-by-technical-route.md`
3. `01-daily-log/weekly-review/`
4. 需要核对细节时再回到对应每日终版日志。
   
   Return to the corresponding final daily log when specific details need to be checked.

### 继续 ANSYS / Fluent 工程 | To Continue the ANSYS / Fluent Work

1. `10-handoff/README.md`
2. `10-handoff/ansys-fluent/START_HERE.md`
3. `10-handoff/ansys-fluent/EXECUTION_RUNBOOK.md`
4. `10-handoff/ansys-fluent/NEXT_STEPS_CHECKLIST.md`

## 记录原则 | Record-Keeping Principles

- 区分“已运行、已验证、当前判断、待核实、未完成”；
  Distinguish between “run,” “verified,” “current assessment,” “to be verified,” and “incomplete.”
- 关键结论必须能追溯到原始数据、代码、日志、实验或验证记录；
  Every key conclusion must be traceable to raw data, code, logs, experiments, or verification records.
- 不把团队上游成果写成个人完成内容，也不因职责边界而放弃对输入的必要审查；
  Do not claim upstream team results as individual work, and do not skip necessary input reviews because of responsibility boundaries.
- AI 可用于解释、代码草拟、信息整理和假设生成，但不能替代守恒、对照、A/B 与人工责任；
  AI may assist with explanations, code drafts, information organization, and hypothesis generation, but it cannot replace conservation checks, controls, A/B tests, or human accountability.
- 未公开资料继续遵守保密和脱敏要求。
  Continue to apply confidentiality and anonymization requirements to non-public materials.
