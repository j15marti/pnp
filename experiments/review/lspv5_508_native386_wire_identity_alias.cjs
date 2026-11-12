#!/usr/bin/env node
'use strict';
/*
 * LSPV-5/508: raw JSON numeric-token audit for one paid auxiliary wire across
 * its declaration, later gate-input ports, signed clause occurrences, and
 * Resolution pivots in the unchanged archived /386 checker.
 * Checker-language audit only; this is not a full R_mix341 implementation.
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
const WIRE=8;

function packet(lex={}){
  const dat=structuredClone(seed);
  const seen={decl:0,input:0,pos_clause:0,neg_clause:0,pivot:0};
  for(const tuple of dat.gate_defs){
    if(tuple[1]===WIRE){tuple[1]='__DECL__';seen.decl++;}
    for(let i=2;i<4;i++)if(tuple[i]===WIRE){tuple[i]='__INPUT_'+seen.input+'__';seen.input++;}
  }
  for(const r of dat.records){
    for(let i=0;i<r.c.length;i++){
      if(r.c[i]===WIRE){r.c[i]='__POS_'+seen.pos_clause+'__';seen.pos_clause++;}
      else if(r.c[i]===-WIRE){r.c[i]='__NEG_'+seen.neg_clause+'__';seen.neg_clause++;}
    }
    if(r.pivot===WIRE){r.pivot='__PIVOT_'+seen.pivot+'__';seen.pivot++;}
    else if(r.pivot===-WIRE){r.pivot='__NPIVOT_'+seen.pivot+'__';seen.pivot++;}
  }
  assert.deepEqual(seen,{decl:1,input:2,pos_clause:2,neg_clause:5,pivot:3});
  let raw=JSON.stringify(dat)+'\n';
  const vals={decl:'8',input:'8',pos_clause:'8',neg_clause:'-8',pivot:'8',...lex};
  raw=raw.replace('"__DECL__"',vals.decl);
  for(let i=0;i<seen.input;i++)raw=raw.replace('"__INPUT_'+i+'__"',Array.isArray(vals.input)?vals.input[i]:vals.input);
  for(let i=0;i<seen.pos_clause;i++)raw=raw.replace('"__POS_'+i+'__"',Array.isArray(vals.pos_clause)?vals.pos_clause[i]:vals.pos_clause);
  for(let i=0;i<seen.neg_clause;i++)raw=raw.replace('"__NEG_'+i+'__"',Array.isArray(vals.neg_clause)?vals.neg_clause[i]:vals.neg_clause);
  for(let i=0;i<seen.pivot;i++){
    raw=raw.replace('"__PIVOT_'+i+'__"',Array.isArray(vals.pivot)?vals.pivot[i]:vals.pivot);
    raw=raw.replace('"__NPIVOT_'+i+'__"',Array.isArray(vals.pivot)?'-'+vals.pivot[i]:'-'+vals.pivot);
  }
  assert(!raw.includes('__'));
  return {bytes:Buffer.from(raw),seen};
}

function run(name,lex,expected,save=false){
  const {bytes,seen}=packet(lex);
  let parsed=null,parseError=null;
  try{parsed=JSON.parse(bytes);}catch(e){parseError=e.message;}
  const tmp=path.join(os.tmpdir(),'lspv5-508-'+process.pid+'-'+name+'.json');
  fs.writeFileSync(tmp,bytes);
  const proc=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',timeout:30000});
  fs.unlinkSync(tmp);
  const accepted=proc.status===0;
  assert.equal(accepted,expected,name+'\n'+proc.stderr);
  const row={name,lexemes:lex,occurrences:seen,parsed:parsed?{
      declaration:parsed.gate_defs[0][1],consumer_inputs:parsed.gate_defs[1].slice(2),
      positive_clause_values:parsed.records.flatMap(r=>r.c).filter(x=>x===WIRE).length,
      negative_clause_values:parsed.records.flatMap(r=>r.c).filter(x=>x===-WIRE).length,
      pivot_values:parsed.records.filter(r=>r.pivot===WIRE).length}:null,
    parse_error:parseError,accepted,expected,bytes:bytes.length,sha256:sha(bytes),
    outcome:accepted?JSON.parse(proc.stdout):null,
    rejection:accepted?null:(proc.stderr.match(/Error: ([^\n]+)/)?.[1]||proc.stderr.slice(0,220))};
  if(save){
    const p=path.join(out,'2026-11-12_1048_LSPV5_508_NATIVE386_WIRE_ALIAS_ACCEPTED.json');
    fs.writeFileSync(p,bytes); row.saved_path=path.relative(root,p);
  }
  return row;
}

const rows=[
  run('canonical_wire_8',{},true),
  run('field_specific_aliases',{
    decl:'8.0',input:['8e0','8.0000000000000000'],
    pos_clause:['8E+0','8.00'],
    neg_clause:['-8.0','-8e0','-8.00','-8E+0','-8.0000'],
    pivot:['8.0e0','8E0','8.000']},true,true),
  run('uniform_exponent_alias',{decl:'8e0',input:'8e0',pos_clause:'8e0',neg_clause:'-8e0',pivot:'8e0'},true),
  run('different_consumer_wire',{input:['9','8']},false),
  run('fractional_declaration',{decl:'8.5'},false),
  run('quoted_declaration',{decl:'"8"'},false),
  run('array_consumer',{input:['[8]','8']},false),
  run('unsafe_declaration',{decl:'9007199254740992'},false),
  run('fractional_clause_literal',{pos_clause:['8.5','8']},false),
  run('flipped_clause_sign',{pos_clause:['-8','8']},false),
  run('different_pivot',{pivot:['9','8','8']},false)
];
const accepted=rows.filter(r=>r.accepted),rejected=rows.filter(r=>!r.accepted);
assert.equal(accepted.length,3);assert.equal(rejected.length,8);
for(const r of accepted){
  assert.equal(r.outcome.paid,39);assert.equal(r.outcome.def,3);assert.equal(r.outcome.res,36);
  assert.equal(r.outcome.records,59);assert.equal(r.outcome.sources,17);assert.equal(r.outcome.negativeTests,11);
}
const result={
  id:'LSPV-5/508',date_local:'2026-11-12 10:48 PST',
  status:'COMPUTATIONAL accepted-byte identity counterexample + PROVED/RESTRICTED parsed-wire quotient lemma; P versus NP OPEN',
  authority:{checker:'experiments/arc/lspv2_386_independent_verify.js',checker_blob:checkerBlob,
    source:'results/raw/arc/2026-11-12_0936_LSPV4_565_P41_W39_NATIVE386_CERT.json',source_blob:sourceBlob,
    source_sha256:sha(fs.readFileSync(source)),runtime:process.version},
  target:'Whether archived /386 binds one paid exported wire consistently across declaration, later gate-input ports, signed clauses, and Resolution pivots over raw accepted JSON bytes.',
  rows,counts:{accepted:accepted.length,rejected:rejected.length,total:rows.length},
  result:'The checker rejects changed parsed wire values but accepts distinct legal JSON numeric token spellings at every audited field when all tokens parse to the same safe integer Number 8. All accepted packets preserve the exact W=39 result.',
  repaired_lemma:'For this checker and certificate, accepted wire identity is identity of parsed safe integers, not raw token identity. A sound abstraction must quotient raw numeric spellings by JSON.parse to safe integers, retain signed literal polarity and declaration-before-use, and preserve the same parsed value across declaration, consumers, clauses, and pivots.',
  repair:'If raw-byte identity is intended, lex and bind a canonical numeric-token grammar before JSON Number coercion. Otherwise specify the accepted language as parsed safe-integer identity classes and authenticate that quotient in every concrete and abstract transformer.',
  cegar:'The field-specific cheap alias path was replayed by the unchanged checker and accepted, so it is genuine and must not be refined away. The changed-value, unsafe, fractional, string, array, polarity, and pivot controls were rejected and may justify corresponding refinements.',
  scope:['Archived /386 sibling checker only','One wire in a three-gate 59-record certificate','Declaration, later gate-input, signed clause, and Resolution-pivot fields'],
  limitations:['No cheaper semantic refutation','No change to W=39','No full historical R_mix341 dispatcher','No P2-B1 or P2-B2/B3 transfer']
};
const rawPath=path.join(out,'2026-11-12_1048_LSPV5_508_NATIVE386_WIRE_ALIAS_RAW.json');
fs.writeFileSync(rawPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
