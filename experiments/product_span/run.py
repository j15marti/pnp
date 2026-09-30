#!/usr/bin/env python3
"""Small exact product-span laboratory.

The current executable mode is intentionally a toy affine encoder. It exists
to validate the GF(2)/ANF machinery before the exact SU/vMS construction is
transcribed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from pnp_lab.boolean import (
    anf_degree,
    coordinate_truth_tables,
    mask_to_truth_values,
    quadratic_product_span_rank,
    sparse_quadratic_relation,
)


def toy_affine_encoder(source_bits: int, outputs: int, seed: int):
    rng = random.Random(seed)
    masks = []
    constants = []
    for _ in range(outputs):
        mask = rng.randrange(1, 1 << source_bits) if source_bits else 0
        masks.append(mask)
        constants.append(rng.randrange(2))

    def encode(u: int) -> list[int]:
        return [((u & mask).bit_count() & 1) ^ c for mask, c in zip(masks, constants)]

    return encode, masks, constants


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--toy-affine", action="store_true")
    parser.add_argument("--source-bits", type=int, required=True)
    parser.add_argument("--outputs", type=int, required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    if not args.toy_affine:
        raise SystemExit(
            "No exact SU/vMS implementation is installed. "
            "Use --toy-affine only for the labeled sanity check."
        )

    encoder, masks, constants = toy_affine_encoder(
        args.source_bits, args.outputs, args.seed
    )
    table_size = 1 << args.source_bits
    coords = coordinate_truth_tables(encoder, args.source_bits, args.outputs)
    degrees = [
        anf_degree(mask_to_truth_values(g, table_size))
        for g in coords
    ]
    result = {
        "status": "COMPUTATIONAL",
        "model": "toy-affine-not-su-vms",
        "source_bits": args.source_bits,
        "outputs": args.outputs,
        "seed": args.seed,
        "affine_masks": masks,
        "affine_constants": constants,
        "coordinate_degrees": degrees,
        "product_span_rank": quadratic_product_span_rank(coords, table_size),
        "feature_count": 1 + args.outputs + args.outputs * (args.outputs - 1) // 2,
        "one_sparse_relation": sparse_quadratic_relation(coords, table_size),
    }

    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
