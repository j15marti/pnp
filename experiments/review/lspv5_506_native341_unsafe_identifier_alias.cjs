#!/usr/bin/env node
'use strict';
/*
 * LSPV-5/506: accepted-byte numeric identifier alias audit for the unchanged
 * archived /341 checker.  This is a checker-language experiment, not a new
 * R_mix341 verifier and not a proof-complexity lower bound.
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||path.join(__dirname,'../..'));
const out=path.resolve(process.argv[3]||path.join(root,'results/raw/review'));
fs.mkdirSync(out,{recursive:true});
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const original=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checkerBlob='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const originalBlob='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(blob(fs.readFileSync(checker)),checkerBlob);
assert.equal(blob(fs.readFileSync(original)),originalBlob);
const seed=JSON.parse(fs.readFileSync(original,'utf8'));
const base=seed.fixtures[0];
const copy=x=>JSON.parse(JSON.stringify(x));

function packet(mode,declLex,refLex){
  const f=copy(base);
  const old=mode==='source'?f.clauses[0].id:f.proof[0].id;
  if(mode==='source'){
    f.clauses[0].id='__DECL_ID__';
    for(const d of f.deleted)if(d.sourceId===old)d.sourceId='__REF_ID__';
  }else{
    f.proof[0].id='__DECL_ID__';
  }
  for(const p of f.proof)p.parents=p.parents.map(x=>x===old?'__REF_ID__':x);
  let raw=JSON.stringify({fixtures:[f],summary:[seed.summary[0]]})+'\n';
  assert(raw.includes('"__DECL_ID__"')&&raw.includes('"__REF_ID__"'));
  raw=raw.replaceAll('"__DECL_ID__"',declLex).replaceAll('"__REF_ID__"',refLex);
  return Buffer.from(raw);
}
function run(name,mode,declLex,refLex,expected,save=false){
  const bytes=packet(mode,declLex,refLex);
  const tmp=path.join(os.tmpdir(),'lspv5-506-'+process.pid+'-'+name+'.json');
  fs.writeFileSync(tmp,bytes);
  const parsed=JSON.parse(bytes);
  const f=parsed.fixtures[0];
  const decl=mode==='source'?f.clauses[0].id:f.proof[0].id;
  const ref=mode==='source'?f.deleted[0].sourceId:f.proof.find(p=>p.parents.includes(decl))?.parents.find(x=>Object.is(x,decl));
  const proc=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',timeout:30000});
  fs.unlinkSync(tmp);
  const accepted=proc.status===0;
  assert.equal(accepted,expected,name+'\n'+proc.stderr);
  const row={name,mode,decl_lexeme:declLex,reference_lexeme:refLex,
    parsed_decl:String(decl),parsed_reference:String(ref),
    parsed_object_is: Object.is(decl,ref),accepted,expected,
    bytes:bytes.length,sha256:sha(bytes),
    checks:accepted?JSON.parse(proc.stdout).checks:null,
    rejection:accepted?null:(proc.stderr.match(/Verifier: ([^\n]+)/)?.[1]||proc.stderr.slice(0,180))};
  if(save){
    const p=path.join(out,'2026-11-12_0748_LSPV5_506_UNSAFE_ID_ALIAS_ACCEPTED.json');
    fs.writeFileSync(p,bytes);
    row.saved_path=path.relative(root,p);
  }
  return row;
}

const rows=[
 run('safe_equal_source','source','9007199254740991','9007199254740991',true),
 run('safe_distinct_source','source','9007199254740990','9007199254740991',false),
 run('unsafe_integer_rounding_alias_source','source','9007199254740992','9007199254740993',true,true),
 run('unsafe_integer_nonalias_source','source','9007199254740992','9007199254740994',false),
 run('unsafe_negative_rounding_alias_source','source','-9007199254740992','-9007199254740993',true),
 run('fractional_integer_alias_source','source','9007199254740992','9007199254740992.0',true),
 run('exponent_integer_alias_source','source','9007199254740992','9.007199254740993e15',true),
 run('overflow_infinity_alias_source','source','1e309','1e400',true),
 run('opposite_infinity_source','source','1e309','-1e309',false),
 run('unsafe_integer_rounding_alias_proof','proof','9007199254740992','9007199254740993',true),
 run('unsafe_integer_nonalias_proof','proof','9007199254740992','9007199254740994',false)
];
const accepted=rows.filter(x=>x.accepted),rejected=rows.filter(x=>!x.accepted);
assert.equal(accepted.length,7);assert.equal(rejected.length,4);
assert(rows.find(x=>x.name==='unsafe_integer_rounding_alias_source').parsed_object_is,true);
const result={
 id:'LSPV-5/506',date_local:'2026-11-12 07:48 PST',
 status:'COMPUTATIONAL original-checker accepted-byte counterexample; P versus NP OPEN',
 authority:{checker:'experiments/arc/lspv2_341_independent_verify.js',checker_blob:checkerBlob,
  source:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',source_blob:originalBlob,
  runtime:process.version},
 exact_scope:'K4 fixture of archived /341 checker; source and first-proof identifier declaration/reference pairs only',
 rows,counts:{accepted:accepted.length,rejected:rejected.length,total:rows.length,
  accepted_assertion_groups:accepted.reduce((a,x)=>a+x.checks,0)},
 result:'Distinct raw JSON numeric ID lexemes can parse to one ECMAScript Number and are then treated as the same Map key.',
 repair:'Authenticate ID lexical type/range before Number coercion: strings under a fixed grammar, or safe integers with Number.isSafeInteger; bind canonical source bytes externally.',
 limitations:['No full historical mixed dispatcher','No new sound refutation','No lower-bound or P2-B1 transfer','P2-B2/B3 remain separate']
};
const rawPath=path.join(out,'2026-11-12_0748_LSPV5_506_NATIVE341_UNSAFE_ID_ALIAS_RAW.json');
fs.writeFileSync(rawPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
