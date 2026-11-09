// Independent strict-3CNF Tseitin replay-cylinder control, LSPV-4/510R.
// Finite symbolic validation only; NOT a native FLMV interpreter.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const gam=n=>{const b=n.toString(2);return '0'.repeat(b.length-1)+b;};
const bin=(n,w)=>n.toString(2).padStart(w,'0');
const graphs=new Map([
 ['K4',[4,Array.from({length:4},(_,a)=>Array.from({length:4},(_,b)=>a<b?[a,b]:null)).flat().filter(x=>Array.isArray(x))]],
 ['K33',[6,Array.from({length:3},(_,a)=>Array.from({length:3},(_,b)=>[a,b+3])).flat()]],
 ['Q3',[8,Array.from({length:8},(_,a)=>[0,1,2].map(b=>a<(a^(1<<b))?[a,a^(1<<b)]:null)).flat().filter(x=>Array.isArray(x))]],
 ['Heawood',[14,Array.from({length:7},(_,j)=>[0,1,3].map(d=>[(j+d)%7,j+7])).flat().sort((a,b)=>a[0]-b[0]||a[1]-b[1])]],
]);
function encode(h,edges,k=2,even=false){
 const m=edges.length, w=Math.floor(Math.log2(m+3*k))+1;
 const header='10100101'+'1'.repeat(h)+'0';
 const clauses=[];
 for(let v=0;v<h;v++){
  const ids=edges.flatMap(([a,b],j)=>a===v||b===v?[j+1]:[]);
  assert.equal(ids.length,3);
  for(let b=0;b<8;b++){
   const signs=[b>>2&1,b>>1&1,b&1];
   if((signs[0]^signs[1]^signs[2])!==(Number(!even&&v===0))) clauses.push(ids.map((id,t)=>[id,signs[t]]));
  }
 }
 for(let j=0;j<k;j++)clauses.push([0,1,2].map(t=>[m+3*j+t+1,(j+t)&1]));
 return {header,w,clauses,bits:header+clauses.flatMap(cl=>cl.map(([id,s])=>bin(id,w)+s)).join('')+'01'};
}
function replayGuard(s){
 const seen=new Set();let queries=0;
 const read=i=>{seen.add(i);queries++;return i<s.length?s[i]:null;};
 if(Array.from({length:8},(_,i)=>read(i)).join('')!=='10100101')return [false,seen,queries];
 let p=8,h=0;
 while(read(p)==='1'){h++;p++;}
 if(read(p)!=='0')return [false,seen,queries];
 p++;
 if(h<4||h%2)return [false,seen,queries];
 const m=3*h/2, k=Math.max(2,Math.ceil((2/5)*Math.ceil(Math.log2(h))));
 const w=Math.floor(Math.log2(m+3*k))+1,step=3*(w+1),core=4*h;
 const end=p+(core+k)*step;
 if(read(end)!=='0'||read(end+1)!=='1'||read(end+2)!==null)return [false,seen,queries];
 const clause=(z,needSign)=>{
  let ids=[],ss=[];
  for(let t=0;t<3;t++){
   let base=p+z*step+t*(w+1),d='';
   for(let b=0;b<w;b++){let x=read(base+b);if(x==null)return null;d+=x;}
   ids.push(parseInt(d,2));
   if(needSign)ss.push(Number(read(base+w)));
  }
  return new Set(ids).size===3?[ids,ss]:null;
 };
 for(let v=0;v<h;v++){
   const four=[0,1,2,3].map(t=>clause(4*v+t,true));
   if(four.some(x=>x==null))return [false,seen,queries];
   const ids=JSON.stringify(four[0][0]);
   if(four.some(x=>JSON.stringify(x[0])!==ids)||four[0][0].some(x=>x<1||x>m))return [false,seen,queries];
   const observed=four.map(x=>x[1].join('')).sort().join('|');
   const wanted=Array.from({length:8},(_,n)=>[(n>>2)&1,(n>>1)&1,n&1]).filter(ss=>(ss[0]^ss[1]^ss[2])!==Number(v===0)).map(ss=>ss.join('')).sort().join('|');
   if(observed!==wanted)return [false,seen,queries];
 }
 for(let e=1;e<=m;e++){
  let count=0;
  for(let v=0;v<h;v++){const c=clause(4*v,false);if(c===null)return [false,seen,queries];if(c[0].includes(e))count++;}
  if(count!==2)return [false,seen,queries];
 }
 for(let j=0;j<k;j++){
  const c=clause(core+j,false);
  if(c===null||c[0].some((id,t)=>id!==m+3*j+t+1))return [false,seen,queries];
 }
 return [true,seen,queries];
}
const results=[];let variants=0;
for(const [name,[h,edges]] of graphs){
 const k=2,{header,w,bits}=encode(h,edges,k),[yes,seen,q]=replayGuard(bits);
 assert.equal(yes,true);
 const flips=Array.from({length:3*k},(_,a)=>header.length+(4*h+Math.floor(a/3))*3*(w+1)+(a%3)*(w+1)+w);
 assert(flips.every(p=>!seen.has(p)));
 for(let code=0;code<1<<(3*k);code++){
   const edit=bits.split('');
   flips.forEach((p,j)=>{if(code&(1<<j))edit[p]=edit[p]==='0'?'1':'0';});
   const check=edit.join(''),[v,seen2]=replayGuard(check);
   assert.equal(v,true);assert.deepEqual(seen2,seen);
   for(const index of seen)if(index<bits.length)assert.equal(check[index],bits[index]);
   variants++;
 }
 const invalid=[bits.slice(1),bits.slice(0,-1),bits+'0',bits.slice(0,-2)+'00',('0'===bits[0]?'1':'0')+bits.slice(1)];
 const change=(p)=>bits.slice(0,p)+(bits[p]==='0'?'1':'0')+bits.slice(p+1);
 invalid.push(change(header.length+w));
 for(const b of invalid)assert.equal(replayGuard(b)[0],false);
 assert.equal(replayGuard(encode(h,edges,k,true).bits)[0],false);
 results.push({name,h,edges:edges.length,k,source_bits:bits.length,read_positions:seen.size,queries:q,unread:flips.length,variants:1<<(3*k),sha256:createHash('sha256').update(bits).digest('hex')});
}
const summary={experiment:'LSPV-4/510R independent Node',status:'COMPUTATIONAL',native_flmv_interpreter:false,total_variants:variants,graphs:results,checks:'PASS'};
console.log(JSON.stringify(summary,null,2));
