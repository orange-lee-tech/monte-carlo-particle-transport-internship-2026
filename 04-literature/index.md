# 文献总索引

更新时间：2026-07-10

本文件是文献知识库的唯一总入口。原始 PDF 不在此重复存放正文，仅登记来源、状态、主题、关键页码和对应笔记路径。

## 状态定义

| 状态 | 含义 |
|---|---|
| 待上传 | 已确定需要，但尚未收到 PDF |
| 已登记 | 已收到 PDF，仅完成元数据登记 |
| 已建页码地图 | 已定位目录与高相关章节 |
| 精读中 | 正在抽取关键事实、图表和参数 |
| 已完成单篇笔记 | 已形成可复用 Markdown 笔记 |
| 已纳入专题综合 | 已进入跨文献比较或组内分享材料 |

## 核心文献

| ID | 文献 | 主题标签 | 状态 | 重点位置 | 笔记路径 |
|---|---|---|---|---|---|
| LIT-001 | 帅文文：《CiADS 缪子源靶后高功率准直器设计》 | `CiADS` `collimator` `thermal` `stress` `cooling` `machine-protection` | 已登记 | 第3章物理与结构设计；第4章热力学分析 | `04-literature/notes/LIT-001-shuai-wenwen-thesis.md` |
| LIT-002 | PSI：《IMPACT Technical Design Report, Volume HIMB》 | `PSI` `HIMB` `collimator` `power-deposition` `cooling` `MPS` | 已建页码地图 | 17–22；50–54；80–84；89–98 | `04-literature/notes/LIT-002-psi-impact-tdr.md` |
| TREE-001 | 用户文献文件夹目录树 | `inventory` | 已登记 | 用于后续选文献 | 本文件下方候选清单 |

## 第一批待上传

| 优先级 | 文件名 | 选择理由 | 状态 |
|---:|---|---|---|
| 1 | `NEW DESIGN OF A COLLIMATOR SYSTEM AT THE PSI PROTON ACCELERATOR.pdf` | 与 PSI 靶后固定孔径准直器直接相关，可补足 TDR 的设计演化与优化依据 | 待上传 |
| 2 | `CSNS_RCS次级准直器吸收体的冷却设计.pdf` | 中文、工程针对性强，适合比较冷却结构、流量、压降与热分析方法 | 待上传 |
| 3 | `A_SIMULATION_BASED_THERMAL_ANALYSIS_OF_A_NEW_CURRE (1).pdf` | 用于补充 CERN 类准直器热分析方法、边界条件与失效判断 | 待上传 |
| 4 | `2023Design and Development of the 200 kW Beam Dump_2-11.pdf` | 用于建立高功率吸收体/beam dump 的工程尺度与瞬态风险参照 | 待上传 |

## 第二批候选池

第一批精读完成前不急于上传。后续根据知识缺口再选：

- `Collimation and Beam Dumps.pdf`
- `BEAM HALO AND SCRAPING.pdf`
- `DOUBLE-WALL COLLIMATOR DESIGN OF THE SNS PROJECT.PDF`
- `COLLIMATOR DESIGN FOR THE HEBT LINE OF THE SNS PROJECT.pdf`
- `THE BEAM COLLIMATOR SYSTEM OF J-PARC RAPID CYCLING SYNCHROTRON.pdf`
- `2006-Design of the two-stage collimation system for CSNS_RCS.pdf`
- `Thermal analy...r in CSNS_RCS_Jie-Bing Yu.pdf`
- `Estimation of Radioactivity Produced in Cooling.pdf`

## 主题标签规范

优先使用以下稳定标签：

`collimator` `beam-dump` `absorber` `beam-halo` `beam-loss` `power-deposition` `thermal` `cooling` `stress` `deformation` `material` `machine-protection` `radiation` `activation` `maintenance` `optimization` `PSI` `CSNS` `CERN` `SNS` `J-PARC` `CiADS`

不得随意制造近义标签。例如统一使用 `machine-protection`，不要同时使用 `MPS`、`protection-system`、`beam-protection` 作为索引标签；这些词可保留在正文中。
