// LSPV-1/426 exact signed graph-PHP polarity-reuse audit. Node 18+.
'use strict';
const assert=(p,m)=>{if(!p)throw Error(m)};
function source(h){
 const p=h+1, V=(i,j)=>i*h+j+1, cs=[];
 for(let i=0;i<p;i++)cs.push(Array.from({length:h},(_,j)=>V(i,j)));
 for(let j=0;j<h;j++)for(let i=0;i<p;i++)for(let k=i+1;k<p;k++)cs.push([-V(i,j),-V(k,j)]);
 return cs;
}
const sorted=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const key=c=>sorted(c).join(',');
function resolve(a,b,pivot){
 const A=new Set(a),B=new Set(b);if(!A.has(pivot)||!B.has(-pivot))return null;
 const S=new Set([...A,...B]);S.delete(pivot);S.delete(-pivot);
 if([...S].some(x=>S.has(-x)))return null;
 return sorted(S);
}
const pop=n=>n.toString(2).split('1').length-1;
const positive=c=>c.filter(x=>x>0).length;
function allClauses(n){let out=[[]];for(let i=1;i<=n;i++){const prev=out;out=[];for(const c of prev){out.push(c, [...c,i], [...c,-i])}}return out;}
function exhaustiveLocal(n){
 const C=allClauses(n);let checks=0,genuine=0;
 for(const a of C)for(const b of C)for(const p of a){
   const c=resolve(a,b,p);if(c===null)continue;
   assert(positive(c)<=positive(a)+positive(b)-1,'polarity:'+key(a)+'/'+key(b));
   assert(c.every(x=>!c.includes(-x)),'tautology');
   checks++;genuine++;
 }
 return {variables:n,clauses:C.length,valid_oriented_res_steps:checks};
}
function sat(a,clauses){return clauses.every(c=>c.some(l=>(l>0)==Boolean((a>>(Math.abs(l)-1))&1)))}
function essential(h){
 const C=source(h), n=h*(h+1),limit=2**n;let sat_orig=0, witnesses=[];
 for(let a=0;a<limit;a++)if(sat(a,C))sat_orig++;
 for(let i=0;i<C.length;i++){let found=null;for(let a=0;a<limit;a++)if(sat(a,C.filter((_,j)=>i!==j))){found=a;break}assert(found!==null,'missing deletion model '+h+':'+i);assert(!sat(found,C),'invalid deletion model');witnesses.push(found)}
 return {holes:h,pigeons:h+1,variables:n,clauses:C.length,positive_occurrences:h*(h+1),reuse_floor:C.length-1-h*(h+1),unsat_models:sat_orig, deletion_witnesses:witnesses, source:C};
}
function readOnce(C){
 const m=C.length, R=Array.from({length:2**m},()=>new Set());
 for(let i=0;i<m;i++)R[2**i].add(key(C[i]));
 const toArr=s=>s?s.split(',').map(Number):[];
 for(let mask=1;mask<R.length;mask++){
   if(pop(mask)<2)continue;
   for(let s=(mask-1)&mask;s;s=(s-1)&mask){
     const t=mask^s;if(s>t)continue;
     for(const a of R[s])for(const b of R[t]){
       const A=toArr(a),B=toArr(b);
       for(const p of A){const c=resolve(A,B,p);if(c!==null)R[mask].add(key(c))}
     }
   }
 }
 let count=0;const bysize=Array(m+1).fill(0);
 for(let mask=1;mask<R.length;mask++){count+=R[mask].size; bysize[pop(mask)]+=R[mask].size;}
 return {total_mask_clause_states:count,by_support_size:bysize,has_empty_full_support:R.at(-1).has(''),full_support_state_count:R.at(-1).size};
}
const local=exhaustiveLocal(4),a2=essential(2),a3=essential(3),dp=readOnce(a2.source);
assert(a2.unsat_models===0&&a3.unsat_models===0,'PHP labels');
assert(a2.reuse_floor===2&&a3.reuse_floor===9,'reuse floors');
assert(!dp.has_empty_full_support,'unexpected read-once refutation');
const bad=resolve([1,2],[-1,3],1);assert(key(bad)==='2,3','good pivot');
assert(resolve([1,2],[-1,3],2)===null,'corrupt pivot accepted');
assert(resolve([1,2],[-1,-2],1)===null,'tautological output accepted');
const satControl=[[1,2],[-1,2]];assert(sat(2,satControl),'SAT control');
const raw={schema:'lspv1_426_v1',scope:'strict ordinary Resolution (not full R_mix341)',status:'PROVED/RESTRICTED symbolic lemma; COMPUTATIONAL audit',local,php2:a2,php3:a3,read_once_php2:dp,controls:{positive_and_negative_model:true,corrupt_pivot_rejected:true,tautology_rejected:true}};
if(typeof process!=='undefined')process.stdout.write(JSON.stringify(raw,null,2)+'\n');
raw