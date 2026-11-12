"use strict";
// LSPV-1/593 original-/386 checker OS reproducer.
// node experiments/arc/lspv1_593_arrayify_core_cli_repair.cjs /tmp/lspv1_593_raw.json
const fs=require("node:fs"), path=require("node:path"), os=require("node:os");
const crypto=require("node:crypto"),vm=require("node:vm"),cp=require("node:child_process");
const assert=require("node:assert/strict"),root=path.resolve(__dirname,"../..");
const checkerPath=path.join(root,"experiments/arc/lspv2_386_independent_verify.js");
const seedPath=path.join(root,"results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json");
const rootPath=path.join(root,"results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf");
const blob=b=>crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const cb=fs.readFileSync(checkerPath),sb=fs.readFileSync(seedPath),rb=fs.readFileSync(rootPath);
assert.equal(blob(cb),"338305c0ce101704205e57543756b8127074a986");
assert.equal(blob(sb),"318c52d99977ea4e91bc8554051138a700c1dc94");
const js=cb.toString("utf8"),a=js.indexOf("function key(c)"),b=js.indexOf("function corrupt(d,mutator)");
assert(a>=0&&b>a);
const ctx=vm.createContext({});
const boot="let tests=0;function check(b,msg){tests++;if(!b)throw Error(msg||('check '+tests));}\n";
vm.runInContext(boot+js.slice(a,b)+"\nglobalThis.audit=checkProof;",ctx);
const clone=x=>JSON.parse(JSON.stringify(x)),seed=JSON.parse(sb.toString("utf8"));
const tokens=rb.toString("utf8").trim().split(/\s+/),cnf=[];let row=[];
assert.equal(tokens[0],"p");assert.equal(tokens[1],"cnf");
for(const t of tokens.slice(4)){const n=Number(t);if(n===0){cnf.push(row);row=[]}else row.push(n);}
assert.deepEqual(seed.records.filter(r=>r.kind==="SOURCE").map(r=>r.c),cnf);
const core=p=>{try{return {ok:true,W:ctx.audit(clone(p),{control:true}).paid}}catch(e){return {ok:false,error:String(e)}}};
function noOwner(p){let x=clone(p);x.gate_defs=[];x.summary.paid_gates=0;x.summary.paid_total--;return x;}
function asObject(p,len){let x=clone(p),r=x.records;x.records=Object.assign({length:len},r);return x;}
function guard999999(p){let x=clone(p);x.spec.guard=999999;for(const r of x.records){r.c=r.c.map(v=>Math.abs(v)===7?(v>0?999999:-999999):v).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);if(r.kind==="RES"&&Math.abs(r.pivot)===7)r.pivot=r.pivot>0?999999:-999999;}return x;}
function naive542(p){let x=clone(p);if(x.gate_defs.length===0){let E=x.spec.edges.length,g=x.spec.guard,z=E+1===g?E+2:E+1;x.gate_defs.push([0,z,1,2]);x.summary.paid_gates++;x.summary.paid_total++;}let last=x.records[x.summary.live_records-1];if(last.pivot===999999){last.pivot=-999999;last.parents.reverse();}return x;}
function repair593(p){let x=clone(p);x.records=Array.from({length:x.summary.live_records},(_,i)=>x.records[i]);return naive542(x);}
const cases=[
 ["baseline",seed,true,true,true],
 ["ownerless_array",noOwner(seed),true,true,true],
 ["ownerless_object_len45",asObject(noOwner(seed),45),true,false,true],
 ["ownerless_object_len_string",asObject(noOwner(seed),"45"),true,false,true],
 ["ownerless_object_len_fraction",asObject(noOwner(seed),44.5),true,false,true],
 ["one_owner_object",asObject(seed,45),true,false,true],
 ["ownerless_object_pivot999999",asObject(guard999999(noOwner(seed)),45),true,false,true],
 ["forged_source",(()=>{let x=asObject(noOwner(seed),45);x.records[0].c=[-1];return x})(),false,false,false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-593-"));
function cli(p,label){const buff=Buffer.from(JSON.stringify(p)+"\n"),file=path.join(tmp,label+".json");fs.writeFileSync(file,buff);const o=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:"utf8",timeout:30000});assert(!o.error,String(o.error));return {ok:o.status===0,status:o.status,sha256:hash(buff)};}
let rows=[];
for(const [name,p,ec,en,er] of cases){
 const pre=core(p),naive=naive542(p),n=cli(naive,name+"_naive"),q=repair593(p),good=cli(q,name+"_repaired"),post=core(q);
 assert.equal(pre.ok,ec,name+" core");assert.equal(n.ok,en,name+" naive");assert.equal(good.ok,er,name+" repaired");
 if(pre.ok){assert(post.ok&&good.ok);assert.equal(post.W-pre.W,p.gate_defs.length?0:1);}
 rows.push({name,core_accept:pre.ok,naive_accept:n.ok,repaired_accept:good.ok,W_before:pre.ok?pre.W:null,W_after:post.ok?post.W:null,naive_sha256:n.sha256,repaired_sha256:good.sha256});
}
const raw={result:"LSPV-1/593",source:{checker_git_blob:blob(cb),seed_git_blob:blob(sb),external_cnf_sha256:hash(rb)},mode:"original checkProof VM and unchanged Node CLI subprocess",cases:rows,passed:true};
const outfile=process.argv[2]||path.join(tmp,"raw.json");
fs.writeFileSync(outfile,JSON.stringify(raw,null,2)+"\n");
console.log(JSON.stringify({passed:true,count:rows.length,outfile}));
