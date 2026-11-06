// LSPV-1/451 standalone independent local-width-three XOR optimum check.
// Run: node experiments/arc/lspv1_451_x3c_3local_xor_selfcheck.mjs
// Node >=18, standard library only. This is NOT the historical R_mix341 checker.
"use strict";
let checks=0;
function assert(p,s){checks++;if(!p)throw Error(s);}
const count=n=>{let a=0;while(n){a+=n&1;n>>>=1;}return a;};
function gadget(q,sets){
  let r=3*q,L=q+1,V=2*r+1+r*L,rows=[],tags=[];
  let t=i=>r+i,z=(i,j)=>2*r+1+i*L+j;
  function add(tag,vars,b){let mask=0n;for(const v of vars)mask^=1n<<BigInt(v);rows.push([mask,b]);tags.push(tag);}
  add("start",[t(0)],0);
  for(let i=0;i<r;i++)add("chain"+i,[t(i),i,t(i+1)],0);
  add("end",[t(r)],1);
  sets.forEach((S,j)=>add("set"+j,S,0));
  for(let i=0;i<r;i++){
    add("fh"+i,[z(i,0)],0);
    for(let j=1;j<L;j++)add("fl"+i+"."+j,[z(i,j-1),z(i,j)],0);
    add("ft"+i,[z(i,L-1),i],0);
  }
  return {q,r,L,V,rows,tags,sets};
}
function best(g){
  let m=g.sets.length, all=(1<<g.r)-1,ans=[Infinity,null,null];
  for(let j=0;j<2**m;j++){
    let syn=0,used=[];
    for(let a=0;a<m;a++)if(j>>a&1){used.push(a);for(const i of g.sets[a])syn^=1<<i;}
    let miss=all^syn, cost=used.length+(g.L+1)*count(miss);
    if(cost<ans[0])ans=[cost,used,miss];
  }
  return {kappa:g.r+2+ans[0],selected:ans[1],missing:ans[2]};
}
function cover(g){
  let target=(1<<g.r)-1,m=g.sets.length;
  for(let mask=0;mask<2**m;mask++)if(count(mask)===g.q){
    let flags=0,repeat=false;
    for(let j=0;j<m;j++)if(mask>>j&1)for(const i of g.sets[j]){
      if(flags>>i&1)repeat=true;flags|=1<<i;
    }
    if(!repeat&&flags===target)return true;
  }
  return false;
}
function certificate(g,b){
  let used=new Set(["start","end"]);
  for(let i=0;i<g.r;i++)used.add("chain"+i);
  b.selected.forEach(i=>used.add("set"+i));
  for(let i=0;i<g.r;i++)if(b.missing>>i&1){
    used.add("fh"+i);used.add("ft"+i);
    for(let j=1;j<g.L;j++)used.add("fl"+i+"."+j);
  }
  let leaves=[];
  for(let j=0;j<g.tags.length;j++)if(used.has(g.tags[j]))leaves.push(j);
  let refs=leaves.map(i=>["s",i]),values=new Map();
  leaves.forEach(i=>values.set("s:"+i,g.rows[i]));
  let steps=[];
  while(refs.length>1){
    let next=[];
    for(let j=0;j<refs.length;j+=2){
      if(j+1===refs.length){next.push(refs[j]);continue;}
      let a=refs[j],d=refs[j+1],A=values.get(a.join(":")),D=values.get(d.join(":"));
      let val=[A[0]^D[0],A[1]^D[1]],id=["d",steps.length];
      steps.push({parents:[a,d],value:val});values.set(id.join(":"),val);next.push(id);
    }
    refs=next;
  }
  assert(leaves.length===b.kappa,"minimum support size");
  assert(steps.length===b.kappa-1,"exact paid steps");
  let root=values.get(refs[0].join(":"));
  assert(root[0]===0n&&root[1]===1,"correct contradictory root");
  for(let i=0;i<steps.length;i++){
    let v=steps[i],P=v.parents.map(([k,j])=>values.get(k+":"+j));
    assert((P[0][0]^P[1][0])===v.value[0]&&(P[0][1]^P[1][1])===v.value[1],"native XOR replay");
  }
  return steps.length;
}
function gauss(g){
  let piv=new Map();
  for(const [mask,rhs] of g.rows){
    let a=mask,b=rhs;
    while(a){
      let k=a.toString(2).length-1;
      if(!piv.has(k)){piv.set(k,[a,b]);a=-1n;break;}
      let p=piv.get(k);a^=p[0];b^=p[1];
    }
    if(a===0n&&b===1)return true;
  }
  return false;
}
function signed3(g){
  let clauses=[];
  for(const [mask,rhs] of g.rows){
    let cols=[];for(let i=0;i<g.V;i++)if(mask>>BigInt(i)&1n)cols.push(i+1);
    assert(cols.length>=1&&cols.length<=3,"source row arity <=3");
    for(let a=0;a<2**cols.length;a++)if(count(a)%2!==rhs)
      clauses.push(cols.map((col,j)=>a>>j&1?-col:col));
  }
  return clauses;
}
function cnfUnsat(clauses,n){
  for(let a=0;a<2**n;a++){
    let ok=true;
    for(const C of clauses)if(!C.some(l=>Boolean(a>>(Math.abs(l)-1)&1)===(l>0))){ok=false;break;}
    if(ok)return false;
  }
  return true;
}
let examples=[
  ["q1-none",1,[]],["q1-yes",1,[[0,1,2]]],
  ["q2-yes",2,[[0,1,2],[3,4,5]]],
  ["q2-no",2,[[0,1,2],[0,3,4],[1,3,5],[2,4,5]]]
];
let seed=451;
function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;}
let triples=[];
for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)for(let c=b+1;c<6;c++)triples.push([a,b,c]);
for(let k=0;k<200;k++){
  let n=Math.floor(random()*9),sets=[];
  for(let j=0;j<n;j++)sets.push(triples[Math.floor(random()*triples.length)]);
  examples.push(["q2-rand"+k,2,sets]);
}
let outputs=[];
for(const [label,q,sets] of examples){
  let g=gadget(q,sets),b=best(g),c=signed3(g);
  assert(gauss(g),"always UNSAT");assert((b.kappa<=g.r+2+q)===cover(g),"X3C iff optimum threshold");
  assert(c.length===g.r*(2*g.L+5)+4*sets.length+2,"exact CNF clause size");
  certificate(g,b);
  if(q===1){
    assert(cnfUnsat(c,g.V),"exhaustive CNF UNSAT");
    let brute=Infinity;
    for(let mask=0;mask<2**g.rows.length;mask++){
      if(count(mask)>=brute)continue;
      let a=0n,rhs=0;
      for(let i=0;i<g.rows.length;i++)if(mask>>i&1){a^=g.rows[i][0];rhs^=g.rows[i][1];}
      if(a===0n&&rhs===1)brute=count(mask);
    }
    assert(brute===b.kappa,"full source-subset minimum");
  }
  if(outputs.length<5)outputs.push({label,variables:g.V,rows:g.rows.length,clauses:c.length,paid_nodes:b.kappa-1,x3c:cover(g)});
}
console.log(JSON.stringify({label:"LSPV1_451_STANDALONE",cases:examples.length,assertions:checks,sample:outputs,status:"restricted XOR-only; not Rmix341"},null,2));
