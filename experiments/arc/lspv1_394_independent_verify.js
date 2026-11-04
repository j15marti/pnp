#!/usr/bin/env node
// LSPV-1/394 independent finite checker, no third-party modules.
// Usage: node lspv1_394_independent_verify.js result.json
const fs=require('fs');
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0;
const assert=(v,m)=>{checks++;if(!v)throw Error('CHECK '+checks+': '+m);};
const xor=xs=>xs.reduce((a,b)=>a^b,0);
const unpack=(n,k)=>Array.from({length:n},(_,j)=>(k>>j)&1);
const same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
function clauses(h,edges,charge){
  const out=[];
  for(let v=0;v<h;v++){
    const inc=[];
    edges.forEach(([a,b],j)=>{if(a===v||b===v)inc.push(j);});
    assert(inc.length===3,'not cubic');
    for(let mask=0;mask<8;mask++){
      const val=unpack(3,mask);
      if(xor(val)!==charge[v])out.push(inc.map((e,j)=>(val[j]?-1:1)*(e+1)));
    }
  }
  return out;
}
function countSat(F,n){
  let num=0;
  for(let mask=0;mask<2**n;mask++){
    let sat=true;
    for(const C of F){
      if(!C.some(lit=>(((mask>>(Math.abs(lit)-1))&1)===(lit>0?1:0)))){
        sat=false;break;
      }
    }
    if(sat)num++;
  }
  return num;
}
function encodeBlock(xs,g){
  const out=[];
  for(let j=0;j<xs.length;j+=g){const b=xs.slice(j,j+g);out.push(xor(b),...b.slice(1));}
  return out;
}
function decodeBlock(xs,g){
  const out=[];
  for(let j=0;j<xs.length;j+=g){const b=xs.slice(j,j+g);out.push(xor(b),...b.slice(1));}
  return out;
}
function popcount(n){let c=0;while(n){c+=n&1;n>>>=1;}return c;}
function minimumCover(edges,n){
  for(let k=0;k<=n;k++)for(let mask=0;mask<2**n;mask++){
    if(popcount(mask)!==k)continue;
    if(edges.every(edge=>edge.some(j=>(mask&(1<<j))!==0)))
      return [k,unpack(n,mask).flatMap((bit,j)=>bit?[j]:[])];
  }
  throw Error('no cover');
}
assert(data.result_id==='LSPV1_394_STAR_LOCALITY_QUERY_TRANSFER','id');
assert(data.graph_records.length===2,'graphs');
for(const record of data.graph_records){
  const {vertices:h,edge_list:es,model_count_by_charge_int:counts}=record;
  assert(h===4||h===6,'h');assert(counts.length===2**h,'charges');
  for(let idx=0;idx<2**h;idx++){
    const charge=unpack(h,idx);
    const F=clauses(h,es,charge);
    assert(F.length===4*h,'CNF clause count');
    const n=countSat(F,es.length);
    assert(n===counts[idx],'direct model count');
    assert(n===(xor(charge)?0:2**(es.length-h+1)),'parity label');
  }
  const center=record.center_charge;
  assert(xor(center)===1,'center odd');
  for(const grp of record.groups){
    const g=grp.group_size;
    assert(h%g===0,'block size');
    for(let idx=0;idx<2**h;idx++){
      const b=unpack(h,idx);
      const y=encodeBlock(b,g);
      assert(same(decodeBlock(y,g),b),'inverse');
      assert(xor(b)===xor(y.filter((_,j)=>j%g===0)),'label parity');
    }
    const root=encodeBlock(center,g);
    const diffs=[];
    for(let p=0;p<h;p++){
      const alt=[...center];alt[p]^=1;
      const leaf=encodeBlock(alt,g),edge=[];
      for(let j=0;j<h;j++)if(root[j]!==leaf[j])edge.push(j);
      diffs.push(edge);
    }
    assert(same(diffs,grp.neighbor_differences),'star edge list');
    const degree=Array.from({length:h},(_,j)=>diffs.filter(e=>e.includes(j)).length);
    assert(same(degree,grp.coordinate_degrees),'degrees');
    assert(Math.max(...degree)===grp.beta,'maximum influence');
    const [tau,best]=minimumCover(diffs,h);
    assert(tau===grp.minimum_star_hitting,'exact min hitting');
    assert(same(best,grp.star_hitting_positions),'cover tie break');
    assert(tau===h/g,'locality lower bound tight');
  }
}
assert(data.malformed_rejections.length===9,'malformed count');
console.log(JSON.stringify({independentChecks:checks,graphs:data.graph_records.length,
  malformedCases:9,verdict:'PASS'}));
