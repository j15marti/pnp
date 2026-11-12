#!/usr/bin/env node
// LSPV-5/507 red-team: independent re-solve of the LSPV-4/565 fixed-DAG
// resident-register peak/recomputation frontier, written without importing
// or calling experiments/arc/lspv4_565_recompute_peak.py.
// Formalization differs on purpose: deletion is an explicit atomic zero-cost
// move; a compute move either allocates fresh or overwrites one parent in place.
// DAG data is read from the LSPV-4/560 fixture constants transcribed here and
// cross-checked against the published W39 certificate by parent arity.
// Usage: node lspv5_507_peak_frontier_redteam.cjs <peak> <capacity> <overwrite:0|1> <recompute:0|1>
'use strict';
const PARENTS=[[],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
 [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
 [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]];
const SIZES=[13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
 14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2];
const N=PARENTS.length, GOAL=34;
function members(m){const r=[];for(let i=0;i<N;i++)if(Math.floor(m/2**i)%2===1) r.push(i);return r;}
// masks up to 2^35 exceed 32-bit ops; use BigInt keys via numbers with arithmetic.
const B=i=>2**i;
const has=(m,i)=>Math.floor(m/B(i))%2===1;
const pay=m=>members(m).reduce((s,i)=>s+SIZES[i],0);
// Binary heap
class Heap{constructor(){this.a=[];}push(x){const a=this.a;a.push(x);let i=a.length-1;while(i>0){const p=(i-1)>>1;if(lt(a[i],a[p])){[a[i],a[p]]=[a[p],a[i]];i=p;}else break;}}
 pop(){const a=this.a,t=a[0],l=a.pop();if(a.length){a[0]=l;let i=0;for(;;){let s=i;const L=2*i+1,R=L+1;if(L<a.length&&lt(a[L],a[s]))s=L;if(R<a.length&&lt(a[R],a[s]))s=R;if(s===i)break;[a[i],a[s]]=[a[s],a[i]];i=s;}}return t;}get size(){return this.a.length;}}
function lt(x,y){return x[0]!==y[0]?x[0]<y[0]:x[1]!==y[1]?x[1]<y[1]:x[2]<y[2];}
function solve(P,CAP,OW,REC){
  // state = [resident mask, done mask (only when REC=0, to forbid recompute)]
  const key=(m,d)=>m+'|'+d;
  const best=new Map(),prev=new Map();
  const h=new Heap(); best.set(key(0,0),[0,0]); h.push([0,0,0,0]);
  let settled=0;
  while(h.size){
    const [w,a,m,d]=h.pop(); const k=key(m,d); const bb=best.get(k);
    if(bb[0]!==w||bb[1]!==a) continue; settled++;
    if(has(m,GOAL)){ // final: delete all but GOAL, charge its payload
      const steps=[];let kk=k;while(prev.has(kk)){const p=prev.get(kk);steps.push(p.mv);kk=p.from;}
      return {P,CAP,OW,REC,feasible:true,res:w,area:a+SIZES[GOAL],settled,moves:steps.reverse()};
    }
    const R=members(m);
    const relax=(nm,nd,nw,na,mv)=>{const nk=key(nm,nd);const c=best.get(nk);
      if(!c||nw<c[0]||(nw===c[0]&&na<c[1])){best.set(nk,[nw,na]);prev.set(nk,{from:k,mv});h.push([nw,na,nm,nd]);}};
    for(const i of R) relax(m-B(i),d,w,a,'del '+i);           // atomic free delete
    const pm=pay(m);
    for(let j=0;j<N;j++){
      if(has(m,j)) continue; if(!REC&&has(d,j)) continue;
      if(!PARENTS[j].every(p=>has(m,p))) continue;
      const nd=REC?0:d+(has(d,j)?0:B(j));
      if(R.length+1<=CAP&&pm+SIZES[j]<=P) relax(m+B(j),nd,w+1,a+pm,'new '+j);
      if(OW) for(const p of PARENTS[j]) if(SIZES[p]>=SIZES[j]&&R.length<=CAP&&pm<=P)
        relax(m-B(p)+B(j),nd,w+1,a+pm,'ow '+j+'<-'+p);
    }
  }
  return {P,CAP,OW,REC,feasible:false,settled};
}
if(require.main===module){
  const [P,CAP,OW,REC]=process.argv.slice(2).map(Number);
  const t=Date.now(); const r=solve(P,CAP,OW,REC); r.ms=Date.now()-t;
  if(r.moves) r.moves=r.moves.filter(s=>!s.startsWith('del')).join(',');
  console.log(JSON.stringify(r));
}
module.exports={solve,PARENTS,SIZES};
