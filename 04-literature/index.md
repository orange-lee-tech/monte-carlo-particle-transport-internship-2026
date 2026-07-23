# 文献总索引

更新时间：2026-07-23

本文件是文献状态的唯一总表。重点区分“文件已入库、机器辅助整理、用户人工精读、进入工程继承/拓展”四种状态。

## 核心文献

| ID | 文献 | 原始文件 | 机器辅助整理 | 用户人工阅读 | 当前用途 | 知识路径 |
|---|---|---|---|---|---|---|
| LIT-001 | 帅文文《CiADS缪子源靶后高功率准直器设计》 | 已有 | 已完成 | 已完成第3、4章主线 | 当前直接继承基线；工程验证中 | `deep-reading/LIT-001-shuai-wenwen-ciads-collimator/` |
| LIT-002 | PSI 2025 IMPACT TDR, Volume HIMB | 已有 | 仅建重点页码地图 | 未系统精读 | 基线继承后补充PSI最新设计方法 | 暂无正式笔记 |
| LIT-003 | PSI：New Design of a Collimator System | 已有 | 已完成 | 未人工精读 | 后续孔径、功率分配和材料方法支撑 | `notes/LIT-003-psi-new-collimator-system.md` |
| LIT-004 | CSNS/RCS次级准直器吸收体冷却设计 | 已有 | 已完成 | 未人工精读 | 后续冷却、活化和维护支撑 | `notes/LIT-004-csns-secondary-collimator-cooling.md` |
| LIT-005 | PSI MHC5热分析与实验校核 | 已有 | 已完成 | 未人工精读 | 后续CFD验证和断水风险支撑 | `notes/LIT-005-psi-current-monitor-thermal-validation.md` |
| LIT-006 | CAFe 200 kW Beam Dump | 已有 | 已完成 | 未人工精读 | 后续高功率吸收器工程闭环支撑 | `notes/LIT-006-cafe-200kw-beam-dump.md` |
| LIT-007 | CERN TCTP热机械计算 | 已有 | 已完成 | 未人工精读 | 后续接触热导、预紧和热挠度支撑 | `notes/LIT-007-cern-tctp-thermomechanical-calculations.md` |
| LIT-008 | SNS双壁准直器 | 已有 | 已完成 | 未人工精读 | 后续双壁、检漏和导热桥支撑 | `notes/LIT-008-sns-double-wall-collimator.md` |
| LIT-009 | J-PARC RCS准直系统 | 已有 | 已完成 | 未人工精读 | 后续调试、BLM和远程维护支撑 | `notes/LIT-009-jparc-rcs-collimator-commissioning.md` |
| LIT-010 | J-PARC冷却水活化估算 | 已有 | 已完成 | 未人工精读 | 后续活化水、回路和维护剂量支撑 | `notes/LIT-010-jparc-cooling-water-activation.md` |

## 当前阅读顺序

```text
完成LIT-001工程继承
→ 复现论文锚点工况
→ 精读LIT-002 PSI TDR
→ 按实际拓展问题选择LIT-003—LIT-010
```

LIT-003—LIT-010当前已经形成可检索的机器辅助笔记和专题综合，但不能标记为“用户已读”。这些资料将在独立拓展前作为方法和风险支撑重新人工阅读。

## 专题综合

| 专题 | 关联文献 | 路径 | 当前定位 |
|---|---|---|---|
| 高功率束流部件热设计工程主线 | LIT-003—LIT-008 | `synthesis/thermal-design-methods-psi-csns.md` | 拓展阶段方法储备 |
| 冷却架构比较 | LIT-004、006、007、008 | `synthesis/cooling-architecture-comparison.md` | 方案选型储备 |
| 调试、运行验证与维护闭环 | LIT-004、005、006、007、009 | `synthesis/commissioning-maintenance-and-validation.md` | 验证路线储备 |
| 冷却水活化与回路设计 | LIT-004、006、008、009、010 | `synthesis/cooling-water-activation-and-loop-design.md` | 辐射与维护储备 |

## 文件管理

- `references/`保存原始PDF/DOCX，不直接修改；
- `deep-reading/`只接收用户人工精读且直接支撑工程继承的文献；
- `notes/`保存外部文献机器辅助结构化笔记；
- `synthesis/`保存跨文献方法综合；
- 新增文献前先说明它填补的明确工程缺口，不再盲目扩充。
