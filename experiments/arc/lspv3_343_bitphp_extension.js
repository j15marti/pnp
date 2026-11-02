#!/usr/bin/env node
"use strict";
// LSPV-3 BPHP-EXTENSION343. Deterministic finite source, sign, and prefix checks.
function produce() {
const out=[];
for(const ell of [1,2,3]) {
const n=1<<ell,m=n+1,clauses=[],ids=[];
for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let z=0;z<n;z++){
let c=[];for(const p of [i,j])for(let b=0;b<ell;b++){let x=p*ell+b+1;c.push((z>>b)&1?-x:x);}
ids.push([i,j,z]);clauses.push(c);
}
function bits(holes){const a=[];for(const h of holes)for(let t=0;t<ell;t++)a.push((h>>t)&1);return a;}
function val(c,a){return c.some(x=>x>0?a[x-1]===1:a[-x-1]===0);}
let deletions=0,flips=0,source_checks=0,prefix_checks=0,collision_checks=0;
for(let k=0;k<ids.length;k++){
const [i,j,z]=ids[k],holes=Array(m).fill(-1),other=Array.from({length:n},(_,a)=>a).filter(a=>a!==z);
holes[i]=holes[j]=z;
let t=0;for(let p=0;p<m;p++)if(p!==i&&p!==j)holes[p]=other[t++];
const a=bits(holes);
for(let q=0;q<clauses.length;q++){if(val(clauses[q],a)!==(q!==k))throw Error("source deletion control");source_checks++;}
for(let q=0;q<2*ell;q++){const changed=clauses[k].slice();changed[q]=-changed[q];if(!val(changed,a))throw Error("sign flip");flips++;}
deletions++;
}
function pref(a,len,s){for(let b=0;b<len;b++)if(((a>>b)&1)!==((s>>b)&1))return false;return true;}
for(let h=0;h<n;h++){
if(!pref(h,1,0)&&!pref(h,1,1))throw Error("first split");
if(Array.from({length:n},(_,z)=>Number(pref(h,ell,z))).reduce((x,y)=>x+y,0)!==1)throw Error("prefix totality");
for(let len=1;len<ell;len++)for(let s=0;s<1<<len;s++){
if(pref(h,len,s)&&!(pref(h,len+1,s)||pref(h,len+1,s|(1<<len))))throw Error("prefix split");
prefix_checks++;
}
}
for(let k=0;k<ids.length;k++){
const [i,j,z]=ids[k];
for(let a=0;a<n;a++)for(let b=0;b<n;b++){
const holes=Array(m).fill(0);holes[i]=a;holes[j]=b;
if(val(clauses[k],bits(holes))!==(a!==z||b!==z))throw Error("binary/unary collision");
collision_checks++;
}
}
const positive=bits(Array.from({length:n},(_,i)=>i));
for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let z=0;z<n;z++){
const cl=[];for(const p of [i,j])for(let b=0;b<ell;b++)cl.push((z>>b)&1?-(p*ell+b+1):p*ell+b+1);
if(!val(cl,positive))throw Error("positive label");
}
const dimacs="p cnf "+m*ell+" "+clauses.length+String.fromCharCode(10)+
clauses.map(c=>c.join(" ")+" 0"+String.fromCharCode(10)).join("");
out.push({ell,n,m,variables:m*ell,clauses:clauses.length,occurrences:2*ell*clauses.length,
dimacs_bytes:dimacs.length,dimacs_bits:8*dimacs.length,deletions,flips,source_checks,
prefix_checks,collision_checks,prefix_atoms:m*(2*n-2)});
}
return {id:"LSPV3-BPHP-EXTENSION343",cases:out,
totals:{deletions:out.reduce((s,c)=>s+c.deletions,0),signflips:out.reduce((s,c)=>s+c.flips,0),
collision_checks:out.reduce((s,c)=>s+c.collision_checks,0)},
limitation:"No complete global ER proof generator, only exact local checks."};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(produce(),null,2));
