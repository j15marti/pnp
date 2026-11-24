const experiment = function experiment(){
"use strict";
let seed=0x2010530;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
const parity=x=>{let p=0;while(x){p^=1;x&=x-1n;}return p;};
const tag=(x,obs)=>obs.reduce((s,w,i)=>s|(parity(x&w)<<i),0);
const assert=(b,m)=>{if(!b)throw Error(m)};
const stats={queries:0,rowsExamined:0,convolutions:0,cutTuples:0,closureRemovals:0};
function closure(blocks,K){
 if(K.some(k=>k<0n))return null;
 let a=blocks.map(b=>({...b,rows:b.rows.slice()})),changed=true;
 while(changed){
  if(a.some(b=>!b.rows.length))return null;
  changed=false;let mins=a.map(b=>b.owners.map((_,j)=>b.rows.reduce((m,r)=>m===null||r.c[j]<m?r.c[j]:m,null)));
  let totals=K.map(()=>0n);
  a.forEach((b,i)=>b.owners.forEach((o,j)=>totals[o]+=mins[i][j]));
  if(totals.some((v,i)=>v>K[i]))return null;
  a=a.map((b,i)=>{let rows=b.rows.filter(r=>b.owners.every((o,j)=>r.c[j]+totals[o]-mins[i][j]<=K[o]));
    if(rows.length!==b.rows.length){changed=true;stats.closureRemovals+=b.rows.length-rows.length;}return {...b,rows};});
 }
 return a;
}
function solve(blocks,K,obs){
 stats.queries++;const Q=1<<obs.length, B=blocks.length,O=K.length,N=B+O;
 const a=closure(blocks,K); if(!a)return Array(Q).fill(null);
 const ed=[];a.forEach((b,i)=>b.owners.forEach((o,j)=>ed.push({i,o,j,dom:[...new Set(b.rows.map(r=>r.c[j]))]})));
 ed.sort((x,y)=>y.dom.length-x.dom.length);let d=Array.from({length:N},(_,i)=>i);
 function find(i){while(d[i]!==i){d[i]=d[d[i]];i=d[i];}return i;}
 const adj=Array.from({length:N},()=>[]),cut=[];
 for(const e of ed){let u=find(e.i),v=find(B+e.o);
  if(u===v)cut.push(e);else{d[u]=v;adj[e.i].push({v:B+e.o,j:e.j});adj[B+e.o].push({v:e.i,j:e.j});}}
 const result=Array(Q).fill(null);const blank=()=>Array(Q).fill(null);
 function put(a,h,c,w){if(a[h]===null||c<a[h].c)a[h]={c,w};}
 function conv(a,b){let c=blank();for(let i=0;i<Q;i++)if(a[i])for(let j=0;j<Q;j++)if(b[j]){
   stats.convolutions++;put(c,i^j,a[i].c+b[j].c,a[i].w|b[j].w);}return c;}
 function branch(idx,rows,budget){
   if(idx<cut.length){const e=cut[idx];for(const v of e.dom){
     if(v>budget[e.o])continue;
     const rr=rows[e.i].filter(r=>r.c[e.j]===v);if(!rr.length)continue;
     let nr=rows.slice(),nk=budget.slice();nr[e.i]=rr;nk[e.o]-=v;branch(idx+1,nr,nk);
   }return;}
   stats.cutTuples++;let seen=new Set();
   function dfs(u,parent,pj){
     seen.add(u);const ch=adj[u].filter(e=>e.v!==parent).map(e=>({...e,msg:dfs(e.v,u,e.j)}));
     if(u>=B){let v=blank();v[0]={c:0n,w:0n};for(const e of ch)v=conv(v,e.msg);
       return v.map(x=>x&&x.c<=budget[u-B]?x:null);}
     let best=blank();
     for(const row of rows[u]){
       stats.rowsExamined++;let v=blank();v[tag(row.w,obs)]={c:0n,w:row.w};
       for(const e of ch){
         const valid=e.msg.map(x=>x&&x.c+row.c[e.j]<=budget[e.v-B]?{c:0n,w:x.w}:null);
         v=conv(v,valid);
       }
       for(let h=0;h<Q;h++)if(v[h])put(best,h,parent<0?0n:row.c[pj],v[h].w);
     }return best;
   }
   let total=blank();total[0]={c:0n,w:0n};
   for(let u=B;u<N;u++)if(!seen.has(u)){
     let v=dfs(u,-1,-1).map(x=>x?{c:0n,w:x.w}:null);total=conv(total,v);
   }
   for(let u=0;u<B;u++)if(!seen.has(u))total=conv(total,dfs(u,-1,-1));
   for(let h=0;h<Q;h++)if(total[h])result[h]=total[h].w;
 }
 branch(0,a.map(b=>b.rows),K.slice());return result;
}
function verify(blocks,K,w){
 let costs=K.map(()=>0n),all=0n;
 for(const b of blocks){let r=b.rows.find(r=>(w&b.mask)===r.w);if(!r)return false;
  all|=r.w;b.owners.forEach((o,j)=>costs[o]+=r.c[j]);}
 return all===w&&costs.every((c,i)=>c<=K[i]);
}
function brute(blocks,K){
 let out=[],cost=K.map(()=>0n);
 function rec(i,w){if(i===blocks.length){out.push(w);return;}
  const b=blocks[i];for(const r of b.rows){
    b.owners.forEach((o,j)=>cost[o]+=r.c[j]);if(cost.every((c,j)=>c<=K[j]))rec(i+1,w|r.w);
    b.owners.forEach((o,j)=>cost[o]-=r.c[j]);}}
 rec(0,0n);return out;
}
function block(owners,weights,offset,target=1){
 // physical multigraph: parallel edges, with the prescribed odd/even boundary.
 let rows=[],mask=0n;for(let i=0;i<owners.length;i++)mask|=1n<<BigInt(offset+i);
 let os=[...new Set(owners)];
 for(let bits=0;bits<1<<owners.length;bits++)if(parity(BigInt(bits))===target){
  let c=os.map(()=>0n);for(let j=0;j<owners.length;j++)if((bits>>j)&1)c[os.indexOf(owners[j])]+=weights[j];
  rows.push({c,w:BigInt(bits)<<BigInt(offset)});}
 return {owners:os,rows,mask};
}
function basis(n){
 let rows=Array(n).fill(0n);
 function reduce(x){for(let j=n-1;j>=0;j--)if(((x>>BigInt(j))&1n)&&rows[j])x^=rows[j];return x;}
 function add(x){x=reduce(x);if(!x)return false;let j=x.toString(2).length-1;rows[j]=x;return true;}
 function nulls(){let out=[];for(let j=0;j<n;j++)if(!rows[j]){
    let x=1n<<BigInt(j);for(let k=0;k<n;k++)if(rows[k]&&parity(x&rows[k]))x^=1n<<BigInt(k);out.push(x);}
  return out;}
 return {add,reduce,nulls,rank:()=>rows.filter(Boolean).length};
}
let tests={seed:"0x2010530",networks:0,forestNetworks:0,cyclicNetworks:0,sat:0,unsat:0,tagCells:0,witnessChecks:0,hullChecks:0,hullProbes:0,referenceFeasibleTuples:0,scaling:[],hostile:[]};
for(let rep=0;rep<180;rep++){
 let B=2+rand(5),O=1,off=0,blocks=[],cyclic=rep%3===0;
 for(let i=0;i<B;i++){
   let first=rand(O),other=O++;
   if(cyclic&&i>0&&i%2===1)other=rand(O-1);
   let owners=[first,other];if(rep%4===0)owners.push(first);
   let weights=owners.map(()=>BigInt(1+rand(12)));
   blocks.push(block(owners,weights,off,rand(2)));off+=owners.length;
 }
 let K=Array.from({length:O},()=>BigInt(rand(15)));
 let ref=brute(blocks,K);tests.referenceFeasibleTuples+=ref.length;
 tests.networks++;tests[cyclic?"cyclicNetworks":"forestNetworks"]++;tests[ref.length?"sat":"unsat"]++;
 for(let q=0;q<=2;q++){
  let obs=Array.from({length:q},()=>{let v=0n;for(let i=0;i<off;i++)if(rand(7)<3)v|=1n<<BigInt(i);return v;});
  let got=solve(blocks,K,obs);
  for(let h=0;h<got.length;h++){tests.tagCells++;
    assert((got[h]!==null)===ref.some(w=>tag(w,obs)===h),"tag cell");
    if(got[h]!==null){assert(verify(blocks,K,got[h])&&tag(got[h],obs)===h,"witness");tests.witnessChecks++;}
  }
 }
 if(ref.length){
  const a=solve(blocks,K,[])[0],W=basis(off),U=basis(off),R=basis(off);
  for(const w of ref)R.add(w^a);
  while(W.rank()+U.rank()<off){
    const p=W.nulls().find(x=>U.reduce(x)!==0n);assert(p!==undefined,"dual");
    const w=solve(blocks,K,[p])[1^parity(p&a)];tests.hullProbes++;
    if(w===null)assert(U.add(p),"identity");else{assert(verify(blocks,K,w)&&W.add(w^a),"new witness");tests.witnessChecks++;}
  }
  assert(W.rank()===R.rank()&&ref.every(w=>W.reduce(w^a)===0n),"hull");tests.hullChecks++;
 }
}
for(const h of [8,16,32,64,128,256]){
 const W=1n<<80n,blocks=Array.from({length:h},(_,i)=>block([i,i+1],[W,W],2*i));
 let K=Array(h+1).fill(W),start={...stats};
 let w=solve(blocks,K,[])[0];assert(w!==null&&verify(blocks,K,w),"scale SAT");
 let satRows=stats.rowsExamined-start.rowsExamined, satConv=stats.convolutions-start.convolutions;
 K[0]=K[h]=0n;let u=solve(blocks,K,[])[0];assert(u===null,"scale UNSAT");
 tests.scaling.push({blocks:h,owners:h+1,minorityEdgesBeforeClosure:h,weightBits:81,satRows,satConv,unsat:true});
}
{
 let blocks=Array.from({length:3},(_,i)=>block([0,1],[2n,2n],2*i));
 for(const K of [[3n,3n],[2n,4n]]){
  let w=solve(blocks,K,[])[0];assert((w!==null)===(K[0]===2n),"partition");
  if(w!==null)assert(verify(blocks,K,w),"partition witness");
  tests.hostile.push({budgets:K.map(String),sat:w!==null});
 }
 // same cost, different parity: retaining only one global cheapest row fails.
 let b=block([0,0],[1n,1n],0);
 let got=solve([b],[1n],[1n]);assert(got.every(x=>x!==null),"same-cost protected alternatives");
 tests.hostile.push({sameCostDifferentTag:true});
}
return {...tests,work:stats};
};
console.log(JSON.stringify(experiment(), null, 2));
