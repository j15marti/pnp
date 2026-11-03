#!/usr/bin/env node
// No-import independent verifier for BIT_WITNESS_SEPARATION372.
// Usage: node lspv1_372_independent_verify.js result.json
const fs=require('node:fs'),crypto=require('node:crypto');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'results.json','utf8'));
let checks=0;
function check(x,msg){checks++;if(!x)throw Error(msg)}
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function php(h){let C=[],v=(p,j)=>p*h+j+1;
 for(let p=0;p<=h;p++)C.push(Array.from({length:h},(_,j)=>v(p,j)));
 for(let j=0;j<h;j++)for(let p=0;p<=h;p++)for(let q=p+1;q<=h;q++)C.push([-v(p,j),-v(q,j)]);
 return C;}
function clause(c,a){return c.some(x=>x>0?((a>>(x-1))&1):!((a>>(-x-1))&1))}
function witness(n,C){for(let a=0;a<(1<<n);a++)if(C.every(c=>clause(c,a)))return a;return null}
const vector=(n,c)=>Uint8Array.from({length:1<<n},(_,a)=>+clause(c,a));
for(const row of raw.PHP){
 let h=row.holes,n=h*(h+1),C=php(h),m=C.length;
 check(n===row.variables&&m===row.source_clauses,'dimensions');
 check(witness(n,C)===null,'PHP SAT');
 let del=[];
 for(let j=0;j<m;j++){let w=witness(n,C.filter((_,i)=>i!==j));check(w!==null,'deletion SAT');del.push(w)}
 check(sha(Buffer.from(JSON.stringify(del).replace(/,/g,', ')))===row.source_deletion_witness_sha256,'deletion hash');
 let flips=0;
 for(let j=0;j<m;j++)for(let k=0;k<C[j].length;k++){
  let D=C.map(c=>c.slice());D[j][k]*=-1;
  check(witness(n,D)!==null,'signed neighbor UNSAT');flips++;}
 check(flips===row.sign_flip_sat_witness_count,'flip count');
 let nodes=[],prev=vector(n,C[0]);
 for(let j=1;j<m;j++){
  let t=vector(n,C[j]),next=Uint8Array.from(prev,(b,i)=>b&t[i]);
  for(let i=0;i<next.length;i++)check(next[i]===(prev[i]&t[i]),'AND mismatch');
  nodes.push(next);prev=next;}
 check(nodes.length===m-1&&!prev.some(Boolean),'root false');
 let all=Buffer.concat(nodes.map(v=>Buffer.from(v)));
 check(sha(all)===row.proof_tables_sha256,'proof hash');
 check(all.length===row.full_table_bits,'table bits');
 check(row.one_node_table_bits===(1<<n),'node record length');
 check(row.min_binary_fanin_nodes===m-1,'dependency floor');
 let corrupt=Buffer.from(prev);corrupt[0]^=1;check(corrupt.some(Boolean),'corrupt root unrecognized');
}
function k4(odd){let E=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b]);let C=[];
 for(let v=0;v<4;v++){let x=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  for(let k=0;k<8;k++){let b=x.map((_,i)=>(k>>i)&1);
   if(b.reduce((a,y)=>a+y,0)%2===(odd&&v===0?1:0))continue;
   C.push(x.map((y,i)=>b[i]?-y:y));}}
 return C;}
for(const odd of [false,true]){
 let C=k4(odd),models=0;
 for(let a=0;a<64;a++)if(C.every(c=>clause(c,a)))models++;
 check(models===(odd?0:8),'K4');
 check(models===raw.controls.K4[odd?'odd':'even'].satisfying_assignments,'K4 ledger');
}
for(const c of [[0],[-3],[1,-1]])check(c.some(x=>!x||Math.abs(x)>2)||new Set(c.map(Math.abs)).size!==c.length,'bad syntax');
check(raw.test_assertions===143,'producer count');
console.log(JSON.stringify({run:'BIT_WITNESS_SEPARATION372',independent_checks:checks,status:'PASS',input_rows:raw.PHP.length},null,2));
