# DIGEST-GATE17
Date: 2026-10-21 10:00 Asia/Seoul.
Scientific status: FAIL for tested indexed-key construction; P versus NP OPEN.

A one-pass deterministic SAT-input transducer hashes its input to a fixed 256-bit key, then emits M=N^(6/5+o(1)) bits by evaluating SHA-256(key,index). Its threshold is p=max(log M,ceil(M^(1/241))). A 256-bit key and the short indexed decoder give each output ordinary KT of polylog(M), hence every output is LOW for sufficiently large inputs. Resource accounting passes: O(N+M polylog M) time and O(log N) workspace. A perfect SAT-label and witness tag before hashing does not fix this.

Executed audit: 102,520 assertions, zero failures, 11 ordinary CNF inputs, 4 physical streaming files, all indexed bits verified. Minimal UNSAT and INDEX-continuation controls passed. A true all-input SAT-to-ordinary-MKTP separation remains OPEN.

Full executable and raw data: local package DIGEST_GATE17_PACKAGE.zip, pending GitHub synchronization.
