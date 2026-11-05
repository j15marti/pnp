#!/usr/bin/env node
// LSPV-2/426 independent finite checker; does not import the producer.
// Usage: node experiments/arc/lspv2_426_independent_verify.js results/raw/arc/2026-11-05_1312_LSPV2_PARTIAL_EXPONENT426_raw.json
const fs=require("fs"),crypto=require("crypto"),assert=require("assert");
const raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
let count=0;const ck=(b,m)=>{assert.ok(b,m);count++};
function parity(x){let p=0;while(x){p^=x&1;x>>=1}return p}
function pop(x){let p=0;while(x){p+=x&1;x>>=1}return p}
function graph(name){const n=name==="K4"?4:8,e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(name==="K4"||pop(i^j)===1)e.push([i,j]);return [n,e]}
function make(n,e,odd){const cs=[];for(let v=0;v<n;v++){const inc=[];e.forEach(([a,b],i)=>{if(a===v||b===v)inc.push(i+1)});ck(inc.length===3,"cubic");for(let k=0;k<8;k++){if(parity(k)===(odd&&v===0?1:0))continue;cs.push(inc.map((id,j)=>((k>>(2-j))&1)?-id:id))}}return cs}
function encode(v,cs){return "p cnf "+v+" "+cs.length+"\n"+cs.map(c=>c.join(" ")+" 0\n").join("")}
function sat(n,cs){for(let bits=0;bits<2**n;bits++)if(cs.every(c=>c.some(l=>Boolean((bits>>(Math.abs(l)-1))&1)===(l>0))))return true;return false}
function audit(r){for(const name of ["K4","cube"]){const [n,e]=graph(name),v=e.length,record=r.families[name],odd=make(n,e,true),even=make(n,e,false);ck(odd.length===4*n&&even.length===4*n,"clauses");for(const [cs,ans,key] of [[odd,false,"odd_sha256"],[even,true,"even_sha256"]]){ck(sat(v,cs)===ans,"label");const s=encode(v,cs);ck(Buffer.byteLength(s)===record.source_bytes,"bytes");ck(crypto.createHash("sha256").update(s).digest("hex")===record[key],"SHA256")}
let indispensable=0,pivotal=0;for(let i=0;i<odd.length;i++){if(sat(v,odd.slice(0,i).concat(odd.slice(i+1))))indispensable++;for(let j=0;j<3;j++){const changed=odd.map(c=>c.slice());changed[i][j]*=-1;if(sat(v,changed))pivotal++}}ck(indispensable===record.clauses_essential&&indispensable===odd.length,"essential");ck(pivotal===record.literal_polarities_pivotal&&pivotal===3*odd.length,"pivotal")}
for(const n of r.diagonal_grid.N)for(const delay of r.diagonal_grid.extractor_delays)for(const k of r.diagonal_grid.reported_degrees){const p=n>=delay?BigInt(n+1)**BigInt(k+2):0n,b=BigInt(n+1)**BigInt(k);ck(n<delay||p>b,"bounded diagonal")}
for(const c of r.actual_small_step_loops){let visits=0;for(let i=0;i<c.executed_padding_steps;i++)visits++;ck(visits===(c.N+1)**(c.exponent+2),"physical finite loop")}
ck(r.assertions===128,"producer checkpoint")}
audit(raw);const normal=count;
for(const mutant of [{...raw,families:{...raw.families,K4:{...raw.families.K4,odd_sha256:"0".repeat(64)}}},{...raw,actual_small_step_loops:raw.actual_small_step_loops.map((x,i)=>i?x:{...x,executed_padding_steps:x.executed_padding_steps+1})}]){let rejected=false;try{audit(mutant)}catch(e){rejected=true}ck(rejected,"corruption rejected")}
console.log(JSON.stringify({independent_assertions:count,successful_base_assertions:normal,mutations_rejected:2,hard_family_controls:["K4","cube"],proof_status:"COMPUTATIONAL controls only"}));
