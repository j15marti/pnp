#!/usr/bin/env node
// Independent LSPV-5/413 replay/scope check. Not a replacement R_mix341 grammar.
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const argv=process.argv.slice(2);
const get=(flag)=>{const i=argv.indexOf(flag);if(i<0||!argv[i+1])throw Error(`missing ${flag}`);return argv[i+1];};
const P={producer:get('--producer'),certificate:get('--certificate'),checker:get('--checker'),record:get('--record')};
const expected={
 producer:'4dd134c4e97fca273668480c64bb220201d67917c2cfe70c471a7bc785e396fc',
 certificate:'12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95',
 checker:'0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae',
 record:'af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be'
};
let checks=0; const ck=(v,m)=>{checks++;if(!v)throw Error(m);};
const h=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const hashes={};for(const k of Object.keys(P)){hashes[k]=h(P[k]);ck(hashes[k]===expected[k],`${k} hash`);}
const rawBytes=fs.readFileSync(P.certificate), raw=JSON.parse(rawBytes), record=JSON.parse(fs.readFileSync(P.record));
ck(raw.version==='LSPV2-MIXED-TSEITIN-MINDAG341/v1','version');ck(raw.fixtures.length===7,'fixtures');
const prod=spawnSync('node',[P.producer],{encoding:null});ck(prod.status===0,'producer exit');
ck(JSON.stringify(JSON.parse(prod.stdout))===JSON.stringify(raw),'semantic replay');
ck(rawBytes.equals(prod.stdout),'byte-identical producer replay');
const base=spawnSync('node',[P.checker,P.certificate],{encoding:'utf8'});ck(base.status===0,'baseline');
ck(JSON.stringify(JSON.parse(base.stdout))===JSON.stringify(record),'record replay');
const src=fs.readFileSync(P.checker,'utf8');
const tags=[...src.matchAll(/p\.rule==="([A-Z0-9_-]+)"/g)].map(x=>x[1]).sort();
ck(JSON.stringify(tags)===JSON.stringify(['AND3','XOR']),'tag set');
ck(src.includes('else throw Error("unknown rule")'),'closed unknown');
ck(src.includes('src.set(c.id,{kind:"factor"'),'source coercion');
ck(src.includes('a.kind==="factor"&&b.kind==="factor"&&p.kind==="factor"'),'AND3 types');
ck(src.includes('a.row&&b.row&&p.row&&p.kind==="affine"'),'XOR types');
const mutations={};
for(const tag of ['RES','LOCAL-CONVERT','DEF']){
 const x=structuredClone(raw);x.fixtures[0].proof[0].rule=tag;
 const d=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-413-')), f=path.join(d,'mut.json');
 fs.writeFileSync(f,JSON.stringify(x));
 const got=spawnSync('node',[P.checker,f],{encoding:'utf8'});
 fs.rmSync(d,{recursive:true,force:true});
 ck(got.status!==0,`${tag} accepted`);ck(got.stderr.includes('unknown rule'),`${tag} reason`);
 mutations[tag]={accepted:false,unknownRule:true};
}
for(const f of raw.fixtures){
 const s=new Set(f.proof.map(n=>n.rule));
 ck([...s].every(x=>x==='AND3'||x==='XOR'),'exhibited tag');
}
console.log(JSON.stringify({
 run:'LSPV-5/413-independent',
 hashes,
 baselineAccepted:true,
 recordChecks:record.checks,
 implementedRuleTags:tags,
 unimplementedDeclaredTags:['RES','LOCAL-CONVERT','DEF'],
 crossRuleRESIntoAND3:'not representable/decided by this checker',
 mutations,
 auditAssertions:checks,
 pVsNP:'OPEN'
},null,2));
