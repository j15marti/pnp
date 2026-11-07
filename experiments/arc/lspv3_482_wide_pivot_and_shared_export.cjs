'use strict';
// LSPV-3/482, declared FACET-A export fragment, NOT historical R_mix341.
// Run: node lspv3_482_wide_pivot_and_shared_export.cjs
let checks=0, rejected=0;
function ck(p,m){checks++; if(!p) throw Error(m||'assertion');}
function clause(C){let s=new Set;for(let x of C){if(!Number.isInteger(x)||!x||s.has(-x))throw Error('malformed clause');s.add(x)}return [...s]}
function res(A,B,p){ck(A.includes(p)&&B.includes(-p),'pivot');return clause(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)))}
function isTrue(C,a){return C.some(l=>(l>0)==Boolean((a>>(Math.abs(l)-1))&1))}
function models(F,n){let m=[];for(let a=0;a<2**n;a++)if(F.every(C=>isTrue(C,a)))m.push(a);return m}
function subsets(n,d){let ss=[[]];for(let x=0;x<n;x++)for(const S of ss.slice())if(S.length<d)ss.push([...S,x]);return ss}
function project(k){let A=Array.from({length:k},(_,i)=>i+2),B=Array.from({length:k},(_,i)=>k+i+2);
 let F=[[1,...A],[-1,...B]],n=2*k+1,M=models(F,n),bad=[],tested=0;
 ck(res(F[0],F[1],1).join()===[...A,...B].join(),'resolvent');
 for(const S of subsets(n,3)){let P=new Set(M.map(v=>S.reduce((m,i,j)=>m|(((v>>i)&1)<<j),0)));tested++;if(P.size!==2**S.length)bad.push(S.map(i=>i+1));}
 ck(M.length===2**(k+1)*(2**k-1),'model count');ck((bad.length===0)===(k>=3),'arity threshold');
 return {k,n,models:M.length,three_support_projections:tested,nonfull_three_support:bad,wide_resolvent:2*k};
}
function facets(a,b,z){return [[-a,z],[-b,z],[a,b,-z]]}
function validGate(a,b,z,fs){for(let x=0;x<4;x++){
 let aa=x&1,bb=(x>>1)&1,zz=aa|bb,V=new Map([[Math.abs(a),a>0?aa:1-aa],[Math.abs(b),b>0?bb:1-bb],[z,zz]]);
 for(const f of fs)if(!f.some(l=>l>0?V.get(l)===1:V.get(-l)===0))return false;
}return true}
function exportAll(sources,steps){
 let lines=sources.map(clause),rSteps=[];for(const t of steps){const out=res(lines[t.i],lines[t.j],t.p);lines.push(out);rSteps.push({...t,out})}
 let next=Math.max(...lines.flat().map(Math.abs))+1,byTerm=new Map(),defs=[],trace=[],out=[];
 function gate(a,b){let k=a+':'+b;if(byTerm.has(k))return byTerm.get(k);let z=next++;let fs=facets(a,b,z);ck(validGate(a,b,z,fs),'gate facets');defs.push({a,b,z,facets:fs});byTerm.set(k,z);return z}
 for(let owner=0;owner<lines.length;owner++){let C=lines[owner];if(C.length<2)continue;
  let row=C.slice(),left=C[0],z;
  for(let i=1;i<C.length;i++){
   let right=C[i];z=gate(left,right);
   let mid=res(row,[-left,z],left);trace.push({owner,from:row.slice(),facet:[-left,z],out:mid.slice()});
   row=res(mid,[-right,z],right);trace.push({owner,from:mid.slice(),facet:[-right,z],out:row.slice()});
   left=z;
  }
  ck(row.length===1&&row[0]===z,'exported unit');out.push({owner,unit:z,original:C});
 }
 let L=lines.reduce((a,C)=>a+Math.max(0,C.length-1),0);
 ck(trace.length===2*L&&defs.length<=L,'cost accounting');
 return {original_source:sources,source_resolution:rSteps,definition_records:defs,derived_export_trace:trace,exported_units:out,L,g:defs.length,q:steps.length,paid_nodes:steps.length+defs.length+trace.length,unshared_upper:steps.length+3*L};
}
let projected=[2,3,4,5].map(project);
let source=[[1,2,3,4],[1,2,3,5],[-1,6,7,8]];
let cert=exportAll(source,[{i:0,j:2,p:1}]);
ck(cert.L===14&&cert.g===12&&cert.paid_nodes===41&&cert.unshared_upper===43,'shared-prefix saving');
for(let b of [
 ()=>res(source[0],source[2],2),
 ()=>clause([1,-1]),
 ()=>validGate(1,2,9,[[1,9],[-2,9],[1,2,-9]])&&(()=>{throw Error('unsound facet')})(),
 ()=>exportAll(source,[{i:0,j:1,p:1}])
]){let failed=false;try{let result=b();if(result===false)throw Error('bad facet rejected')}catch(_){failed=true}ck(failed,'negative control');rejected++}
let summary={run:'LSPV3-482/v2',status:'PROVED/RESTRICTED plus COMPUTATIONAL',model:'declared FACET-A only; original historical R_mix341 remains unauthenticated',projected,compiler:{q:cert.q,L:cert.L,shared_definition_records:cert.g,paid_nodes:cert.paid_nodes,unshared_upper:cert.unshared_upper,units:cert.exported_units.map(u=>({owner:u.owner,unit:u.unit,width:u.original.length})),definition_reuse:2},checks,negative_rejections:rejected};
if(typeof process!=='undefined'&&typeof console!=='undefined')console.log(JSON.stringify(summary,null,2));
globalThis.lspv3_482={summary,cert};
