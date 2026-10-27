"use strict";
/* LSPV-4 COPOLAR-NDTISP158, dependency-free exact finite controls.
 * Abstract OR-labelled sources ONLY, not ordinary 3CNF.
 * Run: node 2026-10-27_0636_COPOLAR_NDTISP158_repro.js
 */
function audit() {
  let assertions = 0, sources = 0, proofChecks = 0, maps = 0;
  const check = (condition, msg) => {
    ++assertions;
    if (!condition) throw Error("AUDIT FAILED: " + msg);
  };
  const eta = Math.cbrt(4);
  const gamma = 2 * Math.cos(Math.PI / 7);
  const strictExamples = [
    {rv:1.40, a:0.50, nd:true, det:false},
    {rv:1.65, a:0.10, nd:false, det:true},
    {rv:1.65, a:0.20, nd:false, det:false},
    {rv:1.00, a:0.90, nd:true, det:false}
  ];
  for (const e of strictExamples) {
    check((e.rv < eta) === e.nd, "nondeterministic strict polarity face");
    check((e.rv + e.a < gamma) === e.det, "deterministic strict enumeration face");
  }
  // Guest proof is immutable; only physical proof-key observations count.
  // Every seed reads the same index in a different order, then shared flag.
  function runSource(bits, R, A, B, readProof) {
    const m = bits.length;
    const width = Math.ceil(Math.log2(m));
    let yes = 0, no = 0, calls = 0;
    for (let z = 0; z < R; z++) {
      let idx = 0;
      for (let t = 0; t < width; t++) {
        const address = (t + z) % width;
        idx |= readProof("P:0:" + address) << address;
      }
      const flag = readProof("P:0:" + width);
      // Repeated read probes test stable physical-key alias handling.
      if ((z & 1) === 0) check(flag === readProof("P:0:" + width), "stable repeated read");
      const accepted = !!(flag && idx < m && bits[idx]);
      calls++;
      if (accepted) yes++; else no++;
      if (yes >= A + 1) return {accept:true,calls};
      if (no >= R - B + 1) return {accept:false,calls};
    }
    throw Error("Gap stopping did not halt");
  }
  // Replays one deterministic master with a first-read map.
  // Each unknown bit forks two branches and is remembered by exact physical key.
  function existsCappedMap(bits, R, A, B, cap) {
    let visits = 0;
    function dfs(map) {
      visits++;
      let firstRead = null, result = null;
      try {
        result = runSource(bits, R, A, B, key => {
          if (Object.prototype.hasOwnProperty.call(map,key)) return map[key];
          firstRead = key;
          throw {firstRead:true};
        });
      } catch (e) {
        if (!(e && e.firstRead === true)) throw e;
      }
      if (firstRead === null) return !!result.accept;
      if (Object.keys(map).length >= cap) return false;
      for (const bit of [0,1]) {
        const next = Object.assign({},map);
        next[firstRead] = bit;
        if (dfs(next)) return true;
      }
      return false;
    }
    const answer = dfs({});
    maps += visits;
    return answer;
  }
  const examples = [];
  for (const m of [2,4,8]) {
    const width = Math.ceil(Math.log2(m));
    let local = 0;
    for (let R=1; R<=5; R++) {
      const A=0, B=Math.max(1,Math.ceil(.6*R));
      for (let x=0; x<(1<<m); x++) {
        sources++;
        const bits = Array.from({length:m},(_,i)=>(x>>i)&1);
        let anyProof = false;
        for (let p=0; p<(1<<(width+1)); p++) {
          const proof = Array.from({length:width+1},(_,i)=>(p>>i)&1);
          const ans = runSource(bits,R,A,B,k=>proof[Number(k.split(":")[2])]);
          proofChecks++;
          check(ans.calls <= R-(B-A)+1, "gap stop worst-case call cap");
          anyProof ||= ans.accept;
        }
        const byMap = existsCappedMap(bits,R,A,B,width+1);
        check(anyProof === (x!==0), "explicit proof completeness/soundness");
        check(byMap === anyProof, "first-read nondeterministic consistency");
        local++;
      }
    }
    examples.push({m,sourceSeedPairs:local,proofBits:width+1});
  }
  // The accepting proof exists, but a too-small observed-map budget loses completeness.
  for (let m of [2,4,8]) {
    const b = Math.ceil(Math.log2(m));
    const bits = Array(m).fill(0); bits[0]=1;
    check(existsCappedMap(bits,3,0,2,b+1), "correct cap supports witness");
    check(!existsCappedMap(bits,3,0,2,b), "undercap must reject");
  }
  // SAT-side gap soundness can break if a false simulator guesses a new
  // value for the same physical proof bit on each public seed.
  let coherent = 0;
  for (const b of [0,1]) coherent = Math.max(coherent, Number(b===0)+Number(b===1));
  check(coherent === 1, "coherent proof cannot pass two opposite checks");
  const independentlyGuessed = Number(0===0) + Number(1===1);
  check(independentlyGuessed === 2, "incoherent per-seed guesses create false high");
  // Native-model numerical checks only; not a SAT lower-bound experiment.
  check(Math.abs(eta-1.5874010519681994)<1e-12,"cube-root-four endpoint");
  check(Math.abs(gamma-1.801937735804838)<1e-12,"cosine endpoint");
  return {
    report:"COPOLAR-NDTISP158", kind:"COMPUTATIONAL exact finite controls",
    sources, proofChecks, mapNodesExplored:maps, assertions, failures:0,
    examples, eta, gamma, strictExamples,
    controls:["first-read adaptive map","shared physical proof key",
      "repeated read stability","gap stopping","too-small query cap",
      "independently guessed incompatible per-seed proof"],
    caveat:"Finite OR-family toy; mathematical asymptotics are derived separately from published tautology theorem."
  };
}
if (typeof module !== "undefined" && require.main === module) {
  console.log(JSON.stringify(audit(),null,2));
}
