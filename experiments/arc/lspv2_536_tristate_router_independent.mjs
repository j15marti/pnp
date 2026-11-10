#!/usr/bin/env node
// LSPV-2/536: independent exact TSC event simulator.
// Follows ECCC TR23-095 Figure 1, not an FLMV native work-tape implementation.
import crypto from 'node:crypto';
const Z=-1;
function simulate(bits,index){
  const m=bits.length,k=Math.log2(m);
  if(!Number.isInteger(k)||k<1)throw Error('bad size');
  const wires=new Map(),listeners=new Map(),gates=[];
  function add(op,a,b,out){
    const id=gates.length;gates.push({op,a,b,out});
    for(const key of new Set([a,b])){
      const v=listeners.get(key)||[];v.push(id);listeners.set(key,v);
    }
  }
  for(let i=0;i<m;i++)wires.set('x'+i,bits[i]);
  for(let j=0;j<k;j++)wires.set('b'+j,(index>>(k-1-j))&1);
  wires.set('one',1);wires.set('r1',1);
  for(let j=0;j<k;j++)add('xor','b'+j,'one','n'+j);
  for(let v=m;v<2*m;v++)add('buffer','x'+(v-m),'r'+v,'o'+v);
  for(let v=m-1;v>=1;v--){
    const d=31-Math.clz32(v);
    add('join','o'+(2*v),'o'+(2*v+1),'o'+v);
    add('buffer','r'+v,'b'+d,'r'+(2*v+1));
    add('buffer','r'+v,'n'+d,'r'+(2*v));
  }
  let events=[];
  for(const w of wires.keys())events.push(...(listeners.get(w)||[]));
  let attempts=0,productive=0;
  for(let pos=0;pos<events.length;pos++){
    const {op,a,b,out}=gates[events[pos]];attempts++;
    const x=wires.has(a)?wires.get(a):Z,y=wires.has(b)?wires.get(b):Z;
    let value=Z;
    if(op==='xor'&&x!==Z&&y!==Z)value=x^y;
    if(op==='buffer'&&y===1)value=x;
    if(op==='join'){
      if(x===Z)value=y;else if(y===Z||y===x)value=x;
      else throw Error('illegal join');
    }
    if(value===Z)continue;
    if(wires.has(out)){if(wires.get(out)!==value)throw Error('non-monotone');continue;}
    wires.set(out,value);productive++;
    events.push(...(listeners.get(out)||[]));
  }
  if(wires.get('o1')!==bits[index])throw Error('wrong bit');
  if(gates.length!==4*m-3+k||productive!==3*k+1||attempts!==3*m+5*k-1)
    throw Error('wrong charge');
  return {gates:gates.length,productive,attempts};
}
function k4(odd){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],body=[];
  for(let v=0;v<4;v++){
    const inc=edges.flatMap(([a,b],e)=>(a===v||b===v)?[e]:[]);
    for(let mask=0;mask<8;mask++){
      let parity=0;for(let j=0;j<3;j++)parity^=(mask>>(2-j))&1;
      if(parity===(odd&&v===0?1:0))continue;
      for(let j=0;j<3;j++)body.push(inc[j]|(((mask>>(2-j))&1)<<7));
    }
  }
  return Buffer.from([...Buffer.from('S3R'),6,16,...body]);
}
function parse(raw){
  if(raw.length<5||raw.subarray(0,3).toString()!=='S3R')return null;
  const n=raw[3],m=raw[4];if(n<3||m<1||raw.length!==5+3*m)return null;
  const clauses=[];
  for(let j=0;j<m;j++){
    const c=[];
    for(let h=0;h<3;h++){
      const q=raw[5+3*j+h];
      if((q&0x60)||(q&31)>=n)return null;
      c.push({index:q&31,negative:!!(q&128)});
    }
    if(new Set(c.map(t=>t.index)).size!==3)return null;
    clauses.push(c);
  }
  return {n,clauses};
}
function label(raw){
  const f=parse(raw);if(!f)return 'MALFORMED';
  for(let mask=0;mask<(1<<f.n);mask++){
    if(f.clauses.every(c=>c.some(l=>Boolean(mask&(1<<l.index))!==l.negative)))return 'SAT';
  }
  return 'UNSAT';
}
let cases=0,rows=[];
for(let k=1;k<=8;k++){
  const m=1<<k;
  for(let pattern=0;pattern<3;pattern++){
    const bits=Array.from({length:m},(_,i)=>pattern===0?(i&1):pattern===1?(((i*7+3)>>2)&1):(((i*i+11)>>3)&1));
    for(let index=0;index<m;index++){simulate(bits,index);cases++;}
    rows.push({k,m,pattern,cases:m,gates:4*m-3+k,productive:3*k+1,attempts:3*m+5*k-1,native_direct_index_steps:k+1});
  }
}
const orig=[k4(true),k4(false)];
const sources=orig.map(b=>({sha256:crypto.createHash('sha256').update(b).digest('hex'),label:label(b),bits:8*b.length}));
if(sources[0].label!=='UNSAT'||sources[1].label!=='SAT')throw Error('bad controls');
const b=orig[0],invalid=[Buffer.alloc(0),Buffer.from('S3R'),b.subarray(0,-1),
  Buffer.concat([Buffer.from('X'),b.subarray(1)]),
  Buffer.concat([b.subarray(0,3),Buffer.from([1]),b.subarray(4)]),
  Buffer.concat([b.subarray(0,4),Buffer.from([0]),b.subarray(5)])];
for(const bad of invalid)if(label(bad)!=='MALFORMED')throw Error('invalid accepted');
console.log(JSON.stringify({status:'PASS',independent_cases:cases,malformed_rejections:invalid.length,sources,rows},null,2));
