'use strict';
// LSPV-1 GRID-BACKDOOR354: original signed sources, Resolution certificate,
// source-minimality, Horn selector and grid minor. No package dependencies.
const crypto=require('crypto');
const canon=C=>[...new Set(C)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function construct(k){
 if(!Number.isInteger(k)||k<2)throw Error('k must be at least two');
 const nodes=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)if(i||j)nodes.push([i,j]);
 const id=new Map(nodes.map(([i,j],t)=>[i+','+j,t+1]));
 const get=(i,j)=>id.get(i+','+j),z=nodes.length+1;
 const base=nodes.map(([i,j])=>i===0||j===0?{kind:'unit',i,j,cl:[get(i,j)]}:
     {kind:'gate',i,j,cl:[-get(i-1,j),-get(i,j-1),get(i,j)]});
 base.push({kind:'conflict',i:k-1,j:k-1,cl:[-get(k-1,k-1)]});
 let next=z+1,rows=[],sources=[],steps=[],tags=[],pairs=new Map();
 function add(c,meta){const a=canon(c);if(a.some(t=>a.includes(-t)))throw Error('taut source');
   const t=rows.length;rows.push(a);sources.push(a);tags.push(meta);return t;}
 function res(a,b,p){const A=rows[a],B=rows[b];if(!A.includes(p)||!B.includes(-p))throw Error('bad pivot');
   const C=canon(A.filter(t=>t!==p).concat(B.filter(t=>t!==-p)));
   if(C.some(t=>C.includes(-t)))throw Error('taut resolvent');
   const t=rows.length;rows.push(C);steps.push({a,b,p,c:C});return t;}
 base.forEach((b,t)=>[z,-z].forEach(g=>{
   if(b.cl.length===1)pairs.set(t+':'+g,[add([g,...b.cl],{t,g,part:0})]);
   else{const q=next++;
     pairs.set(t+':'+g,[add([g,b.cl[0],q],{t,g,part:1,q}),
       add([-q,b.cl[1],b.cl[2]],{t,g,part:2,q}),q]);}
 }));
 const original=[];
 base.forEach((b,t)=>{
   const halves=[z,-z].map(g=>{const a=pairs.get(t+':'+g);return a.length===1?a[0]:res(a[0],a[1],a[2]);});
   const v=res(halves[0],halves[1],z);original.push(v);
 });
 const units=new Map();let neg;
 base.forEach((b,t)=>{
   if(b.kind==='unit')units.set(b.i+','+b.j,original[t]);
   else if(b.kind==='gate'){
     const a=get(b.i-1,b.j),c=get(b.i,b.j-1);
     const u=res(units.get((b.i-1)+','+b.j),original[t],a);
     units.set(b.i+','+b.j,res(units.get(b.i+','+(b.j-1)),u,c));
   }else neg=original[t];
 });
 const end=res(units.get((k-1)+','+(k-1)),neg,get(k-1,k-1));
 if(rows[end].length!==0)throw Error('not a refutation');
 const m=sources.length,N=next-1,r=(k-1)**2;
 if(m!==2*k*k+2*r||N!==k*k+2*r||steps.length!==4*r+k*k+1)throw Error('wrong formula/count');
 for(const v of [0,1])for(const C of sources){
   if(C.some(l=>Math.abs(l)===z && +(l>0)===v))continue;
   if(C.filter(l=>Math.abs(l)!==z&&l>0).length>1)throw Error('not Horn');
 }
 const source_text='p cnf '+N+' '+m+'\n'+sources.map(C=>C.join(' ')+' 0\n').join('');
 return {k,variables:N,clauses:m,deficiency:m-N,grid_minor_tw_lower:k-1,
   selector:z,resolution_nodes:steps.length,source_floor:m-1,dimacs_bytes:Buffer.byteLength(source_text),
   sha256:crypto.createHash('sha256').update(source_text).digest('hex'),sources,steps,source_text};
}
const cases=[2,3,4,5].map(construct);
for(const x of cases)console.log(JSON.stringify({k:x.k,variables:x.variables,clauses:x.clauses,
 deficiency:x.deficiency,grid_minor_tw_lower:x.grid_minor_tw_lower,selector:x.selector,
 resolution_nodes:x.resolution_nodes,source_floor:x.source_floor,dimacs_bytes:x.dimacs_bytes,sha256:x.sha256}));
