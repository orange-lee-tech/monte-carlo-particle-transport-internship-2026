from __future__ import annotations

import re
from pathlib import Path

import numpy as np


# 当前两份 FLUKA USRBIN 文件采用同一网格。
X_MIN_CM, X_MAX_CM = -10.0, 10.0
Y_MIN_CM, Y_MAX_CM = -10.0, 10.0
Z_MIN_CM, Z_MAX_CM = -14.0, 14.0

NX, NY, NZ = 20, 20, 28
EXPECTED_VALUES = NX * NY * NZ

# 支持整数、小数以及 E/e 科学计数法。
NUMBER_PATTERN = re.compile(
    r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][-+]?\d+)?"
)


def sanitize_identifier(text: str) -> str:
    """把文件名转换为合法的 C 标识符。"""
    identifier = re.sub(r"[^0-9A-Za-z_]", "_", text)
    identifier = re.sub(r"_+", "_", identifier).strip("_")

    if not identifier:
        raise ValueError(f"无法从名称生成 C 标识符: {text!r}")

    if identifier[0].isdigit():
        identifier = f"data_{identifier}"

    return identifier.lower()


def read_fluka_values(input_path: Path) -> list[float]:
    """读取 FLUKA .29 文件中 Data follow in a matrix 之后的数据。"""
    lines = input_path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    data_start_line: int | None = None

    for index, line in enumerate(lines):
        if "Data follow in a matrix" in line:
            data_start_line = index + 1
            break

    if data_start_line is None:
        raise ValueError(
            f"未在文件中找到数据起始标记 "
            f"'Data follow in a matrix': {input_path}"
        )

    values: list[float] = []

    for line in lines[data_start_line:]:
        if not line.strip():
            continue

        values.extend(
            float(token)
            for token in NUMBER_PATTERN.findall(line)
        )

    if len(values) != EXPECTED_VALUES:
        raise ValueError(
            f"{input_path.name} 数据量错误："
            f"期望 {EXPECTED_VALUES}，实际 {len(values)}。"
            "程序已停止，不进行补零或截断。"
        )

    return values


def build_3d_array(values: list[float]) -> np.ndarray:
    """
    将 FLUKA 一维数据转换为 [x][y][z] 数组。

    FLUKA 数据顺序为：
    x 索引变化最快，其次 y，最后 z。
    """
    data_3d = np.zeros((NX, NY, NZ), dtype=float)

    index = 0

    for iz in range(NZ):
        for iy in range(NY):
            for ix in range(NX):
                data_3d[ix, iy, iz] = values[index]
                index += 1

    return data_3d


def make_macro_prefix(array_name: str) -> str:
    """生成头文件中使用的宏前缀。"""
    return re.sub(r"[^0-9A-Za-z]", "_", array_name).upper()


def write_header_file(
    header_path: Path,
    array_name: str,
) -> None:
    """生成数组声明头文件。"""
    macro_prefix = make_macro_prefix(array_name)
    include_guard = f"{macro_prefix}_H"

    content = f"""\
#ifndef {include_guard}
#define {include_guard}

#include "udf.h"

#define {macro_prefix}_NX {NX}
#define {macro_prefix}_NY {NY}
#define {macro_prefix}_NZ {NZ}

#define {macro_prefix}_X_MIN_CM ({X_MIN_CM:.1f})
#define {macro_prefix}_X_MAX_CM ({X_MAX_CM:.1f})
#define {macro_prefix}_Y_MIN_CM ({Y_MIN_CM:.1f})
#define {macro_prefix}_Y_MAX_CM ({Y_MAX_CM:.1f})
#define {macro_prefix}_Z_MIN_CM ({Z_MIN_CM:.1f})
#define {macro_prefix}_Z_MAX_CM ({Z_MAX_CM:.1f})

extern const real {array_name}
    [{macro_prefix}_NX]
    [{macro_prefix}_NY]
    [{macro_prefix}_NZ];

#endif
"""

    header_path.write_text(content, encoding="utf-8")


def write_c_file(
    c_path: Path,
    header_filename: str,
    array_name: str,
    data_3d: np.ndarray,
    elements_per_line: int = 6,
) -> None:
    """生成包含实际数组数据的 C 文件。"""
    macro_prefix = make_macro_prefix(array_name)

    with c_path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(f'#include "{header_filename}"\n\n')

        file.write(
            f"const real {array_name}\n"
            f"    [{macro_prefix}_NX]\n"
            f"    [{macro_prefix}_NY]\n"
            f"    [{macro_prefix}_NZ] = {{\n"
        )

        for ix in range(NX):
            file.write(f"  {{ /* X index {ix} */\n")

            for iy in range(NY):
                file.write(f"    {{ /* Y index {iy} */\n")
                file.write("      ")

                for iz in range(NZ):
                    value = data_3d[ix, iy, iz]
                    file.write(f"{value:13.6e}")

                    if iz < NZ - 1:
                        file.write(", ")

                    if (
                        (iz + 1) % elements_per_line == 0
                        and iz < NZ - 1
                    ):
                        file.write("\n      ")

                file.write("\n    }")

                if iy < NY - 1:
                    file.write(",")

                file.write("\n")

            file.write("  }")

            if ix < NX - 1:
                file.write(",")

            file.write("\n")

        file.write("};\n")


def convert_one_file(
    input_path: Path,
    output_dir: Path,
    elements_per_line: int = 6,
) -> tuple[Path, Path]:
    """把一个 .29 文件转换为配套的 .h 和 .c 文件。"""
    output_base = f"{input_path.stem}_heat_deposition"
    array_name = sanitize_identifier(output_base)

    header_path = output_dir / f"{output_base}.h"
    c_path = output_dir / f"{output_base}.c"

    values = read_fluka_values(input_path)
    data_3d = build_3d_array(values)

    write_header_file(
        header_path=header_path,
        array_name=array_name,
    )

    write_c_file(
        c_path=c_path,
        header_filename=header_path.name,
        array_name=array_name,
        data_3d=data_3d,
        elements_per_line=elements_per_line,
    )

    print("=" * 60)
    print(f"输入文件: {input_path}")
    print(f"数据点数: {len(values)} / {EXPECTED_VALUES}")
    print(f"数组名称: {array_name}")
    print(f"头文件:   {header_path}")
    print(f"C 文件:   {c_path}")

    return header_path, c_path


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    input_dir = current_dir / "input"
    output_dir = current_dir / "output"

    if not input_dir.is_dir():
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    input_files = sorted(input_dir.glob("*.29"))

    if not input_files:
        raise FileNotFoundError(
            f"输入目录中未找到 .29 文件: {input_dir}"
        )

    for input_path in input_files:
        convert_one_file(
            input_path=input_path,
            output_dir=output_dir,
            elements_per_line=6,
        )


if __name__ == "__main__":
    main()
