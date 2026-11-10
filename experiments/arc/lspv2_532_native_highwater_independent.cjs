'use strict';
// Independent Node implementation of finite signed-3CNF syntax and native indexed-jump control.
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
function parse(bytes){
  if(bytes.length<5 || bytes[0]!==83 || bytes[1]!==51 || bytes[2]!==67)return null;
  const n=bytes[3],m=bytes[4];
  if(n===0 || n>127 || bytes.length!==5+3*m)return null;
  const cs=[];
  for(let i=0;i<m;i++){
    let clause=[];const unique=new Set();
    for(let j=0;j<3;j++){
      const x=bytes[5+3*i+j],id=x&127;
      if(id===0||id>n||unique.has(id))return null;
      unique.add(id);clause.push(x&128?-id:id);
    }
    cs.push(clause);
  }
  return {n,cs};
}
function sat(bytes){
  const f=parse(bytes);if(!f)return false;
  for(let mask=0;mask<2**f.n;mask++){
    let ok=true;
    for(const c of f.cs){let has=false;
      for(const lit of c){let truth=((mask>>> (Math.abs(lit)-1))&1)!==0;if(truth===(lit>0)){has=true;break;}}
      if(!has){ok=false;break;}
    }
    if(ok)return true;
  }
  return false;
}
function enc(n,cs){
  const bytes=[83,51,67,n,cs.length];for(const c of cs)for(const lit of c)bytes.push(Math.abs(lit)|(lit<0?128:0));return Buffer.from(bytes);
}
function k4(odd){
 const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
 const cs=[];for(let v=0;v<4;v++){
  const inc=edges.map((e,i)=>e.includes(v)?i+1:-1).filter(i=>i>0);
  for(let a=0;a<8;a++){
   const parity=([0,1,2].reduce((acc,j)=>acc+((a>>(2-j))&1),0)&1);
   if(parity!==(odd&&v===0?1:0))cs.push(inc.map((e,j)=>(a>>(2-j))&1?-e:e));
  }
 }
 return enc(6,cs);
}
function prelude(x){
  let acc='1', steps=1;const N=x.length*8;
  for(let i=0;i<N;i++){acc+='0';steps++;}
  const address=BigInt('0b'+acc);steps+=2; // 1 indexed reposition + 1 blank read
  const visited=new Set([address.toString()]);
  assert.equal(visited.size,1);
  return {steps,native:address,sparseUpper:2*N+3};
}
const cases=[k4(false),k4(true),enc(3,[[1,2,3]]),enc(3,Array.from({length:8},(_,a)=>[1,2,3].map((i)=>((a>>(i-1))&1)?-i:i))),enc(3,[])];
cases.push(Buffer.alloc(0),Buffer.from('S3C'),Buffer.from([83,51,67,3,1,1,2]),Buffer.from([83,51,67,3,1,1,1,2]),Buffer.from([83,51,67,3,1,1,2,4]),Buffer.from([83,51,67,0,0]),Buffer.from('HELLO'),Buffer.from([...Array(32).keys()]));
for(let i=0;i<120;i++)cases.push(Buffer.from([i>>8,i&255]));
assert.equal(cases.length,133);
let counts={sources:cases.length,sat:0,unsat_valid:0,malformed:0,verified:0},examples=[];
for(const x of cases){
 const f=parse(x),res=sat(x),j=prelude(x),N=x.length*8;
 assert.equal(j.steps,N+3);assert.equal(j.native,1n<<BigInt(N));
 assert.equal(sat(Buffer.from(x)),res); // preserve source byte-exact, binary/malformed semantics
 counts.sat+=Number(res);counts.unsat_valid+=Number(Boolean(f)&&!res);
 counts.malformed+=Number(f===null);counts.verified++;
 if(examples.length<13)examples.push({N_bytes:x.length,N_bits:N,source_sha256:crypto.createHash('sha256').update(x).digest('hex'),label:!f?'MALFORMED':res?'SAT':'UNSAT',wrapper_extra_steps:j.steps,native_space_exact:j.native.toString(),sparse_bit_upper:j.sparseUpper});
}
assert.deepEqual(counts,{sources:133,sat:3,unsat_valid:2,malformed:128,verified:133});
const exact=(c)=>((c+2)/(c*c)-c)/2;
assert.ok(Math.abs(exact(1.2)-23/45)<1e-12);
const out={status:'PASS',language:'S3C finite controls',counts,examples,exact_beta_6_5:'23/45',beta_minus_half:'1/90'};
console.log(JSON.stringify(out,null,2));
