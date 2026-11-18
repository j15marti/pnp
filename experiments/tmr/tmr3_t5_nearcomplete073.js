/*
TMR-3/073: authenticated near-complete triple-incidence counter for T5.
Portable JavaScript (Node 18+). All inputs are explicit binary words.
All integer counts use BigInt. No graph/count oracle is assumed.
*/
"use strict";
const REV="tmr3-t5-nearcomplete073-js-v1", SEED=202611171724;
function choose(n,k) {
  if(k<0||k>n)return 0n; k=Math.min(k,n-k);
  let x=1n;for(let i=1;i<=k;i++)x=x*BigInt(n-k+i)/BigInt(i);
  return x;
}
function triples(k) {
  const out=[];for(let a=0;a<k;a++)for(let b=a+1;b<k;b++)
    for(let c=b+1;c<k;c++)out.push([a,b,c]);return out;
}
function little(v,w){let s="";for(let i=0;i<w;i++)s+=((v>>i)&1).toString();return s;}
function encode(n,arcs) {
  const w=Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
  return "1".repeat(n)+"0"+"1".repeat(arcs.length)+"0"+
         arcs.map(([a,b])=>little(a,w)+little(b,w)).join("");
}
function decode(bits) {
  if(typeof bits!=="string"||!/^[01]*$/.test(bits))throw Error("nonbinary");
  let p=0;
  function unary(){const s=p;while(p<bits.length&&bits[p]==="1")p++;
    if(p===bits.length)throw Error("delimiter");const v=p-s;p++;return v;}
  const n=unary(),m=unary(),w=Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
  if(bits.length-p!==2*w*m)throw Error("length");
  let arcs=[];for(let i=0;i<m;i++){
    const a=parseInt(bits.slice(p,p+w).split("").reverse().join(""),2);
    const b=parseInt(bits.slice(p+w,p+2*w).split("").reverse().join(""),2);
    p+=2*w;if(a>=n||b>=n)throw Error("endpoint");arcs.push([a,b]);
  }
  arcs=[...new Map(arcs.map(v=>[v.join(","),v])).values()];
  return {n,arcs};
}
function recognize(n,arcs) {
  const ins=Array(n).fill(0),outs=Array(n).fill(0);
  const parents=Array.from({length:n},()=>new Set());
  for(const [a,b] of arcs){if(a===b)return null;ins[b]++;outs[a]++;parents[b].add(a);}
  const H=[],L=[];
  for(let i=0;i<n;i++) {
    if(outs[i]>0&&ins[i]===0)H.push(i);
    else if(outs[i]===0&&ins[i]===3)L.push(i);
    else return null;
  }
  if(H.length<4)return null;
  const idx=new Map(H.map((h,i)=>[h,i])),seen=new Set();
  for(const v of L) {
    if(parents[v].size!==3)return null;
    const t=[...parents[v]].map(h=>idx.get(h));
    if(t.some(x=>x===undefined))return null;
    t.sort((a,b)=>a-b);const key=t.join(",");
    if(seen.has(key))return null;seen.add(key);
  }
  const missing=triples(H.length).filter(t=>!seen.has(t.join(",")));
  const U=new Set(missing.flat());
  if(U.size>=H.length)return null;
  return {k:H.length,missing};
}
function formula(k,missing) {
  const U=[...new Set(missing.flat())].sort((a,b)=>a-b),s=U.length,r=k-s;
  if(k<4||r<1)throw Error("outside-hub requirement");
  const imap=new Map(U.map((h,i)=>[h,i]));
  const holeMasks=missing.map(t=>t.reduce((v,h)=>v|(1<<imap.get(h)),0));
  // BigInt masks permit arbitrary s; Number mask loop is used only for s<=30.
  const m=Number(choose(k,3))-missing.length;
  let sum=0n;
  for(let mask=0n;mask<(1n<<BigInt(s));mask++) {
    let u=0;for(let i=0;i<s;i++)if((mask>>BigInt(i))&1n)u++;
    let f=0;
    for(const h of holeMasks){const v=mask&BigInt(h);if(v===0n||v===BigInt(h))f++;}
    for(let p=0;p<=r;p++) {
      const q=k-u-p;
      const e=Number(choose(u+p,3)+choose(q,3))-f;
      if(e<0)throw Error("negative exponent");
      sum+=choose(r,p)*(1n<<BigInt(e));
    }
  }
  return 5n*(sum-(1n<<BigInt(m)));
}
function forest(n,arcs) {
  const edges=new Set(arcs.map(v=>v.join(",")));
  if(arcs.some(([a,b])=>a===b||edges.has([b,a].join(","))))return 0n;
  const adj=Array.from({length:n},()=>[]);
  for(const [a,b] of arcs){adj[a].push([b,1]);adj[b].push([a,-1]);}
  const seen=new Set(),children=[],color=Array(n).fill(0);let c=0;
  for(let root=0;root<n;root++)if(!seen.has(root)) {
    c++;seen.add(root);const queue=[root];
    for(let i=0;i<queue.length;i++)for(const [v,sgn] of adj[queue[i]])
      if(!seen.has(v)){seen.add(v);children.push([queue[i],v,sgn]);queue.push(v);}
  }
  let total=0n;
  function visit(i) {
    if(i===children.length){if(arcs.every(([a,b])=>(color[b]-color[a]+5)%5===1||
                                 (color[b]-color[a]+5)%5===3))total++;return;}
    const [u,v,sgn]=children[i];
    for(const d of [1,3]){color[v]=((color[u]+sgn*d)%5+5)%5;visit(i+1);}
  }
  visit(0);return total*5n**BigInt(c);
}
function countSource(bits){
  const {n,arcs}=decode(bits),edges=new Set(arcs.map(v=>v.join(",")));
  if(arcs.some(([a,b])=>a===b||edges.has([b,a].join(","))))return {z:0n,method:"unsat"};
  const hit=recognize(n,arcs);
  if(hit)return {z:formula(hit.k,hit.missing),method:"nearcomplete",k:hit.k,d:hit.missing.length};
  return {z:forest(n,arcs),method:"forest"};
}
function incidence(k,missing) {
  const holes=new Set(missing.map(t=>t.join(","))),active=triples(k).filter(t=>!holes.has(t.join(",")));
  return {n:k+active.length,arcs:active.flatMap((t,j)=>t.map(a=>[a,k+j]))};
}
function independent(k,missing){
  const present=triples(k).filter(t=>!new Set(missing.map(h=>h.join(","))).has(t.join(",")));
  const col=Array(k).fill(0);let sum=0n;
  function search(i){
    if(i<k){for(let c=0;c<5;c++){col[i]=c;search(i+1);}return;}
    let prod=1n;
    for(const t of present){
      let n=0;for(let y=0;y<5;y++)if(t.every(v=>[1,3].includes((y-col[v]+5)%5)))n++;
      prod*=BigInt(n);if(prod===0n)break;
    }sum+=prod;
  }search(0);return sum;
}
function random(seed){let x=seed|0;return()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return(x>>>0)/4294967296;};}
function runAudit(){
  const rnd=random(SEED),cases=[];let checks=0;
  for(let k=4;k<=7;k++){
    const ts=triples(k);
    for(let rep=0;rep<(k<=6?12:4);rep++){
      const U=[...Array(k).keys()].filter(()=>rnd()<0.5);
      if(U.length===k)U.pop();
      const missing=ts.filter(t=>t.every(v=>U.includes(v))&&rnd()<0.5);
      const {n,arcs}=incidence(k,missing);
      const got=countSource(encode(n,arcs));
      if(got.method!=="nearcomplete"||got.z!==independent(k,missing))throw Error("nearcomplete mismatch");
      checks++;
    }
  }
  for(const k of [4,5,6,8,10,14]){
    const missing=k<=5?[]:[[0,1,2]];
    const {n,arcs}=incidence(k,missing),out=countSource(encode(n,arcs));
    if(out.method!=="nearcomplete")throw Error("not recognized");
    if(k<=6&&out.z!==independent(k,missing))throw Error("independent mismatch");
    cases.push({k,n,m:arcs.length,d:missing.length,z:out.z.toString()});
    checks++;
  }
  // Sparse 3-palette case: two edge triples with overlapping center hub.
  const E=[[0,1,2],[2,3,4]].flatMap((t,j)=>t.map(h=>[h,5+j]));
  const z=countSource(encode(7,E));
  if(z.z!==independent(5,triples(5).filter(t=>t.join(",")!=="0,1,2"&&t.join(",")!=="2,3,4")))
    throw Error("sparse reference mismatch");
  const col=[0,2,2,4,4];
  for(const t of [[0,1,2],[2,3,4]])
    if(![0,1,2,3,4].some(y=>t.every(v=>[1,3].includes((y-col[v]+5)%5))))
      throw Error("sparse 3-palette witness failed");
  checks+=3;
  for(let n=1;n<=6;n++)for(let z=0;z<6;z++){
    const edges=[];for(let a=0;a<n;a++)for(let b=0;b<n;b++)
      if(a!==b&&rnd()<0.16)edges.push([a,b]);
    const got=countSource(encode(n,edges));const reference=independentGraph(n,edges);
    if(got.z!==reference)throw Error("all-input mismatch");checks++;
  }
  return {revision:REV,seed:SEED,checks,failures:0,cases};
}
function independentGraph(n,edges){
  let sum=0n;const a=Array(n).fill(0);
  function dfs(i){if(i===n){if(edges.every(([u,v])=>[1,3].includes((a[v]-a[u]+5)%5)))sum++;return;}
    for(let c=0;c<5;c++){a[i]=c;dfs(i+1);}}dfs(0);return sum;
}
if(typeof process!=="undefined"&&process.argv&&process.argv[1]&&
   process.argv[1].includes("tmr3_t5_nearcomplete073"))
   console.log(JSON.stringify(runAudit()));
