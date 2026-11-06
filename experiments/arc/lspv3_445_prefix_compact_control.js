#!/usr/bin/env node
/* LSPV-3/445 compact standalone regression. CONDITIONAL FACET-4, not historical R_mix341.
 * Full source-DIMACS and typed-DAG independent verifier: see downloadable archive. */
'use strict';
const assert=require('node:assert/strict');
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y));
function same(a,b){return JSON.stringify(norm(a))===JSON.stringify(norm(b));}
function res(a,b,p){
  assert(a.includes(p)&&b.includes(-p),'oriented pivot');
  let q=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  assert(!q.some(x=>q.includes(-x)),'tautology');
  return q;
}
function val(lit,asg){const b=!!asg[Math.abs(lit)];return lit>0?b:!b;}
function sat(cl,asg){return cl.some(l=>val(l,asg));}
function run(ell){
  const n=2**ell,m=n+1,defs=[],nodes=[],portMap=new Map(),used=new Set();
  let next=m*ell,checks=0,truth=0;
  const ok=(cond,msg)=>{checks++;assert(cond,msg);};
  const add=(a,b,p,want)=>{
    const c=res(a,b,p);
    ok(same(c,want),'exact resolvent');
    nodes.push(c);
    return c;
  };
  for(let i=0;i<m;i++)for(let d=2;d<=ell;d++)for(let prefix=0;prefix<2**d;prefix++){
    const signed=Array.from({length:d},(_,k)=> {
      const v=i*ell+k+1;
      return ((prefix>>(d-1-k))&1)?-v:v;
    });
    const key=i+':'+d+':'+prefix;
    const parent=d===2?signed[0]:portMap.get(i+':'+(d-1)+':'+(prefix>>1)).y;
    const last=signed[d-1], y=++next;
    const T00=norm([parent,last,-y]),T01=norm([parent,-last,-y]),
          T10=norm([-parent,last,-y]),T11=norm([-parent,-last,y]);
    // Four forbidden-row clauses belong to one paid conservative owner.
    defs.push({y,parent,last});
    const A=add(T00,T01,last,[-y,parent]);
    const B=add(T00,T10,parent,[-y,last]);
    const C=T11;
    // Independent wire-level truth table of the entire gate relation.
    for(let pb=0;pb<2;pb++)for(let lb=0;lb<2;lb++)for(let out=0;out<2;out++){
      const asg={};
      asg[Math.abs(parent)]=parent>0?pb:1-pb;
      asg[Math.abs(last)]=last>0?lb:1-lb;
      asg[y]=out;
      const clauses=[T00,T01,T10,T11].every(c=>sat(c,asg));
      ok(clauses===(out===(pb&lb)),'exact gate relation');truth++;
    }
    let P=[],Q;
    if(d===2){P=[A,B];Q=C;}
    else{
      const previous=portMap.get(i+':'+(d-1)+':'+(prefix>>1));
      for(let k=0;k<d-1;k++)
        P.push(add(A,previous.P[k],parent,[-y,signed[k]]));
      P.push(B);
      Q=add(previous.Q,C,parent,[y,...signed.map(v=>-v)]);
    }
    for(let k=0;k<d;k++)ok(same(P[k],[-y,signed[k]]),'exact port');
    ok(same(Q,[y,...signed.map(v=>-v)]),'exact converse port');
    // Both output labels over every original-bit assignment.
    for(let bits=0;bits<2**d;bits++)for(let out=0;out<2;out++){
      const asg={};
      for(let k=0;k<d;k++)asg[i*ell+k+1]=(bits>>(d-1-k))&1;
      asg[y]=out;
      const exact=out===Number(signed.every(l=>val(l,asg)));
      const actual=[...P,Q].every(c=>sat(c,asg));
      ok(exact===actual,'full source-bit relation');truth++;
    }
    portMap.set(key,{y,P,Q});
  }
  const D=m*(2*n-4),R=m*(2*n*(ell-1)-8)+2*D;
  ok(defs.length===D&&nodes.length===R,'exact charged node counts');
  ok(D+R===m*(2*n*ell+4*n-20),'closed form paid count');
  ok([...portMap.values()].reduce((a,v)=>a+v.P.length+1,0)===m*(2*n*ell-4),'port count');
  return {ell,defs:D,paid_resolution:R,total_paid:D+R,checks,truth_rows:truth};
}
for(let ell=2;ell<=4;ell++)console.log(JSON.stringify(run(ell)));
// Corruption controls for rule semantics, independently of certificate producer.
assert.throws(()=>res([1,2],[-2,3],1));
assert.throws(()=>res([1,2],[3,-1],2));
assert.throws(()=>res([1,2],[-1,-2],1));
console.log(JSON.stringify({corruption_controls_rejected:3}));
