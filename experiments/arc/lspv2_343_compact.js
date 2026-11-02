// LSPV-2 LOW-SUPPORT-MINCORE343: exact fixed-Rmix341 core optimizer for n<=3.
// Run: node lspv2_343_compact.js. No dependencies.
// Logical optimum W=minimum UNSAT source-core cardinality minus one; the theorem
// uses at-most-binary-premise soundness plus AND3 on up to 3 source variables.
'use strict';
function truth(c,a){return c.some(x=>((a>>(Math.abs(x)-1))&1)==(x>0?1:0))}
function exact(n,C){
 if(!Number.isInteger(n)||n<0||n>3)return {status:'OUT_OF_EXACT_SCOPE'};
 const assignments=1<<n, full=(1<<assignments)-1;
 const forb=C.map(c=>{let v=0;for(let a=0;a<assignments;a++)
   if(!truth(c,a))v|=1<<a;return v});
 let dist=Array(1<<assignments).fill(Infinity),seq=Array(1<<assignments).fill(null);
 dist[0]=0;seq[0]=[];
 let transitions=0;
 for(let i=0;i<C.length;i++){
   const d=dist.slice(),s=seq.slice();
   for(let x=0;x<dist.length;x++){transitions++;
     if(!Number.isFinite(dist[x]))continue;
     let y=x|forb[i],k=dist[x]+1;
     if(k<d[y]){d[y]=k;s[y]=seq[x].concat(i)}
   }dist=d;seq=s;
 }
 if(seq[full]===null){let a=0;while(C.some(c=>!truth(c,a)))a++;
   return {status:'SAT',witness:a,transitions}}
 const idx=seq[full];let old=full,prev='',proof=[];
 for(let k=0;k<idx.length;k++){
   let f=0;for(let a=0;a<assignments;a++)if(truth(C[idx[k]],a))f|=1<<a;
   if(k){old&=f;proof.push({id:'d'+(k-1),rule:'AND3',
     parents:[prev,'s'+idx[k]],truth:old});prev='d'+(k-1)}
   else{old=f;prev='s'+idx[k]}
 }
 if(old!==0)throw Error('unsound proof');
 return {status:'UNSAT',core:idx,W:idx.length-1,proof,transitions};
}
function blockers(n){let o=[];for(let a=0;a<(1<<n);a++){
 let c=[];for(let i=0;i<n;i++)c.push((a>>i)&1?-(i+1):i+1);o.push(c)}
 return o}
function models(n,C){let z=0;for(let a=0;a<(1<<n);a++)
 if(C.every(c=>truth(c,a)))z++;return z}
function bruteCore(n,C){let m=C.length,best=Infinity;
 for(let S=0;S<(1<<m);S++){
  let k=0,sub=[];for(let j=0;j<m;j++)if((S>>j)&1){k++;sub.push(C[j])}
  if(k<best&&models(n,sub)===0)best=k;
 }return Number.isFinite(best)?best:null}
let checks=0,cases=0,report=[];
for(let n=0;n<=3;n++){
 const cs=blockers(n),r=exact(n,cs);
 if(r.status!=='UNSAT'||r.W!==(1<<n)-1||r.W!==bruteCore(n,cs)-1)
   throw Error('bad exact extremum');checks++;
 report.push({n,clauses:cs.length,W:r.W});
 for(let s=0;s<(1<<cs.length);s++){
  let sub=cs.filter((_,j)=>(s>>j)&1),v=exact(n,sub);
  if((v.status==='UNSAT')!==(models(n,sub)===0))throw Error('bad label');
  cases++;checks++;
 }
}
const G=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
if(exact(4,G).status!=='OUT_OF_EXACT_SCOPE'||models(4,G)!==0)throw Error('bad scope');
console.log(JSON.stringify({version:'LOW-SUPPORT-MINCORE343',rule:'Rmix341',report,
 exhaustive_cube_subfamilies:cases,assertions:checks,source_support_limit:3,
 note:'Proof of global optimum uses essential-source capacity lower bound and AND3 upper bound; full independent verifier and controls in companion archive.'},null,2));
