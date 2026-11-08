#!/usr/bin/env node
'use strict';
// Independent finite control for a restricted dynamic sparse-port compiler.
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const signed=v=>v>=128?v-256:v;
function encode(clauses,n){return Buffer.from([195,n,clauses.length,...clauses.flat().map(l=>(l+256)%256)]);}
function k4(charge){const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cls=[];
  for(let v=0;v<4;v++) {const E=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
    for(let mask=0;mask<8;mask++){let parity=((mask&1)+((mask>>1)&1)+((mask>>2)&1))%2;
      if(parity===charge[v]) continue;
      cls.push(E.map((id,j)=>((mask>>j)&1)?id:-id));
    }}return cls;
}
function label(src){if(src.length<3 || src[0]!==195 || src[1]>12 || src.length!==3+3*src[2])return 'MALFORMED';
 const n=src[1],cls=[];
 for(let i=0;i<src[2];i++){
  const c=[signed(src[3+3*i]),signed(src[4+3*i]),signed(src[5+3*i])];
  if(c.some(v=>v===0||Math.abs(v)>n)||new Set(c.map(Math.abs)).size!==3)return 'MALFORMED';
  cls.push(c);
 }
 for(let mask=0;mask<(1<<n);mask++)if(cls.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===Number(l>0)))))return 'SAT';
 return 'UNSAT';
}
const bit=(src,pos)=>(src[Math.floor(pos/8)]>>(pos%8))&1;
function shape(src){let n=src.length*8,r=Math.ceil(Math.sqrt(n+1)),L=2*Math.max(1,Math.floor(Math.log2(n+1))+1);return {n,r,L,base:2**L};}
function addr(src,i,L,state){const n=src.length*8;
 let v=0;if(n)for(let j=0;j<L;j++)v+=bit(src,(i*7+j)%n)*(2**j);
 return state ? (v >= 2**(L-1) ? v - 2**(L-1) : v + 2**(L-1)) : v;
}
function original(src){const {n,r,L,base}=shape(src),mem=new Map(),trace=[];
 let probes=0,addresses=[],state=0;
 for(let i=0;i<r;i++){
  let a=base+addr(src,i,L,state),old=mem.get(a)??0,v=old^(n?bit(src,i%n):0)^(i&1)^state;
  mem.set(a,v);addresses.push(a);probes+=n?L+1:0;
  state=state^old^Number(i%3===0);
 }
 for(let i=r-1;i>=0;i--){let a=base+addr(src,i,L,state),out=mem.get(a)??0;
   trace.push(out);probes+=n?L:0;state=state^out^(i&1);}
 return {result:label(src),trace,probes,distinct:mem.size,virtual:Math.max(base,...addresses),r,L,finalState:state};
}
function sparse(src){const {n,r,L}=shape(src),keys=[],vals=[],trace=[];
 let compares=0,probes=0,state=0;
 function access(key,write){for(let i=0;i<keys.length;i++){compares++;if(keys[i]===key){if(write!==null)vals[i]=write;return vals[i];}}
  if(write===null)return 0;keys.push(key);vals.push(write);return write;
 }
 for(let i=0;i<r;i++){
  const a=addr(src,i,L,state),old=access(a,null);
  const v=old^(n?bit(src,i%n):0)^(i%2)^state;
  access(a,v);probes+=n?L+1:0;state=state^old^Number(i%3===0);
 }
 for(let i=r-1;i>=0;i--){const a=addr(src,i,L,state),out=access(a,null);
  trace.push(out);probes+=n?L:0;state=state^out^(i&1);
 }
 return {result:label(src),trace,probes,distinct:keys.length,compares,finalState:state,
         physical:keys.length*(L+2)+4*L+64};
}
let seed=0x5a17b3d0;function rand(){seed^=(seed<<13);seed^=(seed>>>17);seed^=(seed<<5);return seed>>>0;}
const odd=encode(k4([1,0,0,0]),6),even=encode(k4([0,0,0,0]),6);
assert.equal(label(odd),'UNSAT');assert.equal(label(even),'SAT');
let ss=[Buffer.alloc(0),Buffer.from([195]),Buffer.from([195,1,0]),odd,even,encode(k4([1,0,0,0]).slice(0,-1),6)];
for(let b=0;b<256;b++)ss.push(Buffer.from([b]));
for(let j=0;j<300;j++){let len=rand()%65;ss.push(Buffer.from(Array.from({length:len},()=>rand()%256)));}
for(let j=0;j<100;j++){let charges=Array.from({length:4},()=>rand()%2),buf=encode(k4(charges),6);
 if(rand()%2){buf=Buffer.from(buf);buf[rand()%buf.length]^=(1<<(rand()%8));}ss.push(buf);}
let checks=0,labels={},maxGap=0,collisions=0,cmp=0;
for(const src of ss){let a=original(src),b=sparse(src);
 assert.equal(a.result,b.result);checks++;
 assert.deepEqual(a.trace,b.trace);checks++;
 assert.equal(a.probes,b.probes);checks++;
 assert.equal(a.distinct,b.distinct);checks++;
 assert(b.distinct<=a.r);checks++;
 assert(b.compares<=3*a.r*a.r);checks++;
 assert.equal(a.finalState,b.finalState);checks++;
 assert(b.physical<=a.r*(a.L+2)+4*a.L+64);checks++;
 labels[a.result]=(labels[a.result]||0)+1;
 collisions+=a.r-a.distinct;cmp+=b.compares;maxGap=Math.max(maxGap,a.virtual-b.physical);
}
const result={label:'LSPV2_504_JS',samples:ss.length,assertions:checks,labels,max_highwater_gap:maxGap,total_key_comparisons:cmp,access_collisions:collisions,odd_sha256:crypto.createHash('sha256').update(odd).digest('hex'),native_machine_executed:false};
console.log(JSON.stringify(result,null,2));
