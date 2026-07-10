# 文献总索引

更新时间：2026-07-10

本文件是文献知识库的唯一总入口。原始文献不在此重复存放正文，仅登记来源、原始目录、状态、主题、关键页码和对应笔记路径。

## 状态定义

| 状态 | 含义 |
|---|---|
| 待上传 | 已确定需要，但尚未收到文件 |
| 已登记 | 已收到文件，仅完成元数据登记 |
| 已建页码地图 | 已定位目录与高相关章节 |
| 精读中 | 正在抽取关键事实、图表和参数 |
| 已完成单篇笔记 | 已形成可复用 Markdown 笔记 |
| 已纳入专题综合 | 已进入跨文献比较或组内分享材料 |

## 核心文献

| ID | 文献 | 原始目录 | 主题标签 | 状态 | 重点位置 | 笔记路径 |
|---|---|---|---|---|---|---|
| LIT-001 | 帅文文：《CiADS 缪子源靶后高功率准直器设计》 | 已上传文件；本地原目录待登记 | `CiADS` `collimator` `thermal` `stress` `cooling` `machine-protection` | 已登记 | 第3章物理与结构设计；第4章热力学分析 | `04-literature/notes/LIT-001-shuai-wenwen-thesis.md` |
| LIT-002 | PSI：《IMPACT Technical Design Report, Volume HIMB》 | 已上传文件；本地原目录待登记 | `PSI` `HIMB` `collimator` `power-deposition` `cooling` `machine-protection` | 已建页码地图 | 17–22；50–54；80–84；89–98 | `04-literature/notes/LIT-002-psi-impact-tdr.md` |
| LIT-003 | PSI：*New Design of a Collimator System at the PSI Proton Accelerator* | `D:\BaiduNetdiskDownload\文献\others\` | `PSI` `collimator` `beam-loss` `power-deposition` `thermal` `stress` `material` `optimization` `machine-protection` | 已纳入专题综合 | PDF第1–5页；重点为第2页图5、第4页图8–10和表1、第5页表2 | `04-literature/notes/LIT-003-psi-new-collimator-system.md` |
| LIT-004 | 余洁冰等：《CSNS/RCS次级准直器吸收体的冷却设计》 | `D:\BaiduNetdiskDownload\文献\CSNS\` | `CSNS` `collimator` `absorber` `cooling` `thermal` `activation` `radiation` `machine-protection` `maintenance` | 已纳入专题综合 | PDF第1–4页；重点为第1页图2、第2页图3–4、第3页图5、第4页图6–7 | `04-literature/notes/LIT-004-csns-secondary-collimator-cooling.md` |
| LIT-005 | PSI：*A Simulation Based Thermal Analysis of a New Current Monitor at PSI Proton Accelerator* | `D:\BaiduNetdiskDownload\文献\Cern\` | `PSI` `current-monitor` `thermal` `cooling` `CFD-validation` `power-deposition` `machine-protection` | 已纳入专题综合 | PDF第2–4页；重点为第3页图2–3、第4页图4–5及断水分析 | `04-literature/notes/LIT-005-psi-current-monitor-thermal-validation.md` |
| LIT-006 | 贾欢等：*Design and Development of the 200-kW Beam Dump* | `D:\BaiduNetdiskDownload\文献\` | `beam-dump` `absorber` `power-deposition` `thermal` `cooling` `stress` `deformation` `material` `activation` `maintenance` `commissioning` | 已纳入专题综合 | PDF第3–9页；重点为图5–8、图13–15及热结构和运行参数 | `04-literature/notes/LIT-006-cafe-200kw-beam-dump.md` |
| LIT-007 | CERN：*Summary of calculations performed on TCTP collimators* | `D:\BaiduNetdiskDownload\文献\Cern\` | `CERN` `collimator` `thermal` `cooling` `stress` `deformation` `contact-conductance` `bolted-joint` `brazing` `creep` `bakeout` | 已纳入专题综合 | 文档第5–11、12–13、22–40页；重点为接触压力、热导、热挠度和烘烤稳定性 | `04-literature/notes/LIT-007-cern-tctp-thermomechanical-calculations.md` |
| LIT-008 | SNS：*Double-Wall Collimator Design of the SNS Project* | `D:\BaiduNetdiskDownload\文献\SNS\` | `SNS` `collimator` `absorber` `double-wall` `cooling` `thermal-shock` `helium` `leak-detection` `Inconel-718` `machine-protection` | 已纳入专题综合 | PDF第1–3页；重点为第2页图2–3、第3页表1及图5–6 | `04-literature/notes/LIT-008-sns-double-wall-collimator.md` |
| TREE-001 | 用户文献文件夹目录树 | `D:\BaiduNetdiskDownload\文献\` | `inventory` | 已登记 | 用于后续选文献 | 本文件下方候选清单 |

## 专题综合

| 专题 | 关联文献 | 路径 |
|---|---|---|
| 高功率束流部件热设计的六条工程主线 | LIT-003～LIT-008 | `04-literature/synthesis/thermal-design-methods-psi-csns.md` |
| 准直与吸收结构冷却架构比较 | LIT-004、LIT-006、LIT-007、LIT-008 | `04-literature/synthesis/cooling-architecture-comparison.md` |

## 第一批上传队列

| 优先级 | 文件名 | 所在文件夹 | 状态 |
|---:|---|---|---|
| 1 | `NEW DESIGN OF A COLLIMATOR SYSTEM AT THE PSI PROTON ACCELERATOR.pdf` | `D:\BaiduNetdiskDownload\文献\others\` | 已完成并纳入专题综合 |
| 2 | `CSNS_RCS次级准直器吸收体的冷却设计.pdf` | `D:\BaiduNetdiskDownload\文献\CSNS\` | 已完成并纳入专题综合 |
| 3 | `A_SIMULATION_BASED_THERMAL_ANALYSIS_OF_A_NEW_CURRE (1).pdf` | `D:\BaiduNetdiskDownload\文献\Cern\` | 已完成；实际内容为PSI MHC5监测器 |
| 4 | `2023Design and Development of the 200 kW Beam Dump_2-11.pdf` | `D:\BaiduNetdiskDownload\文献\` | 已完成并纳入专题综合 |

## 第二批当前优先队列

| 优先级 | 文件名 | 所在文件夹 | 选择理由 | 状态 |
|---:|---|---|---|---|
| 1 | `LHC-TC-ER-0001-00-10.pdf`／本次上传为`.docx`版 | `D:\BaiduNetdiskDownload\文献\Cern\` | 补充CERN准直器冷却、热机械、接触热导、螺栓预紧和烘烤稳定性 | 已完成并纳入专题综合 |
| 2 | `DOUBLE-WALL COLLIMATOR DESIGN OF THE SNS PROJECT.PDF` | `D:\BaiduNetdiskDownload\文献\SNS\` | 补充双壁隔离、氦检漏、铜丝导热桥和整束脉冲容错 | 已完成并纳入专题综合 |
| 3 | `THE BEAM COLLIMATOR SYSTEM OF J-PARC RAPID CYCLING SYNCHROTRON.pdf` | `D:\BaiduNetdiskDownload\文献\J-PARC\` | 补充运行经验、可维护性和失效反馈 | 下一篇待上传 |
| 4 | `Estimation of Radioactivity Produced in Cooling.pdf` | `D:\BaiduNetdiskDownload\文献\水冷\` | 专门补充冷却水活化和回路源项 | 待上传 |

## 其他候选池

- `Collimation and Beam Dumps.pdf` — `D:\BaiduNetdiskDownload\文献\`
- `BEAM HALO AND SCRAPING.pdf` — `D:\BaiduNetdiskDownload\文献\`
- `Conceptual design of an off-momentum collimation system in the CERN Super Proton Synchrotron for High-Luminosity Large Hadron Collider proton beams-PhysRevAccelBeams.24.093002.pdf` — `D:\BaiduNetdiskDownload\文献\Cern\`
- `LHC COLLIMATOR CONTROLS FOR A SAFE LHC OPERATION.pdf` — `D:\BaiduNetdiskDownload\文献\Cern\`
- `Simulations and measurements of beam loss patterns at the CERN Large Hadron Collider.pdf` — `D:\BaiduNetdiskDownload\文献\Cern\`
- `2006-Design of the two-stage collimation system for CSNS_RCS.pdf` — `D:\BaiduNetdiskDownload\文献\CSNS\`
- `Thermal analy...r in CSNS_RCS_Jie-Bing Yu.pdf` — `D:\BaiduNetdiskDownload\文献\CSNS\`

## 主题标签规范

优先使用以下稳定标签：

`collimator` `beam-dump` `absorber` `beam-halo` `beam-loss` `power-deposition` `thermal` `cooling` `stress` `deformation` `material` `contact-conductance` `bolted-joint` `brazing` `creep` `bakeout` `double-wall` `helium` `leak-detection` `thermal-shock` `machine-protection` `radiation` `activation` `maintenance` `commissioning` `optimization` `PSI` `CSNS` `CERN` `SNS` `J-PARC` `CiADS`

不得随意制造近义标签。例如统一使用 `machine-protection`，不要同时使用 `MPS`、`protection-system`、`beam-protection` 作为索引标签；这些词可保留在正文中。

## 上传提醒规则

后续要求用户上传文献时，必须同时给出：

1. 文件名；
2. 所在文件夹；
3. 上传优先级；
4. 选择该文献的理由；
5. 上传后预期产出。
