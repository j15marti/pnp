#!/usr/bin/env node
// LSPV-1/393 independent no-import reproducer of source and SAT-neighbor claims.
'use strict';
const fs=require('fs'); const crypto=require('crypto');
const file=process.argv[2]||'results/raw/arc/2026-11-04_0900_LSPV1_CHARGE_COORDINATE393_raw.json';
const raw=JSON.parse(fs.readFileSync(file,'utf8'));
let checks=0;
const assert=(v,msg)=>{checks++; if(!v)throw Error(msg||('assert '+checks))};
const gamma=n=>{if(n<1)throw Error('gamma');let b=n.toString(2);return '0'.repeat(b.length-1)+b;};
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
function edges(n){
  let set=new Set(); const add=(a,b)=>{if(a>b)[a,b]=[b,a];set.add(a+','+b)};
  if(n===4){for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)add(a,b)}
  else{if(n<6||n%2)throw Error('n');let k=n/2;
    for(let i=0;i<k;i++){add(i,(i+1)%k);add(k+i,k+(i+1)%k);add(i,k+i)}}
  return [...set].map(x=>x.split(',').map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
}
function cnf(n,charge){
  let E=edges(n);let inc=Array.from({length:n},()=>[]);
  E.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
  inc.forEach(a=>a.sort((x,y)=>x-y));let C=[];
  for(let v=0;v<n;v++)for(let k=0;k<8;k++){
    let bits=[(k>>2)&1,(k>>1)&1,k&1];
    if(((bits[0]+bits[1]+bits[2])%2)!==charge[v])
      C.push(inc[v].map((id,j)=>[id, bits[j]===0]));
  }
  return {C,E};
}
function encode(c,v){
  let width=Math.floor(Math.log2(v+1))+1;
  return '1011'+gamma(v+1)+gamma(c.length+1)+
    c.map(cl=>gamma(cl.length+1)+cl.map(([id,sgn])=>
      Number(sgn)+id.toString(2).padStart(width,'0')).join('')).join('');
}
function enc1(n,b){return '1'+gamma(n+1)+String(b.reduce((a,x)=>a^x,0))+b.slice(1).join('')}
function good(C,mask){return C.every(cl=>cl.some(([id,sign])=>
  (Number(Boolean(mask&(1<<(id-1))))===Number(sign))))}
function models(C,v){let count=0;for(let mask=0;mask<(1<<v);mask++)if(good(C,mask))count++;return count}
function evalSpecial(y){
  let queried=new Set(); const read=i=>{queried.add(i);return y[i]};
  let first=read(0);if(first!=='1')return {lab:null,probes:queried.size};
  try{
    let i=1,z=0;while(read(i)==='0'){i++;z++;if(i>=y.length)throw Error('bad')};
    let b='1';i++;
    for(let j=0;j<z;j++){let q=read(i+j);if(q===undefined)throw Error('short');b+=q};i+=z;
    let n=parseInt(b,2)-1;
    if(!((n===4)||(n>=6&&n%2===0))||i+n!==y.length)return {lab:'M',probes:queried.size};
    return {lab:read(i)==='1'?'U':'S',probes:queried.size};
  }catch(e){return {lab:'M',probes:queried.size}}
}
assert(raw.result_id==='LSPV1_393','id');
let neighbors=0;
for (const row of raw.records){
  let n=row.h,b=Array.from({length:n},(_,i)=>i===0&&row.label==='odd'?1:0);
  let {C,E}=cnf(n,b);let c=encode(C,E.length), y=enc1(n,b);
  assert(row.e0_sha256===hash(c),'e0 bytes');
  assert(row.e1_sha256===hash(y),'e1 bytes');
  assert(c.length===row.e0_bits&&y.length===row.e1_bits,'length');
  assert(C.length===row.clauses,'clauses');
  assert(C.reduce((a,x)=>a+x.length,0)===row.signs,'literal occ');
  const out=evalSpecial(y);
  assert(out.lab===(row.label==='odd'?'U':'S'),'label');
  assert(out.probes===row.e1_probes,'probes');
  const count=models(C,E.length);assert(count===row.num_models,'models');
  for(let j=0;j<(1<<n);j++){
    const charges=Array.from({length:n},(_,i)=>(j>>i)&1);
    const yy=enc1(n,charges),o=evalSpecial(yy);
    assert(o.lab===(charges.reduce((a,x)=>a^x,0)?'U':'S'),'all charges');
  }
  if(row.label==='odd'){
    assert(count===0,'odd original models');
    for(let i=0;i<C.length;i++){
      let witness=-1;
      for(let mask=0;mask<(1<<E.length);mask++){
        if(!good([C[i]],mask)&&good(C.filter((_,j)=>j!==i),mask)){witness=mask;break;}
      }
      assert(witness>=0,'source essential');
      for(let j=0;j<C[i].length;j++){
        const copy=C.map(cl=>cl.map(t=>t.slice()));copy[i][j][1]=!copy[i][j][1];
        assert(good(copy,witness),'flipped literal SAT witness');neighbors++;
      }
    }
    assert(row.verified_single_sign_flip_SAT===12*n,'all flips count');
    assert(row.logical_node_min===4*n-1,'declared mixed minimum');
  }else assert(count===2**(E.length-n+1),'even affine model count');
}
assert(neighbors===raw.signed_neighbor_cases,'neighbor aggregate');
assert(raw.malformed_rejected===9,'negative controls metadata');
for(let n of [4,6,8,10]){
  let odd=[1,...Array(n-1).fill(0)],even=Array(n).fill(0);
  let u=evalSpecial(enc1(n,odd)),s=evalSpecial(enc1(n,even));
  assert(u.lab==='U'&&s.lab==='S','opposite label');
  assert(u.probes<enc1(n,odd).length&&s.probes<enc1(n,even).length,'unread body');
}
console.log(JSON.stringify({verifier:'independent-js',checks,neighbors,records:raw.records.length,passed:true}));
