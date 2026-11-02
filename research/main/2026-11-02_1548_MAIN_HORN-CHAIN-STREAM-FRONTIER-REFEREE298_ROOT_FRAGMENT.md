## LSPV-5 REFEREE298: exact Horn-chain streaming frontier

For

$$
F_n=(x_1)\land\bigwedge_{i=1}^{n-1}(\neg x_i\lor x_{i+1})\land(\neg x_n),
$$

all $n+1$ sources are indispensable.  In the unchanged binary-premise
$R_{\mathrm{mix341}}$, source ancestry forces at least $n$ charged nodes and
the unit-propagation Resolution chain attains them:

$$
W_{R_{\mathrm{mix341}}}(F_n)=n.
$$

In the separately declared load-plus-inference schedule model, the exact
frontier is $Q_{\min}=2n+1$ at minimum live-record capacity three.  Canonical
ordered input permits $O(N)$-time, $O(\log N)$-writable-space streaming.  Thus
logical DAG size is not itself a comparable peak-space lower bound.  The
same-shape last-sign flip is SAT; all source deletions, eight malformed inputs
and three corrupt proofs passed, with 1,121,543 independent assertion groups.
This yields only a linear encoded-length lower bound and proves none of B1,
B2 or B3.  P versus NP remains open.

