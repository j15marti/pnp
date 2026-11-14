"use strict";
const run=function main() {
  "use strict";
  function enc(n, clauses) {
    const w = n.toString(2).length;
    return "1".repeat(n) + "0" + "1".repeat(clauses.length) + "0" +
      clauses.flat().map(([sign, v]) => String(sign) + v.toString(2).padStart(w, "0")).join("");
  }
  function parse(src) {
    if (!src || /[^01]/.test(src)) return null;
    const i = src.indexOf("0");
    if (i <= 0) return null;
    const k = src.indexOf("0", i + 1);
    if (k < 0 || k - i - 1 <= 0) return null;
    const n = i, m = k - i - 1, w = n.toString(2).length;
    const payload = src.slice(k + 1);
    if (payload.length !== 3 * m * (w + 1)) return null;
    const clauses = [];
    for (let c = 0; c < m; c++) {
      const seen = new Set(), clause = [];
      for (let l = 0; l < 3; l++) {
        const off = (3 * c + l) * (w + 1);
        const sign = Number(payload[off]);
        const v = parseInt(payload.slice(off + 1, off + 1 + w), 2);
        if (v < 1 || v > n || seen.has(v)) return null;
        seen.add(v); clause.push([sign, v]);
      }
      clauses.push(clause);
    }
    return {n, clauses};
  }
  function decide(src) {
    const parsed = parse(src);
    if (!parsed) return "MALFORMED";
    const {n, clauses} = parsed;
    if (n > 20) throw Error("finite test cap, not an algorithmic claim");
    for (let assignment = 0; assignment < (1 << n); assignment++) {
      if (clauses.every(clause => clause.some(([sign, v]) => (((assignment >> (v - 1)) & 1) ^ sign) === 1)))
        return "SAT";
    }
    return "UNSAT";
  }
  // The physical fast path copies and compares one source symbol per transition.
  // The nonmatch fallback uses an exact total parser/exhaustive decider.
  // This driver checks semantic fallback outputs, not its TM instruction trace.
  function specialized(src, target, label) {
    const copied = [], L = src.length;
    let equal = L === target.length;
    for (let i = 0; i < L; i++) {
      copied.push(src[i]);
      if (i >= target.length || src[i] !== target[i]) equal = false;
    }
    if (equal) return {output:label, copySteps:L+1, readyToHaltSteps:1, hit:true};
    return {output:decide(copied.join("")), copySteps:L+1, readyToHaltSteps:null, hit:false};
  }
  const bitClause = (base, mask) => [0,1,2].map(j => [(mask >> j) & 1, base + j]);
  const fixtures = {
    sat:enc(3,[[[0,1],[0,2],[0,3]]]),
    unsat:enc(3,Array.from({length:8},(_,m)=>bitClause(1,m))),
    horn:enc(3,[[[1,1],[1,2],[0,3]],[[1,1],[1,2],[1,3]]]),
    product:enc(6,[
      ...Array.from({length:8},(_,m)=>bitClause(1,m)),
      ...Array.from({length:8},(_,m)=>bitClause(4,m))
    ])
  };
  const totals = {targets:0,hitOneStep:0,offTarget:0,mismatches:0,malformedFallback:0,satFallback:0,unsatFallback:0,invalidPhi2Edges:0};
  const details=[];
  for (const [name,target] of Object.entries(fixtures)) {
    const label=decide(target);
    if (label==="MALFORMED") throw Error("invalid constructed fixture");
    const tests=new Set(Object.values(fixtures));
    for (let j=0;j<target.length;j++) {
      tests.add(target.slice(0,j)+(target[j]==="0"?"1":"0")+target.slice(j+1));
    }
    for(const s of ["","0","1",target+"0","0"+target,target.slice(0,-1)]) tests.add(s);
    for(let length=0;length<=8;length++)
      for(let i=0;i<2**length;i++) tests.add(i.toString(2).padStart(length,"0").slice(-length||undefined));
    let hits=0, off=0;
    for(const x of tests) {
      const r=specialized(x,target,label), truth=decide(x);
      if(r.output!==truth) {totals.mismatches++; throw Error(`output mismatch ${name}`);}
      if(r.hit) {
        hits++;totals.targets++;
        if(r.readyToHaltSteps!==1) throw Error("failed constant postcopy step");
        totals.hitOneStep++;
        if(2>r.readyToHaltSteps+0) totals.invalidPhi2Edges++;
      } else {
        off++;totals.offTarget++;
        if(truth==="MALFORMED") totals.malformedFallback++;
        if(truth==="SAT") totals.satFallback++;
        if(truth==="UNSAT") totals.unsatFallback++;
      }
    }
    if(hits!==1) throw Error(`target-specific mismatch for ${name}: ${hits}`);
    details.push({name,L:target.length,label,testInputs:tests.size,hits,offTarget:off,copySteps:target.length+1,readySteps:1});
  }
  if(totals.targets!==4||totals.hitOneStep!==4||totals.invalidPhi2Edges!==4||totals.mismatches!==0)throw Error("aggregate mismatch");
  return {title:"TMR-4/014 program-oblivious ready-state counterexample",model:"unary n,m header; binary signed proper 3CNF; exact exhaustive off-target semantic fallback",execution:"hosted V8 self-contained; no physical TM trace for fallback",finiteTests:totals,fixtures:details,randomSeed:null,conclusion:"for every target F, one distinct uniform all-length correct finite program has paid copy followed by exactly one terminal step at its target; program-blind union permits a cost-one ready-to-goal edge",status:"COMPUTATIONAL for tests; mathematical conditional scope CANDIDATE awaiting peer review"};
};
console.log(JSON.stringify(run(),null,2));
