#!/usr/bin/env node
/* Independent verifier of LSPV-2/407 completion divergence.
 * Reconstructs truth tables and GF(2) sums from producer's raw result.
 * Usage: node lspv2_407_independent.js [raw.json]
 */
const fs = require('fs');
const path = process.argv[2] || '2026-11-04_2012_LSPV2_PORT_DIVERGENCE407_raw.json';
const data = JSON.parse(fs.readFileSync(path,'utf8'));
let tests = 0;
function ok(x,msg){tests++; if(!x) throw new Error(msg);}
function norm(names,rhs){return {variables:[...new Set(names)].sort(),rhs};}
function rowEquals(a,b){return a.rhs===b.rhs && JSON.stringify(a.variables)===JSON.stringify(b.variables);}
function rowXor(a,b){const d={}; for(const s of [...a.variables,...b.variables])d[s]=1-(d[s]||0);return norm(Object.keys(d).filter(k=>d[k]),a.rhs^b.rhs);}
function valRow(r,v){return r.variables.reduce((p,k)=>p^v[k],0)===r.rhs;}
const p=data.proof;
ok(p.length===6,'six paid records');
ok(JSON.stringify(p.map(v=>v.rule))===JSON.stringify(['AND3','DEF','DEF','XOR','XOR','LOCAL-CONVERT']),'rule sequence');
ok(p[0].parents.join()==='S1,S2','AND original provenance');
ok(p[1].output==='a'&&p[2].output==='b','fresh outputs');
ok(JSON.stringify(p[2].parents)==='[2]','DEF b references paid parent gate');
ok(p[1].inputs.join()==='x,y'&&p[2].inputs.join()==='a,y','gate input order');
ok(rowEquals(p[0].row,norm(['x'],1)),'AND3 affine annotation');
ok(rowEquals(p[1].port,norm(['a','x','y'],0)),'DEF a equation');
ok(rowEquals(p[2].port,norm(['a','b','y'],0)),'DEF b equation');
ok(rowEquals(p[3].row,rowXor(p[1].port,p[2].port)),'first GF2 signed row');
ok(rowEquals(p[4].row,rowXor(p[3].row,p[0].row)),'second GF2 signed row');
ok(JSON.stringify(p[5].clause)==='["b"]','final clause');
let sourceModels=0;
for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){
 const s=(x===1)&&((x|y)===1),a=x^y,b=a^y,v={x,y,a,b};
 if(s){sourceModels++;ok(b===1,'positive target entailed');}
 ok(b===x,'conservative cancellation');
 ok(valRow(p[1].port,v)&&valRow(p[2].port,v),'paid row definitions');
 ok(valRow(p[3].row,v),'GF2 cancellation');
 if(s)ok(valRow(p[0].row,v)&&valRow(p[4].row,v),'source row');
 const opposite=(x===0)&&((x|y)===1);
 if(opposite)ok(b===0,'signed-source falsifier');
 const invalidB=(a^y)^1;
 if(s)ok(invalidB===0,'XNOR falsifier');
}
ok(sourceModels===2,'two SAT original-source valuations');
ok(data.Splus.accepted&&!data.Sminus.accepted,'distinct semantics');
ok(data.Sminus.first_rejected_node===4,'first disputed row export');
for(const v of Object.values(data.falsifiers))ok(!v.accepted,'invalid fixture rejected');
console.log(JSON.stringify({status:'PASS',independent_checks:tests,completion_difference:'Splus accepts; Sminus rejects at node 4',source_models:sourceModels}));