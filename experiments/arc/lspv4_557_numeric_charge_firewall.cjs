'use strict';
// LSPV-4/557: independently replay numeric-only lexical padding on the exact
// original archived /341 checker as Node operating-system subprocesses.
// From repo root: node experiments/arc/lspv4_557_numeric_charge_firewall.cjs
// This is a historical fixture/subchecker audit, NOT R_mix341 completion.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=process.cwd();
const checkerRel='experiments/arc/lspv2_341_independent_verify.js';
const fixtureRel='results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json';
const checker=path.join(ROOT,checkerRel);
const fixture=path.join(ROOT,fixtureRel);
function gitBlob(bytes){
 return crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
}
const checkerBytes=fs.readFileSync(checker),seedBytes=fs.readFileSync(fixture);
assert.equal(gitBlob(checkerBytes),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(gitBlob(seedBytes),'6cf9b0fe1e5a9419e8967d836c707c385418b810');
const seed=seedBytes.toString('utf8'),f=JSON.parse(seed).fixtures[0],E=f.graph.edges.length,V=f.graph.n;
assert.equal(E,18);assert.equal(V,12);assert.equal(f.clauses.length,48);
assert.equal(f.proof.length,47);
function sat(mask){
 for(const c of f.clauses){
  let yes=false;
  for(const lit of c.literals){
   const value=(mask>>>(Math.abs(lit)-1))&1;
   if((lit>0&&value===1)||(lit<0&&value===0)){yes=true;break;}
  }
  if(!yes)return false;
 }
 return true;
}
let satModels=0;for(let m=0;m<(1<<E);m++)if(sat(m))satModels++;
assert.equal(satModels,64,'exhaustive SAT model count');
const witness='101001000000100000';
let witnessMask=0;for(let i=0;i<E;i++)if(witness[i]==='1')witnessMask|=1<<i;
assert(sat(witnessMask));
function rank(rows,n){
 rows=rows.slice();let pivot=0;
 for(let col=0;col<n;col++){
  let j=pivot;while(j<rows.length&&!((rows[j]>>>col)&1))j++;
  if(j===rows.length)continue;
  [rows[pivot],rows[j]]=[rows[j],rows[pivot]];
  for(let i=0;i<rows.length;i++)if(i!==pivot&&((rows[i]>>>col)&1))rows[i]^=rows[pivot];
  pivot++;
 }
 return pivot;
}
const evenRows=[];
for(let v=1;v<V;v++){
 let row=0;for(let i=0;i<E;i++){if(f.graph.edges[i].includes(v))row^=(1<<i);}
 evenRows.push(row);
}
assert.equal(rank(evenRows,E),11);
assert.equal(rank([...evenRows,(1<<0)|(1<<1)],E),12);
function mutate(lex){
 const key='"charges":["1",';
 assert(seed.includes(key),'unique exact fixture charge lexeme');
 return seed.replace(key,'"charges":['+lex+',');
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-557-')),file=path.join(tmp,'packet.json');
function check(raw){
 fs.writeFileSync(file,raw,'utf8');
 const p=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:1<<21});
 if(p.error)throw p.error;
 if(p.status===0){const obj=JSON.parse(p.stdout);return {accepted:true,checks:obj.checks,bytes:Buffer.byteLength(raw)};}
 return {accepted:false,error:(p.stderr||p.stdout||'').trim().slice(0,180),bytes:Buffer.byteLength(raw)};
}
const cases=[],hostiles=[];
try{
 for(const k of [0,1,2,8,64,512,4096]){
  const lex='1.5'+'0'.repeat(k),o=check(mutate(lex));
  assert(o.accepted,'numeric trailing-0 k='+k+': '+o.error);
  assert.equal(o.bytes,8574+k);assert.equal(o.checks,3273);
  cases.push({type:'numeric_decimal_padding',k,lexeme_length:lex.length,...o});
 }
 for(const q of [1,2,10,1000,2097151]){
  const val=q*4294967296+1;
  assert(Number.isSafeInteger(val));
  const o=check(mutate(String(val)));
  assert(o.accepted,'safe number 1+2^32*q rejected at q='+q+': '+o.error);
  cases.push({type:'numeric_safe_integer_residue',q,charge:val,...o});
 }
 for(const [label,lex,accepted] of [
  ['string_prior','"1"',true],
  ['numeric_bit_one','1',false],
  ['numeric_one_point_zero','1.0',false],
  ['numeric_zero','0',false],
  ['integer_wrap_zero','4294967296',false],
  ['numeric_half','0.5',false],
  ['boolean_prior','true',true],
  ['decimal_exponent','1.5e0',true]
 ]){
  const o=check(mutate(lex));assert.equal(o.accepted,accepted,label);
  cases.push({type:'control',label,lexeme:lex,...o});
 }
 const base=mutate('1.50000000');
 for(const [label,raw] of [
  ['invalid_json_digit',base.replace('1.50000000','1.500x0000')],
  ['forged_signed_source',base.replace('"literals":[1,2,13]','"literals":[1,2,999]')],
  ['missing_parent',base.replace('"parents":[0,1]','"parents":[-999,1]')],
  ['incorrect_affine_sink',base.replace('"mask":"0x0","rhs":1','"mask":"0x0","rhs":0')]
 ]){
  assert.notEqual(raw,base);const o=check(raw);assert(!o.accepted,label);
  hostiles.push({label,...o});
 }
 const result={id:'LSPV4_557_NUMERIC_CHARGE_FIREWALL',date_pst:'2026-11-11 20:36 PST',
  authority:{checker:checkerRel,checker_git_blob:gitBlob(checkerBytes),
   fixture:fixtureRel,fixture_git_blob:gitBlob(seedBytes)},
  environment:{node:process.version,execution:'unchanged original checker as Node OS subprocess',
   byte_length:'UTF8 compact JSON plus existing newline',random_seed:null},
  source:{edges:E,vertices:V,clauses:f.clauses.length,sat_models:satModels,
   witness,even_vertex_equation_rank:11,with_vertex_zero_two_edge_constraint_rank:12},
  proof:{paid_and3:36,paid_xor:11,records:f.proof.length,parent_applications:94},
  cases,hostiles,limits:'Original /341 fixture parser only, not unified historical R_mix341 or a valid UNSAT proof'};
 console.log(JSON.stringify(result,null,2));
}finally{fs.rmSync(tmp,{force:true,recursive:true});}
