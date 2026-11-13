'use strict';
const fs=require('fs'),os=require('os'),path=require('path'),crypto=require('crypto'),cp=require('child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const fixture=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const out=path.join(root,'results/raw/arc/2026-11-13_0848_LSPV5_526_NATIVE341_NUMERIC_ALIAS_RAW.json');
const acceptedOut=path.join(root,'results/raw/arc/2026-11-13_0848_LSPV5_526_NATIVE341_NUMERIC_ALIAS_ACCEPTED.json');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function replaceOnce(s,a,b){if(!s.includes(a))throw Error('missing target '+a);return s.replace(a,b);}
function run(raw,label){const d=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-526-')),f=path.join(d,label+'.json');fs.writeFileSync(f,raw);const p=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8'});fs.rmSync(d,{recursive:true,force:true});let parsed=null;if(p.status===0){parsed=JSON.parse(p.stdout);delete parsed.file;}return{accepted:p.status===0,status:p.status,parsed,error:(p.stderr.split('\n').find(x=>x.includes('Error:'))||'').trim()};}
const source=fs.readFileSync(fixture,'utf8'),canonical=JSON.stringify(JSON.parse(source));
const mutations=[
 ['graph_n','"n":4','"n":4e0'],
 ['edge_endpoints','"edges":[[0,1]','"edges":[[-0,1e0]'],
 ['charges','"charges":[1,0,0,0]','"charges":[1e0,-0,0e0,0.000]'],
 ['source_vertex','"vertex":0','"vertex":-0'],
 ['source_pattern','"pattern":0','"pattern":0e999'],
 ['source_literals','"literals":[1,2,3]','"literals":[1e0,2.0,3e0]'],
 ['proof_support','"support":[0,1,2]','"support":[-0,1e0,2.0]'],
 ['proof_table','"table":246','"table":2.46e2']
];
const base=run(canonical,'baseline');if(!base.accepted)throw Error('baseline rejected');
const cases=[];for(const [name,target,replacement] of mutations){const raw=replaceOnce(canonical,target,replacement),r=run(raw,name);if(!r.accepted||JSON.stringify(r.parsed)!==JSON.stringify(base.parsed))throw Error(name+' mismatch');cases.push({name,target,replacement,sha256:sha(Buffer.from(raw)),checker:r});}
let composite=canonical;for(const [,target,replacement] of mutations)composite=replaceOnce(composite,target,replacement);const cr=run(composite,'composite');if(!cr.accepted||JSON.stringify(cr.parsed)!==JSON.stringify(base.parsed))throw Error('composite mismatch');
const badControls=[
 ['fractional_vertex','"vertex":0','"vertex":0.5'],
 ['fractional_literal','"literals":[1,2,3]','"literals":[1.5,2,3]'],
 ['fractional_table','"table":246','"table":246.5']
].map(([name,a,b])=>{const r=run(replaceOnce(canonical,a,b),name);if(r.accepted)throw Error(name+' accepted');return{name,checker:r};});
const result={run:'LSPV-5/526',timestamp_pst:'2026-11-13 08:48 PST',node:process.version,inputs:{checker:path.relative(root,checker),checker_sha256:sha(fs.readFileSync(checker)),fixture:path.relative(root,fixture),fixture_sha256:sha(fs.readFileSync(fixture)),canonical_sha256:sha(Buffer.from(canonical))},baseline:{sha256:sha(Buffer.from(canonical)),checker:base},accepted_aliases:cases,composite:{sha256:sha(Buffer.from(composite)),bytes:Buffer.byteLength(composite),checker:cr,saved_as:path.relative(root,acceptedOut)},nonintegral_controls:badControls,theorem:'The archived /341 accepted-byte language is not a canonical-decimal-integer language. At the tested graph, source, proof and table coordinates, JSON numeric lexemes -0, exponent notation and integral decimal notation are accepted whenever JSON.parse maps them to the same Number value as the canonical integer.',classification:{failure:'P2-D1 canonical numeric byte-syntax authentication failure',not_shown:['semantic unsoundness','cheap native refutation','P2-C3','P2-B1','P2-B2/B3 transfer']},cegar:'All eight alias paths and their composite were replayed in the authoritative checker and are genuine. They cannot be refined away. A canonical field-specific integer lexer would be a new versioned grammar.',cost:'Aliases produce exactly the baseline parsed proof and logical work. Physical byte length and parsing work differ and must be charged in a machine model.'};
fs.writeFileSync(acceptedOut,composite);fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({run:result.run,aliases:cases.length,checks:base.parsed.checks,cases:base.parsed.cases.length,composite_sha256:result.composite.sha256},null,2));
