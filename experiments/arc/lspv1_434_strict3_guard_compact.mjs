// LSPV-1/434 compact independently runnable finite controls. Node >=18.
// Full source-labelled producer, certificate and negative controls in archive.
'use strict';
import assert from 'node:assert/strict';
const cases={K4:[4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()],K33:[6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()],Cube:[8,Array.from({length:8},(_,i)=>[0,1,2].filter(b=>i<(i^(1<<b))).map(b=>[i,i^(1<<b)])).flat()]};
let checks=0;const ok=(x,msg)=>{assert(x,msg);checks++};
function rank(rs){const p=new Map;let n=0;for(let r of rs){let x=BigInt(r);while(x){const k=x.toString(2).length-1;if(p.has(k))x^=p.get(k);else{p.set(k,x);n++;break}}}return n}
function lit(v,x){const b=Boolean((BigInt(x)>>BigInt(Math.abs(v)-1))&1n);return v>0?b:!b}
function sat(C,x){return C.some(v=>lit(v,x))}
function old(v,edges,odd){let C=[];for(let j=0;j<v;j++){const es=edges.map((e,i)=>e.includes(j)?i+1:0).filter(Boolean);ok(es.length===3,'cubic');for(let t=0;t<8;t++){const bits=[t&1,(t>>1)&1,(t>>2)&1];if((bits[0]^bits[1]^bits[2])===(odd&&j===0?1:0))continue;C.push(es.map((x,k)=>bits[k]?-x:x))}}return C}
function guard(F,n){let G=[];for(let i=0;i<F.length;i++){const [a,b,c]=F[i],y=n+2+i;G.push([n+1,a,y],[-y,b,c])}return G}
function evaluate(name,meta,odd){const [v,edges]=meta,n=edges.length,F=old(v,edges,odd),G=guard(F,n),m=F.length;ok(m===4*v&&G.length===8*v,'source counts');ok(G.every(c=>new Set(c.map(Math.abs)).size===3),'proper ternary');const model=[];for(let x=0;x<(1<<n);x++)if(F.every(c=>sat(c,BigInt(x))))model.push(x);ok((model.length===0)===Boolean(odd),'parity');const base=1n<<BigInt(n),witness=[base];for(let j=0;j<n;j++)witness.push(base+(1n<<BigInt(j)));for(let i=0;i<m;i++){let x=0;while(!sat(F[i].slice(1),BigInt(x)))x++;witness.push(base+BigInt(x)+(1n<<BigInt(n+1+i)))}ok(witness.every(w=>G.every(c=>sat(c,w))),'witnesses');let span=rank(witness.map(w=>w^base));ok(span===n+m,'affine hyperplane');let full=span;if(!odd){const x=model[0];let w=BigInt(x);for(let i=0;i<m;i++){const y=n+2+i,p=G.slice(2*i,2*i+2);if(!p.every(c=>sat(c,w))){w|=1n<<BigInt(y-1);ok(p.every(c=>sat(c,w)),'local witness')}}ok(G.every(c=>sat(c,w)),'g=0 model');full=rank([...witness.map(z=>z^base),w^base]);ok(full===n+m+1,'full affine hull')}
for(let x=0;x<(1<<n);x++){let all=F.every(c=>sat(c,BigInt(x)));let gadget=true;for(let i=0;i<m;i++){const p=G.slice(2*i,2*i+2),y=n+2+i;const r=[0n,1n<<BigInt(y-1)].some(t=>p.every(c=>sat(c,BigInt(x)|t)));ok(r===sat(F[i],BigInt(x)),'projection');gadget&&=r}ok(gadget===all,'cofactor projection')}
return {graph:name,odd,source_clauses:m,guard_clauses:G.length,variables:n+1+m,affine_rank:full,models_F:model.length}}
const out=[];for(const [name,meta] of Object.entries(cases))for(const odd of [true,false])out.push(evaluate(name,meta,odd));console.log(JSON.stringify({run:'LSPV1-434-compact',checks,cases:out},null,2));
