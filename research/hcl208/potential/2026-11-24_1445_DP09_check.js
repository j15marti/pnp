function checkDP09(){
 const R={cases:0,sat:0,unsat:0,assertions:0,closureScans:0,pins:0,leafRows:0,messages:0,pairAttempts:0,edgeQueries:0,referenceWords:0,rankCases:0,scales:[]};
 const assert=(x)=>{R.assertions++;if(!x)throw Error("assertion "+R.assertions)};
 let seed=2081445;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const bit=i=>1n<<BigInt(i), mask=vs=>vs.reduce((a,v)=>a|bit(v),0n);
 function clause(c){let vs=[...new Set(c.map(l=>Math.abs(l)-1))];return {vs,ok:x=>c.some(l=>Boolean(x&bit(Math.abs(l)-1))===(l>0))}}
 function solve(n,clauses,reference=true){
  const fs=clauses.map(clause);let seen=mask(fs.flatMap(f=>f.vs));
  for(let i=0;i<n;i++)if(!(seen&bit(i)))fs.push({vs:[i],ok:()=>true});
  if(fs.length<2)fs.push({vs:[],ok:()=>true});
  const pins=new Map();let changed=true,conflict=false;
  function rows(f){let a=[];for(let j=0;j<2**f.vs.length;j++){let x=0n;let good=true;for(let k=0;k<f.vs.length;k++){let v=f.vs[k],b=(j>>k)&1;if(pins.has(v)&&pins.get(v)!==b)good=false;if(b)x|=bit(v)}if(good&&f.ok(x))a.push(x)}return a}
  while(changed&&!conflict){changed=false;outer:for(const f of fs){R.closureScans++;let a=rows(f);if(!a.length){conflict=true;break}for(const v of f.vs)if(!pins.has(v)){let b=Boolean(a[0]&bit(v));if(a.every(x=>Boolean(x&bit(v))===b)){pins.set(v,+b);R.pins++;changed=true;break outer}}}}
  const ref=[];if(reference)for(let j=0;j<2**n;j++){R.referenceWords++;let x=BigInt(j);if(fs.every(f=>f.ok(x)))ref.push(x)}
  R.cases++;if(conflict){R.unsat++;if(reference)assert(ref.length===0);return {count:"0",peak:0,pairs:0,maxWidth:0}}
  const adj=fs.map(()=>[]);function link(a,b){adj[a].push(b);adj[b].push(a)}
  function tree(l,r){if(r-l===1)return l;let m=(l+r)>>1,a=tree(l,m),b=tree(m,r),u=adj.length;adj.push([]);link(u,a);link(u,b);return u}tree(0,fs.length);
  const sm=new Map(),tm=new Map();let peak=0,maxWidth=0,pa=R.pairAttempts;
  const key=(u,v)=>u+","+v;
  function scope(u,v){let k=key(u,v);if(sm.has(k))return sm.get(k);let s=u<fs.length?mask(fs[u].vs):adj[u].filter(a=>a!==v).reduce((x,a)=>x|scope(a,u),0n);sm.set(k,s);return s}
  function msg(u,v){let k=key(u,v);if(tm.has(k))return tm.get(k);let s=scope(u,v),b=s&scope(v,u),tab=new Map();let width=b.toString(2).replace(/0/g,"").length;maxWidth=Math.max(maxWidth,width);
   function put(x,c){let z=x&b,old=tab.get(z);if(old)old.c+=c;else tab.set(z,{x,c})}
   if(u<fs.length){for(const x of rows(fs[u])){R.leafRows++;put(x,1n)}}
   else {let nb=adj[u].filter(a=>a!==v);if(nb.length===1){for(const a of msg(nb[0],u).values()){R.pairAttempts++;put(a.x,a.c)}}else{let [l,r]=nb;let ov=scope(l,u)&scope(r,u);for(const a of msg(l,u).values())for(const c of msg(r,u).values()){R.pairAttempts++;if(((a.x^c.x)&ov)===0n)put(a.x|c.x,a.c*c.c)}}}
   assert(tab.size<=2**width);peak=Math.max(peak,tab.size);tm.set(k,tab);R.messages++;return tab
  }
  let total=null,witness=null;
  for(let u=0;u<adj.length;u++)for(const v of adj[u])if(u<v){let a=msg(u,v),b=msg(v,u),counts=new Map(),s=scope(u,v)&scope(v,u);let z=0n;for(const [k,x] of a){R.edgeQueries++;if(b.has(k)){let y=b.get(k),c=x.c*y.c;counts.set(k,c);z+=c;witness=x.x|y.x}}
   if(total===null)total=z;else assert(total===z);
   if(reference){let expected=new Map();for(const x of ref){let k=x&s;expected.set(k,(expected.get(k)||0n)+1n)}assert(expected.size===counts.size);for(const [k,c] of expected)assert(counts.get(k)===c)}
  }
  if(reference)assert(total===BigInt(ref.length));if(total>0n){R.sat++;assert(fs.every(f=>f.ok(witness)));for(const [v,b] of pins)assert(Boolean(witness&bit(v))===Boolean(b))}else R.unsat++;
  return {count:String(total),peak,pairs:R.pairAttempts-pa,maxWidth}
 }
 for(let m=0;m<256;m++){let cs=[];for(let j=0;j<8;j++)if(m>>j&1)cs.push([1,2,3].map((v,i)=>(j>>i&1)?v:-v));solve(3,cs)}
 const triples=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]], fano=triples.flatMap(t=>[t,t.map(x=>-x)]);assert(solve(7,fano).count==="0");for(let j=0;j<14;j++)assert(solve(7,fano.filter((_,i)=>i!==j)).count==="5");
 for(let i=0;i<80;i++){let n=4+rnd(4),cs=[];for(let j=0;j<4+rnd(13);j++){let v=new Set();while(v.size<3)v.add(1+rnd(n));cs.push([...v].map(x=>rnd(2)?x:-x))}solve(n,cs)}
 for(const n of [8,16,32,64,128]){for(const bad of [false,true]){let cs=[];for(let i=1;i<=n;i++){let j=i%n+1;cs.push(...(bad&&i===n?[[i,j],[-i,-j]]:[[-i,j],[i,-j]]))}let x=solve(n,cs,n<=8);assert(x.count===(bad?"0":"2"));R.scales.push({n,bad,...x})}}
 function basis(xs){let b=Array(8).fill(0);for(let x of xs){for(let i=7;i>=0;i--)if(x>>i&1){if(b[i])x^=b[i];else{b[i]=x;break}}}return b}
 const rank=x=>basis(x).filter(Boolean).length;
 function reduce(x,b){for(let i=7;i>=0;i--)if((x>>i&1)&&b[i])x^=b[i];return x}
 for(let j=0;j<500;j++){let A=Array.from({length:1+rnd(6)},()=>rnd(64)),B=Array.from({length:1+rnd(6)},()=>rnd(64)),H=Array.from({length:1+rnd(5)},()=>rnd(64));let a=rank(A),b=rank(B),p=rank(H),u=rank([...A,...B]),k=a+b-u;let ha=p+a-rank([...H,...A]),hb=p+b-rank([...H,...B]),hu=p+u-rank([...H,...A,...B]);let hbasis=basis(H),aq=A.map(x=>reduce(x,hbasis)),bq=B.map(x=>reduce(x,hbasis));let kp=rank(aq)+rank(bq)-rank([...aq,...bq]);assert(kp===k+hu-ha-hb);assert(p+kp>=k);assert((p+kp===k)===(ha===p&&hb===p));R.rankCases++}
 // Exhaustively verify both affine-guard labels on two independent NAE triples.
 let counts=[0,0];for(let x=0;x<64;x++){let a=x&7,b=x>>3;if(a!==0&&a!==7&&b!==0&&b!==7)counts[(x&1)^((x>>3)&1)]++}assert(counts[0]===18&&counts[1]===18);R.crossGuardCounts=counts;
 return R
}
console.log(JSON.stringify(checkDP09(),null,2));
