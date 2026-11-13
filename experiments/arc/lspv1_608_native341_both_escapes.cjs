"use strict";
// LSPV-1/608: Corrected original-/341 dual witness-escape native OS replay.
// node experiments/arc/lspv1_608_native341_both_escapes.cjs [raw.json]
// NOT the unrecovered historical all-rule R_mix341 checker.
const fs=require("fs"),path=require("path"),os=require("os"),cp=require("child_process"),
crypto=require("crypto"),assert=require("assert/strict");
const root=path.resolve(__dirname,"../.."),checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js"),
seed=path.join(root,"results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json");
const hash=b=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");
const cb=fs.readFileSync(checker),sb=fs.readFileSync(seed),raw=sb.toString("utf8"),base=JSON.parse(raw);
assert.equal(hash(cb),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(hash(sb),"393d13265192b4e43073c6f6559bc22b6a71ece5");
assert.equal(base.fixtures[0].evenWitness,"000000");
assert.equal(base.fixtures[0].deleted[0].assignment,"000000");
const signed=JSON.stringify(base.fixtures[0].clauses),dag=JSON.stringify(base.fixtures[0].proof);
function change(s,which,token){
 const re=which==="even"?/("evenWitness":\s*")000000(")/:/("assignment":\s*")000000(")/;
 assert.ok(re.test(s),which+" exact source witness missing");
 return s.replace(re,(_,a,b)=>a+"00000"+token+b);
}
function corrupt(fn){let d=structuredClone(base);fn(d);return JSON.stringify(d)}
const cases=[
 ["baseline",raw,true],
 ["escape_even",change(raw,"even","\\u0030"),true],
 ["escape_deleted",change(raw,"deleted","\\u0030"),true],
 ["escape_both_corrected",change(change(raw,"even","\\u0030"),"deleted","\\u0030"),true],
 ["newline_even",change(raw,"even","\\n"),false],
 ["newline_deleted",change(raw,"deleted","\\n"),false],
 ["newline_both",change(change(raw,"even","\\n"),"deleted","\\n"),false],
 ["wrong_bit_even",change(raw,"even","1"),false],
 ["wrong_bit_deleted",change(raw,"deleted","1"),false],
 ["corrupt_source",corrupt(d=>d.fixtures[0].clauses[0].literals[0]=999),false],
 ["corrupt_parent",corrupt(d=>d.fixtures[0].proof[0].parents[0]="MISSING"),false],
 ["corrupt_sink",corrupt(d=>d.fixtures[0].proof.at(-1).row.rhs^=1),false]
];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-608-")),results=[];
try{
 for(const [name,packet,expected] of cases){
  const parsed=JSON.parse(packet),sameDecoded=JSON.stringify(parsed)===JSON.stringify(base),
   sameSource=JSON.stringify(parsed.fixtures[0].clauses)===signed,
   sameProof=JSON.stringify(parsed.fixtures[0].proof)===dag;
  if(expected)assert.ok(sameDecoded&&sameSource&&sameProof,name+" altered the proof");
  const f=path.join(dir,results.length+".json");fs.writeFileSync(f,packet);
  const p=cp.spawnSync(process.execPath,[checker,f],{encoding:"utf8",timeout:30000,maxBuffer:4000000});
  const accepted=p.status===0;assert.equal(accepted,expected,name);
  const parsedOut=accepted?JSON.parse(p.stdout):null;
  const d={name,expected,accepted,bytes:Buffer.byteLength(packet),sameDecoded,sameSource,sameProof,
   escapes:(packet.match(/\\u0030/g)||[]).length,
   evenEscaped:/"evenWitness":\s*"00000\\u0030"/.test(packet),
   deletedEscaped:/"assignment":\s*"00000\\u0030"/.test(packet),
   assertions:parsedOut?.checks??null,
   error:accepted?null:((p.stderr||"").match(/Error: [^\r\n]*/)||[])[0]||"REJECT"};
  if(name==="escape_both_corrected"){
   assert.equal(d.escapes,2);assert.ok(d.evenEscaped&&d.deletedEscaped);
   assert.equal(parsedOut.cases[0].proofNodes,15);
  }
  results.push(d);
 }
 const out={run:"LSPV-1/608",date_pst:"2026-11-12 20:00 PST",
  pinned_original_checker_blob:hash(cb),pinned_seed_blob:hash(sb),
  original_native_os_executions:true,
  scope:"Original /341 SOURCE/AND3/XOR checker, NOT complete historical R_mix341",
  previous_runner_falsifier:"LSPV-3/603 edit(field,token) ignores third input, making both-escaped case one-escaped",
  accepted:results.filter(r=>r.accepted).length,rejected:results.filter(r=>!r.accepted).length,
  assertion_groups:results.filter(r=>r.accepted).reduce((s,x)=>s+x.assertions,0),cases:results};
 assert.equal(out.accepted,4);assert.equal(out.rejected,8);assert.equal(out.assertion_groups,5604);
 const output=JSON.stringify(out,null,2)+"\n";
 if(process.argv[2])fs.writeFileSync(process.argv[2],output);
 process.stdout.write(output);
}finally{fs.rmSync(dir,{recursive:true,force:true})}
