#!/usr/bin/env node
'use strict';
/*
 * LSPV-5/510: exact-byte parse/reserialize closure attack against the
 * unchanged archived /341 checker.  This invokes that checker as an OS Node
 * subprocess; it does not reimplement or repair its accepted language.
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||path.join(__dirname,'../..'));
const out=path.resolve(process.argv[3]||path.join(root,'results/raw/review'));
fs.mkdirSync(out,{recursive:true});
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checkerBlob='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const seedBlob='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(gitBlob(fs.readFileSync(checker)),checkerBlob);
assert.equal(gitBlob(fs.readFileSync(seedPath)),seedBlob);
const seed=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const base=seed.fixtures[0];
const clone=x=>JSON.parse(JSON.stringify(x));

function relabelFixture(pairs){
  const f=clone(base);
  for(const [old,token] of pairs){
    for(const c of f.clauses)if(c.id===old)c.id=token;
    for(const p of f.proof)p.parents=p.parents.map(x=>x===old?token:x);
    for(const d of f.deleted)if(d.sourceId===old)d.sourceId=token;
  }
  return f;
}
function packet(pairs,lexemes){
  const f=relabelFixture(pairs);
  let raw=JSON.stringify({fixtures:[f],summary:[seed.summary[0]]})+'\n';
  for(const [token,lexeme] of lexemes){
    const needle=JSON.stringify(token);
    assert(raw.includes(needle),'missing placeholder '+token);
    raw=raw.replaceAll(needle,lexeme);
  }
  return Buffer.from(raw);
}
function canonical(bytes){return Buffer.from(JSON.stringify(JSON.parse(bytes))+'\n');}
function runBytes(name,bytes,expected){
  const tmp=path.join(os.tmpdir(),`lspv5-510-${process.pid}-${name}.json`);
  fs.writeFileSync(tmp,bytes);
  const proc=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',timeout:30000,maxBuffer:8*1024*1024});
  fs.unlinkSync(tmp);
  if(proc.error)throw proc.error;
  const accepted=proc.status===0;
  assert.equal(accepted,expected,name+'\n'+proc.stderr);
  const parsed=JSON.parse(bytes).fixtures[0];
  return {name,accepted,expected,bytes:bytes.length,sha256:sha256(bytes),
    first_ids:parsed.clauses.slice(0,2).map(x=>({type:x.id===null?'null':typeof x.id,string:String(x.id)})),
    checks:accepted?JSON.parse(proc.stdout).checks:null,
    rejection:accepted?null:(proc.stderr.match(/Error: Verifier: ([^\n]+)/)?.[1]||proc.stderr.split('\n')[0])};
}
function pairCase(name,aLex,bLex,rawExpected,canonicalExpected,save=false){
  const raw=packet([['s0','__A__'],['s1','__B__']],[['__A__',aLex],['__B__',bLex]]);
  const can=canonical(raw);
  const rawRow=runBytes(name+'_raw',raw,rawExpected);
  const canRow=runBytes(name+'_canonical',can,canonicalExpected);
  const parsedRaw=JSON.parse(raw).fixtures[0].clauses.slice(0,2).map(x=>x.id);
  const parsedCan=JSON.parse(can).fixtures[0].clauses.slice(0,2).map(x=>x.id);
  const row={name,a_lexeme:aLex,b_lexeme:bLex,
    raw_ids_distinct:!Object.is(parsedRaw[0],parsedRaw[1]),
    canonical_ids_distinct:!Object.is(parsedCan[0],parsedCan[1]),
    raw:rawRow,canonical:canRow};
  if(save){
    const acceptedPath=path.join(out,'2026-11-12_1248_LSPV5_510_NATIVE341_INFINITY_NULL_ACCEPTED.json');
    const rejectedPath=path.join(out,'2026-11-12_1248_LSPV5_510_NATIVE341_CANONICAL_NULL_COLLISION_REJECTED.json');
    fs.writeFileSync(acceptedPath,raw);fs.writeFileSync(rejectedPath,can);
    row.saved_accepted=path.relative(root,acceptedPath);
    row.saved_rejected=path.relative(root,rejectedPath);
  }
  return row;
}

const baseline=Buffer.from(JSON.stringify({fixtures:[clone(base)],summary:[seed.summary[0]]})+'\n');
const cases=[
  {name:'baseline',raw:runBytes('baseline',baseline,true),canonical:runBytes('baseline_canonical',canonical(baseline),true)},
  pairCase('infinity_null','1e400','null',true,false,true),
  pairCase('positive_negative_infinity','1e400','-1e400',true,false),
  pairCase('finite_null','1e308','null',true,true),
  pairCase('string_infinity_null','"Infinity"','null',true,true),
  pairCase('null_null','null','null',false,false),
  pairCase('infinity_infinity','1e400','1e309',false,false),
  pairCase('boolean_null','false','null',true,true)
];

// Direct hostile mutations retain the same exact CLI boundary.
const hostile=[];
for(const [name,mut] of [
  ['missing_parent',f=>f.proof[0].parents[0]='missing'],
  ['bad_and3_table',f=>f.proof[0].table^=1],
  ['bad_sink',f=>f.proof.at(-1).row.rhs^=1],
  ['forged_source',f=>f.clauses[0].literals[0]=999]
]){
  const f=clone(base);mut(f);
  const bytes=Buffer.from(JSON.stringify({fixtures:[f],summary:[seed.summary[0]]})+'\n');
  hostile.push(runBytes(name,bytes,false));
}

const decisive=cases.find(x=>x.name==='infinity_null');
assert.equal(decisive.raw.accepted,true);
assert.equal(decisive.canonical.accepted,false);
assert.equal(decisive.raw_ids_distinct,true);
assert.equal(decisive.canonical_ids_distinct,false);
assert.equal(decisive.canonical.rejection,'unique source id');
assert(cases.find(x=>x.name==='finite_null').canonical.accepted);
assert(cases.find(x=>x.name==='string_infinity_null').canonical.accepted);

const result={
  id:'LSPV-5/510',date_local:'2026-11-12 12:48 PST',
  status:'COMPUTATIONAL accepted-byte counterexample plus PROVED/RESTRICTED non-closure lemma; P versus NP OPEN',
  target:'closure of the pinned archived /341 accepted language under JSON.stringify(JSON.parse(bytes))+LF',
  authority:{checker:'experiments/arc/lspv2_341_independent_verify.js',checker_git_blob:checkerBlob,
    seed:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',seed_git_blob:seedBlob,
    runtime:process.version,execution:'fresh OS Node subprocess per verdict'},
  theorem:'The pinned /341 accepted language is not closed under ECMAScript parse/reserialization.',
  mechanism:'Raw JSON number 1e400 parses to Number Infinity; Map distinguishes Infinity from null, but JSON.stringify serializes Infinity as null, collapsing two live source IDs.',
  cases,hostile,
  counts:{cli_runs:cases.reduce((n,x)=>n+(x.raw?1:0)+(x.canonical?1:0),0)+hostile.length,
    accepted:cases.reduce((n,x)=>n+Number(x.raw?.accepted)+Number(x.canonical?.accepted),0),
    rejected:cases.reduce((n,x)=>n+Number(x.raw&&!x.raw.accepted)+Number(x.canonical&&!x.canonical.accepted),0)+hostile.length,
    accepted_assertion_groups:cases.reduce((n,x)=>n+(x.raw?.checks||0)+(x.canonical?.checks||0),0)},
  cegar:'The raw path is genuine and must remain. The parse/reserialize transformer is unsound for this accepted language; rejection of its image does not prove the raw path spurious.',
  repair:'Either retain typed parsed identity including non-finite Number versus null, or define and authenticate a narrower canonical ID grammar. The latter changes the historical accepted language and cannot be retroactively substituted.',
  exact_scope:['one K4 fixture of archived /341 SOURCE/AND3/XOR checker','no full historical mixed dispatcher','no Resolution/LOCAL-CONVERT/paid-DEF/branching transfer','no proof-size lower bound','P2-B2/B3 separate']
};
const rawPath=path.join(out,'2026-11-12_1248_LSPV5_510_NATIVE341_INFINITY_NULL_CANONICALIZATION_RAW.json');
fs.writeFileSync(rawPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
