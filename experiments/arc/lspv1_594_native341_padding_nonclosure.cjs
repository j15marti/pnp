"use strict";
// LSPV-1/594, November 12, 2026 PST.
// Native /341 fixed-length acceptance is not closed under locally legal
// redundant AND3 introduction. This invokes the unchanged historical CLI.
// Usage: node experiments/arc/lspv1_594_native341_padding_nonclosure.cjs [raw-output.json]
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const crypto = require("node:crypto");
const cp = require("node:child_process");
const assert = require("node:assert/strict");
const root = path.resolve(__dirname, "../..");
const checker = path.join(root, "experiments/arc/lspv2_341_independent_verify.js");
const fixture = path.join(root, "results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const gitBlob = b => crypto.createHash("sha1").update(Buffer.concat([
  Buffer.from("blob " + b.length + "\0"), b
])).digest("hex");
const sha256 = b => crypto.createHash("sha256").update(b).digest("hex");
const checkerBytes = fs.readFileSync(checker);
const fixtureBytes = fs.readFileSync(fixture);
assert.equal(gitBlob(checkerBytes), "fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(gitBlob(fixtureBytes), "fe27fe1011d0021e721ccaeb747ed58da65d7464");
const src = checkerBytes.toString("utf8");
assert(src.includes('assert(f.proof.length===4*V-1,"proof candidate length")'));
const packet = JSON.parse(fixtureBytes);
const clone = x => structuredClone(x);
const cases = [];
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "lspv1-594-"));
function run(obj, id) {
  const b = Buffer.from(JSON.stringify(obj) + "\n");
  const f = path.join(temp, id + ".json");
  fs.writeFileSync(f, b);
  const r = cp.spawnSync(process.execPath, [checker, f], {encoding:"utf8",timeout:30000});
  assert(!r.error, String(r.error));
  return {accepted:r.status===0,status:r.status,stderr:r.stderr,
    stdout:r.stdout,sha256:sha256(b)};
}
function clauseSat(c,bits) {
  return c.some(l => l>0 ? bits[Math.abs(l)-1]===1 : bits[Math.abs(l)-1]===0);
}
function localCheck(f,p) {
  const source = new Map(f.clauses.map(c=>[c.id,c]));
  if(p.rule!=="AND3" || p.parents.length!==2 || p.parents[0]===p.parents[1]) return false;
  const a=source.get(p.parents[0]),b=source.get(p.parents[1]);
  if(!a || !b || p.kind!=="factor") return false;
  const support=[...new Set([...a.literals,...b.literals].map(l=>Math.abs(l)-1))];
  if(support.length>3 || support.length!==p.support.length ||
     !support.every(s=>p.support.includes(s))) return false;
  let table=0;
  for(let m=0;m<(1<<support.length);m++) {
    const bits=Array(f.graph.edges.length).fill(0);
    for(let j=0;j<p.support.length;j++)bits[p.support[j]]=(m>>j)&1;
    if(clauseSat(a.literals,bits)&&clauseSat(b.literals,bits))table |= 1<<m;
  }
  return table===p.table;
}
const baseline=run(packet,"baseline");
assert(baseline.accepted,"historical /341 baseline must accept");
for (let i=0;i<packet.fixtures.length;i++) {
  const f=packet.fixtures[i],V=f.graph.n;
  const old=f.proof.find(p=>p.rule==="AND3"&&p.parents.every(s=>String(s).startsWith("s")));
  assert(old && localCheck(f,old));
  assert.equal(f.proof.length,4*V-1);
  const pad=clone(old);
  pad.id="lspv1_594_fresh_"+i;
  assert(!new Set([...f.clauses.map(x=>x.id),...f.proof.map(x=>x.id)]).has(pad.id));
  assert(localCheck(f,pad));
  assert(!localCheck(f,{...pad,table:pad.table^1}),"wrong AND3 table must fail local check");
  assert(!localCheck(f,{...pad,parents:[pad.parents[0],pad.parents[0]]}),
         "duplicate AND3 parents must fail local check");
  const obj=clone(packet),target=obj.fixtures[i];
  target.proof.splice(target.proof.length-1,0,pad);
  assert.equal(target.proof.length,4*V);
  assert.deepEqual(target.proof.at(-1),f.proof.at(-1));
  assert.deepEqual(target.clauses,f.clauses);
  assert(target.proof.every((p,j)=>j===target.proof.length-2 ||
    JSON.stringify(p)===JSON.stringify(f.proof[j<target.proof.length-2?j:j-1])));
  const outcome=run(obj,"pad_"+i);
  assert(!outcome.accepted,"padded packet unexpectedly accepted");
  assert(outcome.stderr.includes("proof candidate length"),
         "unexpected failure instead of pinned length check: "+outcome.stderr);
  cases.push({graph:f.graph.name,vertices:V,edges:f.graph.edges.length,
    paid_before:f.proof.length,paid_after:target.proof.length,
    original_cli:"ACCEPT",padded_cli:"REJECT",
    local_AND3:"VALID",root_and_proof_sink_unchanged:true,
    error:"proof candidate length",mutant_sha256:outcome.sha256});
}
for (let j=0;j<2;j++) {
  const obj=clone(packet),p=obj.fixtures[0].proof[0];
  if(j===0)p.table ^= 1;
  else p.parents[1]=p.parents[0];
  const out=run(obj,"control_"+j);
  assert(!out.accepted);
  const phrase=j===0?"incorrect AND3 conjunction":"duplicate parents";
  assert(out.stderr.includes(phrase),out.stderr);
}
const result={claim:"LSPV-1/594",date:"2026-11-12 08:31 PST",
  scope:"exact historical /341 fixture checker, not full R_mix341",
  mode:"unchanged original Node CLI OS subprocess",
  checker_git_blob:gitBlob(checkerBytes),fixture_git_blob:gitBlob(fixtureBytes),
  baseline_stdout_sha256:sha256(Buffer.from(baseline.stdout)),
  cases,hostile_controls:2,pass:true};
const outfile=process.argv[2] || path.join(temp,"result.json");
fs.writeFileSync(outfile,JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify({pass:true,cases:cases.length,hostile_controls:2,outfile}));
