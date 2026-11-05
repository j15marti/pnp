# WC-0001: The bridge dilemma for worst-case derivation cost
Setting: R a Cook-Reckhow system (poly-time checkable proofs), cost_R = proof size (or checker time).

**Prop 1 (weak systems).** If W_R(N) >= 2^{N^eps} unconditionally (Resolution: Haken 1985; Urquhart; Ben-Sasson-Wigderson 2001;
cutting planes: Pudlak 1997; bounded-depth Frege: Ajtai, Krajicek-Pudlak-Woods, Pitassi-Beame-Impagliazzo),
then B_R := (SAT in P => W_R poly) is equivalent to (SAT not in P), since its consequent is false. Status: KNOWN THEOREM + trivial logic.

**Prop 2 (optimal system).** If O is an optimal proof system (p-simulates all), then SAT in P => NP = coNP => some p-bounded system
exists => O p-bounded, so B_O holds. And W_O superpoly <=> NP != coNP (Cook-Reckhow 1979). Existence of O: open
(Krajicek-Pudlak 1989: exists if NE = coNE). Status: KNOWN THEOREM.

**Cor.** Any fixed-R worst-case lower bound that is *sufficient* for P != NP via a bridge of this form, with R Cook-Reckhow
and cost = length, yields NP != coNP when R is strong enough for the bridge to be nontrivial. So the route is at least as hard as
NP != coNP; Frege/EF lower bounds are open and regarded as barrier-level hard. Free strategy search is nondeterminism and is exactly why.

**Consequence for the program.** To target P vs NP specifically, cost_R must include a component that a P algorithm can keep small but a
nondeterministic certificate cannot (e.g. simultaneous time-space of a *uniform deterministic* derivation, not just checkable size). That
is the existing ARC/FLMV spine; the new constraint is that the bridge must be proved for that cost, not for length. OPEN.
Sources: Cook-Reckhow 1979; Krajicek-Pudlak 1989; https://theoryofcomputing.org/articles/v022a004/ ; https://msekce.karlin.mff.cuni.cz/~krajicek/frege.pdf
END_OF_VERIFIED_REPORT::CLAUDE::WC-0001
