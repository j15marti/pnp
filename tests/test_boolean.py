from pnp_lab.boolean import (
    anf_degree,
    coordinate_truth_tables,
    mask_to_truth_values,
    quadratic_product_span_rank,
    sparse_quadratic_relation,
)


def test_anf_degree_affine_and_quadratic():
    # x0 xor x1 on inputs 00,01,10,11 in integer index order.
    assert anf_degree([0, 1, 1, 0]) == 1
    # x0 AND x1.
    assert anf_degree([0, 0, 0, 1]) == 2


def test_affine_encoder_product_span_is_small():
    def encoder(u: int):
        x0 = u & 1
        x1 = (u >> 1) & 1
        return [x0, x1, x0 ^ x1]

    coords = coordinate_truth_tables(encoder, source_bits=2, output_bits=3)
    assert all(anf_degree(mask_to_truth_values(g, 4)) <= 1 for g in coords)
    assert quadratic_product_span_rank(coords, 4) <= 4
    assert sparse_quadratic_relation(coords, 4) is not None
