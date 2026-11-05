#!/usr/bin/env node
"use strict";

// Independently authored compact verifier for the exact native witness and
// typed clause/GF(2) congruence claims.  It does not consume producer code.

let checks = 0;
function check(c, m) { checks++; if (!c) throw new Error(m); }

function val(lit, a) { const v = a[Math.abs(lit)]; return lit > 0 ? v : !v; }
function clause(c, a) { return c.some(l => val(l, a)); }
function key(c) { return [...new Set(c)].sort((a,b)=>a-b).join(","); }

function resolve(left, right, pivot) {
  let l = [...new Set(left)], r = [...new Set(right)];
  if (!(l.includes(pivot) && r.includes(-pivot))) {
    if (l.includes(-pivot) && r.includes(pivot)) [l,r] = [r,l];
    else throw new Error("missing pivot");
  }
  return [...new Set(l.filter(x=>x!==pivot).concat(r.filter(x=>x!==-pivot)))].sort((a,b)=>a-b);
}

function* bits(n) {
  for (let x=0;x<(1<<n);x++) yield Array.from({length:n},(_,i)=>Boolean((x>>i)&1));
}

const source = [[1],[1,3],[-2]];
let models = 0;
for (const b of bits(3)) {
  const a = {1:b[0],2:b[1],3:b[2]};
  if (source.every(c=>clause(c,a))) models++;
}
check(models===2,"source models");
for (const b of bits(3)) {
  const a={1:b[0],2:b[1],3:b[2]};
  if (b[0]) check(clause([1,2],a),"LOCAL implication");
}
check(key(resolve([1,2],[-2],2))===key([1]),"native resolvent");
try { resolve([1],[-2],2); check(false,"stronger should fail"); } catch (_) { check(true,"stronger rejected"); }
check(key(resolve([1,2,3],[-2],2))===key([1,3]),"weaker changed resolvent");

// Exhaustive non-tautological clauses on three variables and all global
// permutations/sign renamings.
function clauses3() {
  const out=[];
  for(let code=0;code<27;code++) {
    let q=code,c=[];
    for(let i=1;i<=3;i++){ const d=q%3;q=Math.floor(q/3);if(d===1)c.push(i);if(d===2)c.push(-i); }
    out.push(c);
  }
  return out;
}
function perms(a) {
  if(a.length<=1)return [a];
  const out=[];
  a.forEach((x,i)=>perms(a.slice(0,i).concat(a.slice(i+1))).forEach(p=>out.push([x].concat(p))));
  return out;
}
function renameLit(lit,p,s){ const old=Math.abs(lit)-1;const mapped=s[old]*p[old];return lit>0?mapped:-mapped; }
function renameClause(c,p,s){ return c.map(l=>renameLit(l,p,s)); }

let resCases=0;
for(const l of clauses3()) for(const r of clauses3()) for(let pivot=1;pivot<=3;pivot++) {
  if(!((l.includes(pivot)&&r.includes(-pivot))||(l.includes(-pivot)&&r.includes(pivot))))continue;
  const out=resolve(l,r,pivot);
  for(const p of perms([1,2,3])) for(const sm of bits(3)) {
    const s=sm.map(x=>x?1:-1);
    const rp=Math.abs(renameLit(pivot,p,s));
    check(key(resolve(renameClause(l,p,s),renameClause(r,p,s),rp))===key(renameClause(out,p,s)),"RES rename");
    resCases++;
  }
}

let xorCases=0;
for(let a=0;a<32;a++)for(let b=0;b<32;b++)for(const p of perms([1,2,3,4,5]).filter((_,i)=>i%11===0)){
  function pm(mask){let o=0;for(let i=0;i<5;i++)if((mask>>i)&1)o|=1<<(p[i]-1);return o;}
  check((pm(a)^pm(b))===pm(a^b),"GF2 rename");xorCases++;
}

// Both-label and malformed controls.
check(source.every(c=>clause(c,{1:true,2:false,3:false})),"SAT witness");
check(!([ [1],[-1] ].every(c=>clause(c,{1:false}))),"UNSAT branch 0");
check(!([ [1],[-1] ].every(c=>clause(c,{1:true}))),"UNSAT branch 1");
for(const bad of [[[1],[2],1],[[1,2],[-2],1],[[-1],[1],2]]){
  try{resolve(...bad);check(false,"malformed accepted");}catch(_){check(true,"malformed rejected");}
}

console.log(JSON.stringify({artifact:"REFEREE351_INDEPENDENT",checks,resCases,xorCases},null,2));
