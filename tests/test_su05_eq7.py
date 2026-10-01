from pnp_lab.su05_eq7 import (
    construct_maximal_orbit_minor,
    modulo_seed_coordinate_anf_degrees,
    scan_boolean_grid_interpolants,
)


def test_su05_eq7_constructs_full_quadratic_minor():
    result = construct_maximal_orbit_minor(2, 17)
    assert result["feature_count"] == 4
    assert result["rank"] == 4
    assert result["is_maximal_rank"] is True
    assert result["polynomial_degree"] == 7


def test_boolean_grid_scan_small_case_is_maximal_off_constants():
    result = scan_boolean_grid_interpolants(7, 4, 4)
    assert result["feature_count"] == 11
    assert result["rank_distribution"] == {1: 1, 2: 1, 11: 14}
    assert result["all_nonconstant_messages_maximal_rank"] is True


def test_modulo_wrapper_anf_stress_control():
    result = modulo_seed_coordinate_anf_degrees(
        7, 4, 4, [0, 0, 0, 1]
    )
    assert result["source_bits"] == 6
    assert result["coordinate_anf_degrees"] == [3, 3, 3, 3]
