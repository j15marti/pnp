#!/usr/bin/env node
"use strict";
/* LSPV-4 346; independent-dependency-free executable. Run: node lspv4_346_arity_weighted_horn_macro_compact.js
   A comparative Horn-UP macro is NOT silently added to preselected Rmix341.
   Status: exact mathematical all-arity theorem; finite checks COMPUTATIONAL. */
const assert=require("assert");
function src(m) {const c=[[1]];for(let i=1;i<m-1;i++)c.push([-i,i+1]);c.push([-(m-1)]);return c;}
function sat(f,a){return f.every(c=>c.some(x=>Boolean(a[Math.abs(x)-1])===(x>0)));}
function models(f,n){let k=0;for(let x=0;x<2**n;x++){let a=Array.from({length:n},(_,i)=>(x>>i)&1);k+=Number(sat(f,a));}return k;}
function witness(m,j){if(j===0)return Array(m-1).fill(0);if(j===m-1)return Array(m-1).fill(1);return Array.from({length:m-1},(_,i)=>Number(i<j));}
function signBits(f,n){const w=n.toString(2).length;return f.flat().map(x=>(x<0?"1":"0")+Math.abs(x).toString(2).padStart(w,"0")).join("");}
function hornUP(f){const a={};const steps=[];for(;;){let found=false;for(let j=0;j<f.length;j++){
 const c=f[j];if(c.some(x=>Object.hasOwn(a,Math.abs(x))&&Boolean(a[Math.abs(x)])===(x>0)))continue;
 const rem=c.filter(x=>!Object.hasOwn(a,Math.abs(x)));
 if(rem.length===0){steps.push({op:"conflict",source:j});return steps;}
 if(rem.length===1){a[Math.abs(rem[0])]=Number(rem[0]>0);steps.push({op:"unit",source:j,lit:rem[0]});found=true;break;}
}if(!found)throw Error("unit propagation did not refute");}}
function resolve(a,b,p){assert(a.includes(p)&&b.includes(-p));const x=[...new Set([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)])];assert(!x.some(v=>x.includes(-v)));return x.sort((i,j)=>Math.abs(i)-Math.abs(j));}
function replay(f,proof){const db={};f.forEach((c,i)=>db["S"+i]=c);for(let i=0;i<proof.length;i++){const st=proof[i];assert.deepStrictEqual(st.out,resolve(db[st.left],db[st.right],st.pivot));db["D"+i]=st.out;}assert.deepStrictEqual(db["D"+(proof.length-1)],[]);}
function tseitin(charges){const e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);const cs=[];for(let v=0;v<4;v++){const ids=e.flatMap((x,i)=>x.includes(v)?[i+1]:[]);for(let mask=0;mask<8;mask++){const bits=[mask&1,(mask>>1)&1,(mask>>2)&1];if(bits.reduce((x,y)=>x+y,0)%2===charges[v])continue;cs.push(ids.map((id,i)=>bits[i]?-id:id));}}return cs;}
const out=[];let flipChecks=0,deleteChecks=0,traceChecks=0;
for(let m=2;m<=10;m++){const f=src(m),n=m-1;assert.equal(models(f,n),0);const original=signBits(f,n);
for(let j=0;j<m;j++){const a=witness(m,j);assert(sat(f.filter((_,i)=>i!==j),a));assert(!sat(f,a));deleteChecks++;
for(let k=0;k<f[j].length;k++){let g=f.map(c=>c.slice());g[j][k]*=-1;assert(sat(g,a));let b=signBits(g,n);assert.equal(b.length,original.length);assert.equal([...b].filter((x,i)=>x!==original[i]).length,1);flipChecks++;}}
let previous=f[0],proof=[];
for(let j=1;j<m;j++){let next=resolve(previous,f[j],j);proof.push({left:j===1?"S0":"D"+(j-2),right:"S"+j,pivot:j,out:next});previous=next;}
replay(f,proof);
const trace=hornUP(f);assert.equal(trace.length,m);assert.equal(trace.at(-1).op,"conflict");traceChecks+=m;
assert.equal(proof.length,m-1); // Exact: source-essential floor and matching proof.
out.push({m,n,source_clauses:m,occurrence_signs:2*m-2,unit_macro_nodes:1,arity_weighted_cost:m-1,resolution_nodes:m-1});}
assert.equal(flipChecks,90);assert.equal(deleteChecks,54);
assert.equal(models(tseitin([1,0,0,0]),6),0);assert.equal(models(tseitin([0,0,0,0]),6),8);
const result={run:"LSPV4_ARITY_WEIGHTED_HORN_MACRO346",date_local:"2026-11-02 17:32 PST",
 status:{source_capacity:"PROVED/EXACT",finite:"COMPUTATIONAL",B2_B3:"OPEN"},
 m_range:[2,10],deleteChecks,flipChecks,traceChecks,oddTseitinModels:0,evenTseitinModels:8,by_m:out};
process.stdout.write(JSON.stringify(result,null,2)+"\n");
