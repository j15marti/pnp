# RP-CYCLE-SPECTRAL10 | 2026-10-21

ESTABLISHED (restricted): For input x of length v>=3, sample uniform bits z on edges of complete graph K_v and accept iff x[0]=1 and its binary vertex-edge incidence matrix H satisfies Hz!=0. RP YES probability 1-2^(-(v-1))>=3/4; all NO tapes reject. The verifier runs in O(v^2) time, O(v) workspace, m=v(v-1)/2 random bits, no advice.

Fourier: normalized acceptance spectrum has L1 exactly 2-2^(2-v)<2. OBDD: for any random-bit ordering, the middle prefix/suffix graphic-matroid intersection has rank at least rho(e)=ceil((sqrt(1+8e)-1)/2) for e=floor(m/2), so every exact OBDD has width at least 2^rho(e), exponential in v. The bound is sharp at the middle layer.

Independent finite audit: all 359426 balanced edge partitions for v=3..7, zero rank violations; exact Fourier norms checked for v=3..6. P vs RP remains OPEN. The :12 replay-footprint theorem is not contradicted because this verifier has exponentially many possible parity-register configurations, despite reading every tape bit once.

NEXT: seek a uniform polynomial-time equivalent-verifier spectral-norm bound for every RP machine; neither OBDD nor Fourier norms individually characterize language hardness. Detailed local report and script preserved, not published here.
