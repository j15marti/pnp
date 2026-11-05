#!/usr/bin/env node
/* LSPV-1/425 independent no-import proof-condition verifier.
 * Exhaustively recompiles pairs of signed GF(2) equations on four vars into
 * strict Boolean Resolution, including shared premise and constant rows.
 * Uses a separate representation from Python's tuple-keyed clauses.
 */
let assertions=0;
function must(ok,msg){ assertions++; if(!ok)throw new Error(msg); }
function assignments(vars){let out=[];for(let n=0;n<2**vars.length;n++){
  const a={};for(let j=0;j<vars.length;j++)a[vars[j]]=(n>>j)&1;out.push(a);
}return out;}
function parity(s,a){return s.reduce((t,v)=>t^a[v],0);}
function holds(eq,a){return parity(eq.s,a)===eq.r;}
function falsifier(eq,a){return eq.s.map(v=>a[v]?-v:v).sort((x,y)=>x-y);}
function clauseHolds(c,a){return c.some(l=>a[Math.abs(l)]===(l>0?1:0));}
function key(a,vars){return vars.map(v=>a[v]).join('');}
function blockers(eq){let out=new Map();for(const a of assignments(eq.s))
  if(!holds(eq,a))out.set(key(a,eq.s),falsifier(eq,a));return out;}
function subtract(c,p){return c.filter(v=>v!==p);}
function sameOrSubset(a,b){return a.every(x=>b.includes(x));}
function strict(c,d,p){must(c.includes(p)&&d.includes(-p),'bad-pivot');
  let r=[...new Set([...subtract(c,p),...subtract(d,-p)])].sort((x,y)=>x-y);
  must(!r.some(l=>r.includes(-l)),'tautological-resolvent');return r;}
function pair(a,b){
  const U=[...new Set([...a.s,...b.s])].sort((x,y)=>x-y);
  const I=a.s.filter(v=>b.s.includes(v));const C=U.filter(v=>!I.includes(v));
  const out={s:C,r:a.r^b.r},cand=blockers(out),P=blockers(a),Q=blockers(b);
  let steps=0;const isFalse=e=>e.s.length===0&&e.r===1;
  const isTrue=e=>e.s.length===0&&e.r===0;
  if(isFalse(a)||isFalse(b)){must((isFalse(a)?P:Q).has(''),'missing false clause');return {steps:0,output:cand.size};}
  if(isTrue(a)||isTrue(b))return {steps:0,output:cand.size};
  for(const z of assignments(C)){
    if(holds(out,z))continue;
    let leaves=[];
    for(const u of assignments(I)){
      const val={...z,...u};const va=!holds(a,val),vb=!holds(b,val);
      must(va!==vb,'must be exactly one violated equation');
      const e=va?a:b,src=va?P:Q;
      const cl=src.get(key(val,e.s));must(cl!==undefined,'missing parent clause');
      leaves.push(cl);
    }
    // Independent assignment enumeration is little-endian, so resolve I[0] first.
    for(let j=0;j<I.length;j++){
      let next=[];for(let i=0;i<leaves.length;i+=2){
        const x=leaves[i],y=leaves[i+1],pivot=I[j];
        let result;
        if(x.includes(pivot)&&y.includes(-pivot))result=strict(x,y,pivot);
        else if(y.includes(pivot)&&x.includes(-pivot))result=strict(y,x,pivot);
        else if(!x.includes(pivot)&&!x.includes(-pivot))result=x;
        else if(!y.includes(pivot)&&!y.includes(-pivot))result=y;
        else throw new Error('missing-pivot cannot inherit');
        steps+=result===x||result===y?0:1; next.push(result);
      }leaves=next;
    }
    must(leaves.length===1,'one root per target');
    let target=falsifier(out,z);
    must(sameOrSubset(leaves[0],target),'root not subclause');
    for(const val of assignments(U))if(holds(a,val)&&holds(b,val))
      must(clauseHolds(leaves[0],val),'source-authenticated consequence failed');
  }
  must(steps<=2**U.length,'improved compiler bound');
  return {steps,output:cand.size};
}
function combos(vals){const out=[[]];for(const v of vals){for(const a of [...out])out.push([...a,v]);}return out;}
const rows=combos([1,2,3,4]).flatMap(s=>[{s,r:0},{s,r:1}]);
must(rows.length===32,'all 32 equations');
let cases=0,steps=0,blockersOut=0,max=0;
for(const a of rows)for(const b of rows){const x=pair(a,b);cases++;steps+=x.steps;blockersOut+=x.output;max=Math.max(max,x.steps);}
must(cases===1024,'case coverage');must(steps===2210,'strict step count');
must(blockersOut===2592,'blocker count');must(max===15,'max pair steps');
// Hostile controls: exact K4 odd and even parity charges and corruption.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const source=Array.from({length:4},(_,v)=>({s:edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean),r:v===0?1:0}));
const satCount = src => assignments([1,2,3,4,5,6]).filter(z=>src.every(e=>holds(e,z))).length;
must(satCount(source)===0,'odd K4 UNSAT');must(satCount(source.map(e=>({...e,r:0})))===8,'even K4 SAT');
const original=[1,-2],second=[-1,3];const inferred=strict(original,second,1);
must(JSON.stringify(inferred)===JSON.stringify([-2,3]),'strict pivot certificate');
let rejected=0;
for(const bad of [()=>strict(original,second,2),()=>strict(original,second,3),
                  ()=>strict([1,2],[3,-4],1),()=>strict([1,-3],[-1,3],1)]){
  try{bad()}catch{rejected++;}
}
must(rejected===4,'all four mutated certificates rejected');
let malformed=0;
for(const e of [{s:[1,1],r:1},{s:[0],r:0},{s:[1],r:2}]){
  try{must(e.r===0||e.r===1,'invalid rhs');must(e.s.every(v=>v>0),'invalid id');
      must(new Set(e.s).size===e.s.length,'duplicates');}catch{malformed++;}
}
must(malformed===3,'malformed equation rejects');
console.log(JSON.stringify({cases,steps,blockersOut,max,rejected,malformed,assertions,method:'independent strict resolution'},null,2));
