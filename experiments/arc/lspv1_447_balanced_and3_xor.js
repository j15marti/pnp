#!/usr/bin/env node
/* Compact independent 447 generator/check: historical-declared local AND3/XOR
   semantics only, not an accepted-byte R_mix341 proof format. */
const assert=require('assert');
const xor=a=>a.reduce((s,v)=>s^v,0);
const falsify=(vs,b)=>vs.map((v,i)=>b[i]?-v:v);
const clOK=(cl,a)=>cl.some(l=>a[Math.abs(l)]===(l>0?1:0));
function check(k,odd){
  const c=Array.from({length:k},(_,i)=>i+1),g=Array.from({length:k-1},(_,i)=>k+i+1);
  let next=2*k,groups=[];
  function pack(v,sign,kind){
    const p=next++,q=next++;let clause=[];
    for(let sp of [1,-1])for(let sq of [1,-1])clause.push([sign?v:-v,sp*p,sq*q]);
    groups.push({kind,clauses:clause,scope:[v,p,q],vars:[v],rhs:sign?1:0});
  }
  for(let i=0;i<k;i++)pack(c[i],odd&&i===0?'yes':false,'input');
  for(let i=0;i<k-1;i++){
    let vs=[i?g[i-1]:c[0],c[i+1],g[i]];
    let clauses=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let z=0;z<2;z++)
      if((a^b^z)===1)clauses.push(falsify(vs,[a,b,z]));
    groups.push({kind:'xor',clauses,scope:vs,vars:vs,rhs:0});
  }
  pack(g.at(-1),false,'output');
  assert.equal(groups.length,2*k);assert.equal(next-1,4*k+1);
  let rows=[],source=0;
  for(const group of groups){
    const vs=group.scope;assert.equal(new Set(vs).size,3);
    assert.equal(group.clauses.length,4);
    for(let mask=0;mask<8;mask++){
      const a={};vs.forEach((v,i)=>a[v]=(mask>>i)&1);
      const conj=group.clauses.every(cl=>clOK(cl,a));
      const row=xor(group.vars.map(v=>a[v]))===group.rhs;
      assert.equal(conj,row,'AND3 4-clause local factor exactly equals affine row');
    }
    source+=4; rows.push({vs:new Set(group.vars),rhs:group.rhs,d:2});
  }
  let paid=groups.length*3;
  while(rows.length>1){
    const newRows=[];
    for(let i=0;i<rows.length;i+=2){
      if(i+1===rows.length){newRows.push(rows[i]);continue;}
      const a=rows[i],b=rows[i+1],vs=new Set(a.vs);
      for(const v of b.vs)if(vs.has(v))vs.delete(v);else vs.add(v);
      newRows.push({vs,rhs:a.rhs^b.rhs,d:1+Math.max(a.d,b.d)});paid++;
    }rows=newRows;
  }
  assert.equal(source,8*k);assert.equal(paid,8*k-1);
  assert.equal(rows[0].vs.size,0);assert.equal(rows[0].rhs,odd?1:0);
  const lower=Math.ceil(Math.log2(5*k+3)),span=rows[0].d;
  assert(span<=2+Math.ceil(Math.log2(2*k)));
  if(odd){assert(span>=lower&&span<=lower+1);if((k&(k-1))===0)assert.equal(span,lower)}
  return {k,odd,proper3clauses:source,originalVars:next-1,paid,span,lower:odd?lower:null,root:odd?'0=1':'0=0'};
}
const results=[];for(let k of [2,3,4,5,8,16,32])for(let odd of [false,true])results.push(check(k,odd));
console.log(JSON.stringify({status:'restricted declared R_mix341 semantics; B3 and P vs NP OPEN',results},null,2));
