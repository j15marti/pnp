'use strict';
// TMR-4/092 standalone BigInt verification of original five-way state compiler.
// Node.js 20+. Run: node experiments/tmr/tmr4_t5_grid092_standalone.js
// Proven all-order bound is in research/agents/tmr-4/*GRID_OBDD_BARRIER092.md.
const assert=require('assert');
const R=(a,b)=>[1,3].includes((b-a+5)%5);
const OUT=Array.from({length:5},(_,a)=>[0,1,2,3,4].reduce((s,b)=>s|(R(a,b)?1<<b:0),0));
const IN=Array.from({length:5},(_,a)=>[0,1,2,3,4].reduce((s,b)=>s|(R(b,a)?1<<b:0),0));
function grid(r){
  const arcs=[];
  for(let i=0;i<r;i++)for(let j=0;j<r;j++){
    const u=i*r+j;
    for(const [di,dj] of [[1,0],[0,1]]){
      if(i+di===r||j+dj===r)continue;
      const v=(i+di)*r+j+dj;
      arcs.push((i+j)%2===0?[u,v]:[v,u]);
    }
  }
  arcs.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
  return {n:r*r,arcs};
}
function adjacency(g){
  const out=Array.from({length:g.n},()=>[]);
  const inc=Array.from({length:g.n},()=>[]);
  for(const [u,v] of g.arcs){out[u].push(v);inc[v].push(u)}
  return {out,inc};
}
function initial(n){return String.fromCharCode(...Array(n).fill(96))}
function transition(state,v,a,out,inc){
  if(state==='!')return '!';
  const q=state.charCodeAt(v)-65;
  if(!(q&(1<<a)))return '!';
  const masks=Array.from(state,x=>x.charCodeAt(0)-65);
  masks[v]=0;
  for(const w of out[v])if(masks[w]){
    masks[w]&=OUT[a];
    if(!masks[w])return '!';
  }
  for(const u of inc[v])if(masks[u]){
    masks[u]&=IN[a];
    if(!masks[u])return '!';
  }
  return String.fromCharCode(...masks.map(x=>65+x));
}
function compile(g){
  const {out,inc}=adjacency(g);
  let states=new Map([[initial(g.n),1n]]);
  let width=0,nodes=0,transitions=0;
  for(let v=0;v<g.n;v++){
    width=Math.max(width,states.size);
    nodes+=states.size;transitions+=5*states.size;
    let next=new Map();
    for(const [state,mult] of states)
      for(let a=0;a<5;a++){
        const nxt=transition(state,v,a,out,inc);
        next.set(nxt,(next.get(nxt)||0n)+mult);
      }
    const total=[...next.values()].reduce((a,b)=>a+b,0n);
    assert.equal(total,5n**BigInt(v+1),'prefix counts');
    states=next;
  }
  const accepted=[...states].filter(([s])=>s!=='!').reduce((a,[,m])=>a+m,0n);
  const rejected=states.get('!')||0n;
  assert.equal(accepted+rejected,5n**BigInt(g.n));
  return {width,nodes,transitions,accepted:accepted.toString(),rejected:rejected.toString()};
}
function pointwise(g,col){
  const {out,inc}=adjacency(g);let state=initial(g.n);
  for(let v=0;v<g.n;v++)state=transition(state,v,col[v],out,inc);
  return state!=='!';
}
function direct(g,col){return g.arcs.every(([u,v])=>R(col[u],col[v]))}
let tests=0;const results=[];
const maxR=Math.min(10,Math.max(2,Number(process.env.MAX_GRID||8)));
for(let r=2;r<=maxR;r++){
  const g=grid(r);const comp=compile(g);
  const limit=r<=3?5**g.n:1200;
  let seed=9327+r;
  for(let z=0;z<limit;z++){
    const colors=[];
    if(r<=3){
      let t=z;for(let i=0;i<g.n;i++){colors.push(t%5);t=Math.floor(t/5)}
    }else{
      for(let i=0;i<g.n;i++){
        seed=(Math.imul(seed,1664525)+1013904223)>>>0;
        colors.push(seed%5);
      }
    }
    assert.equal(pointwise(g,colors),direct(g,colors),'original source mismatch');
    tests++;
  }
  results.push({r,n:g.n,m:g.arcs.length,...comp});
}
console.log(JSON.stringify({results,pointwise_tests:tests,unexpected_failures:0}));
