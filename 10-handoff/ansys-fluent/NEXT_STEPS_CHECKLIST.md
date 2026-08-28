# 当前执行检查清单：B 线先行，随后 A/B 汇合

> 本清单只描述**下一次接手实际要做的操作**，不是项目综述。

## Gate B5 — Capping / Region / Volume Mesh

- [ ] 打开当前 Share 后 Fluent Meshing 状态；不要 Update All。
- [ ] 执行 `/boundary/manage/list`，保存当前 Face Zone ID。
- [ ] 逐个显示长细管候选 zone，确认管体完整。
- [ ] 找到两个真实开口端面；确认它们是否为独立 Face Zone。
- [ ] 清除旧 Capping 中失效的 zone 选择。
- [ ] 用当前端面重新建立 inlet / outlet cap。
- [ ] 单独显示 cap，确认只封真实开口，不横切管腔。
- [ ] Create / Update Regions。
- [ ] 验收：water 为连续 fluid region；铜/钢为 solid；dead/void 数量合理。
- [ ] 只有上述通过后才生成 Volume Mesh。
- [ ] 验收：无 `Mesh topology corrupted`、无 unresolved non-manifold、管腔贯通。
- [ ] 保存明确命名的 Volume Mesh 检查点。

**若 B5 未通过：不要碰 A4/UDF。**

## Gate A4 — 新几何坐标标定与热源挂接

- [ ] 进入 Solver 后先识别新版 water / copper / steel Cell Zone。
- [ ] 禁止复用旧 `zone 10 = source`。
- [ ] 使用新数据路线 `fort.30 → RAW30_ENERGY_SOURCE`，旧 `.29 → ENERGY_PLAN` 仅作回归。
- [ ] 先验证轴向关系 `CAD +X → FLUKA +Z`。
- [ ] 对横向 Y/Z ↔ X/Y 的交换与正负号做候选变换 A/B。
- [ ] 用峰值位置 `(-1.85,+0.95,26.25) cm` 做空间验证。
- [ ] 挂 Source 后做 `Σ(q''' × cell volume)` 功率积分。
- [ ] 以完整盒 `31.035322255 kW` 为上游锚点，解释几何截取后的差异。
- [ ] 热斑位置、功率、挂接区域三项同时合理后，A4 才算通过。

## Gate S1 — Solver

- [ ] Energy = On。
- [ ] 材料身份正确。
- [ ] inlet / outlet 正确。
- [ ] 流固接口正确。
- [ ] 质量流量守恒检查。
- [ ] 能量输入/输出检查。
- [ ] 温度监控量进入平台后保存 case/data 检查点。

## 停止条件

出现以下任一情况，停止当前层级继续“试参数”：

- `Mesh topology corrupted`
- `SIGSEGV`
- 大量 `non-manifold configuration`
- 某局部接口数万级 inter-zone intersection
- Region 身份明显违反物理直觉
- UDF 热斑落在错误部件或明显错误方向

先回到上一个 Gate 查根因。
