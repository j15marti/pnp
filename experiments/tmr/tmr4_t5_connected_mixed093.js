'use strict';
// TMR-4/093: original-source connected mixed T5-CSP standalone verifier, Node 18+.
// Run: node experiments/tmr/tmr4_t5_connected_mixed093.js
const assert=require('node:assert/strict'),crypto=require('node:crypto');
const R=(a,b)=>((b-a+5)%5===1)||((b-a+5)%5===3);
const OUT=Array.from({length:5},(_,a)=>Array.from({length:5},(_,b)=>R(a,b)?1<<b:0).reduce((x,y)=>x|y,0));
const IN=Array.from({length:5},(_,a)=>Array.from({length:5},(_,b)=>R(b,a)?1<<b:0).reduce((x,y)=>x|y,0));
function source(r,unsat) {
  let arcs=[];
  for(let i=0;i<r;i++)for(let j=0;j<r;j++){
    const u=i*r+j;
    for(const [di,dj] of [[0,1],[1,0]]){
      if(i+di>=r||j+dj>=r)continue;
      let v=(i+di)*r+j+dj;
      arcs.push((i+j)%2===0?[u,v]:[v,u]);
    }
  }
  let w=Array.from({length:r*r},(_,v)=>v).find(v=>(Math.floor(v/r)+v%r)%2===1);
  arcs.push([w,r*r]);if(unsat)arcs.push([r*r,w]);
  arcs.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  return {n:r*r+1,arcs};
}
function canonical(g){
  assert(Number.isInteger(g.n)&&g.n>0);
  let prev=[-1,-1];
  for(const [u,v] of g.arcs){
    assert(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<g.n&&v<g.n&&u!==v);
    assert(u>prev[0]||(u===prev[0]&&v>prev[1]));prev=[u,v];
  }
  return JSON.stringify({arcs:g.arcs,n:g.n})+'\n';
}
const digest=g=>crypto.createHash('sha256').update(canonical(g)).digest('hex');
function adjacency(g){
  let out=Array.from({length:g.n},()=>[]),inc=Array.from({length:g.n},()=>[]);
  for(const [u,v] of g.arcs){out[u].push(v);inc[v].push(u)}
  return {out,inc};
}
function transition(s,v,a,adj){
  if(s==='!'||!(s[v]&(1<<a)))return '!';
  let t=s.slice();t[v]=0;
  for(const w of adj.out[v])if(t[w]){t[w]&=OUT[a];if(!t[w])return '!'}
  for(const u of adj.inc[v])if(t[u]){t[u]&=IN[a];if(!t[u])return '!'}
  return t;
}
const key=s=>s==='!'?'!':s.map(x=>String.fromCharCode(65+x)).join('');
const unkey=s=>s==='!'?'!':[...s].map(c=>c.charCodeAt(0)-65);
function compile(g){
  const adj=adjacency(g);let layer=new Map([[key(Array(g.n).fill(31)),1n]]);
  let width=0,nodes=0;
  for(let v=0;v<g.n;v++){
    width=Math.max(width,layer.size);nodes+=layer.size;
    let next=new Map();
    for(const [k,num] of layer)for(let a=0;a<5;a++){
      const z=key(transition(unkey(k),v,a,adj));
      next.set(z,(next.get(z)||0n)+num);
    }
    layer=next;
    assert.equal([...layer.values()].reduce((a,b)=>a+b,0n),5n**BigInt(v+1));
  }
  const rejected=layer.get('!')||0n;
  const accepted=5n**BigInt(g.n)-rejected;
  return {accepted:accepted.toString(),rejected:rejected.toString(),width,nodes};
}
function direct(g,a){return g.arcs.every(([u,v])=>R(a[u],a[v]))}
function runOne(g,a){
  const adj=adjacency(g);let s=Array(g.n).fill(31);
  for(let v=0;v<g.n;v++){s=transition(s,v,a[v],adj);if(s==='!')return false}
  return true;
}
function mismatch(v,c){return [0,1,2].map(b=>(c&(1<<b))?-(3*v+b+1):(3*v+b+1))}
function buildCNF(g){
  let c=[];for(let v=0;v<g.n;v++)for(let z=5;z<8;z++)c.push(mismatch(v,z));
  for(const [u,v] of g.arcs)for(let a=0;a<5;a++)for(let b=0;b<5;b++)
    if(!R(a,b))c.push([...mismatch(u,a),...mismatch(v,b)]);
  assert.equal(c.length,3*g.n+15*g.arcs.length);return c;
}
function cnfEval(codes,clauses){
  const bits=codes.flatMap(c=>[c&1,(c>>1)&1,(c>>2)&1]);
  return clauses.every(cl=>cl.some(z=>bits[Math.abs(z)-1]===Number(z>0)));
}
let seed=93093;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
const gates={sources:0,pointwise:0,cnf:0,invalid:0,domain:0,matchingChecks:0};
for(let rev of [false,true])for(let X=0;X<32;X++)for(let Y=0;Y<32;Y++){
  let a=0,b=0,A=0,B=0;const rel=rev?(p,q)=>R(q,p):R;
  for(let p=0;p<5;p++)for(let q=0;q<5;q++)if(X&(1<<p)&&Y&(1<<q)&&rel(p,q)){a|=1<<p;b|=1<<q}
  for(let p=0;p<8;p++)for(let q=0;q<8;q++)
    if(p<5&&q<5&&X&(1<<p)&&Y&(1<<q)&&rel(p,q)){A|=1<<p;B|=1<<q}
  assert.equal(a,A);assert.equal(b,B);gates.domain++;
}
let report=[];
for(let r=2;r<=7;r++){
  let pair=[];
  for(let unsat of [false,true]){
    const g=source(r,unsat),sha=digest(g);gates.sources++;
    const c=compile(g);if(unsat)assert.equal(c.accepted,'0');
    const samples=r===2?5**g.n:1000;
    for(let i=0;i<samples;i++){
      let a;
      if(r===2){let t=i;a=Array.from({length:g.n},()=>{let z=t%5;t=Math.floor(t/5);return z})}
      else a=Array.from({length:g.n},()=>rand()%5);
      assert.equal(runOne(g,a),direct(g,a));gates.pointwise++;
    }
    if(r<=5){
      const cnf=buildCNF(g);
      for(let i=0;i<250;i++){
        const code=Array.from({length:g.n},()=>rand()%(i%2?8:5));
        assert.equal(cnfEval(code,cnf),code.every(x=>x<5)&&direct(g,code));
        gates.cnf++;if(code.some(x=>x>=5))gates.invalid++;
      }
    }
    pair.push({status:unsat?'UNSAT':'SAT',sha256:sha,...c});
  }
  assert.equal(BigInt(pair[0].accepted)%2n,0n);
  report.push({r,pair});
}
console.log(JSON.stringify({gates,report,unexpected_failures:0}));
