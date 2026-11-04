'use strict';
// Independently enumerated 2-variable truth masks; no Python imports or shared evaluator.
const L=[1,-1,2,-2]; const U=L.map(x=>[x]);
for(const a of [1,-1]) for(const b of [2,-2]) U.push([a,b]);
function models(cs,n){let mask=0;for(let a=0;a<(1<<n);a++){
  let ok=1; for(const c of cs){let tr=0;for(const l of c){if(!!(a&(1<<(Math.abs(l)-1)))===(l>0)){tr=1;break;}}if(!tr){ok=0;break;}}
  if(ok) mask|=1<<a;
}return mask;
}
let stats={checked:0,sat:0,unsat:0,remove_tests:0,flip_tests:0,discrepancies:0};
for(let v=0;v<(1<<U.length);v++){
 let F=U.filter((_,i)=>(v>>i)&1),n=2,z=3,H=F.flatMap(c=>[c.slice(),[...c,z],[...c,-z]]);
 let yes=!!models(F,2),pyes=!!models(H,3);
 if(yes!==pyes) throw Error('status mismatch '+v);
 if(yes)stats.sat++; else stats.unsat++;
 const enc=H.map(c=>c.slice().sort((a,b)=>a-b).join(','));if(new Set(enc).size!==enc.length)throw Error('duplicate');
 for(let i=0;i<H.length;i++){
   let removed=H.filter((_,j)=>i!==j);
   if(!!models(removed,3)!==yes)throw Error('removal '+v+':'+i);stats.remove_tests++;
   if(!yes)for(const lit of H[i]){
      const altered=H.map((c,j)=>i===j?c.map(x=>x===lit?-x:x):c);
      if(models(altered,3)!==0)throw Error('flip '+v+':'+i+':'+lit);stats.flip_tests++;
   }
 }
 stats.checked++;
}
function essential(F,n){return F.reduce((s,_,i)=>s+(models(F.filter((_,j)=>i!==j),n)!==0?1:0),0)}
const triangle=[[1,2],[-1,-2],[2,3],[-2,-3],[1,3],[-1,-3]];
const pad=triangle.flatMap(c=>[c.slice(),[...c,4],[...c,-4]]);
if(models(triangle,3)!==0 || models(pad,4)!==0 || essential(triangle,3)!==6 || essential(pad,4)!==0)throw Error('triangle failed');
stats.triangle={originalEssential:6,paddedEssential:0,clausesBefore:6,clausesAfter:18};
console.log(JSON.stringify(stats));
