# RP-BLOCK-SPECTRAL7 | 2026-10-21

STATUS: ESTABLISHED only for explicitly promised bounded block-state and local Fourier-spectrum RP verifiers. P=RP, P!=RP and P!=NP remain OPEN.

Theorem: Suppose a uniform RP verifier uses independent consecutive random blocks and at most w(n)=poly(n) explicitly enumerable states between ell(n)=poly(n) blocks. Every deterministic block transition is total, exact, uniform polynomial-time, and depends on earlier random blocks only via the boundary state. Every transition indicator has Fourier spectral L1 at most a known polynomial B(n). Then a deterministic polynomial-time layered reachability algorithm, using an explicit finite-field trace small-bias set at every block, decides the language and reconstructs an accepting tape for every YES input.
