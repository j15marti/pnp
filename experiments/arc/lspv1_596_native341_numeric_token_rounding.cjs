"use strict";
// LSPV-1/596: original /341 checker decimal-token rounding replay.
// From repo root: node experiments/arc/lspv1_596_native341_numeric_token_rounding.cjs
const fs=require("fs"),vm=require("vm"),assert=require("assert"),crypto=require("crypto");
const sourcePath="experiments/arc/lspv2_341_independent_verify.js";
const packetPath="results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json";
const source=fs.readFileSync(sourcePath,"utf8");
const fixtureText=fs.readFileSync(packetPath,"utf8");
const original=JSON.parse(fixtureText).fixtures[0];
const base=JSON.stringify({fixtures:[original],summary:{length:1}});
function gitsha(s){const b=Buffer.from(s);return crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex")}
assert.strictEqual(gitsha(source),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.strictEqual(gitsha(fixtureText),"fe27fe1011d0021e721ccaeb747ed58da65d7464");
const cases=[
 ["baseline",null,true,null],
 ["decimal_integral","7.0",true,"seven"],
 ["noninteger_above","7.0000000000000001",true,"seven"],
 ["noninteger_below","6.9999999999999999",true,"seven"],
 ["scientific_integral","7e0",true,"seven"],
 ["fractional_rejected","7.000000000000001",false,"seven"],
 ["fractional_half_rejected","7.5",false,"seven"],
 ["string_noninteger_rejected",'"7.0000000000000001"',false,"seven"],
 ["string_integer",'"7"',true,"seven"],
 ["underflow_positive","1e-400",true,"zero"],
 ["underflow_negative","-1e-400",true,"zero"],
 ["nonzero_fraction_rejected","1e-8",false,"zero"],
 ["string_underflow_rejected",'"1e-400"',false,"zero"]
];
function replay(raw){
 let text="";
 let host={require:m=>{if(m==="fs")return{readFileSync:()=>raw};throw Error("unexpected module "+m)},
 process:{argv:["node",sourcePath,"fixture.json"]},console:{log:s=>text+=s}};
 try{vm.runInNewContext(source,host,{filename:sourcePath,timeout:25000});return{accepted:true,checks:JSON.parse(text).checks}}
 catch(e){return{accepted:false,error:String(e.message)}}
}
const rows=[];
for(const [name,token,expect,which] of cases){
 let raw=base;
 if(which){
  const old=which==="zero"?'"mask":"0x0"':'"mask":"0x7"';
  assert(raw.includes(old),name);
  raw=raw.replace(old,'"mask":'+token);
 }
 let out=replay(raw);assert.strictEqual(out.accepted,expect,name+": "+JSON.stringify(out));
 let parsed=JSON.parse(raw).fixtures[0].proof.find(p=>p.id===(which==="zero"?"d14":"d2")).row.mask;
 rows.push({name,raw_token:token,parsed_value:parsed,parsed_type:typeof parsed,accepted:out.accepted,checks:out.checks,error:out.error,bytes:Buffer.byteLength(raw)});
}
let models=0;
for(let m=0;m<64;m++)if(original.clauses.every(c=>c.literals.some(l=>l>0?!!(m&(1<<(l-1))):!(m&(1<<(-l-1))))))models++;
assert.strictEqual(models,0);
const output={id:"LSPV1-596",scope:"unchanged recovered /341 SOURCE/AND3/XOR checker, not full historical R_mix341",original_checker_git_blob:gitsha(source),original_fixture_git_blob:gitsha(fixtureText),source:{edges:6,clauses:original.clauses.length,paid:original.proof.length,models},cases:rows,accepted:rows.filter(x=>x.accepted).length,rejected:rows.filter(x=>!x.accepted).length,execution:"OS Node VM replay when executed locally; hosted V8 original-code replay was run during report preparation",P_vs_NP:"OPEN"};
console.log(JSON.stringify(output,null,2));
