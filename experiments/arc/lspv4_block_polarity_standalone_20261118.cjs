#!/usr/bin/env node
/* Reproducible exact finite counterexample + original FLMV recurrence audit.
 * No external dependencies. No runtime lower-bound claimed.
 * Usage: node lspv4_block_polarity_standalone_20261118.cjs
 */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const HASH=(b)=>crypto.createHash('sha256').update(b).digest('hex');
let checks=0, exhaustiveChecks=0;
function B(t,u){const cs=[];for(let i=0;i<t;i++)cs.push(((u>>i)&1)?-(i+1):i+1);return [cs.concat(t+u+1),cs.concat(-(t+u+1))]}
function clauseSat(cl,z){return cl.some(l=>(Number((BigInt(z)>>BigInt(Math.abs(l)-1))&1n)===((l>0)?1:0)))}
function blockBad(t,u,z){let [p,q]=B(t,u);for(let x=0;x<2;x++){const bits=BigInt(z) | (BigInt(x)<<BigInt(t+u)); if(clauseSat(p,bits)&&clauseSat(q,bits))return false}return true}
function model(t,U){const cls=U.flatMap(u=>B(t,u));let num=0;for(let bits=0;bits<2**(t+(2**t));bits++){if(cls.every(c=>clauseSat(c,bits)))num++}return num}
function audit(){let cases=[];for(let t=1;t<=5;t++){const q=2**t, U=Array.from({length:q},(_,i)=>i);for(let z=0;z<q;z++){assert.equal(U.filter(u=>blockBad(t,u,z)).length,1);checks++}
for(let omitted=0;omitted<q;omitted++){const sub=U.filter(u=>u!==omitted);for(let z=0;z<q;z++){const bad=sub.filter(u=>blockBad(t,u,z));assert.deepEqual(bad,z===omitted?[]:[z]);checks++; if(z!==omitted){assert(blockBad(t,z,z));checks++}}
if(t<=3){assert.equal(model(t,sub),2**q);exhaustiveChecks++}}
if(t<=3){assert.equal(model(t,U),0);exhaustiveChecks++;assert.equal(model(t,[]),2**(t+q));exhaustiveChecks++}
cases.push({t,q,clauses:2*q,unique_bad_per_z:true,delete_one_sat_models:2**q});}
let f=1,g=1,c=1.33,flmv=[];for(let k=1;k<=12;k++){f=c*f/(1+f);g=c*c*g/(1+c*g);flmv.push({k,det:Math.min((1/f-c)/k,c**(-k)),co:Math.min((1/g-c)/k,c**(-2*k))})}
const res={source:'FLMV JACM 2005 Theorems 5.7,6.4',cases,checks,exhaustiveChecks,flmv_c_1_33:flmv,finite_status:'COMPUTATIONAL; symbolic proof in report',unrestricted_p_np:'OPEN'};
const out=JSON.stringify(res,null,2)+'\n';fs.writeFileSync('LSPV4_BLOCK_POLARITY_STANDALONE_RAW_20261118.json',out);console.log('PASS',checks,'local checks,',exhaustiveChecks,'brute counts; det',Math.max(...flmv.map(x=>x.det)),'co',Math.max(...flmv.map(x=>x.co)),'raw_sha256',HASH(out));}
audit();
