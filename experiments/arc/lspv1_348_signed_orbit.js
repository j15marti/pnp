'use strict';
// LSPV-1 348: signed hyperoctahedral orbit of the authenticated G342.
// No dependencies. Run: node experiments/arc/lspv1_348_signed_orbit.js
const BASE=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
const order=(a,b)=>Math.abs(a)-Math.abs(b)||a-b;
function canonical(F){return F.map(c=>[...c].sort(order).join(',')).sort().join(';');}
function parse(k){return k.split(';').map(row=>row.split(',').map(Number));}
function perms(a){if(a.length<=1)return [a];return a.flatMap((x,i)=>perms([...a.slice(0,i),...a.slice(i+1)]).map(rest=>[x,...rest]));}
const PERMS=perms([1,2,3,4]);
function apply(F,p,mask){return F.map(c=>c.map(v=>(v<0?-1:1)*((mask>>(Math.abs(v)-1))&1?-1:1)*p[Math.abs(v)-1]));}
function satCount(F){let c=0;for(let mask=0;mask<16;mask++){if(F.every(row=>row.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0))))c++;}return c;}
function resolve(A,B,p){if(A.includes(-p)&&B.includes(p)){[A,B]=[B,A];}if(!A.includes(p)||!B.includes(-p))throw Error('invalid resolution pivot');let C=[...A.filter(x=>x!==p),...B.filter(x=>x!==-p)];let seen=new Set(C);if(C.some(x=>seen.has(-x)))throw Error('tautological resolution');return [...seen].sort(order);}
function witness(F,p,mask){const S=apply(F,p,mask);
  let pvar=(i)=>(p[i-1])*(((mask>>(i-1))&1)?-1:1);
  const d0=resolve(S[0],S[3],pvar(4));
  const d1=resolve(S[2],d0,pvar(3));
  const d2=resolve(S[3],S[5],pvar(4));
  const d3=resolve(S[4],d2,pvar(3));
  const d4=resolve(S[1],d3,pvar(2));
  const d5=resolve(d1,d4,pvar(1));
  if(d5.length||d0.length!==2||d1.length!==1||d2.length!==2||d3.length!==2||d4.length!==1)throw Error('broken six-resolution refutation');
  return [d0,d1,d2,d3,d4,d5];
}
function atlas(){
 const orbit=new Map();
 let transformations=0,proofNodesChecked=0,delControls=0,flipControls=0;
 for(const p of PERMS)for(let mask=0;mask<16;mask++){
  transformations++;
  const F=apply(BASE,p,mask),k=canonical(F);
  if(!orbit.has(k))orbit.set(k,{p,mask});
  witness(BASE,p,mask);proofNodesChecked+=6;
 }
 if(transformations!==384||orbit.size!==192)throw Error('orbit size incorrect');
 const neighbors=new Set(),neighborTypes=new Map(),deletionMultiset=[];
 for(const [key] of orbit){
  const F=parse(key);if(satCount(F)!==0)throw Error('orbit member SAT');
  const deletion=F.map((_,i)=>satCount(F.filter((_,j)=>i!==j))).sort((a,b)=>a-b);
  if(deletion.join(',')!=='1,1,1,3,3,3')throw Error('deletion-model mismatch');
  delControls+=6;
  if(deletionMultiset.length===0)deletionMultiset.push(...deletion);
  for(let i=0;i<F.length;i++)for(let j=0;j<F[i].length;j++){
   const G=F.map(c=>[...c]);G[i][j]*=-1;
   if(satCount(G)<=0)throw Error('one-occurrence flip UNSAT');
   flipControls++;
   neighbors.add(canonical(G));
  }
 }
 if(neighbors.size!==2688||flipControls!==2688)throw Error('neighbor collision');
 const occurrenceTypes=[];
 for(let i=0;i<BASE.length;i++)for(let j=0;j<BASE[i].length;j++){
  const F=BASE.map(c=>[...c]);F[i][j]*=-1;
  const subtype=new Set();
  for(const p of PERMS)for(let mask=0;mask<16;mask++)subtype.add(canonical(apply(F,p,mask)));
  if(subtype.size!==384)throw Error('neighbor orbit unexpected');
  const rep=[...subtype].sort()[0];
  if(!neighborTypes.has(rep))neighborTypes.set(rep,[]);
  neighborTypes.get(rep).push([i+1,j+1]);
 }
 if(neighborTypes.size!==7||[...neighborTypes.values()].some(x=>x.length!==2))throw Error('signflip orbit classes mismatch');
 const stabilizer=[];
 for(const p of PERMS)for(let mask=0;mask<16;mask++)if(canonical(apply(BASE,p,mask))===canonical(BASE))stabilizer.push({permutation:p,complemented_variables:[1,2,3,4].filter(i=>mask&(1<<(i-1)))});
 if(stabilizer.length!==2)throw Error('wrong stabilizer');
 return {run:'LSPV1_SIGNED_ORBIT_MINCOST348',calculus:'Rmix341 binary premise unit weight',status:'PROVED/EXACT conditional on signed-rule equivariance; finite COMPUTATIONAL',original:BASE,group_order:384,orbit_size:orbit.size,stabilizer,proof_nodes_checked:proofNodesChecked,mixed_W_interval:[5,6],resolution_only_W_peer_reported:6,deletion_model_counts:deletionMultiset,source_deletion_checks:delControls,one_occurrence_sign_flips:flipControls,distinct_sat_neighbor_formulas:neighbors.size,distinct_sat_neighbor_orbits:neighborTypes.size,neighbor_orbit_classes:[...neighborTypes.values()],neighbor_orbit_size:384,control_labels:{original:'UNSAT',all_signed_renamings:'UNSAT',all_one_occurrence_flips:'SAT'},limitations:'Finite signed-orbit reduction only, not an asymptotic mixed lower bound or B3. Exact mixed W=6 unresolved due DEF seam.'};
}
if(typeof module!=='undefined' && require.main===module)console.log(JSON.stringify(atlas(),null,2));
if(typeof module!=='undefined')module.exports={atlas,BASE,canonical,parse,apply,satCount,resolve};
