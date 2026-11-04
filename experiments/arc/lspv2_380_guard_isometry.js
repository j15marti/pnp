'use strict';
// LSPV-2/380: exact guard-resolution isometry finite experiment.
// Source cost zero, every distinct Resolution inference DAG node costs one.
// All 512 proper two-variable source sets, including the empty clause.
const fs=require('fs');
const assert=require('assert');
const base=[[],[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function key(C){return C.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(',');}
const all=base.map(C=>C.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b));
const index=new Map(all.map((C,i)=>[key(C),i]));
function resolvents(A,B){let R=[]; for (const x of A){if(!B.includes(-x))continue;
 let D=[...new Set([...A.filter(a=>a!==x),...B.filter(a=>a!==-x)])];
 if(D.some(y=>D.includes(-y)))continue;
 D.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b); R.push(D);}
 return R;
}
function minDag(source){if(source & 1)return 0;const seen=new Uint8Array(1<<all.length); const todo=[source], dist=[0];seen[source]=1;
 for(let at=0;at<todo.length;at++){let mask=todo[at],d=dist[at];
   for(let i=0;i<all.length;i++)if(mask&(1<<i))for(let j=i;j<all.length;j++)if(mask&(1<<j)){
     for(const D of resolvents(all[i],all[j])){let k=index.get(key(D)); assert(k!==undefined);
       if(mask&(1<<k))continue;
       if(k===0)return d+1;
       const nxt=mask|(1<<k);if(!seen[nxt]){seen[nxt]=1;todo.push(nxt);dist.push(d+1)}
     }
   }
 }
 return null;
}
function evalClause(C,x){return C.some(v=>!!(x>>(Math.abs(v)-1)&1)===(v>0));}
function satSource(mask){for(let x=0;x<4;x++)if(all.every((C,i)=>!(mask&(1<<i))||evalClause(C,x)))return true;return false;}
function guard(C){return [-3,...C].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function isSATGuard(mask){for(let x=0;x<8;x++)if(all.every((C,i)=>!(mask&(1<<i))||evalClause(guard(C),x)))return true;return false;}
function entailsNegGuard(mask){for(let x=0;x<8;x++)if((x&4)&&all.every((C,i)=>!(mask&(1<<i))||evalClause(guard(C),x)))return false;return true;}
function closure(mask){let M=mask;while(true){let N=M;
for(let i=0;i<all.length;i++)if(M&(1<<i))for(let j=i;j<all.length;j++)if(M&(1<<j))for(const D of resolvents(all[i],all[j]))N|=1<<index.get(key(D));
if(N===M)return M;M=N;}}
let rows=[],checks=0,counts={sat:0,unsat:0,unsat_cost_hist:{},nontrivial_unsat:0,max_min_nodes:0};
for(let mask=0;mask<(1<<all.length);mask++){
 const sat=satSource(mask), gSat=isSATGuard(mask),entails=entailsNegGuard(mask),q=minDag(mask),closed=closure(mask);
 assert(gSat);assert.equal(entails,!sat);assert.equal(q===null,sat);assert.equal((closed&1)!==0,!sat);checks+=4;
 for(let i=0;i<all.length;i++)if(mask&(1<<i))for(let j=i;j<all.length;j++)if(mask&(1<<j)){
  let orig=resolvents(all[i],all[j]).map(key).sort();
  let gd=resolvents(guard(all[i]),guard(all[j])).map(D=>key(D.filter(v=>v!==-3))).sort();
  assert.deepEqual(gd,orig);checks++;
 }
 if(sat)counts.sat++;else{counts.unsat++;counts.max_min_nodes=Math.max(counts.max_min_nodes,q);counts.unsat_cost_hist[q]=(counts.unsat_cost_hist[q]||0)+1;if(q>0)counts.nontrivial_unsat++;}
 rows.push({mask,sat,entails_neg_t:entails,source_resolution_min_nodes:q,source_closure_mask:closed});
}
function malformedReject(clauses){if(!Array.isArray(clauses))return true;return clauses.some(C=>!Array.isArray(C)||C.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>2)||new Set(C).size!==C.length||C.some(v=>C.includes(-v)));}
const malformed=[null,[[0]],[[3]],[[1,-1]],[[1,1]],[true],[[2.5]]];for(const v of malformed){assert(malformedReject(v));checks++;}
const data={run:'LSPV-2/380',model:'strict ordinary DAG Resolution, 2 variable proper clauses, learned-node cost one, source cost zero',all_clauses:all,formula_count:rows.length,counts,checks,malformed_rejected:malformed.length,rows};
fs.writeFileSync(process.argv[2]||'lspv2_380_raw.json',JSON.stringify(data,null,2)+'\n');
console.log(JSON.stringify({formula_count:rows.length,counts,checks,malformed_rejected:malformed.length}));