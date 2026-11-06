#!/usr/bin/env node
'use strict';
// LSPV-3/443 compact independent original-source/core control. No proof-size certificate.
// Run: node lspv3_443_core_control.js
const crypto=require('crypto');
let assertions=0;
const ok=(x,m)=>{assertions++;if(!x)throw Error(m)};
function gen(n,seed){let x=seed>>>0;const next=()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return x>>>0;};let out=[];
for(let i=0;i<8*n;i++){let ids=[];while(ids.length<3){let t=1+next()%n;if(!ids.includes(t))ids.push(t);}out.push(ids.map(j=>(next()&1)?j:-j));}return out;}
const dim=(n,c)=>'p cnf '+n+' '+c.length+'\n'+c.map(a=>a.join(' ')+' 0\n').join('');
const sat=(c,a)=>c.some(l=>{let b=((a>>>(Math.abs(l)-1))&1)===1;return l>0?b:!b;});
const cases=[
{n:10,seed:113,sha:'686f8db38a0dce4b8d83f2f445576ce5ae1212531a716297090af2b6ebb0ce55',min:3,ids:[2,4,24,31,33,42,49,51,53,67,79]},
{n:12,seed:36,sha:'fc82ae6a889fb735caf7c632eb131d525ebf9f92c7e22f5212516a7d98ebdbd2',min:5,ids:[6,20,22,38,40,43,47,56,66,81,89]}];
for(const r of cases){let c=gen(r.n,r.seed),input=dim(r.n,c),digest=crypto.createHash('sha256').update(input).digest('hex');ok(digest===r.sha,'original source hash mismatch');ok(c.every(t=>t.length===3&&new Set(t.map(Math.abs)).size===3),'not strict3');
let low=1e8;for(let a=0;a<(1<<r.n);a++)low=Math.min(low,c.reduce((k,z)=>k+(!sat(z,a)?1:0),0));ok(low===r.min,'bad original');
let core=r.ids.map(j=>c[j]);ok(new Set(r.ids).size===r.ids.length,'duplicate source');
for(let a=0;a<(1<<r.n);a++)ok(core.some(z=>!sat(z,a)),'core SAT');
for(let drop=0;drop<core.length;drop++){let witness=-1;for(let a=0;a<(1<<r.n);a++){if(core.every((z,j)=>j===drop||sat(z,a))){witness=a;break;}}ok(witness>=0,'core not essential');}
let changed=c.map(z=>z.slice());changed[0][0]*=-1;ok(crypto.createHash('sha256').update(dim(r.n,changed)).digest('hex')!==digest,'hash insensitive');
}
console.log(JSON.stringify({status:'PASS',assertions,claim:'source-truth/core-UNSAT/deletion-SAT controls; MILP global optimality NOT independently verified'},null,2));