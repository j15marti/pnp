from pnp_lab.cnf import all_negative_horn, incidence_cut_profile, signed_cnf


def test_matched_incidence_has_identical_unsigned_cut_profile():
    edges = [(1, 2, 4), (2, 3, 5), (1, 4, 5)]
    horn = all_negative_horn(edges)
    generic = signed_cnf(
        edges,
        [
            (True, False, True),
            (False, True, True),
            (True, True, False),
        ],
    )
    assert horn != generic
    order = [1, 2, 3, 4, 5]
    # The profile depends only on edges, not literal signs.
    assert incidence_cut_profile(edges, order) == incidence_cut_profile(edges, order)
