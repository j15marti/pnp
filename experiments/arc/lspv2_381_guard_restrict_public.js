#!/usr/bin/env node
"use strict";
// Public compact reproducer for LSPV-2/381, independently described signed-AND2 grammar.
// Complete Python producer and independent JS checker also shipped in local reproducibility archive.
function norm(xs){const s=new Set(xs);if([...s].some(x=>s.has(-x)))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1))}
function res(a,b,p){if(a.includes(p)&&b.includes(-p))return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
 if(a.includes(-p)&&b.includes(p))return norm([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]);
 throw Error("illegal signed pivot")}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
let checked=0;for(const a of [1,-1]){
 const t=2,z=3;
 const S1=norm([-t,a]),S2=norm([-t,-a]);
 const D2=norm([-z,a]),D3=norm([z,-t,-a]);
 const R1=res(S2,D2,1),R2=res(S1,D3,1),R3=res(R1,R2,z);
 if(!eq(R1,norm([-t,-z]))||!eq(R2,norm([-t,z]))||!eq(R3,[-t]))throw Error("bad guarded proof");
 if(!eq(res([a],[-a],1),[]))throw Error("bad t=1 restricted proof");
 checked+=4;
}
const c=[];for(let a of [0,1,-1])for(let b of [0,2,-2])c.push(norm([a,b].filter(Boolean)));
const vals=[0,1,3,-3,4,-4];function sub(C,e){let out=[];
 for(let l of C){let v=e[Math.abs(l)];if(l<0)v=v===0?1:v===1?0:-v;if(v===1)return null;if(v!==0)out.push(v)}return norm(out)}
let cases=0,nonnull=0;
for(const A of c)for(const B of c)for(const pivot of [1,2]){
 if(!((A.includes(pivot)&&B.includes(-pivot))||(A.includes(-pivot)&&B.includes(pivot))))continue;
 const R=res(A,B,pivot);
 for(let a of vals)for(let b of vals){
 cases++;const e={1:a,2:b},P=sub(A,e),Q=sub(B,e),V=R===null?null:sub(R,e);
 if(V===null)continue;
 nonnull++;
 if((P!==null&&P.every(x=>V.includes(x)))||(Q!==null&&Q.every(x=>V.includes(x))))continue;
 if(P===null||Q===null)throw Error("missing premise");
 const D=res(P,Q,Math.abs(e[pivot]));
 if(D===null||!D.every(x=>V.includes(x)))throw Error("substitution transport failed");
 }
}
if(cases!==1296||nonnull!==864)throw Error("unexpected coverage");
console.log(JSON.stringify({fixture_polarities:2,guarded_proof_nodes:4,restricted_proof_nodes:1,substitution_cases:cases,non_tautological_cases:nonnull,status:"PASS"},null,2));