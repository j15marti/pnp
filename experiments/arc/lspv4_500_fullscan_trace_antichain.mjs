// Independent finite control of the LSPV-4/500 trace-antichain theorem.
// No native FLMV machine; no claim of universal SAT hardness.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const magic='10110101', n=16, m=192, edgeList=[];
for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edgeList.push([a,b]);
function clausesFor(charge){
 const clauses=[];
 for(let v=0;v<4;v++){
  const ed=edgeList.map(([a,b],i)=>a===v||b===v?i:-1).filter(i=>i>=0);
  assert.equal(ed.length,3);
  for(let k=0;k<8;k++){
   const bits=[(k>>2)&1,(k>>1)&1,k&1];
   if((bits[0]^bits[1]^bits[2])!==(charge===v?1:0)){
    clauses.push(ed.map((e,i)=>[e,bits[i]]));
   }
  }
 }
 return clauses;
}
const odd0=clausesFor(0),odd1=clausesFor(1),even=clausesFor(-1);
const fresh=[];
for(let a=6;a<16;a++)for(let b=a+1;b<16;b++)for(let c=b+1;c<16;c++){
 for(let z=0;z<8;z++){
  if(z===7)continue;
  fresh.push([[a,(z>>2)&1],[b,(z>>1)&1],[c,z&1]]);
 }
}
assert.equal(fresh.length,840);
const common=fresh.slice(0,175), variants=fresh.slice(175,303);
function enc(clauses){
 assert.equal(clauses.length,m);
 return magic+n.toString(2).padStart(6,'0')+m.toString(2).padStart(12,'0')+
 clauses.map(cl=>cl.map(([id,s])=>s+id.toString(2).padStart(4,'0')).join('')).join('');
}
function satisfies(clauses,asgn){return clauses.every(cl=>cl.some(([v,s])=>asgn[v]!==s));}
function bruteCore(C){for(let mask=0;mask<64;mask++){
 const a=Array.from({length:6},(_,i)=>(mask>>i)&1);
 if(satisfies(C,a))return true;
}return false;}
assert.equal(bruteCore(odd0),false);assert.equal(bruteCore(odd1),false);assert.equal(bruteCore(even),true);
const allTrueFresh=[0,0,0,0,0,0,...Array(10).fill(1)];
const pack=(i,which)=>enc([...which,...common,variants[i]]);
const odd=Array.from({length:128},(_,i)=>pack(i,i%2===0?odd0:odd1));
const both=Array.from({length:128},(_,i)=>pack(i,i%2===0?odd0:even));
for(let i=0;i<128;i++){
 assert.equal(odd[i].length,2906);assert.equal(both[i].length,2906);
 assert.equal(satisfies([...odd0,...common,variants[i]],allTrueFresh),false);
 assert.equal(satisfies([...even,...common,variants[i]],allTrueFresh),true);
}
assert.equal(new Set(odd).size,128);assert.equal(new Set(both).size,128);
function sha(s){return crypto.createHash('sha256').update(s).digest('hex');}
assert.equal(sha(odd[0]),'167ede525c2c62ce4fd4e7944b46e65d19fa46b5145d9ba112535d0d4ce7083a');
assert.equal(sha(both[127]),'8f4e704af01d9d5ac3c25d181e8d4154bd0e033971357a9b59b8ec5d4e063f08');
const prefixes=new Set([enc([...odd0,...common,variants[0]]).slice(0,266),enc([...odd1,...common,variants[0]]).slice(0,266)]);
function guest(s,full){
 const visited=new Set();const read=i=>{visited.add(i);return s[i];};
 if(full)for(let i=0;i<s.length;i++)read(i);
 if(s.length!==2906||s.slice(0,26)!==magic+n.toString(2).padStart(6,'0')+m.toString(2).padStart(12,'0'))
  return {output:'MALFORMED',read:visited};
 let prefix='';for(let i=0;i<266;i++)prefix+=read(i);
 if(prefixes.has(prefix))return {output:'UNSAT',read:visited};
 let clauses=[];
 for(let k=0;k<192;k++){
  const row=[];
  for(let j=0;j<3;j++){
   const p=26+(3*k+j)*5,s=+read(p),v=parseInt(Array.from({length:4},(_,t)=>read(p+1+t)).join(''),2);
   row.push([v,s]);
  }
  clauses.push(row);
 }
 // Only the even-charge finite SAT fixture reaches this fallback.
 // For a total all-input decider, replace this line with general SAT solving.
 assert.ok(satisfies(clauses,allTrueFresh));
 return {output:'SAT',read:visited};
}
function cache(inputs,full,h){
 const a=[];let calls=0,hits=0,compares=0;
 for(let x of inputs){
  let found=false;
  for(let anchor of a){
   if(anchor.s.length!==x.length)continue;
   let match=true;
   for(let pos of anchor.read){compares++;if(anchor.s[pos]!==x[pos]){match=false;break;}}
   if(match){found=true;break;}
  }
  if(found)hits++;
  else{const g=guest(x,full);calls++;a.unshift({s:x,read:[...g.read].sort((p,q)=>p-q),label:g.output});a.length=Math.min(h,a.length);}
 }
 return {calls,hits,comparisons:compares};
}
const results={};
for(let [name,children] of [['odd_two_core',odd],['odd_even',both]]){
 results[name]={};for(let [mode,full] of [['prefix',false],['full',true]]){
  results[name][mode]={};for(let h of [1,2,4,8])results[name][mode][h]=cache(children,full,h);
 }
}
assert.equal(results.odd_two_core.prefix[2].calls,2);
assert.equal(results.odd_two_core.prefix[2].hits,126);
assert.equal(results.odd_even.prefix[2].calls,96);
for(let name of Object.keys(results))for(let h of [1,2,4,8]){
 assert.equal(results[name].full[h].calls,128);
 assert.equal(results[name].full[h].hits,0);
}
const out={status:'PASS',role:'LSPV-4/500',bits:2906,
 sha_first_odd:sha(odd[0]),sha_last_even:sha(both[127]),results};
console.log(JSON.stringify(out,null,2));
