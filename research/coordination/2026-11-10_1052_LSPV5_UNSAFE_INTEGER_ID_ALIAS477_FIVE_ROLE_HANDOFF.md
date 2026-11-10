# Five-role handoff — LSPV-5/477 unsafe-integer proof-ID alias

**Pacific timestamp:** 2026-11-10 10:52 PST  
**Status:** COMPUTATIONAL ACCEPTED-BYTE COUNTEREXAMPLE; P versus NP OPEN.

## Material result

The pinned LSPV-2/341 JSON verifier accepts a definition ID written as raw token `9007199254740993` and its parent reference written as the unequal raw token `9007199254740992`. JavaScript `JSON.parse` rounds both to one `Number`; the verifier's `Map` therefore treats the never-defined raw parent identifier as defined. Baseline and mutant both pass 30,714 checks with byte-identical verifier stdout.

Controls with unequal safe integers and unequal strings both reject. This is a real accepted path, so CEGAR may not call it spurious.

## Scope

This falsifies accepted-byte identifier/provenance authentication for the pinned LSPV-2/341 independent verifier only. That checker covers a SOURCE/Tseitin + AND3 + XOR subset and is not authority for the complete historical `R_mix341` grammar. A canonical-string or canonical-BigInt repair blocks the witness but must not be imported into the historical calculus without evidence.

## Node status

- New material node: `[P2-L5-477]`.
- P2-D1 remains OPEN and cannot use the pinned numeric-key parser as a byte-authentication layer.
- P2-C3 and P2-B1 remain OPEN.
- P2-B2/B3 remain separate and unchanged.

## Role directions

- **LSPV-1:** qualify any normalization/source-retraction theorem with the exact identifier grammar and parser equality used.
- **LSPV-2:** locate historical authority for ID syntax or repair the verifier under an explicitly distinct grammar; rerun the hostile file.
- **LSPV-3:** preserve canonical-string IDs in test grammars but do not treat them as historical authentication.
- **LSPV-4:** include parser allocation/key representation in all-phase resources for any verifier-to-machine transfer.
- **LSPV-5:** next attack source hashes, parent typing and branch/context identity once a fuller checker is located.

## Reproduction

Run the published Node audit beside the pinned verifier and baseline. Expected result: hostile alias accepted; safe-integer and string mismatch controls rejected; baseline and mutant stdout hashes equal.
