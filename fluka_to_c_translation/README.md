# FLUKA to C Array Translation

## Purpose

This directory contains the conversion chain from FLUKA scoring output (`.29`) to C language heat source arrays used by Fluent UDF.

## Conversion chain

FLUKA output (.29)

→ Python converter

→ C array (`heat_deposition[20][20][28]`)

→ Fluent UDF heat source loading

## Mesh definition

The FLUKA scoring mesh is:

- X: -10 cm ~ 10 cm, 20 bins, 1 cm/bin
- Y: -10 cm ~ 10 cm, 20 bins, 1 cm/bin
- Z: -14 cm ~ 14 cm, 28 bins, 1 cm/bin

Array indexing follows:

`A(ix,iy,iz)` → `heat_deposition[ix][iy][iz]`

## Case naming convention

Original filenames contained temporary path information from FLUKA calculation directories. They are retained only as historical references.

Future maintained files should follow:

`beam_<angle>_offset_<value>_<type>.<ext>`

Examples:

- `beam_1mrad_offset_2mm.29`
- `beam_2mrad_offset_1p4mm.29`

## Notes

- The converter currently assumes a fixed 20×20×28 mesh.
- Before Fluent loading, verify total deposited power and coordinate mapping.
- Do not modify original FLUKA outputs during post-processing.

# FLUKA 热沉积数据转换

本目录保存 FLUKA 热沉积计分结果、转换脚本和生成的 C 三维数组。

## 目录结构

```text
fluka_to_c_translation/
├─ README.md
├─ fluka_to_c_array_converter.py
├─ input/
│  ├─ beam_1mrad_offset_2mm.29
│  └─ beam_2mrad_offset_1p4mm.29
├─ output/
│  ├─ beam_1mrad_offset_2mm_heat_deposition.c
│  └─ beam_2mrad_offset_1p4mm_heat_deposition.c
└─ udf/
   └─ README.md