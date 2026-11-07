import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import {spawnSync} from 'node:child_process';
const [checker,packet]=process.argv.slice(2); if(!checker||!packet)throw Error('usage: node verifier checker packet');
const baseline=fs.readFileSync(packet,'utf8'), base=JSON.parse(baseline); let checks=0;
function assert(x,m){checks++;if(!x)throw Error(m)}
function rawAlias(kind,a,b){const d=structuredClone(base),f=d.fixtures[0];let old;
 if(kind==='source'){old=f.clauses[0].id;f.clauses[0].id='__D__';for(const x of f.deleted)if(x.sourceId===old)x.sourceId='__D__'}
 else{old=f.proof[0].id;f.proof[0].id='__D__'}
 for(const p of f.proof)p.parents=p.parents.map(x=>x===old?'__R__':x);
 return JSON.stringify(d).replaceAll('"__D__"',a).replaceAll('"__R__"',b)}
function run(raw){const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv416-')),p=path.join(dir,'x.json');fs.writeFileSync(p,raw);const r=spawnSync('node',[checker,p],{encoding:'utf8'});fs.rmSync(dir,{recursive:true,force:true});return r.status===0}
assert(run(baseline),'baseline');
for(const [kind,a,b] of [['source','-0','0'],['source','1','1.0'],['source','1','1e0'],['source','1','1E+0'],['source','-1','-1.0'],['derived','-0','0'],['derived','1','1e0']])assert(run(rawAlias(kind,a,b)),`${kind} ${a}/${b}`);
assert(!run(rawAlias('source','0','1')),'source distinct control');
assert(!run(rawAlias('derived','1','2')),'derived distinct control');
assert(Object.is(JSON.parse('-0'),-0),'JSON preserves negative zero');
assert(!Object.is(JSON.parse('-0'),JSON.parse('0')),'signed zero values differ under SameValue');
assert(new Map([[JSON.parse('-0'),'x']]).get(JSON.parse('0'))==='x','Map SameValueZero alias');
assert(JSON.parse('1')===JSON.parse('1.0')&&JSON.parse('1')===JSON.parse('1e0'),'lexical value aliases');
console.log(JSON.stringify({status:'PASS',checks}));
