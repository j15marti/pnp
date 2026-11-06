#!/usr/bin/env node
// LSPV-2/438: host-language reproduction, NOT a native FLMV-machine measurement.
import assert from 'node:assert/strict';
function edgeList(h){
  const e=[];
  if(h===4)for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)e.push([u,v]);
  if(h===8)for(let u=0;u<8;u++)for(let j=0;j<3;j++){
    const v=u^(1<<j);if(u<v)e.push([u,v]);
  }
  return e;
}
function template(h){
  const e=edgeList(h), w=Math.floor(Math.log2(e.length))+1;
  const adj=Array.from({length:h},()=>[]);
  e.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)});
  adj.forEach(a=>a.sort((x,y)=>x-y));return {e,w,adj};
}
function encoded(h,a,b,t){
  let out='1'.repeat(h)+'0';
  for(let half=0;half<2;half++)for(let v=0;v<h;v++)for(let r=0;r<2;r++){
    const charge=((half===0?a:b)>>v)&1;
    const signs=[half,r,half^r^1^charge];
    for(let j=0;j<3;j++)out+=t.adj[v][j].toString(2).padStart(t.w,'0')+signs[j];
  }
  return out;
}
function check(s,h,t){
  if(s.slice(0,h+1)!=='1'.repeat(h)+'0'||s.length!==h+1+12*h*(t.w+1))return 'MALFORMED';
  let p=0;
  for(let v=0;v<h;v++){
    let charge=null;
    for(let half=0;half<2;half++)for(let r=0;r<2;r++){
      const offset=h+1+(half*2*h+2*v+r)*3*(t.w+1), signs=[];
      for(let j=0;j<3;j++){
        const k=offset+j*(t.w+1), id=parseInt(s.slice(k,k+t.w),2);
        if(id<1||id>t.e.length)return 'MALFORMED';
        if(id!==t.adj[v][j])return 'OUT_OF_FAMILY';
        signs.push(Number(s[k+t.w]));
      }
      if(signs[0]!==half||signs[1]!==r)return 'OUT_OF_FAMILY';
      const c=signs[2]^half^r^1;
      if(charge===null)charge=c;else if(charge!==c)return 'OUT_OF_FAMILY';
    }
    p^=charge;
  }
  return p?'IN_FAMILY_UNSAT':'IN_FAMILY_SAT';
}
let tests=0;
for(const h of [4,8]){
  const t=template(h), lim=1<<h;
  for(let a=0;a<lim;a++)for(let b=0;b<lim;b++){
    const s=encoded(h,a,b,t);
    const expected=a===b?((a.toString(2).split('1').length-1)%2?'IN_FAMILY_UNSAT':'IN_FAMILY_SAT'):'OUT_OF_FAMILY';
    assert.equal(check(s,h,t),expected);tests++;
  }
  assert.equal(check(encoded(h,0,0,t)+'0',h,t),'MALFORMED');tests++;
}
console.log(JSON.stringify({status:'PASS',tests,scope:'K4 and cube exhaustive half-charge pairs'}));
