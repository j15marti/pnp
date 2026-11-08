#!/usr/bin/env node
/* Independent JS replay for LSPV-5/438.  Not the historical /341 checker. */
import fs from "node:fs";
const raw = JSON.parse(fs.readFileSync(
  new URL("./raw/lspv5_438_terminal_overlap_redteam_results.json", import.meta.url),
  "utf8"));
let checks=0; const ck=(x,m)=>{checks++;if(!x)throw Error(m)};
const S=[[1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
[2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
[1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
[4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]];
const Q=[[-1,-3,7],[1,-7],[3,-7]];
const E=[[2,3,5,7,10,11,13,14],[0,1,8,9,12],
[0,1,2,3,4,6,8,9,10,11,12,15]];
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
const key=c=>norm(c).join(",");
const clause=k=>k===""?[]:k.split(",").map(Number);
const same=(a,b)=>key(a)===key(b);
const sat=(c,a)=>c.some(z=>((a>>(Math.abs(z)-1))&1)===(z>0?1:0));
function resolvents(A,B){
  const out=new Set();
  for(let v=1;v<=7;v++){
    let a=A,b=B;if(a.includes(-v)&&b.includes(v))[a,b]=[b,a];
    if(!a.includes(v)||!b.includes(-v))continue;
    const c=norm([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);
    if(!c.some(x=>c.includes(-x)))out.add(key(c));
  }return out;
}
function closure(leaves){
  const n=leaves.length, full=(1<<n)-1, T=Array.from({length:full+1},()=>new Set());
  leaves.forEach((c,i)=>T[1<<i].add(key(c)));
  for(let sz=2;sz<=n;sz++)for(let mask=1;mask<=full;mask++)if(pop(mask)===sz){
    const low=mask&-mask;let left=(mask-1)&mask;
    while(left){if(left&low){const right=mask^left;if(right)
      for(const a of T[left])for(const b of T[right])
        for(const c of resolvents(clause(a),clause(b)))T[mask].add(c);
    }left=(left-1)&mask;}
  }return T;
}
const pop=x=>{let n=0;while(x){x&=x-1;n++;}return n};
const memo=new Map();
function reaches(g,sourceIds,U,C){
  const mk=[g,sourceIds.join("."),U.join("."),key(C)].join("|");
  if(memo.has(mk))return memo.get(mk);
  const rem=sourceIds.filter(x=>!U.includes(x));
  const T=closure([C,...rem.map(i=>S[i])]);
  const ans=T.at(-1).has(key(Q[g]));memo.set(mk,ans);return ans;
}
function maxShare(g,h,I){
  let best=-1,bestClause=null,candidates=0;
  for(let mask=1;mask<(1<<I.length);mask++){
    const U=I.filter((_,i)=>mask&(1<<i));
    const T=closure(U.map(i=>S[i]));
    for(const cKey of T.at(-1)){candidates++;const C=clause(cKey);
      if(reaches(g,E[g],U,C)&&reaches(h,E[h],U,C)&&U.length-1>best){
        best=U.length-1;bestClause={source_subset:U,clause:C};
      }
    }
  }return {best,candidates,bestClause};
}

const recovered=[];
for(let g=0;g<3;g++){
  const R=[];
  for(let i=0;i<16;i++)for(let a=0;a<128;a++)
    if(S.every((c,j)=>j===i||sat(c,a))&&!sat(Q[g],a)){R.push(i);break;}
  recovered.push(R);
}
ck(JSON.stringify(recovered)===JSON.stringify(E),"essential sets");
const I02=E[0].filter(x=>E[2].includes(x)), I12=E[1].filter(x=>E[2].includes(x));
ck(JSON.stringify(I02)==="[2,3,10,11]","I02");
ck(JSON.stringify(I12)==="[0,1,8,9,12]","I12");
const a=maxShare(0,2,I02),b=maxShare(1,2,I12);
ck(a.best===0&&a.candidates===4,"0-2 sharing maximum");
ck(b.best===1&&b.candidates===31,"1-2 sharing maximum");
ck(!reaches(2,E[2],E[1],Q[1]),"Q1 macro unexpectedly reaches Q2 floor");
ck(raw.independent_connected_arity_floor===15,"floor");
ck(raw.minimum_tree_sharing_controls[0].best_common_minimum_tree_subproof.shared_nodes===0,"raw 02");
ck(raw.minimum_tree_sharing_controls[1].best_common_minimum_tree_subproof.shared_nodes===1,"raw 12");
// Hostile controls.
ck(!same(Q[2],[3,7]),"corrupt goal");
ck(!same(S[3],[-1,-2,-4]),"corrupt source");
ck(!resolvents(Q[1],S[4]).has(key(Q[2])),"illegal macro inference");
console.log(JSON.stringify({status:"PASS",assertions:checks,
independent_floor:15,minimum_tree_shared_nodes:{"0-2":a.best,"1-2":b.best},
q1_as_q2_floor_macro:false,hostile_controls:3,historical_R_mix341_checker_run:false,
p_vs_np:"OPEN"},null,2));
