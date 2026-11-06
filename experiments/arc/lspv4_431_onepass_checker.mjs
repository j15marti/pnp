#!/usr/bin/env node
// LSPV-4/431: independent fixed-width 3-CNF one-pass namespace controls.
// Self-contained. Does not emulate FLMV physical machine.
import crypto from 'node:crypto';
const w=n=>Math.floor(Math.log2(7*n+4))+1;
const id=(n,i,k)=>({x:1+i,p:1+n+i,q:1+2*n+i,r:1+3*n+i,s:1+4*n+i,d:1+5*n+i})[k];
function encode(n,mask,B){
  const lit=v=>'0'+v.toString(2).padStart(w(n),'0');
  let s='01101011'+'1'.repeat(n)+'0';
  for(let i=0;i<n;i++){
    s+='10'+[id(n,i,(mask&(1<<i))?'x':'d'),id(n,i,'p'),id(n,i,'q')].map(lit).join('');
  }
  for(const j of B)s+='01'+[id(n,j,'x'),id(n,j,'r'),id(n,j,'s')].map(lit).join('');
  return s+'00';
}
function parse(s){
  if(!s.startsWith('01101011'))throw Error('magic');
  let i=8,n=0;while(s[i]==='1'){n++;i++;}
  if(n<1||s[i++]!=='0')throw Error('n');
  let core=[],tail=[];
  while(i<s.length){
    const tag=s.slice(i,i+2);i+=2;if(tag==='00')break;
    if(tag!=='10'&&tag!=='01')throw Error('tag');
    let c=[];for(let k=0;k<3;k++){
      if(s[i++]!=='0')throw Error('sign');
      c.push(parseInt(s.slice(i,i+w(n)),2));i+=w(n);
    }
    if(new Set(c).size!==3)throw Error('duplicate');
    (tag==='10'?core:tail).push(c);
  }
  if(i!==s.length||core.length!==n)throw Error('length');
  return {n,core,tail};
}
let count=0;
const sizes={1:46,2:73,3:94,4:130,5:154,6:178,7:202,8:226};
for(let n=1;n<=8;n++){
  const seen=new Set();
  for(let S=0;S<(1<<n);S++){
    seen.add(encode(n,S,[]).slice(0,-2));
    for(let j=0;j<n;j++){
      const src=encode(n,S,[j]);const {core,tail}=parse(src);
      const c=new Set(core.flat());
      const disj=tail.flat().every(x=>!c.has(x));
      if(disj!==!(S&(1<<j)))throw Error('disjointness contradiction');
      if(src.length!==sizes[n])throw Error('size');
      count+=3;
    }
  }
  if(seen.size!==(1<<n))throw Error('state collision');
  count++;
}
for(const [n,S,j,expected] of [
 [8,0,0,'be74978a400ba2af9fbfffeda1fbf8f1229325069e2deafcfdcf01900b33818c'],
 [8,0,3,'31e5efefff7823e613878ff225a5f7fdbe0334b2e3d3089690314b9b95b29ad2']
]){
 const h=crypto.createHash('sha256').update(encode(n,S,[j])).digest('hex');
 if(h!==expected)throw Error('source SHA mismatch');
 count++;
}
console.log(JSON.stringify({independent_checks:count,exhaustive_n:[1,8],max_prefix_states:256}));
