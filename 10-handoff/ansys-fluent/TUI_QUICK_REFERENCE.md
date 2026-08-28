# Fluent Meshing TUI 快查表

> 每次重新 Surface Mesh / Share 后，Zone ID 都可能变化。任何诊断前先执行 `/boundary/manage/list`。

| 目的 | 命令 | 风险 |
|---|---|---|
| 提高日志详细度 | `/report/verbosity 2` | 安全 |
| 列出当前 Face Zone | `/boundary/manage/list` | 只读 |
| 清除 marked faces | `/boundary/clear-marked-faces` | 只清标记 |
| 标记两个 zone 的真实三角面相交 | `/boundary/mark-face-intersection` | 只标记 |
| 标记 Fluent 准备 Join 的候选面 | `/boundary/remesh/mark-join-faces` | 只标记 |
| 统计 marked faces | `(tgapi-util-count-marked-faces '(ID1 ID2))` | 只读 |
| 检查 self-intersection | `(tgapi-util-mark-self-intersecting-faces '(ID1 ID2) #t)` | 只标记 |
| 检查 duplicate faces | `(tgapi-util-mark-duplicate-faces '(ID1 ID2))` | 只标记 |
| 真正 Join / Remesh | GUI/TUI Join、Remesh | 修改网格，谨慎 |

## 诊断判据

- `self-intersection > 0`：单个表面自身可能有问题。
- `duplicate > 0`：重复面/重复网格。
- inter-zone intersection 数万级：两实体接口相交/重合异常。
- Join candidates 很多但 intersection 很少：tolerance/gap 可能过宽。
- 同类健康接口为 0、某一根管为几万：优先锁定局部 CAD。
- `Mesh topology corrupted / SIGSEGV`：停止 Fluent 调参，回几何。

## 已验证对照（仅为历史证据，ID 不可复用）

```text
主体 ↔ wall.5  ≈ 79,829 intersection faces
主体 ↔ wall.6  ≈ 69,515 intersection faces
主体 ↔ wall.7  = 0
```
