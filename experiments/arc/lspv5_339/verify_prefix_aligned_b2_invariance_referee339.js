#!/usr/bin/env node
"use strict";

const fs=require("fs");
const path=process.argv[2]||"results/raw/arc/lspv5_339/prefix_aligned_b2_invariance_referee339.json";
const raw=JSON.parse(fs.readFileSync(path,"utf8"));
let checks=0;
function check(ok,msg){checks++;if(!ok)throw new Error(msg);}

const universe=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function clauses(mask){return universe.filter((_,i)=>(mask>>i)&1).map(c=>new Set(c));}
function label(cs){for(let m=0;m<4;m++)if(cs.every(c=>[...c].some(l=>Boolean((m>>(Math.abs(l)-1))&1)===(l>0))))return"SAT";return"UNSAT";}
function resolvents(a,b){const out=[];for(const l of a)if(b.has(-l)){const c=new Set([...a].filter(x=>x!==l).concat([...b].filter(x=>x!==-l)));if(![...c].some(x=>c.has(-x)))out.push(c);}return out;}
function keyClause(c){return [...c].sort((a,b)=>a-b).join(",");}
function keyState(rows){return [...rows.keys()].sort().join(";");}
function minW(cs){let rows=new Map(cs.map(c=>[keyClause(c),c]));if(rows.has(""))return 0;let q=[[rows,0]],seen=new Set([keyState(rows)]);while(q.length){const [avail,cost]=q.shift(),a=[...avail.values()];for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)for(const c of resolvents(a[i],a[j])){const kc=keyClause(c);if(avail.has(kc))continue;if(kc==="")return cost+1;const nxt=new Map(avail);nxt.set(kc,c);const ks=keyState(nxt);if(!seen.has(ks)){seen.add(ks);q.push([nxt,cost+1]);}}}return null;}
function emit(mask){const cs=universe.filter((_,i)=>(mask>>i)&1);return Buffer.from(`p cnf 2 ${cs.length}\n`+cs.map(c=>c.join(" ")+" 0\n").join(""));}
function bits(buf){return[...buf].map(b=>b.toString(2).padStart(8,"0")).join("");}
function enc(s){const n=s.length;return"1".repeat(n)+"0"+s+"0".repeat(n*n);}
function dec(s){if(/[^01]/.test(s))throw Error("nonbit");let n=0;while(n<s.length&&s[n]==="1")n++;if(n===s.length||s.length!==(n+1)**2)throw Error("shape");const p=s.slice(n+1,n+1+n),z=s.slice(n+1+n);if(/1/.test(z))throw Error("pad");return p;}
function isqrt(n){return Math.floor(Math.sqrt(n));}

check(raw.artifact==="PREFIX-ALIGNED-B2-INVARIANCE-REFEREE339","artifact");
check(raw.cases===256&&raw.sat===95&&raw.unsat===161,"counts");
check(raw.max_toy_resolution_W===3,"max W");
check(raw.theorem.B2.includes("equivalent"),"B2 theorem");
check(raw.theorem.same_machine_profile.startsWith("not invariant"),"profile firewall");
check(raw.status.B1_Rmix341==="OPEN"&&raw.status.B2_Rmix341==="OPEN"&&raw.status.B3_Rmix341==="OPEN","mixed open");
check(raw.status.P_vs_NP==="OPEN","P vs NP");

const recomputed=[];
for(let mask=0;mask<256;mask++){
 const cs=clauses(mask),lab=label(cs),w=minW(cs),b=bits(emit(mask)),e=enc(b);
 check(dec(e)===b,`roundtrip ${mask}`);
 check((w===null)===(lab==="SAT"),`complete ${mask}`);
 const r=raw.records[mask];check(r.mask===mask&&r.label===lab&&r.W_resolution===w,`record ${mask}`);
 check(r.e0_bits===b.length&&r.e2_bits===(b.length+1)**2&&e.length===r.e2_bits,`length ${mask}`);
 recomputed.push({lab,w,n0:b.length,n2:e.length});
}
function wbar(key,N){let z=0;for(const r of recomputed)if(r.lab==="UNSAT"&&r[key]<=N)z=Math.max(z,r.w);return z;}
for(const r of recomputed)for(const d of[-1,0,1]){const N=Math.max(0,r.n2+d),t=Math.max(0,isqrt(N)-1);check(wbar("n2",N)===wbar("n0",t),`profile ${N}`);}

const p="101001",honest=enc(p);check(dec(honest)===p,"small wrapper");
for(const bad of[honest.slice(0,-1),honest+"0","1".repeat(honest.length),honest.slice(0,-2)+"10",honest+"x"]){let rej=false;try{dec(bad);}catch{rej=true;}check(rej,"malformed");}
let q=16,word=0,sum=0;for(let nxt=1;nxt<2**q;nxt++){sum+=(word^nxt).toString(2).split("1").length-1;word=nxt;}sum+=word.toString(2).split("1").length-1;check(sum===131070,"clock xor");

console.log(JSON.stringify({artifact:raw.artifact,independent_checks:checks,status:"PASS"},null,2));
