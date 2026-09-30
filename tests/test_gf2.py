from pnp_lab.gf2 import dependent_subset, rank_bitvectors


def test_rank_bitvectors():
    assert rank_bitvectors([0b001, 0b010, 0b011]) == 2
    assert rank_bitvectors([0, 0]) == 0
    assert rank_bitvectors([0b101, 0b010, 0b111]) == 2


def test_dependent_subset():
    vectors = [0b001, 0b010, 0b011]
    relation = dependent_subset(vectors)
    assert relation is not None
    value = 0
    for i in relation:
        value ^= vectors[i]
    assert value == 0
    assert relation
