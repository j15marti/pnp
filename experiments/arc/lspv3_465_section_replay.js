// LSPV-3/465 self-contained section-tree checker. Run: node lspv3_465_section_replay.js
"use strict";
function fail(m){throw Error(m)}
function gate(a,b,z){let out=[];for(let t=0;t<8;t++){let u=t&1,v=(t>>1)&1,w=(t>>2)&1;if(w!==(u^v))out.push([u?-a:a,v?-b:b,w?-z:z]);}return out}
function make(k){let c=[],z=[];for(let i=0;i<k-1;i++)z.push(k+i+1);c.push(...gate(1,2,z[0]));for(let j=1;j<z.length;j++)c.push(...gate(z[j-1],j+2,z[j]));return{c,z}}
function leaf(c,z,p){for(let mask=0;mask<1<<z.length;mask++){const v={};p.forEach((a,i)=>{if(a!==2)v[i+1]=a});z.forEach((a,i)=>{v[a]=(mask>>i)&1});if(c.every(cl=>cl.some(l=>v[Math.abs(l)]!==undefined&&v[Math.abs(l)]===(l>0?1:0))))return true}return false}
const rows=[];let checks=0;
for(let k=2;k<=7;k++){const {c,z}=make(k);let eligible=0,incomplete=0;for(let u=0;u<3**k;u++){let t=u,p=[];for(let i=0;i<k;i++){p.push(t%3);t=Math.floor(t/3)}const a=leaf(c,z,p),b=!p.includes(2);if(a!==b)fail("bad section k="+k+" u="+u);eligible+=a;incomplete+=!b;checks++}if(eligible!==2**k||c.length!==4*(k-1))fail("bad count");rows.push({k,proper_3CNF_clauses:c.length,fresh:k-1,full_eligible_leaves:eligible,ineligible_partial_leaves:incomplete})}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],source=[];for(let v=0;v<4;v++){const inc=edges.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean);for(let b=0;b<8;b++)if((((b&1)+((b>>1)&1)+((b>>2)&1))%2))source.push(inc.map((x,i)=>((b>>i)&1)?-x:x))}
let models=0;const branch=new Set();for(let a=0;a<64;a++){if(source.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))){models++;branch.add(a&1);const parity=[2,3,4,5].reduce((s,j)=>s^((a>>(j-1))&1),0);if(parity!==0)fail("K4 cut parity");checks++}}if(models!==8||branch.size!==2)fail("bad K4 models");
console.log(JSON.stringify({rows,k4_even_charge_source_clauses:source.length,k4_models:models,checks,model:"constant full auxiliary assignments at each original-only decision-tree leaf",status:"COMPUTATIONAL, not historical R_mix341 accepted-byte"},null,2));
