# 当前任务说明

更新时间：2026-07-23

## 1. 当前阶段

工作已从“论文阅读和软件入门”进入“帅文文计算链工程继承与物理验证”阶段。

当前主线：

```text
帅文文论文与原始资料
→ FLUKA .29热沉积数据
→ Python转换为C数组.c/.h
→ Fluent UDF坐标、单位和功率映射
→ Fluent温度场
→ Mechanical热应力
→ 论文锚点工况回归
→ 独立拓展
```

## 2. 已完成

- 帅文文论文第3、4章主线精读与7份Zotero记录整理；
- `.29 → .c/.h`转换程序重构；
- 11200个热沉积数据的数量、顺序和逐点数值独立验证，结果PASS；
- 第一版Fluent UDF编译、加载和source铜区挂接；
- 第一版稳态Fluent温度场运行、保存和重启；
- 体素覆盖率诊断UDF建立；
- 文献目录合并和仓库编号收口。

## 3. 当前验证重点

1. 核实FLUKA输出单位和5 mA束流强度来源；
2. 完成voxel—cell覆盖率诊断；
3. 解释FLUKA参考功率与Fluent映射功率差异；
4. 将正式`DEFINE_SOURCE`主程序纳入版本管理；
5. 区分当前偏移工况与论文31.9 kW锚点工况；
6. 重新建立Fluent—Mechanical温度和应力回归；
7. 将同一流程复用于第二偏移工况。

## 4. 当前资料状态

| 资料 | 状态 | 位置 |
|---|---|---|
| 帅文文论文精读与继承矩阵 | 已完成整理，工程继承中 | `04-literature/deep-reading/LIT-001-shuai-wenwen-ciads-collimator/` |
| 外部文献LIT-003—LIT-010 | 机器辅助笔记完成，用户尚未系统精读 | `04-literature/notes/` |
| FLUKA输入和转换程序 | 已入库 | `fluka_to_c_translation/` |
| 数据一致性验证 | PASS | `fluka_to_c_translation/verification/` |
| Fluent/Mechanical接手记录 | 进行中 | `06-cases/ansys-cases/` |
| 每日与周度记录 | 持续维护 | `01-daily-log/` |

## 5. 文献安排

当前不继续盲目扩充外部文献。

合理顺序为：

```text
完成帅文文工作继承
→ 形成可靠热工计算基线
→ 精读PSI TDR
→ 根据实际拓展问题选择CERN/SNS/J-PARC/CSNS文献
→ 开展新结构、新工况或新方法
```

外部文献的作用是同步方法、了解已有成果和预警风险，不直接提供当前设备设计参数。

## 6. 仓库读取顺序

开展重要工作前读取：

1. `README.md`
2. `WORKING_RULES.md`
3. `00-admin/current-task.md`
4. 对应工程模块README或验证记录
5. 与问题直接相关的日志、代码和文献笔记

聊天作为即时工作区，GitHub作为长期事实库。