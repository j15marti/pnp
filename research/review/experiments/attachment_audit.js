#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');

const sourceDir = process.argv[2] || path.join(__dirname, '..', 'attachments', '2026-10-10');
const outPath = process.argv[3] || path.join(__dirname, 'attachment_audit_results.json');
const names = ['01-generator.html', '02-hash.html', '03-hash_tool.html'];
function contextFor(file) {
  const text = fs.readFileSync(path.join(sourceDir,file), 'utf8');
  const script = text.match(/<script>([\s\S]*?)<\/script>/)[1];
  const elements = new Map();
  const document = { getElementById(id) {
    if (!elements.has(id)) elements.set(id, {value:'',textContent:'',style:{},addEventListener(){}});
    return elements.get(id);
  }};
  const localMath = Object.create(Math);
  const context = vm.createContext({document,Math:localMath,TextEncoder,navigator:{clipboard:{writeText:async()=>{}}},setTimeout});
  vm.runInContext(script,context);
  return {context,elements,localMath,sha256:crypto.createHash('sha256').update(text).digest('hex')};
}
const gen=contextFor(names[0]), six=contextFor(names[1]), eight=contextFor(names[2]);
function seededRandom(seed) {
  let state=seed>>>0;
  return () => {state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};
}
function fixedDrawOutput(seed) {
  gen.localMath.random=seededRandom(20261010);
  gen.elements.get('seedInput').value=seed;
  vm.runInContext('generateHash()',gen.context);
  return gen.elements.get('outputText').textContent;
}
const seedTests=['A','B','1234567890123456','not-a-seed','!',''].map(seed=>({seed,output:fixedDrawOutput(seed)}));
const nonempty=seedTests.filter(x=>x.seed.replace(/[^A-Za-z0-9]/g,'').length);
if(new Set(nonempty.map(x=>x.output)).size!==1)throw new Error('Expected exact seed independence for nonempty cleaned seeds');
const hash6=six.context.compact6CharHash, hash8=eight.context.compact8CharHash;
let collision6=null;
const seen=new Map();
const nextSample=seededRandom(4042026);
for(let i=0;i<1000000;i++){
  const s='pnp:'+Array.from({length:4},()=>Math.floor(nextSample()*4294967296).toString(16).padStart(8,'0')).join(''),h=hash6(s);
  if(seen.has(h)){collision6={first:seen.get(h),second:s,hash:h,examined:i+1};break;}
  seen.set(h,s);
}
if(collision6 && hash6(collision6.first)!==hash6(collision6.second))throw new Error('Collision did not reproduce');
const capacity=[6,7,8].map(d=>({characters:d,alphabet:62,range_bound:(62n**BigInt(d)).toString(),bits:d*Math.log2(62)}));
const result={status:'FINITE_EXECUTABLE_AUDIT_ONLY',sources:names.map((name,i)=>({name,sha256:[gen,six,eight][i].sha256})),seedTests,nonemptySeedIndependence:true,capacity,collision6,eightCharSpotChecks:['','A','pnp-audit:1'].map(input=>({input,hash:hash8(input)})),limitations:'No 8-character collision search performed. Capacities and seed independence are exact; finite collision does not establish computational hardness or a SAT lower bound.'};
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
