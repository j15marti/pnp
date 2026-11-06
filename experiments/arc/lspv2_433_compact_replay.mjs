// LSPV-2/433 standalone compact proof-carrying dead-scan erasure check.
// Native FLMV resource measurement is NOT claimed.
import assert from 'node:assert/strict';
const CERT=['READ_ALL_PRIVATE','RESTORE_FRESH_STATE','CALL_GUEST_FRESH'];
const normalize=p=>JSON.stringify(p)===JSON.stringify(CERT)?['CALL_GUEST_FRESH']:null;
assert.deepEqual(normalize(CERT),['CALL_GUEST_FRESH']);
for(const bad of [
 ['READ_ALL_WRITES_GUEST_STATE','RESTORE_FRESH_STATE','CALL_GUEST_FRESH'],
 ['READ_ALL_PRIVATE','RETAIN_INDEX_HEAD','CALL_GUEST_FRESH'],
 ['READ_ALL_EXTERNAL_IO','RESTORE_FRESH_STATE','CALL_GUEST_FRESH']])assert.equal(normalize(bad),null);
function edges(graph){let v=graph==='K4'?4:8,es=[];
 for(let i=0;i<v;i++)for(let j=i+1;j<v;j++)if(graph==='K4'||((i^j).toString(2).match(/1/g)||[]).length===1)es.push([i,j]);return [v,es];}
function formula(graph,odd){let [v,es]=edges(graph),c=[];
 for(let u=0;u<v;u++){let inc=es.flatMap(([i,j],e)=>u===i||u===j?[e+1]:[]);assert.equal(inc.length,3);
  let charge=u===0?1:(!odd&&u===1?1:0);
  for(let a=0;a<8;a++)if((((a&1)+((a>>1)&1)+((a>>2)&1))&1)!==charge)c.push(inc.map((e,k)=>(a>>k)&1?-e:e));}
 return [es.length,c];}
function enc(n,c,pad=-1){let bin=(i,k)=>i.toString(2).padStart(k,'0'),s=bin(0xa7,8)+bin(n,8)+bin(c.length,8);
 for(let j=0;j<c.length;j++){for(let lit of c[j])s+=bin((lit<0?128:0)+Math.abs(lit),8);s+=j===pad?'1':'0';}return s;}
function decide(s,full){let seen=new Set();const rd=i=>(seen.add(i),s[i]);
 if(full)for(let i=0;i<s.length;i++)rd(i);
 if(s.length<24||/[^01]/.test(s))return ['MALFORMED',seen];
 const v=(p,k)=>parseInt(Array.from({length:k},(_,j)=>rd(p+j)).join(''),2);
 let n=v(8,8),m=v(16,8);if(v(0,8)!==0xa7||n<1||n>12||s.length!==24+25*m)return ['MALFORMED',seen];
 let clauses=[];for(let j=0;j<m;j++){let row=[];for(let k=0;k<3;k++){let z=v(24+25*j+8*k,8),idx=z&127;if(!idx||idx>n)return ['MALFORMED',seen];row.push(z&128?-idx:idx);}clauses.push(row);}
 for(let a=0;a<(1<<n);a++)if(clauses.every(row=>row.some(z=>(((a>>(Math.abs(z)-1))&1)===+(z>0)))))return ['SAT',seen];
 return ['UNSAT',seen];}
function cache(xs,full){let prev=null,reads=null,calls=0,hits=0;
 for(let s of xs){let shared=prev!==null&&prev.length===s.length&&[...reads].every(i=>s[i]===prev[i]);
  if(shared){hits++;continue;}calls++;[,reads]=decide(s,full);prev=s;}
 return {calls,hits};}
let total=0,before=0,after=0;
for(let graph of ['K4','cube'])for(let odd of [false,true]){
 let [n,c]=formula(graph,odd),xs=[enc(n,c),...Array.from({length:10},(_,i)=>enc(n,c,i))];
 let label=odd?'UNSAT':'SAT';for(let x of xs){assert.equal(decide(x,false)[0],label);assert.equal(decide(x,true)[0],label);}
 let a=cache(xs,false),b=cache(xs,true);assert.equal(a.calls,1);assert.equal(a.hits,10);assert.equal(b.calls,11);assert.equal(b.hits,0);
 total+=xs.length;before+=b.calls;after+=a.calls;
}
assert.equal(total,44);assert.equal(before,44);assert.equal(after,4);
console.log(JSON.stringify({result:'PASS',cases:total,full_read_calls:before,certified_erased_calls:after,reuse_gains:before-after}));
