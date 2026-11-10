#!/usr/bin/env node
'use strict';
// LSPV-1/554. Run from j15marti/pnp repository root.
// Original /341 verifier semantics UNMODIFIED except for in-memory I/O.
// Source/AND3/XOR fragment only, NOT complete historical R_mix341.
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const pp='experiments/arc/lspv2_341_mixed_tseitin_min_dag.js';
const vp='experiments/arc/lspv2_341_independent_verify.js';
const p=fs.readFileSync(pp,'utf8'),v=fs.readFileSync(vp,'utf8');
const sha=s=>{let b=Buffer.from(s);return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');};
assert.equal(sha(p),'4081022e8a3841d79f751a3d3a7a10decbb026da');
assert.equal(sha(v),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
function replace1(s,old,newText){assert.equal(s.split(old).length,2,'unique anchor: '+old);return s.replace(old,newText);}
const a='add("PRISM16",32,prism(16));';
let ps=replace1(p,a,a+'\nfor(const k of [3,4,5,8,12,24,40]) add("PRISM_NEW_"+k,2*k,prism(k));\nfor(let mask=1;mask<64;mask++){if((mask.toString(2).split("1").length-1)%2===1)add("ODD_CHARGE_"+mask,6,prism(3));}');
ps=replace1(ps,'const charges=Array(g.n).fill(0);charges[0]=1;',
'const charges=Array(g.n).fill(0);if(g.name.startsWith("ODD_CHARGE_")){let mask=Number(g.name.split("_").at(-1));for(let i=0;i<g.n;i++)charges[i]=(mask>>i)&1;}else charges[0]=1;');
ps=replace1(ps,'const evenWitness=solve(g,even);','const evenWitness=solve(g,Array(g.n).fill(0));');
const mute={log(){}};
const packet=new Function('console',ps+';return data;')(mute);
const vs=replace1(v,"const fs=require('fs'); const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));",'const data=packet;');
const check=new Function('packet','console',vs+';return verify(data);');
const good=check(packet,mute);
const prism=good.cases.filter(z=>z.name.startsWith('PRISM_NEW_'));
const charge=good.cases.filter(z=>z.name.startsWith('ODD_CHARGE_'));
assert.equal(prism.length,7);assert.equal(charge.length,32);assert.equal(packet.fixtures.length,46);
for(const x of prism){let k=Number(x.name.split('_').at(-1));assert.equal(x.proofNodes,8*k-1);assert.equal(x.essential,8*k);assert(x.allEssential);}
for(const x of charge){assert.equal(x.proofNodes,23);assert.equal(x.essential,24);assert(x.allEssential);}
function reject(label,f){let clone=JSON.parse(JSON.stringify(packet));f(clone);try{check(clone,mute)}catch(e){return {label,pass:true,error:String(e)}}throw Error('negative control accepted: '+label);}
const negative=[
reject('signed source',x=>{x.fixtures.find(f=>f.graph.name==='PRISM_NEW_40').clauses[0].literals[0]*=-1}),
reject('affine sink',x=>{x.fixtures.find(f=>f.graph.name==='PRISM_NEW_40').proof.at(-1).row.rhs^=1}),
reject('even charge',x=>{x.fixtures.find(f=>f.graph.name==='ODD_CHARGE_1').charges[0]^=1}),
reject('unsupported RES',x=>{x.fixtures.find(f=>f.graph.name==='PRISM_NEW_40').proof[0].rule='RES'}),
reject('deleted clause',x=>{x.fixtures.find(f=>f.graph.name==='PRISM_NEW_40').clauses.pop()})
];
console.log(JSON.stringify({
 status:'COMPUTATIONAL, recovered SOURCE/AND3/XOR checker only',
 producer_blob:sha(p),verifier_blob:sha(v),
 acceptance:{original_fixtures:7,total_fixtures:46,checks:good.checks,prism,odd_charge_names:charge.map(x=>x.name)},negative,
 note:'Generator extensions declared. Original checker logic unchanged; external source and full R_mix341 rule inventory NOT authenticated.'
},null,2));
