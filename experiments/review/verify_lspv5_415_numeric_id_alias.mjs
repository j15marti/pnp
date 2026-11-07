import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import {spawnSync} from 'node:child_process';
const [checker,packet]=process.argv.slice(2); if(!checker||!packet) throw Error('usage: node verifier checker packet');
let checks=0; const assert=(x,m)=>{checks++;if(!x)throw Error(m)}; const base=JSON.parse(fs.readFileSync(packet,'utf8'));
function rawAlias(kind,a,b){const d=structuredClone(base),f=d.fixtures[0]; let old;
 if(kind==='source'){old=f.clauses[0].id;f.clauses[0].id='__A__';for(const x of f.deleted)if(x.sourceId===old)x.sourceId='__A__'}else{old=f.proof[0].id;f.proof[0].id='__A__'}
 for(const p of f.proof)p.parents=p.parents.map(x=>x===old?'__B__':x);
 return JSON.stringify(d).replaceAll('"__A__"',String(a)).replaceAll('"__B__"',String(b));}
function run(raw){const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv415-')),p=path.join(dir,'x.json');fs.writeFileSync(p,raw);const r=spawnSync('node',[checker,p],{encoding:'utf8'});fs.rmSync(dir,{recursive:true,force:true});return r.status===0;}
assert(run(fs.readFileSync(packet,'utf8')),'baseline');
assert(run(rawAlias('source','9007199254740992','9007199254740993')),'source collision');
assert(run(rawAlias('derived','9007199254740992','9007199254740993')),'derived collision');
assert(run(rawAlias('source','1152921504606846976','1152921504606846977')),'2^60 collision');
assert(!run(rawAlias('source','9007199254740990','9007199254740991')),'safe distinct');
assert(!run(rawAlias('source','9007199254740992','9007199254740994')),'representable distinct');
assert(JSON.parse('9007199254740992')===JSON.parse('9007199254740993'),'Number collision');
assert(Number.isSafeInteger(JSON.parse('9007199254740991')),'safe boundary');
assert(!Number.isSafeInteger(JSON.parse('9007199254740992')),'unsafe boundary');
console.log(JSON.stringify({status:'PASS',checks}));
