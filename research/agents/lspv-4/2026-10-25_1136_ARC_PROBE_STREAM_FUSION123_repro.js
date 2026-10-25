// ARC-PROBE-STREAM-FUSION123. Reproduce: node 2026-10-25_1136_ARC_PROBE_STREAM_FUSION123_repro.js
// Logical counters only; no FLMV physical trace.
const audit = function audit(){
const z={run_id:"ARC-PROBE-STREAM-FUSION123",model:"logical operation counters; NOT FLMV tape trace",assertions:0,failures:0,sources:0,sat_sources:0,unsat_sources:0,oracle_calls:0,oracle_clause_reads:0,oracle_literal_inspections:0,oracle_nodes:0,written_bits:0,unchanged_zero_writes:0,changed_one_writes:0,event_updates:0,two_level_chains:0,finite_strict_shrinks:0,large:[],exponent_checks:[]};
function ck(v,msg){z.assertions++;if(!v){z.failures++;throw Error(msg);}}
function gamma(x){ck(Number.isInteger(x)&&x>0,"gamma");let s=x.toString(2);return"0".repeat(s.length-1)+s;}
function bpad(x,w){let s=x.toString(2);ck(s.length<=w,"pad");return"0".repeat(w-s.length)+s;}
function enc(f,record){let w=Math.max(1,Math.ceil(Math.log2(f.v+1))),s=gamma(f.v+1)+gamma(f.c.length+1);for(let c of f.c){ck(c.length===3,"3CNF");let seen=new Set();for(let lit of c){ck(lit!==0&&Math.abs(lit)<=f.v&&!seen.has(Math.abs(lit)),"proper");seen.add(Math.abs(lit));s+=(lit<0?"1":"0")+bpad(Math.abs(lit),w);}}if(record){z.written_bits+=s.length;for(let x of s){if(x==="0")z.unchanged_zero_writes++;else z.changed_one_writes++;}}return s.length;}
function eight(){let out=[];for(let i=0;i<8;i++)out.push([i&1?-1:1,i&2?-2:2,i&4?-3:3]);return out;}
function padded(bit,q){let c=bit?[[1,2,3]]:eight();for(let i=0;i<q;i++){let j=4+3*i;c.push([j,j+1,j+2]);}return{v:3+3*q,c};}
function solve(f){z.oracle_calls++;function recur(a){z.oracle_nodes++;let pivot=0,all=true;for(let c of f.c){z.oracle_clause_reads++;let sat=false,free=false,first=0;for(let lit of c){z.oracle_literal_inspections++;let x=a[Math.abs(lit)];if(x===0){free=true;if(!first)first=Math.abs(lit);}else if(x===1&&lit>0||x===-1&&lit<0){sat=true;break;}}if(!sat&&!free)return false;if(!sat){all=false;if(!pivot)pivot=first;}}if(all)return true;let v=a.slice();v[pivot]=1;if(recur(v))return true;v=a.slice();v[pivot]=-1;return recur(v);}return recur(new Int8Array(f.v+1));}
function next(bit,N){let q=Math.max(8,Math.ceil(Math.sqrt(N)/(1+Math.log2(Math.max(2,N)))));return padded(bit,q);}
function stream(bit){return bit?[["OPEN",1],["CLAUSE",1],["CLOSE",1]]:[["OPEN",1],["CLAUSE",1],["CLAUSE",-1],["CLOSE",1]];}
function dp(e){let live=false,rows=new Set([""]);for(let[a,v]of e){z.event_updates++;if(a==="OPEN"){ck(!live,"open");let n=new Set();for(let s of rows){n.add(s+"0");n.add(s+"1");}rows=n;live=true;}else if(a==="CLAUSE"){ck(live,"clause");rows=new Set([...rows].filter(s=>s===(v>0?"1":"0")));}else{ck(live,"close");rows=new Set([...rows].map(s=>s.slice(0,-1)));live=false;}}ck(!live,"fully closed");return rows.has("");}
function test(f,label){const N=enc(f,false),b=solve(f);ck(b===label,"root");let y=next(b,N),Y=enc(y,true);ck(solve(y)===b,"child status");let b2=solve(y),v=next(b2,Y),Z=enc(v,true);ck(solve(v)===b,"grandchild status");ck(dp(stream(b))===b,"root stream");ck(dp(stream(solve(v)))===b,"grandchild stream");z.sources++;z.two_level_chains++;if(b)z.sat_sources++;else z.unsat_sources++;let isShort=(Y<N&&Z<Y);if(isShort)z.finite_strict_shrinks++;return {N,L1:Y,L2:Z,sat:b,root_clauses:f.c.length,child_clauses:y.c.length,grandchild_clauses:v.c.length,strict:isShort};}
const E=eight();for(let mask=0;mask<256;mask++){let clauses=[];for(let j=0;j<8;j++)if(mask&(1<<j))clauses.push(E[j]);test({v:3,c:clauses},mask!==255);}
for(let p of[100,1000])for(let bit of[false,true])z.large.push({padding:p,...test(padded(bit,p),bit)});
for(let K of[2,4,10,50,200]){let t=Math.max(1.05,.6+.5*K),s=Math.max(.5,.5*K),steps=0;while((t>=241/200||s>=11642479/23232400)&&steps<80){let tt=Math.max(1.05,.6+.5*t),ss=Math.max(.5,.5*s);ck(tt<=t+1e-12&&ss<=s+1e-12,"monotone");t=tt;s=ss;steps++;}ck(steps<80&&t<241/200&&s<11642479/23232400,"conditional finite hit");z.exponent_checks.push({K,steps,t,s,conditional:true});}
ck(z.written_bits===z.unchanged_zero_writes+z.changed_one_writes,"write partition");ck(z.sat_sources>=5&&z.unsat_sources>=3,"both labels");ck(z.large.some(v=>v.strict),"actual finite shrink");return z;
};
console.log(JSON.stringify(audit(),null,2));
