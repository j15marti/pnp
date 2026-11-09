#!/usr/bin/env node
// Independent LSPV-2/523 verifier. Two declared calculi, neither R_mix341.
import crypto from 'node:crypto';
let assertions = 0;
function check(test, label='check') { assertions++; if (!test) throw new Error(label); }
const hash = s => crypto.createHash('sha256').update(s).digest('hex');
function encode(clauses,n) {return 'T3|'+n+'|'+clauses.length+'|'+clauses.map(c=>c.join(',')).join('|')+'\n';}
function parse(s) {
  if (!/^T3\|[1-9][0-9]*\|[1-9][0-9]*\|/.test(s) || !s.endsWith('\n') || s.slice(0,-1).includes('\n')) throw Error('header');
  const f=s.slice(0,-1).split('|'), n=Number(f[1]), m=Number(f[2]);
  if (!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||f.length!==m+3) throw Error('count');
  let cs=f.slice(3).map(part=>part.split(',').map(z=>{
    if (!/^-?[1-9][0-9]*$/.test(z)) throw Error('literal');
    const x=Number(z);if(!Number.isSafeInteger(x)||Math.abs(x)>n)throw Error('range');return x;
  }));
  for(let c of cs){if(c.length<1||c.length>3||new Set(c.map(Math.abs)).size!==c.length)throw Error('proper');
    for(let j=1;j<c.length;j++)if(Math.abs(c[j-1])>=Math.abs(c[j]))throw Error('canonical');}
  if(encode(cs,n)!==s)throw Error('canonical');return {n,cs};
}
function horn(n){return [[1],...Array.from({length:n-1},(_,i)=>[-i-1,i+2]),[-n]];}
function resolution(a,b,p) {
  if(!(a.includes(p)&&b.includes(-p))){if(b.includes(p)&&a.includes(-p))[a,b]=[b,a];else throw Error('pivot');}
  let c=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])].sort((u,v)=>Math.abs(u)-Math.abs(v));
  if(c.some(x=>c.includes(-x)))throw Error('tautology');return c;
}
function checkedProof(source,proof){
  let {n,cs}=parse(source);if(hash(source)!==proof.sha)throw Error('source');
  let nodes=new Map(cs.map((c,j)=>['s'+j,c]));
  for(let step of proof.steps){
    if(nodes.has(step.id)||!nodes.has(step.a)||!nodes.has(step.b)||!Number.isInteger(step.p)||step.p<1||step.p>n)throw Error('node');
    let want=resolution(nodes.get(step.a),nodes.get(step.b),step.p);
    if(JSON.stringify(want)!==JSON.stringify(step.out))throw Error('conclusion');nodes.set(step.id,want);
  }
  if(!proof.steps.length||nodes.get(proof.steps.at(-1).id).length!==0)throw Error('not refuted');
  return proof.steps.length;
}
function proofChain(n){
  let cs=horn(n), steps=[],previous='s0',value=[1];
  for(let i=1;i<=n;i++) {let out=resolution(value,cs[i],i);steps.push({id:'r'+i,a:previous,b:'s'+i,p:i,out});value=out;previous='r'+i;}
  return {sha:hash(encode(cs,n)),steps};
}
function rupEmpty(s){
  let {cs}=parse(s),assign=new Map(),reads=0,passes=0,propagations=0;
  while(true){passes++;let changed=false;
    for(let c of cs){reads++;let open=[],satisfied=false;
      for(let lit of c){let v=Math.abs(lit),a=assign.get(v);
        if(a===undefined)open.push(lit);else if(a===(lit>0)){satisfied=true;break;}}
      if(satisfied)continue;
      if(open.length===0)return {accepted:true,reads,passes,propagations};
      if(open.length===1){let lit=open[0],v=Math.abs(lit),bit=lit>0;
        if(!assign.has(v)){assign.set(v,bit);propagations++;changed=true;}}
    }
    if(!changed)return {accepted:false,reads,passes,propagations};
  }
}
function k4(charges){
  let edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
  let cs=[];for(let vertex=0;vertex<4;vertex++){
    let ids=edges.map((e,i)=>e.includes(vertex)?i+1:null).filter(x=>x!==null);
    for(let mask=0;mask<8;mask++)if((((mask&1)+((mask>>1)&1)+((mask>>2)&1))%2)!==charges[vertex]){
      cs.push(ids.map((v,j)=>(mask&(1<<(2-j)))?-v:v));
    }
  }return cs;
}
function modelExists(cs,n){for(let mask=0;mask<(1<<n);mask++)if(cs.every(c=>c.some(x=>Boolean(mask&(1<<(Math.abs(x)-1)))===(x>0))))return true;return false;}
const chain=[];
for(let n=1;n<=16;n++){
  let src=encode(horn(n),n),p=proofChain(n),got=checkedProof(src,p),macro=rupEmpty(src);
  check(parse(src).cs.length===n+1);check(got===n);check(macro.accepted);check(macro.reads>=n+1);
  for(let excluded=0;excluded<=n;excluded++){
    let values=Array.from({length:n},(_,j)=>excluded===0?false:excluded===n?true:j<excluded),
        satisfiable=horn(n).every((c,j)=>j===excluded||c.some(x=>values[Math.abs(x)-1]===(x>0)));
    check(satisfiable,'indispensable '+n+'/'+excluded);
  }
  chain.push({n,source_sha256:hash(src),source_bytes:Buffer.byteLength(src),micro_resolution_nodes:got,macro_rup_add_records:1,rup_clause_reads:macro.reads,rup_assignments:macro.propagations,rup_rounds:macro.passes});
}
let src=encode(horn(4),4),p=proofChain(4);
function mustReject(o){let failed=false;try{checkedProof(src,o)}catch(e){failed=true}check(failed,'malformed proof must reject');}
for(let variation=0;variation<7;variation++){
  let bad=JSON.parse(JSON.stringify(p));
  if(variation===0)bad.sha='0'.repeat(64);
  if(variation===1)bad.steps[1].p=4;
  if(variation===2)bad.steps[1].a='s99';
  if(variation===3)bad.steps[1].out=[-2];
  if(variation===4)bad.steps[1].id='r1';
  if(variation===5)bad.steps[0].a='r4';
  if(variation===6)bad.steps=[{id:'r1',a:'s0',b:'s1',p:1,out:[]}];
  mustReject(bad);
}
const invalid=['T3|1|2|1|-1','T3|1|1|01\n','T3|2|1|1,1\n','T3|1|1|0\n','T3|1|1|1\n\n','T3|2|1|2,1\n','T3|2|1|1,3\n'];
for(let x of invalid){let failed=false;try{parse(x)}catch(e){failed=true}check(failed,'malformed original');}
let t=[];for(let bits=0;bits<16;bits++){
  let charges=Array.from({length:4},(_,i)=>(bits>>(3-i))&1),c=k4(charges),source=encode(c,6),sat=modelExists(c,6);
  check(parse(source).cs.length===16);check(sat===(charges.reduce((a,b)=>a+b,0)%2===0));
  t.push({charges,sat,source_sha256:hash(source),source_bytes:Buffer.byteLength(source)});
}
console.log(JSON.stringify({status:'PASS',assertions,chain,tseitin:t,invalid_rejections:invalid.length,corrupted_trace_rejections:7},null,2));
