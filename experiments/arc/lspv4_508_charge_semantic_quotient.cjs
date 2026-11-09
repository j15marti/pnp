#!/usr/bin/env node
'use strict';
// LSPV-4/508: finite, hosted-language independent control, NOT native FLMV.
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
function graphs(){
  let K4=[],K33=[],Q3=[],Fano=[];
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
  for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
  for(let v=0;v<8;v++)for(let d of [1,2,4])if(v<(v^d))Q3.push([v,v^d]);
  for(let l=0;l<7;l++)for(let d of [0,1,3])Fano.push([(l+d)%7,l+7]);
  return [['K4',4,K4],['K3,3',6,K33],['Q3',8,Q3],['Heawood',14,Fano]];
}
const bit=(x,w)=>x.toString(2).padStart(w,'0');
function source(H,edges,mask){
  let es=edges.map(([a,b])=>[Math.min(a,b),Math.max(a,b)]).sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
  const m=es.length,w=Math.ceil(Math.log2(m+1)),adj=Array.from({length:H},()=>[]);
  assert.equal(m,3*H/2);
  es.forEach(([a,b],i)=>{adj[a].push(i+1);adj[b].push(i+1)});
  let s=bit(165,8)+bit(H,12)+bit(m,12),quartets=[];
  for(let v=0;v<H;v++){
    assert.equal(adj[v].length,3);
    const q=[],e=adj[v].sort((a,b)=>a-b);
    for(let t=0;t<8;t++){
      let sign=[t>>2,(t>>1)&1,t&1];
      if((sign[0]^sign[1]^sign[2])===((mask>>v)&1))continue;
      for(let j=0;j<3;j++){
        s+=bit(e[j],w);if(j===2)q.push(s.length);s+=String(sign[j]);
      }
    }
    assert.equal(q.length,4);quartets.push(q);
  }
  return {s,quartets,es};
}
function valid(H,edges,s){
  const anchor=source(H,edges,0);
  if(s.length!==anchor.s.length)return false;
  let mask=0;
  for(let v=0;v<H;v++){
    const b=s[anchor.quartets[v][0]];
    if(b!=='0'&&b!=='1')return false;
    if(b==='0')mask|=1<<v;
  }
  return source(H,edges,mask).s===s;
}
function xorSolves(H,es,charge){
  const m=es.length,rows=[];
  for(let v=0;v<H;v++){
    let row=0n;
    es.forEach(([a,b],i)=>{if(a===v||b===v)row^=1n<<BigInt(i)});
    rows.push(row|BigInt((charge>>v)&1)<<BigInt(m));
  }
  let pivotrow=0;
  for(let k=0;k<m;k++){
    let pivot=-1;
    for(let r=pivotrow;r<H;r++)if(((rows[r]>>BigInt(k))&1n)!==0n){pivot=r;break}
    if(pivot<0)continue;
    [rows[pivotrow],rows[pivot]]=[rows[pivot],rows[pivotrow]];
    for(let r=0;r<H;r++)if(r!==pivotrow&&((rows[r]>>BigInt(k))&1n)!==0n)rows[r]^=rows[pivotrow];
    pivotrow++;
  }
  let mask=(1n<<BigInt(m))-1n;
  return !rows.some(r=>(r&mask)===0n&&((r>>BigInt(m))&1n)===1n);
}
function pc(i){let r=0;while(i){r^=i&1;i>>>=1}return r}
function bdd(H){
  let current=Array.from({length:1<<H},(_,i)=>pc(i)),u=new Map(),count=0,levels=[];
  for(let d=H-1;d>=0;d--){
    const next=[];let created=0;
    for(let j=0;j<current.length;j+=2){
      const a=current[j],b=current[j+1];
      if(a===b){next.push(a);continue}
      const key=d+','+a+','+b;
      if(!u.has(key)){u.set(key,2+count++);created++}
      next.push(u.get(key));
    }
    current=next;levels[d]=created;
  }
  assert.equal(current.length,1);
  return {count,levels};
}
function main(){
  const rows=[];
  for(const [name,H,edges] of graphs()){
    const q=1<<H;let replay=0,observed=0,last=-1;
    for(let i=0;i<q;i++){
      const mask=i^(i>>1),v=pc(mask);
      assert.equal(v,i&1);
      if(last!==-1){const flip=mask^last;assert.equal(pc(flip),1);assert.equal(flip&(flip-1),0)}
      last=mask;
      const packet=source(H,edges,mask);
      if(i<128||H<=8)assert(valid(H,edges,packet.s));
      for(let j=0;j<H;j++){
        assert.equal(1-Number(packet.s[packet.quartets[j][0]]),(mask>>j)&1);observed++;
      }
      if(i<256||H<=8){assert.equal(xorSolves(H,packet.es,mask),v===0);replay++}
    }
    const {s,quartets}=source(H,edges,0),toggle=(t,j)=>t.slice(0,j)+(t[j]==='0'?'1':'0')+t.slice(j+1);
    assert(!valid(H,edges,s.slice(0,-1)));
    assert(!valid(H,edges,toggle(s,0)));
    assert(!valid(H,edges,toggle(s,quartets[0][0]+1)));
    const b=bdd(H);assert.equal(b.count,2*H-1);
    assert.deepEqual(b.levels,[1,...Array(H-1).fill(2)]);
    const sha={};
    for(let k of [0,1])sha[k]=crypto.createHash('sha256').update(source(H,edges,k).s).digest('hex');
    rows.push({name,H,m:edges.length,N:s.length,q,trie_nodes:2*q-1,
      minimal_OBDD_internal:b.count,minimal_OBDD_total:b.count+2,
      gf2_checks:replay,sign_checks:observed,gray_labels:q,sha});
  }
  return {status:'COMPUTATIONAL; restricted exact controls',passed:true,rows};
}
if(require.main===module)console.log(JSON.stringify(main(),null,2));
module.exports={main};
