#!/usr/bin/env node
'use strict';
/*
 * LSPV-5/507: raw JSON numeric-token audit of the paid-owner declaration to
 * DEF-record reference join in the unchanged archived /386 checker.
 * This audits checker language only; it is not a new R_mix341 verifier.
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||path.join(__dirname,'../..'));
const out=path.resolve(process.argv[3]||path.join(root,'results/raw/review'));
fs.mkdirSync(out,{recursive:true});
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const source=path.join(root,'results/raw/arc/2026-11-12_0936_LSPV4_565_P41_W39_NATIVE386_CERT.json');
const checkerBlob='338305c0ce101704205e57543756b8127074a986';
const sourceBlob='97a96f3f6212c20c4bfa5ced26cad7b18f9722e8';
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(gitBlob(fs.readFileSync(checker)),checkerBlob);
assert.equal(gitBlob(fs.readFileSync(source)),sourceBlob);
const seed=JSON.parse(fs.readFileSync(source,'utf8'));

function packet(owner,declLex,refLex){
  const dat=structuredClone(seed);
  const tuple=dat.gate_defs.find(t=>t[0]===owner);
  assert(tuple,'missing owner '+owner);
  tuple[0]='__OWNER_DECL__';
  let refs=0;
  for(const r of dat.records){
    if(r.kind==='DEF'&&r.gate===owner){r.gate='__OWNER_REF__';refs++;}
  }
  assert(refs>0,'owner has no DEF reference');
  let raw=JSON.stringify(dat)+'\n';
  assert(raw.includes('"__OWNER_DECL__"')&&raw.includes('"__OWNER_REF__"'));
  raw=raw.replaceAll('"__OWNER_DECL__"',declLex).replaceAll('"__OWNER_REF__"',refLex);
  return {bytes:Buffer.from(raw),refs};
}

function run(name,owner,declLex,refLex,expected,save=false){
  const {bytes,refs}=packet(owner,declLex,refLex);
  const parsed=JSON.parse(bytes);
  const parsedDecl=parsed.gate_defs.find(t=>t[1]===seed.gate_defs.find(x=>x[0]===owner)[1])[0];
  const parsedRefs=parsed.records.filter(r=>r.kind==='DEF'&&r.gate===parsedDecl).length;
  const tmp=path.join(os.tmpdir(),'lspv5-507-'+process.pid+'-'+name+'.json');
  fs.writeFileSync(tmp,bytes);
  const proc=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',timeout:30000});
  fs.unlinkSync(tmp);
  const accepted=proc.status===0;
  assert.equal(accepted,expected,name+'\n'+proc.stderr);
  const row={name,owner,decl_lexeme:declLex,reference_lexeme:refLex,
    parsed_decl:String(parsedDecl),parsed_decl_negative_zero:Object.is(parsedDecl,-0),
    referenced_facets:refs,parsed_matching_facets:parsedRefs,accepted,expected,
    bytes:bytes.length,sha256:sha(bytes),
    outcome:accepted?JSON.parse(proc.stdout):null,
    rejection:accepted?null:(proc.stderr.match(/Error: ([^\n]+)/)?.[1]||proc.stderr.slice(0,220))};
  if(save){
    const p=path.join(out,'2026-11-12_0948_LSPV5_507_NATIVE386_OWNER_ALIAS_ACCEPTED.json');
    fs.writeFileSync(p,bytes);
    row.saved_path=path.relative(root,p);
  }
  return row;
}

const rows=[
  run('canonical_owner_one',1,'1','1',true),
  run('fraction_exponent_owner_one',1,'1.0','1e0',true,true),
  run('signed_exponent_owner_one',1,'1E+0','1.0000000000000000',true),
  run('negative_zero_owner_zero',0,'-0','0e100',true),
  run('underflow_zero_owner_zero',0,'1e-324','-1e-324',true),
  run('different_live_owner_reference',1,'1','2',false),
  run('fractional_declaration',1,'1.5','1',false),
  run('fractional_reference',1,'1','1.5',false),
  run('quoted_declaration',1,'"1"','1',false),
  run('array_reference',1,'1','[1]',false),
  run('unsafe_declaration',1,'9007199254740992','9007199254740992',false)
];
const accepted=rows.filter(r=>r.accepted),rejected=rows.filter(r=>!r.accepted);
assert.equal(accepted.length,5);assert.equal(rejected.length,6);
for(const r of accepted){
  assert.equal(r.outcome.paid,39);assert.equal(r.outcome.def,3);
  assert.equal(r.outcome.res,36);assert.equal(r.outcome.records,59);
  assert.equal(r.outcome.sources,17);assert.equal(r.outcome.negativeTests,11);
}
const result={
  id:'LSPV-5/507',date_local:'2026-11-12 09:48 PST',
  status:'COMPUTATIONAL accepted-byte identity counterexample + PROVED/RESTRICTED parsed-owner lemma; P versus NP OPEN',
  authority:{checker:'experiments/arc/lspv2_386_independent_verify.js',checker_blob:checkerBlob,
    source:'results/raw/arc/2026-11-12_0936_LSPV4_565_P41_W39_NATIVE386_CERT.json',source_blob:sourceBlob,
    source_sha256:sha(fs.readFileSync(source)),runtime:process.version},
  target:'Whether archived /386 authenticates paid-owner identity consistently from gate_defs declaration to DEF gate reference over raw accepted JSON bytes.',
  rows,counts:{accepted:accepted.length,rejected:rejected.length,total:rows.length},
  result:'The checker requires safe-integer parsed values, then joins owner declarations to DEF references with ECMAScript Map equality. Distinct numeric token spellings that parse to the same Number are accepted with identical proof and cost summaries.',
  repair:'If raw-byte identity is intended, lex and bind a canonical owner-token grammar before JSON Number coercion; otherwise specify the accepted language as parsed safe-integer identity classes and include that quotient in every abstraction.',
  scope:['Archived /386 sibling checker only','Three-owner 59-record native certificate','Owner declaration and DEF-reference fields only'],
  limitations:['No semantic refutation shortcut','No change to W=39','No full historical R_mix341 dispatcher','No P2-B1 or P2-B2/B3 transfer']
};
const rawPath=path.join(out,'2026-11-12_0948_LSPV5_507_NATIVE386_OWNER_ALIAS_RAW.json');
fs.writeFileSync(rawPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
