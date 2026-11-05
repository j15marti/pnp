#!/usr/bin/env node
"use strict";

let assertions = 0;
function check(x, m) { assertions++; if (!x) throw new Error(m); }
function g(mask, a, b) { return (mask >> (2*a+b)) & 1; }
function val(lit, asn) { return Boolean(asn[Math.abs(lit)]) === (lit > 0); }
function facet(mask,a,b,left,right,out) {
  return [a===0?left:-left, b===0?right:-right, g(mask,a,b)?out:-out];
}

let facetChecks=0;
for (let mask=0;mask<16;mask++) for (const [left,right] of [[1,2],[2,1],[1,1]])
for (let x=0;x<2;x++) for (let y=0;y<2;y++) for (let z=0;z<2;z++) {
  const asn={1:x,2:y,3:z}; let all=true;
  for (let a=0;a<2;a++) for (let b=0;b<2;b++) {
    all = all && facet(mask,a,b,left,right,3).some(l=>val(l,asn)); facetChecks++;
  }
  check(all === (z===g(mask,asn[left],asn[right])), "facet equivalence");
}

const selected=facet(3,1,1,1,1,2);
check(JSON.stringify(selected)===JSON.stringify([-1,-1,-2]), "selected raw facet");
const normalized=[...new Set(selected)].sort((a,b)=>a-b);
check(JSON.stringify(normalized)===JSON.stringify([-2,-1]), "selected normalized facet");
check(JSON.stringify(normalized.filter(l=>Math.abs(l)!==1))===JSON.stringify([-2]), "resolvent");

const base=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
const key=c=>[...new Set(c)].sort((a,b)=>a-b).join(",");
const truth=(c,x,y)=>c.some(l=>val(l,{1:x,2:y}));
function closure(src) {
  const map=new Map(src.map(c=>[key(c),c]));
  let changed=true;
  while(changed){ changed=false; const cs=[...map.values()];
    for(const a of cs) for(const b of cs) for(const p of [1,2]) {
      for(const [pa,pb] of [[p,-p],[-p,p]]) if(a.includes(pa)&&b.includes(pb)) {
        const r=[...new Set([...a.filter(l=>l!==pa),...b.filter(l=>l!==pb)])];
        if(r.some(l=>r.includes(-l))) continue;
        const k=key(r); if(!map.has(k)){map.set(k,r);changed=true;}
      }
    }
  }
  return map;
}
let sat=0,unsat=0;
for(let bits=0;bits<256;bits++){
  const src=base.filter((_,i)=>(bits>>i)&1);
  let ok=false; for(let x=0;x<2;x++)for(let y=0;y<2;y++)
    if(src.every(c=>truth(c,x,y)))ok=true;
  const refutes=closure(src).has("");
  check(refutes===!ok,"resolution completeness on two variables");
  if(ok)sat++;else unsat++;
}
check(sat===95&&unsat===161,"label counts");

console.log(JSON.stringify({run:"LSPV5_REFEREE357_INDEPENDENT",assertions,facetChecks,
  selector:{raw:selected,normalized,resolvent:[-2],selectorAccepts:true,aggregateAccepts:false},
  twoVariable:{formulae:256,sat,unsat}},null,2));
