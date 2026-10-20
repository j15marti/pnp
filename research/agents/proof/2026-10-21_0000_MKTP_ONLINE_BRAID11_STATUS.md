# MKTP-ONLINE-BRAID11 | 2026-10-21 00:00 Asia/Seoul

Status: TWO EXPLICIT REDUCTION CANDIDATES FALSIFIED. P versus NP is OPEN.

Fixed k=1024, p(M)=max(ceil(log2 M),ceil(M^(1/1024))), M=B_N=sum_{j=1}^N ceil(j^(1/5))=N^(6/5+o(1)).

Candidate A, one-way ONLINE-BRAID: each source bit x_j yields r_j=ceil(j^(1/5)) output bits. Its first output bit is x_j; other bits are a nonlinear function of x_j, x_(j+1), j and output index. B_j=r*j-sum_{h=1}^{r-1}h^5, r=ceil(j^(1/5)), permits exact polylog-time indexing. The physical transducer makes N source reads and one EOF check, writes exactly M bits, uses O(log N) work space and O(M log^2 N) bit time on one work tape, with only first/current/lookahead source bits retained.

Falsifier A1: explicitly constructible SAT formulas S_m (repeated positive 3-clauses) and UNSAT U_m (complete eight-clause 3-variable contradiction and padding) both have source-free polylog-time indexed target programs, so ordinary KT is polylog(N), beneath p(M) asymptotically on both labels. The 8-clause core is minimally UNSAT; 24 one-sign flips and five long-common-prefix continuation pairs independently tested.

Falsifier A2: for either fixed SAT label, encode an arbitrary r-bit independent payload in otherwise irrelevant proper 3-CNF clauses. N=Theta(r log r) and the audited target recovers each source bit at B_(j-1). Each padding orbit has 2^r distinct targets. At most 2^(p+1) length-M outputs have KT<=p. Therefore for uniformly random payload Pr[KT(output)<=p] <= 2^(p+1-r). In finite parameter r=32: N=1069, M=4045, p=12, upper bound 2^-19. Counting establishes existence, not an explicit high-KT string.

Candidate B, EVAL-SAMPLER: q=ceil(N^(1/5)) assignments are actually evaluated against the complete formula; output bits select cached evaluation plus a public index mask. Source reads (q+1)N; physical head moves (2q+1)N including q full rewinds; O(q+log N) working bits, O((qN+M)polylog N) time. Equal-sized unique-SAT and UNSAT proper 3CNFs yield identical all-zero sample traces and exactly identical target words, so this contractor fails semantics before any KT claim.

Audits: 7,312 assertions for candidate A; 1,880 for B; zero failed. Full local report/scripts/raw results are in the conversation artifacts, not included in this commit.

Source alignment: MMW STOC 2019 Theorem 4.2 provides O(Mp) time/O(p) space with Sigma_3SAT oracle queries O(p); at fixed k=1024 the oracle-step exponent is 1.201171875, but an unknown polynomial PH simulator may exceed 1.205. OPS is for specific gap/promise models; CHMY uses randomized one-way-input one-work-tape MCSP; Ilango 2026 proves a random-oracle reduction. None supplies the missing uniform all-input both-label ordinary MKTP semantics.

OPEN arrow: Construct a nonrecoverable, syntax-aware, all-input SAT-to-ordinary-indexed-MKTP target that defeats both irrelevant-payload and unique-witness sampling tests, with a genuine high-KT proof on the required label.

References:
https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf
https://toc.ilab.sztaki.hu/articles/v017a011/index.html
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
https://epubs.siam.org/doi/abs/10.1137/24M1652568
