#!/usr/bin/env python3
"""Adversarial byte-language audit of the exact published LSPV-3/509 compact checker."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time


def load_peer():
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent / "arc" / "lspv3_509_compact_source_bound.py",
        here.with_name("peer509_exact.py"),
    ]
    for path in candidates:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("peer509_exact", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise FileNotFoundError("exact LSPV-3/509 checker not found")


peer = load_peer()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("ascii")


def outcome(src, packet):
    try:
        return {"accepted": True, "result": peer.verify(src, packet)}
    except Exception as exc:
        return {"accepted": False, "exception": type(exc).__name__, "message": str(exc)}


def closed_schema_verify(src, packet):
    def strict_pairs(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate key")
            obj[key] = value
        return obj

    def reject_constant(token):
        raise ValueError("non-JSON numeric constant: " + token)

    obj = json.loads(
        packet.decode("ascii"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
    )
    if type(obj) is not dict or set(obj) != {"nodes", "root", "source_sha256"}:
        raise ValueError("top-level schema")
    if canonical(obj) != packet:
        raise ValueError("noncanonical packet")
    return peer.verify(src, packet)


def repaired_outcome(src, packet):
    try:
        return {"accepted": True, "result": closed_schema_verify(src, packet)}
    except Exception as exc:
        return {"accepted": False, "exception": type(exc).__name__, "message": str(exc)}


def main():
    started = time.perf_counter()
    src, packet = peer.family("K4")
    base = json.loads(packet)

    extra_scalar = dict(base)
    extra_scalar["calculus"] = "NOT-C_509"

    extra_shadow = dict(base)
    extra_shadow["source_sha256_shadow"] = "0" * 64

    extra_nested = dict(base)
    extra_nested["unchecked"] = {"claim": "false", "row": [1, 2, 3]}

    extra_nan = dict(base)
    extra_nan["unchecked"] = math.nan

    duplicate = packet[:-1] + b',"root":0}'
    source_mutation = src.replace(b"1 2 3 0\n", b"1 2 -3 0\n", 1)

    tests = {
        "baseline": (src, packet),
        "unknown_calculus_key": (src, canonical(extra_scalar)),
        "unknown_shadow_digest_key": (src, canonical(extra_shadow)),
        "unknown_nested_object": (src, canonical(extra_nested)),
        "unknown_nonstandard_NaN": (src, canonical(extra_nan)),
        "duplicate_root_member": (src, duplicate),
        "source_sign_mutation_without_digest_update": (source_mutation, packet),
    }
    mutation_bytes = {
        "baseline": "none",
        "unknown_calculus_key": 'top-level member: "calculus":"NOT-C_509"',
        "unknown_shadow_digest_key": 'top-level member: "source_sha256_shadow":"' + "0" * 64 + '"',
        "unknown_nested_object": 'top-level member: "unchecked":{"claim":"false","row":[1,2,3]}',
        "unknown_nonstandard_NaN": 'top-level member: "unchecked":NaN',
        "duplicate_root_member": 'appended duplicate member: "root":0',
        "source_sign_mutation_without_digest_update": "first exact source line 1 2 3 0 changed to 1 2 -3 0",
    }

    results = {}
    for name, (test_src, test_packet) in tests.items():
        results[name] = {
            **outcome(test_src, test_packet),
            "closed_schema_repair": repaired_outcome(test_src, test_packet),
            "packet_bytes": len(test_packet),
            "packet_sha256": hashlib.sha256(test_packet).hexdigest(),
            "source_sha256": hashlib.sha256(test_src).hexdigest(),
            "exact_mutation_bytes": mutation_bytes[name],
        }

    assert results["baseline"]["accepted"]
    assert results["unknown_calculus_key"]["accepted"]
    assert results["unknown_shadow_digest_key"]["accepted"]
    assert results["unknown_nested_object"]["accepted"]
    assert results["unknown_nonstandard_NaN"]["accepted"]
    assert not results["duplicate_root_member"]["accepted"]
    assert not results["source_sign_mutation_without_digest_update"]["accepted"]
    assert results["baseline"]["closed_schema_repair"]["accepted"]
    for name in (
        "unknown_calculus_key",
        "unknown_shadow_digest_key",
        "unknown_nested_object",
        "unknown_nonstandard_NaN",
        "duplicate_root_member",
        "source_sign_mutation_without_digest_update",
    ):
        assert not results[name]["closed_schema_repair"]["accepted"]

    record = {
        "experiment": "LSPV5_443_PEER509_CLOSED_SCHEMA_AUDIT",
        "status": "COMPUTATIONAL_EXACT_PUBLISHED_BLOB_REPLAY",
        "peer_git_blob": "9ed8ab48a2a280bce7a5c10c3da455573d0052a4",
        "peer_file_sha256": hashlib.sha256(open(peer.__file__, "rb").read()).hexdigest(),
        "finding": (
            "The exact C_509 compact checker rejects duplicate members and source mutation, "
            "but accepts canonical packets with arbitrary unchecked top-level members and "
            "also Python's non-RFC NaN token in an unchecked member. The used proof fields "
            "remain source-bound and sound in these controls; this is a closed-schema / "
            "accepted-byte-language gap, not a falsification of Theorem 509.1. The tested "
            "repair rejects nonstandard constants and requires the exact three top-level keys."
        ),
        "tests": results,
        "elapsed_seconds": time.perf_counter() - started,
        "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
