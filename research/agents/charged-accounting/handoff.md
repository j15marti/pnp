# Charged Accounting handoff

21 November 2026, 22:45 PST. [DYNAMIC-PAID-BACKDOOR-LEDGER1](PNP_Charged_accounting_2026-11-21_224500_Paid_Backdoor_Ledger.md). KNOWN THEOREM for strong 2-CNF backdoor acquisition, PROVED/EXACT restricted integration with the current canonical Boolean encoding and one-tape execution. Independent review pending.

A fixed correct solver authenticates the original N-bit input, iteratively searches for a ternary hitting set, and solves at most 2^h binary residuals. Failed searches through minimum size h use fewer than 9*3^h/4 nodes. Full same-execution upper bounds are T=O(3^h N^5), S=O(N), physical CM=O(3^h N^6), descriptive CM separately O(3^h N^6). For any fixed C, h<=C log2 N yields time O(N^(5+C log2 3)). This is a known backdoor method with a new current-encoding ledger, not a new general SAT algorithm. October BACKDOOR-PRODUCT-FIREWALL97 already records the method and large-h cheap controls.

On Construction's two-hub family h<=2, so the paid shortcut is polynomial. Succinct k/label input replay sharpens descriptive CM to Theta_A(T log(T+2)), hence O(N^5 log N), while physical CM remains O(N^6). Full original input is charged physically throughout retention.

Actual READY event has U=answer, B=public equal-prior pair/A/k, Pi=one bit, E=one real read, b=1,h_framing=0,rho=1. Duplicating that obligation q times sets rho=q and still gives just one event. No further private-prefix service follows from correctness. Prior first-passage obligations remain historical prefix charges.

[Audit](../../../experiments/dynamic_accounting_paid_backdoor_20261121.py), [raw](../../../results/raw/dynamic_accounting_paid_backdoor_20261121.json). New 1024 finite restriction/acquisition cases, six maximal failed searches and four exact cache-overlap checks. No compiler rerun or TM timing. P versus NP OPEN.

ONE next dependency to Discovery/Construction, with Bounds/Synthesis integration and Redteam review: broader decision-safe representation with a proved polynomial acquisition bound, or actual reachable post-READY obligation beyond the cached label. Large minimum syntactic h alone is insufficient. Prior [star first-passage report](PNP_Charged_accounting_2026-11-21_214300_Star_First_Passage.md) retains its scope.
