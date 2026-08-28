from __future__ import annotations

import math
import re
import sys
from pathlib import Path


CASE_NAME = "beam_1mrad_offset_2mm"
SCI_NUMBER = re.compile(
    r"[-+]?(?:\d+\.\d*|\.\d+|\d+)[Ee][-+]?\d+"
)
C_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
C_LINE_COMMENT = re.compile(r"//.*?$", re.MULTILINE)


class VerificationError(RuntimeError):
    pass


def parse_fluka_values(path: Path) -> list[float]:
    text = path.read_text(encoding="utf-8", errors="replace")
    marker = "Data follow in a matrix"
    marker_position = text.find(marker)

    if marker_position < 0:
        raise VerificationError(f"missing FLUKA data marker in {path}")

    data_text = text[text.find("\n", marker_position) + 1 :]
    values = [float(token) for token in SCI_NUMBER.findall(data_text)]

    if not values:
        raise VerificationError(f"no FLUKA data values found in {path}")

    return values


def parse_header_metadata(path: Path) -> dict[str, float | int]:
    text = path.read_text(encoding="utf-8", errors="strict")

    def read_int(suffix: str) -> int:
        match = re.search(rf"#define\s+\w+_{suffix}\s+(\d+)", text)
        if match is None:
            raise VerificationError(f"missing {suffix} macro in {path}")
        return int(match.group(1))

    def read_float(suffix: str) -> float:
        match = re.search(
            rf"#define\s+\w+_{suffix}\s+\(\s*([-+]?\d+(?:\.\d+)?)\s*\)",
            text,
        )
        if match is None:
            raise VerificationError(f"missing {suffix} macro in {path}")
        return float(match.group(1))

    return {
        "nx": read_int("NX"),
        "ny": read_int("NY"),
        "nz": read_int("NZ"),
        "x_min": read_float("X_MIN_CM"),
        "x_max": read_float("X_MAX_CM"),
        "y_min": read_float("Y_MIN_CM"),
        "y_max": read_float("Y_MAX_CM"),
        "z_min": read_float("Z_MIN_CM"),
        "z_max": read_float("Z_MAX_CM"),
    }


def parse_c_values(path: Path) -> list[float]:
    text = path.read_text(encoding="utf-8", errors="strict")
    text = C_BLOCK_COMMENT.sub("", text)
    text = C_LINE_COMMENT.sub("", text)

    assignment = text.find("=")
    terminator = text.rfind("};")

    if assignment < 0 or terminator < assignment:
        raise VerificationError(f"cannot isolate C array initializer in {path}")

    initializer = text[assignment + 1 : terminator]
    values = [float(token) for token in SCI_NUMBER.findall(initializer)]

    if not values:
        raise VerificationError(f"no C array values found in {path}")

    return values


def c_flat_index_to_xyz(index: int, ny: int, nz: int) -> tuple[int, int, int]:
    ix, remainder = divmod(index, ny * nz)
    iy, iz = divmod(remainder, nz)
    return ix, iy, iz


def fluka_linear_index(ix: int, iy: int, iz: int, nx: int, ny: int) -> int:
    return (iz * ny + iy) * nx + ix


def build_reference_in_c_text_order(
    fluka_values: list[float], nx: int, ny: int, nz: int
) -> list[float]:
    reference: list[float] = []

    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                source_index = fluka_linear_index(ix, iy, iz, nx, ny)
                reference.append(fluka_values[source_index])

    return reference


def format_value(value: float) -> str:
    return f"{value:.16e}"


def verify() -> bool:
    root = Path(__file__).resolve().parent
    input_path = root / "input" / f"{CASE_NAME}.29"
    c_path = root / "output" / f"{CASE_NAME}_heat_deposition.c"
    h_path = root / "output" / f"{CASE_NAME}_heat_deposition.h"

    for path in (input_path, c_path, h_path):
        if not path.is_file():
            raise VerificationError(f"required file not found: {path}")

    metadata = parse_header_metadata(h_path)
    nx = int(metadata["nx"])
    ny = int(metadata["ny"])
    nz = int(metadata["nz"])
    expected_count = nx * ny * nz

    fluka_values = parse_fluka_values(input_path)
    c_values = parse_c_values(c_path)
    reference_values = build_reference_in_c_text_order(
        fluka_values, nx, ny, nz
    )

    count_ok = (
        len(fluka_values) == expected_count
        and len(c_values) == expected_count
        and len(reference_values) == expected_count
    )

    if len(c_values) == len(reference_values):
        absolute_errors = [
            abs(reference - generated)
            for reference, generated in zip(reference_values, c_values)
        ]
        relative_errors: list[float] = []

        for reference, generated in zip(reference_values, c_values):
            difference = abs(reference - generated)
            if reference != 0.0:
                relative_errors.append(difference / abs(reference))
            elif generated == 0.0:
                relative_errors.append(0.0)
            else:
                relative_errors.append(math.inf)

        max_abs_error = max(absolute_errors, default=math.inf)
        max_rel_error = max(relative_errors, default=math.inf)
        mismatch_count = sum(error != 0.0 for error in absolute_errors)
    else:
        max_abs_error = math.inf
        max_rel_error = math.inf
        mismatch_count = abs(len(reference_values) - len(c_values))

    fluka_sum = math.fsum(fluka_values)
    c_sum = math.fsum(c_values)

    fluka_max = max(fluka_values)
    fluka_max_linear = fluka_values.index(fluka_max)
    fluka_max_ix = fluka_max_linear % nx
    fluka_max_iy = (fluka_max_linear // nx) % ny
    fluka_max_iz = fluka_max_linear // (nx * ny)

    c_max = max(c_values)
    c_max_flat = c_values.index(c_max)
    c_max_index = c_flat_index_to_xyz(c_max_flat, ny, nz)

    dimensions_ok = (nx, ny, nz) == (20, 20, 28)
    bounds_ok = (
        metadata["x_min"], metadata["x_max"],
        metadata["y_min"], metadata["y_max"],
        metadata["z_min"], metadata["z_max"],
    ) == (-10.0, 10.0, -10.0, 10.0, -14.0, 14.0)
    values_ok = mismatch_count == 0 and max_abs_error == 0.0
    maxima_ok = fluka_max == c_max and (
        fluka_max_ix, fluka_max_iy, fluka_max_iz
    ) == c_max_index
    sums_ok = fluka_sum == c_sum

    passed = all(
        (count_ok, dimensions_ok, bounds_ok, values_ok, maxima_ok, sums_ok)
    )

    print("=" * 72)
    print("FLUKA .29 -> C ARRAY INDEPENDENT VERIFICATION")
    print("=" * 72)
    print(f"case                         : {CASE_NAME}")
    print(f"result                       : {'PASS' if passed else 'FAIL'}")
    print()
    print("[header]")
    print(f"dimensions                   : {nx} x {ny} x {nz}")
    print(
        "bounds [cm]                  : "
        f"X[{metadata['x_min']}, {metadata['x_max']}], "
        f"Y[{metadata['y_min']}, {metadata['y_max']}], "
        f"Z[{metadata['z_min']}, {metadata['z_max']}]"
    )
    print()
    print("[counts]")
    print(f"expected                     : {expected_count}")
    print(f"FLUKA data                   : {len(fluka_values)}")
    print(f"C array data                 : {len(c_values)}")
    print()
    print("[pointwise comparison at identical (ix, iy, iz)]")
    print(f"mismatch count               : {mismatch_count}")
    print(f"maximum absolute error       : {format_value(max_abs_error)}")
    print(f"maximum relative error       : {format_value(max_rel_error)}")
    print()
    print("[global statistics]")
    print(f"FLUKA sum                    : {format_value(fluka_sum)}")
    print(f"C array sum                  : {format_value(c_sum)}")
    print(f"sum difference               : {format_value(c_sum - fluka_sum)}")
    print(f"FLUKA minimum                : {format_value(min(fluka_values))}")
    print(f"C array minimum              : {format_value(min(c_values))}")
    print(f"FLUKA maximum                : {format_value(fluka_max)}")
    print(f"C array maximum              : {format_value(c_max)}")
    print(
        "maximum index                : "
        f"FLUKA[{fluka_max_ix},{fluka_max_iy},{fluka_max_iz}] / "
        f"C{c_max_index}"
    )
    print()
    print("[samples]")
    sample_indices = [
        (0, 0, 0),
        (0, 5, 0),
        (5, 7, 3),
        (10, 10, 14),
        (fluka_max_ix, fluka_max_iy, fluka_max_iz),
        (nx - 1, ny - 1, nz - 1),
    ]

    seen: set[tuple[int, int, int]] = set()
    for ix, iy, iz in sample_indices:
        if (ix, iy, iz) in seen:
            continue
        seen.add((ix, iy, iz))
        source_index = fluka_linear_index(ix, iy, iz, nx, ny)
        c_index = (ix * ny + iy) * nz + iz
        print(
            f"[{ix:02d},{iy:02d},{iz:02d}] "
            f"FLUKA={format_value(fluka_values[source_index])}  "
            f"C={format_value(c_values[c_index])}"
        )

    print()
    print("[ordering conclusion]")
    print("FLUKA linear stream          : x fastest, then y, then z")
    print("C array semantic index       : array[ix][iy][iz]")
    print("C initializer text traversal : x outer, y middle, z inner")
    print(
        "mapping rule                  : "
        "n -> ix=n%NX, iy=(n//NX)%NY, iz=n//(NX*NY)"
    )
    print(
        "ordering verification         : "
        f"{'PASS' if values_ok else 'FAIL'}"
    )
    print("=" * 72)

    return passed


def main() -> int:
    try:
        return 0 if verify() else 1
    except (OSError, ValueError, VerificationError) as exc:
        print(f"verification error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
