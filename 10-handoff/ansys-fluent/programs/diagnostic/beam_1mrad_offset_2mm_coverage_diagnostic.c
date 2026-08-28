#include "udf.h"
#include <stdio.h>

#include "beam_1mrad_offset_2mm_heat_deposition.h"

#define HD_NX BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_NX
#define HD_NY BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_NY
#define HD_NZ BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_NZ

#define HD_X_MIN_CM BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_X_MIN_CM
#define HD_X_MAX_CM BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_X_MAX_CM
#define HD_Y_MIN_CM BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_Y_MIN_CM
#define HD_Y_MAX_CM BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_Y_MAX_CM
#define HD_Z_MIN_CM BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_Z_MIN_CM
#define HD_Z_MAX_CM BEAM_1MRAD_OFFSET_2MM_HEAT_DEPOSITION_Z_MAX_CM

#define HEAT_SOURCE_SCALE_W_M3 5.0e12
#define FLUKA_VOXEL_VOLUME_M3 1.0e-6
#define VOLUME_MATCH_LOW 0.99e-6
#define VOLUME_MATCH_HIGH 1.01e-6

static real mapped_volume_m3[HD_NX][HD_NY][HD_NZ];
static long mapped_cell_count[HD_NX][HD_NY][HD_NZ];

static int map_centroid_to_voxel(
    const real centroid[ND_ND],
    int *ix,
    int *iy,
    int *iz
)
{
    real x_cm;
    real y_cm;
    real z_cm;
    real dx_cm;
    real dy_cm;
    real dz_cm;

    x_cm = centroid[0] * 100.0;
    y_cm = centroid[1] * 100.0;
    z_cm = centroid[2] * 100.0;

    if (
        x_cm < HD_X_MIN_CM || x_cm >= HD_X_MAX_CM ||
        y_cm < HD_Y_MIN_CM || y_cm >= HD_Y_MAX_CM ||
        z_cm < HD_Z_MIN_CM || z_cm >= HD_Z_MAX_CM
    ) {
        return 0;
    }

    dx_cm = (HD_X_MAX_CM - HD_X_MIN_CM) / (real) HD_NX;
    dy_cm = (HD_Y_MAX_CM - HD_Y_MIN_CM) / (real) HD_NY;
    dz_cm = (HD_Z_MAX_CM - HD_Z_MIN_CM) / (real) HD_NZ;

    *ix = (int) ((x_cm - HD_X_MIN_CM) / dx_cm);
    *iy = (int) ((y_cm - HD_Y_MIN_CM) / dy_cm);
    *iz = (int) ((z_cm - HD_Z_MIN_CM) / dz_cm);

    if (
        *ix < 0 || *ix >= HD_NX ||
        *iy < 0 || *iy >= HD_NY ||
        *iz < 0 || *iz >= HD_NZ
    ) {
        return 0;
    }

    return 1;
}

DEFINE_ON_DEMAND(report_heat_source_coverage)
{
#if RP_HOST
    Message("Coverage diagnostic must be executed in serial Fluent.\n");
    return;
#elif RP_NODE
    return;
#else
    Domain *domain;
    Thread *thread;
    cell_t cell;
    real centroid[ND_ND];
    real volume_m3;
    real source_w_m3;
    real zone_total_volume_m3;
    real zone_in_box_volume_m3;
    real zone_power_w;
    real total_cell_volume_m3;
    real total_in_box_volume_m3;
    real total_mapped_power_w;
    real total_expected_power_w;
    real total_power_difference_w;
    real uncovered_expected_power_w;
    real undercovered_deficit_w;
    real overcovered_excess_w;
    real expected_voxel_power_w;
    real mapped_voxel_power_w;
    real difference_w;
    real recovery_ratio;
    real dx_cm;
    real dy_cm;
    real dz_cm;
    real x_center_cm;
    real y_center_cm;
    real z_center_cm;
    long zone_total_cells;
    long zone_in_box_cells;
    long total_cells;
    long total_in_box_cells;
    long total_outside_box_cells;
    long uncovered_voxels;
    long undercovered_voxels;
    long matched_voxels;
    long overcovered_voxels;
    int ix;
    int iy;
    int iz;
    FILE *csv;

    domain = Get_Domain(1);

    total_cells = 0;
    total_in_box_cells = 0;
    total_outside_box_cells = 0;
    total_cell_volume_m3 = 0.0;
    total_in_box_volume_m3 = 0.0;
    total_mapped_power_w = 0.0;

    uncovered_voxels = 0;
    undercovered_voxels = 0;
    matched_voxels = 0;
    overcovered_voxels = 0;

    uncovered_expected_power_w = 0.0;
    undercovered_deficit_w = 0.0;
    overcovered_excess_w = 0.0;

    for (ix = 0; ix < HD_NX; ++ix) {
        for (iy = 0; iy < HD_NY; ++iy) {
            for (iz = 0; iz < HD_NZ; ++iz) {
                mapped_volume_m3[ix][iy][iz] = 0.0;
                mapped_cell_count[ix][iy][iz] = 0;
            }
        }
    }

    Message("\n");
    Message("============================================================\n");
    Message("FLUKA-TO-FLUENT VOXEL COVERAGE DIAGNOSTIC (SERIAL)\n");
    Message("============================================================\n");

    thread_loop_c(thread, domain) {
        zone_total_cells = 0;
        zone_in_box_cells = 0;
        zone_total_volume_m3 = 0.0;
        zone_in_box_volume_m3 = 0.0;
        zone_power_w = 0.0;

        begin_c_loop(cell, thread) {
            ++zone_total_cells;
            ++total_cells;

            volume_m3 = C_VOLUME(cell, thread);
            zone_total_volume_m3 += volume_m3;
            total_cell_volume_m3 += volume_m3;

            C_CENTROID(centroid, cell, thread);

            if (map_centroid_to_voxel(centroid, &ix, &iy, &iz)) {
                ++zone_in_box_cells;
                ++total_in_box_cells;

                zone_in_box_volume_m3 += volume_m3;
                total_in_box_volume_m3 += volume_m3;

                mapped_volume_m3[ix][iy][iz] += volume_m3;
                mapped_cell_count[ix][iy][iz] += 1;

                source_w_m3 =
                    beam_1mrad_offset_2mm_heat_deposition[ix][iy][iz]
                    * HEAT_SOURCE_SCALE_W_M3;

                zone_power_w += source_w_m3 * volume_m3;
                total_mapped_power_w += source_w_m3 * volume_m3;
            } else {
                ++total_outside_box_cells;
            }
        }
        end_c_loop(cell, thread)

        Message(
            "zone=%d total_cells=%ld in_box_cells=%ld "
            "total_volume_m3=%.16e in_box_volume_m3=%.16e "
            "mapped_power_W=%.16e\n",
            THREAD_ID(thread),
            zone_total_cells,
            zone_in_box_cells,
            zone_total_volume_m3,
            zone_in_box_volume_m3,
            zone_power_w
        );
    }

    total_expected_power_w = 0.0;

    for (ix = 0; ix < HD_NX; ++ix) {
        for (iy = 0; iy < HD_NY; ++iy) {
            for (iz = 0; iz < HD_NZ; ++iz) {
                expected_voxel_power_w =
                    beam_1mrad_offset_2mm_heat_deposition[ix][iy][iz]
                    * HEAT_SOURCE_SCALE_W_M3
                    * FLUKA_VOXEL_VOLUME_M3;

                mapped_voxel_power_w =
                    beam_1mrad_offset_2mm_heat_deposition[ix][iy][iz]
                    * HEAT_SOURCE_SCALE_W_M3
                    * mapped_volume_m3[ix][iy][iz];

                total_expected_power_w += expected_voxel_power_w;

                if (mapped_volume_m3[ix][iy][iz] <= 0.0) {
                    ++uncovered_voxels;
                    uncovered_expected_power_w += expected_voxel_power_w;
                } else if (mapped_volume_m3[ix][iy][iz] < VOLUME_MATCH_LOW) {
                    ++undercovered_voxels;
                    difference_w = expected_voxel_power_w - mapped_voxel_power_w;
                    if (difference_w > 0.0) {
                        undercovered_deficit_w += difference_w;
                    }
                } else if (mapped_volume_m3[ix][iy][iz] <= VOLUME_MATCH_HIGH) {
                    ++matched_voxels;
                } else {
                    ++overcovered_voxels;
                    difference_w = mapped_voxel_power_w - expected_voxel_power_w;
                    if (difference_w > 0.0) {
                        overcovered_excess_w += difference_w;
                    }
                }
            }
        }
    }

    total_power_difference_w = total_expected_power_w - total_mapped_power_w;
    recovery_ratio = 0.0;
    if (total_expected_power_w != 0.0) {
        recovery_ratio = total_mapped_power_w / total_expected_power_w;
    }

    Message("------------------------------------------------------------\n");
    Message("total_cells=%ld\n", total_cells);
    Message("total_in_box_cells=%ld\n", total_in_box_cells);
    Message("total_outside_box_cells=%ld\n", total_outside_box_cells);
    Message("total_cell_volume_m3=%.16e\n", total_cell_volume_m3);
    Message("total_in_box_volume_m3=%.16e\n", total_in_box_volume_m3);
    Message("expected_FLUKA_power_W=%.16e\n", total_expected_power_w);
    Message("mapped_Fluent_power_W=%.16e\n", total_mapped_power_w);
    Message("power_difference_W=%.16e\n", total_power_difference_w);
    Message("recovery_ratio=%.16e\n", recovery_ratio);
    Message("------------------------------------------------------------\n");
    Message("uncovered_voxels=%ld\n", uncovered_voxels);
    Message("undercovered_voxels=%ld\n", undercovered_voxels);
    Message("matched_voxels=%ld\n", matched_voxels);
    Message("overcovered_voxels=%ld\n", overcovered_voxels);
    Message("uncovered_expected_power_W=%.16e\n", uncovered_expected_power_w);
    Message("undercovered_deficit_W=%.16e\n", undercovered_deficit_w);
    Message("overcovered_excess_W=%.16e\n", overcovered_excess_w);

    csv = fopen("beam_1mrad_offset_2mm_coverage.csv", "w");

    if (csv == NULL) {
        Message("ERROR: cannot create coverage CSV in Fluent working directory.\n");
        Message("============================================================\n");
        return;
    }

    fprintf(
        csv,
        "ix,iy,iz,x_center_cm,y_center_cm,z_center_cm,"
        "raw_heat_deposition,expected_power_W,mapped_cell_count,"
        "mapped_volume_m3,mapped_power_W,recovery_ratio,power_difference_W\n"
    );

    dx_cm = (HD_X_MAX_CM - HD_X_MIN_CM) / (real) HD_NX;
    dy_cm = (HD_Y_MAX_CM - HD_Y_MIN_CM) / (real) HD_NY;
    dz_cm = (HD_Z_MAX_CM - HD_Z_MIN_CM) / (real) HD_NZ;

    for (ix = 0; ix < HD_NX; ++ix) {
        x_center_cm = HD_X_MIN_CM + ((real) ix + 0.5) * dx_cm;

        for (iy = 0; iy < HD_NY; ++iy) {
            y_center_cm = HD_Y_MIN_CM + ((real) iy + 0.5) * dy_cm;

            for (iz = 0; iz < HD_NZ; ++iz) {
                z_center_cm = HD_Z_MIN_CM + ((real) iz + 0.5) * dz_cm;

                expected_voxel_power_w =
                    beam_1mrad_offset_2mm_heat_deposition[ix][iy][iz]
                    * HEAT_SOURCE_SCALE_W_M3
                    * FLUKA_VOXEL_VOLUME_M3;

                mapped_voxel_power_w =
                    beam_1mrad_offset_2mm_heat_deposition[ix][iy][iz]
                    * HEAT_SOURCE_SCALE_W_M3
                    * mapped_volume_m3[ix][iy][iz];

                recovery_ratio = 0.0;
                if (expected_voxel_power_w != 0.0) {
                    recovery_ratio =
                        mapped_voxel_power_w / expected_voxel_power_w;
                }

                difference_w = expected_voxel_power_w - mapped_voxel_power_w;

                fprintf(
                    csv,
                    "%d,%d,%d,%.8e,%.8e,%.8e,%.16e,%.16e,%ld,"
                    "%.16e,%.16e,%.16e,%.16e\n",
                    ix,
                    iy,
                    iz,
                    x_center_cm,
                    y_center_cm,
                    z_center_cm,
                    beam_1mrad_offset_2mm_heat_deposition[ix][iy][iz],
                    expected_voxel_power_w,
                    mapped_cell_count[ix][iy][iz],
                    mapped_volume_m3[ix][iy][iz],
                    mapped_voxel_power_w,
                    recovery_ratio,
                    difference_w
                );
            }
        }
    }

    fclose(csv);

    Message("CSV written: beam_1mrad_offset_2mm_coverage.csv\n");
    Message("============================================================\n");
#endif
}
