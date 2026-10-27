// LSPV-4 HEADMOVE-SELECT-AUTH143, pure JS deterministic reproducer.
// Run: node 2026-10-26_1940_HEADMOVE_SELECT_AUTH143_repro.js
// Scope: unindexed Select interface and exact model accounting, not a SAT lower bound.
function selectOne(bits, r) {
  let count = 0;
  for (let i = 0; i < bits.length; ++i) {
    count += bits[i];
    if (count === r) return i + 1;
  }
  throw Error("invalid select request");
}
function check(ok, label) { if (!ok) throw Error("failed: " + label); }
function run() {
  const counts = { exhaustive_select: 0, zero_input_sensitivity: 0,
    cache_controls: 0, one_tape_exponent: 0, jump_faces: 0, virtual_itinerary: 0 };
  const per_m = [];
  for (let m = 1; m <= 12; ++m) {
    for (let mask = 0; mask < (1 << m); ++mask) {
      const x = Array.from({length: m}, (_,i) => (mask >> i) & 1);
      const actual = selectOne(x.concat(Array(m).fill(1)), m);
      check(actual === 2*m - x.reduce((a,b)=>a+b,0), "select identity");
      counts.exhaustive_select++;
    }
    const zeros = Array(m).fill(0);
    check(selectOne(zeros.concat(Array(m).fill(1)),m)===2*m, "zero base");
    for (let i = 0; i < m; ++i) {
      const changed = zeros.slice();
      changed[i] = 1;
      check(selectOne(changed.concat(Array(m).fill(1)),m)===2*m-1, "sensitivity");
      counts.zero_input_sensitivity++;
    }
    per_m.push({m, inputs:1<<m, select_m_on_zeros:2*m, required_bit_probes:m});
  }
  for (const m of [1,3,5,8,12]) {
    for (const mask of [0,(1<<m)-1,Math.floor((1<<m)/3)]) {
      const x = Array.from({length:m}, (_,i)=>(mask>>i)&1);
      const cachedWeight=x.reduce((a,b)=>a+b,0);
      for (const q of [1,2,7,31]) {
        const answer=2*m-cachedWeight;
        for (let t=0;t<q;++t) check(answer===selectOne(x.concat(Array(m).fill(1)),m),"cache");
        counts.cache_controls++;
      }
    }
  }
  for (const [t,s] of [[1,0],[1.3,.5],[1,1.5],[1.4,.5]]) {
    const t1=t+Math.max(1,s), p1=Math.max(1,s);
    check(t1>=2 && p1>=1,"one-tape exponent ceiling");
    counts.one_tape_exponent++;
  }
  for (const [t,s,j,expected] of [[1.1,.4,.4,false],[1.2,.4,.4,true],
                                    [1,0,1,true],[1,1,0,true]]) {
    check((t+s+j>2-1e-9)===expected, "jump exponent");
    counts.jump_faces++;
  }
  const itineraries=[];
  for (const m of [1,2,3,4,8,16,32,64,128,256,512]) {
    const w=Math.ceil(Math.log2(15*m+1));
    const b=Math.max(32,Math.ceil(Math.log2(20*m+1)));
    const hdr=8+2*b, row=3*(w+1)+1, N=hdr+20*m*row, G=16*m*row;
    const addresses=[];
    for(let i=0;i<m;++i) addresses.push(hdr+2*i*row,hdr+18*m*row+2*i*row);
    const D=addresses.slice(1).reduce((sum,v,i)=>sum+Math.abs(v-addresses[i]),0);
    check(addresses.every(v=>v>=0&&v<N),"addresses");
    check(D>=m*G,"many virtual crossings");
    check(D<=(addresses.length+1)*N,"probe-to-path upper");
    counts.virtual_itinerary++;
    itineraries.push({m,N_bits:N,probes:2*m,middle_gap_bits:G,virtual_distance:D,
      indexed_probe_bit_time_upper:2*m*Math.ceil(Math.log2(N+1))**2});
  }
  const total_assertion_groups=Object.values(counts).reduce((a,b)=>a+b,0);
  check(total_assertion_groups===8347,"count guard");
  return {id:"HEADMOVE-SELECT-AUTH143",scope:"unindexed bitvector Select; virtual-source-access firewall; not a SAT lower bound",
    seed:"none; exhaustive",counts,total_assertion_groups,per_m,itineraries,
    status:"COMPUTATIONAL checks 0 failures; symbolic proofs in companion LaTeX report",
    known_limit:"No general 3CNF lower bound; no restriction on preprocessed or arithmetically indexed sources."};
}
if (typeof require !== "undefined" && require.main === module) console.log(JSON.stringify(run(),null,2));
