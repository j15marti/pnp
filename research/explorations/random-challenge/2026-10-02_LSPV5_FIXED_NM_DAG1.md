# LSPV-5 fixed-(n,m) universal 3-CNF classifier experiment

Status: COMPUTATIONAL EXACT for enumeration/semantic counts; UPPER BOUNDS for ordered decision-DAG node counts. P versus NP remains OPEN.

## Scope

Simple genuine 3-CNF only: three distinct variables per clause and no duplicate clauses. For n=3 there are only eight distinct clauses, so D(3,9), D(3,10), and D(3,11) do not exist in this simple-CNF model. D(3,8) contains the unique set of all eight clauses and is constant UNSAT.

For n=4 there are 32 possible clauses. Exact dynamic programming over unions of clause-falsifying Q4 edges was used for m=8 through 11.

## Exact counts

| n | m | raw formulas | semantic functions | UNSAT | SAT |
|---|---:|---:|---:|---:|---:|
| 4 | 8 | 10,518,300 | 29,417 | 272 | 10,518,028 |
| 4 | 9 | 28,048,800 | 24,573 | 15,936 | 28,032,864 |
| 4 | 10 | 64,512,240 | 20,413 | 264,032 | 64,248,208 |
| 4 | 11 | 129,024,480 | 15,997 | 2,118,080 | 126,906,400 |

Semantic diversity decreases monotonically across this range even as the UNSAT population grows rapidly.

## Ordered reduced decision-DAG upper bounds

Clause-presence inputs are queried with the promise that exactly m of the 32 clause bits are selected. Reduction merges identical residual classifier behavior. These counts are exact for the stated fixed query order but are not proven global minima.

| m | grouped by omitted variable | sign round-robin | Gray round-robin |
|---:|---:|---:|---:|
| 8 | 1,890 | 720 | 1,094 |
| 9 | 17,470 | 2,776 | 4,807 |
| 10 | 55,513 | 5,342 | 9,691 |
| 11 | 96,644 | 7,771 | 14,458 |

The sign-round-robin order is best among these tested orders. The resulting upper-bound sequence is 720, 2776, 5342, 7771.

## Interpretation and guardrails

The decrease in semantic-function count does not imply a decrease in this ordered query model's classifier size. Conversely, these growing ordered-DAG counts are not circuit lower bounds. An adaptive decision DAG may be smaller, and an unrestricted Boolean circuit may exploit intermediate functions unavailable to clause-query DAGs.

The next exact target is a certificate-producing adaptive minimizer over canonical residual classifier functions. A valid lower-bound certificate must establish optimality over every legal next query and account correctly for DAG sharing; merely testing many query orders is insufficient.

D(3,8) is retained as a constant-UNSAT regression control. D(3,9..11) are excluded rather than treated as new problems because duplicates are unavoidable and semantically redundant in the simple-CNF model.

END_OF_NOTE::FIXED_NM_DAG1
