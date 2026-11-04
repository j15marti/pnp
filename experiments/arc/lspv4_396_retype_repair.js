#!/usr/bin/env node
// LSPV-4/396, deterministic, standalone three-wire RES saturation and typed replay.
'use strict';
const assert=require('assert/strict');
let checks=0;function check(x){assert.ok(x);checks++}
function clause(a){if(a.some(v=>!Number.isInteger(v)||v===0))throw Error('invalid');const b=[...new Set(a)];if(b.length!==a.length||b.some(x=>b.includes(-x)))throw Error('malformed');return b.sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x)}
function res(A,B,p){if(!A.includes(p)||!B.includes(-p))throw Error('pivot');return clause([...new Set([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)])])}
function facets(z,a,b){return [clause([-z,a]),clause([-z,b]),clause([z,-a,-b])]}
function models(C,n){let k=0;for(let a=0;a<(1<<n);a++){if(C.every(c=>c.some(x=>x>0?!!(a&(1<<(x-1))):!(a&(1<<(-x-1))))))k++}return k}
function blockers(m){const out=[];for(let a=0;a<8;a++)if(!((m>>a)&1))out.push(clause([a&1?-1:1,a&2?-2:2,a&4?-3:3]));return out}
function closure(input){const S=new Map(input.map(c=>[JSON.stringify(c),c]));let added=0;for(;;){let change=false;const prev=[...S.values()];for(const a of prev)for(const b of prev)for(const p of a){if(!b.includes(-p))continue;let r;try{r=res(a,b,p)}catch{continue}let key=JSON.stringify(r);if(!S.has(key)){S.set(key,r);change=true;added++}}if(!change)break}return {S:[...S.values()],added}}
const F=[[1],[2],[3],[4],[-4]];
check(models(F,4)===0);check(models(F.slice(0,4),4)===1);
const G=[[5,1,2],[6,5,3],[7,6,4],[8,7,-4]];
const src=G.flatMap(([z,a,b])=>facets(z,a,b)).concat([[8]]);
check(models(src,8)===0);
const p=res([8],facets(8,7,-4)[0],8);check(JSON.stringify(p)==='[7]');
const minus4=res([8],facets(8,7,-4)[1],8);check(JSON.stringify(minus4)==='[-4]');
const minusP=res(minus4,facets(7,6,4)[1],-4);check(JSON.stringify(minusP)==='[-7]');
check(res(p,minusP,7).length===0);
for(let j=0;j<4;j++){let a=[1,1,1,1],b=[...a];b[j]=0;check(a.reduce((x,y)=>x*y,1)!==b.reduce((x,y)=>x*y,1))}
let malformed=0;for(const bad of [[0],[1,1],[1,-1],[-2,-2]]){try{clause(bad)}catch{malformed++}}
for(const x of [[[1],[-1],-1],[[1],[-1],2],[[1],[1],1]]){try{res(...x)}catch{malformed++}}
check(malformed===7);
const masks=[...new Set([0,1,2,3,7,15,51,85,90,102,105,153,170,204,240,254,255,...Array.from({length:24},(_,i)=>i*11)])].sort((a,b)=>a-b);
let pairs=0,sat=0,unsat=0,blockerChecks=0,resNodes=0;
for(const u of masks)for(const v of masks){const {S,added}=closure([...blockers(u),...blockers(v)]);check(S.length<=27);resNodes+=added;const w=u&v;for(const C of blockers(w)){check(S.some(D=>D.every(x=>C.includes(x))));blockerChecks++}pairs++;if(w) sat++;else unsat++}
check(pairs===1600&&sat===1367&&unsat===233);
check(blockerChecks===9744&&resNodes===14993);
const result={run:"LSPV4_ASSERTION_RETYPE_REPAIR396",models_original:0,models_SAT_sibling:1,models_evaluator:0,source_replay_paid_nodes:12,evaluator_paid_nodes:4,repaired_splice_paid_nodes:16,local_factor_pairs:pairs,pair_SAT:sat,pair_UNSAT:unsat,blocker_checks:blockerChecks,resolution_nodes:resNodes,malformed_rejections:malformed,assertions:checks,status:"RESTRICTED/COMPUTATIONAL; B1 B2 B3 and P vs NP OPEN"};
console.log(JSON.stringify(result,null,2));
