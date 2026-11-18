"use strict";
const beat=(a,b)=>[1,3].includes((b-a+5)%5);
const width=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
const bits=(x,w)=>Array.from({length:w},(_,i)=>(x>>i)&1).join("");
function encode(n,arcs) {
  arcs=[...arcs].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  return "1".repeat(n)+"0"+"1".repeat(arcs.length)+"0"+
    arcs.map(([u,v])=>bits(u,width(n))+bits(v,width(n))).join("");
}
function parse(s) {
  if(!s || /[^01]/.test(s)) throw Error("not binary");
  let i=0;
  function unary(){let j=i;while(i<s.length&&s[i]==="1")i++;if(i===s.length)throw Error("unterminated");let r=i-j;i++;return r}
  let n=unary(),m=unary(),w=width(n),arcs=[],previous=[-1,-1];
  if(s.length-i!==2*m*w)throw Error("wrong length");
  function num(){let z=0;for(let k=0;k<w;k++)z+=(s[i++]==="1")*2**k;return z}
  for(let e=0;e<m;e++) {let u=num(),v=num();
    if(u>=n||v>=n||u<previous[0]||(u===previous[0]&&v<=previous[1]))throw Error("noncanonical arc");
    arcs.push([u,v]);previous=[u,v];
  }
  return {n,arcs};
}
function count(n,arcs) {
  const S=new Set(arcs.map(x=>x.join(",")));
  for(const [u,v] of arcs)if(u===v||S.has(v+","+u))return {Z:0n,c:null,r:null,b:null};
  let p=Array.from({length:n},(_,i)=>i),tree=Array.from({length:n},()=>[]),chords=[];
  function find(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x}
  for(const [u,v] of arcs) {let a=find(u),b=find(v);
    if(a===b)chords.push([u,v]);else {p[a]=b;tree[u].push([v,1]);tree[v].push([u,0])}
  }
  const root=new Map();
  for(let v=0;v<n;v++)if(!root.has(find(v)))root.set(find(v),v);
  const boundarySet=new Set(chords.flat());
  for(const v of [...boundarySet].sort((a,b)=>a-b)){let c=find(v);
    if(!root.has("chord"+c)){root.set("chord"+c,v);root.set(c,v)}
  }
  const roots=[...root.entries()].filter(([k])=>typeof k==="number").map(([,v])=>v);
  const rootSet=new Set(roots);
  const boundary=[...boundarySet].filter(x=>!rootSet.has(x)).sort((a,b)=>a-b);
  const children=Array.from({length:n},()=>[]),visited=new Set(),order=[];
  for(const r of roots){let stack=[r];visited.add(r);
    while(stack.length){let v=stack.pop();order.push(v);
      for(const [u,d] of tree[v])if(!visited.has(u)){visited.add(u);children[v].push([u,d]);stack.push(u)}
    }
  }
  if(order.length!==n)throw Error("forest traversal");
  const pin=new Map(roots.map(v=>[v,0]));
  let rootedTotal=0n;
  function evaluate(k){
    if(k<boundary.length){for(let color=0;color<5;color++){pin.set(boundary[k],color);evaluate(k+1)}pin.delete(boundary[k]);return}
    for(const [u,v] of chords)if(!beat(pin.get(u),pin.get(v)))return;
    const dp=Array.from({length:n},()=>Array(5).fill(0n));
    for(const v of order.slice().reverse())for(let a=0;a<5;a++){
      if(pin.has(v)&&pin.get(v)!==a)continue;
      let mul=1n;
      for(const [u,d] of children[v]){let sum=0n;
        for(let b=0;b<5;b++)if(d?beat(a,b):beat(b,a))sum+=dp[u][b];
        mul*=sum;
      }dp[v][a]=mul;
    }
    let ways=1n;for(const r of roots)ways*=dp[r][0];rootedTotal+=ways;
  }
  evaluate(0);
  return {Z:5n**BigInt(roots.length)*rootedTotal,c:roots.length,r:chords.length,b:boundary.length};
}
function brute(n,arcs){
  let count=0n,colors=Array(n).fill(0);
  function go(i){if(i===n){if(arcs.every(([u,v])=>beat(colors[u],colors[v])))count++;return}
    for(let a=0;a<5;a++){colors[i]=a;go(i+1)}
  }go(0);return count;
}
function main(){
  let state=20261117,checks=0,cases=0,maxB=0,rMax=0;
  function rand(){state^=state<<13;state^=state>>>17;state^=state<<5;return(state>>>0)/4294967296}
  for(let n=0;n<=6;n++)for(let t=0;t<(n===6?18:70);t++){
    let arcs=[],p=[0.10,0.35,0.70,1][t%4];
    for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand()<p)
      arcs.push(rand()<.5?[u,v]:[v,u]);
    const src=encode(n,arcs),ob=parse(src),ans=count(ob.n,ob.arcs),truth=brute(n,arcs);
    if(ans.Z!==truth)throw Error("wrong count "+JSON.stringify({n,arcs}));
    checks++;
    if(ans.c!==null){if(ans.r!==arcs.length-n+ans.c||ans.b>Math.min(n,2*ans.r))throw Error("rank bound");
      if(ans.r===0&&ans.Z!==5n**BigInt(ans.c)*2n**BigInt(n-ans.c))throw Error("forest formula");
      checks+=2;maxB=Math.max(maxB,ans.b);rMax=Math.max(rMax,ans.r);}
    cases++;
  }
  let bad=0;for(const word of ["","111","2","000","001","101","01011"]){try{parse(word)}catch(e){bad++}}
  if(bad<5)throw Error("malformed rejection");
  return {revision:"tmr1-t5-feedback074-js1",seed:20261117,cases,checks,malformed_rejected:bad,max_boundary_exponent:maxB,max_cotree_rank:rMax,failures:0,scope:"COMPUTATIONAL exact check against independent brute force"};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(main()));
