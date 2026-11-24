const run = function run(){
 let seed=15112026; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const stats={assertions:0,moments:0,transitions:0,peakKeys:0,closurePins:0,closureScans:0,creditCalls:0,rankCases:0,greedyOptima:0,randomSAT:0,randomUNSAT:0,certSAT:0,certUNSAT:0,unknown:0,lifts:0,scales:[]};
 const ck=(v,msg)=>{stats.assertions++;if(!v)throw Error(msg)};
 const bit=i=>1n<<BigInt(i), hi=x=>x.toString(2).length-1;
 const par=x=>{let r=0;while(x){r^=1;x&=x-1n}return r};
 const red=(x,B)=>{let t=0n;for(const [p,r,a] of B)if(x&bit(p)){x^=r;t^=a}return [x,t]};
 const ins=(B,x,t=0n)=>{let [r,a]=red(x,B);if(!r)return false;B.push([hi(r),r,t^a]);B.sort((a,b)=>b[0]-a[0]);return true};
 const bas=rs=>{let B=[];for(const r of rs)ins(B,r);return B};
 const rank=rs=>bas(rs).length;
 const has=(B,r)=>red(r,B)[0]===0n;
 const width=rs=>{let r=rank(rs),w=0;for(let j=0;j<=rs.length;j++)w=Math.max(w,rank(rs.slice(0,j))+rank(rs.slice(j))-r);return w};
 const guard=pins=>{let B=[];for(const [r,v] of pins){let [a,b]=red(r,B);if(!a){if(Number(b)!==v)return null}else ins(B,r,BigInt(v))}return B};
 const eligible=(r,rows,V)=>has(V,r)&&(rows.includes(r)||Array.from({length:rows.length+1},(_,j)=>has(bas(rows.slice(0,j)),r)||has(bas(rows.slice(j)),r)).every(Boolean));
 function choose(events,n){
  const rows=events.map(e=>e.rows),vs=rows.map(bas),pool=[...new Set(rows.flat().filter(Boolean))];
  const items=pool.map(r=>({r,s:rows.map((a,i)=>eligible(r,a,vs[i]))}));
  items.sort((a,b)=>b.s.filter(Boolean).length-a.s.filter(Boolean).length||(a.r<b.r?-1:1));
  let B=[],chosen=[];for(const it of items)if(ins(B,it.r))chosen.push(it);
  const D=vs.map((v,i)=>v.length-chosen.filter(a=>a.s[i]).length);
  return {items,chosen,D,r:B.length};
 }
 function chartCount(n,G,h){if(!G)return 0n;let [r,t]=red(h,G);return r?0n:(t?-1n:1n)*bit(n-G.length)}
 // Deterministic XOR-state monitor with explicit output truth table.
 const bad=(e,x)=>{let s=0;for(let j=0;j<e.rows.length;j++)if(par(e.rows[j]&x))s^=e.labels[j];return e.bad[s]};
 function moment(e,n,G,h){
  stats.moments++;if(!G)return 0n;
  const [hh,hs]=red(h,G), rr=e.rows.map(r=>red(r,G)), B=[],deps=[];
  rr.forEach(([r],j)=>{let [a,b]=red(r,B);if(a)ins(B,r,bit(j));else deps.push(b^bit(j))});
  let [remain,lambda]=red(hh,B);if(remain)return 0n;
  let cols=rr.map((_,j)=>deps.reduce((v,d,k)=>v|((d&bit(j))?bit(k):0n),0n));
  let suf=Array(cols.length+1);suf[cols.length]=[];
  for(let j=cols.length-1;j>=0;j--){suf[j]=suf[j+1].slice();ins(suf[j],cols[j])}
  // syndrome -> array of signed automaton state weights
  let M=new Map([[0n,Array.from({length:e.bad.length},(_,i)=>i===0?1n:0n)]]);
  for(let j=0;j<cols.length;j++){
   const N=new Map();for(const [p,arr] of M)for(let v=0;v<2;v++){
    stats.transitions++;const q=p^(v?cols[j]:0n);if(!has(suf[j+1],q))continue;
    let a=N.get(q);if(!a){a=Array(e.bad.length).fill(0n);N.set(q,a)}
    const delta=(v^Number(rr[j][1]))?e.labels[j]:0,sgn=v&&(lambda&bit(j))?-1n:1n;
    for(let s=0;s<arr.length;s++)a[s^delta]+=sgn*arr[s];
   }
   M=N;stats.peakKeys=Math.max(stats.peakKeys,M.size);
  }
  let v=(M.get(0n)||[]).reduce((a,x,s)=>a+(e.bad[s]?x:0n),0n);
  return (hs?-v:v)*bit(n-G.length-B.length);
 }
 const ref=(e,n,pins,h)=>{let s=0n;for(let x=0n;x<bit(n);x++)if(pins.every(([r,v])=>par(r&x)===v)&&bad(e,x))s+=par(h&x)?-1n:1n;return s};
 function close(events,n,pins,lib){
  while(true){stats.closureScans++;let G=guard(pins);if(!G)return null;let total=chartCount(n,G,0n);
   if(events.some(e=>moment(e,n,G,0n)===total))return null;
   let changed=false;for(const r of lib){if(has(G,r))continue;
    for(let v=0;v<2;v++){let g=guard([...pins,[r,v]]),sz=chartCount(n,g,0n);
     if(events.some(e=>moment(e,n,g,0n)===sz)){pins.push([r,1-v]);stats.closurePins++;changed=true;break}}
    if(changed)break;
   }if(!changed)return G;
  }
 }
 function solve(events,n,features){
  const b=choose(events,n),lib=b.chosen.map(a=>a.r),pins=[];let G=close(events,n,pins,lib);
  if(!G)return {label:"UNSAT",D:b.D};
  let D=chartCount(n,G,0n),a=features.map(h=>events.reduce((s,e)=>s+moment(e,n,G,h),0n));
  // One edge, two events. Fixed pointwise PSD lower credit, scaled by 2 D^2.
  function credit(g){stats.creditCalls++;if(!g)return 0n;let tot=chartCount(n,g,0n),m=events.reduce((s,e)=>s+moment(e,n,g,0n),0n);
   let c=2n*D*D*(tot-m)-D*D*m;
   for(let j=0;j<a.length;j++)if(a[j]){
    c+=2n*D*a[j]*events.reduce((s,e)=>s+moment(e,n,g,features[j]),0n);
    for(let k=0;k<a.length;k++)if(a[k])c-=a[j]*a[k]*chartCount(n,g,features[j]^features[k]);
   }return c;
  }
  let root=credit(G),rootDen=2n*D*D*D;
  if(root<=0n)return {label:"UNKNOWN",D:b.D,credit:Number(root)/Number(rootDen)};
  let maxw=0;
  for(const r of lib){G=close(events,n,pins,lib);ck(G&&credit(G)>0n,"closure credit");
   for(let i=0;i<events.length;i++){let w=width(events[i].rows.map(r=>red(r,G)[0]));maxw=Math.max(maxw,w);ck(w<=width(events[i].rows)+b.D[i],"lift width")}
   if(has(G,r))continue;
   const g0=guard([...pins,[r,0]]);pins.push([r,credit(g0)>0n?0:1]);
  }
  G=close(events,n,pins,lib);ck(G&&credit(G)>0n,"leaf credit");
  // Solve triangular system, unobserved/free coordinates =0.
  let x=0n;for(const [p,r,t] of G.slice().reverse())if(par(r&x)!==Number(t))x^=bit(p);
  ck(pins.every(([r,v])=>par(r&x)===v)&&events.every(e=>!bad(e,x)),"source witness");
  stats.lifts++;return {label:"SAT",D:b.D,credit:Number(root)/Number(rootDen),maxw,x:x.toString()};
 }
 // General rank law and safe-basis deficiency, with random arbitrary extra guards.
 for(let t=0;t<120;t++){
  let n=3+rnd(4),events=Array.from({length:2+rnd(2)},()=>({rows:Array.from({length:2+rnd(4)},()=>BigInt(1+rnd((1<<n)-1)))}));
  let b=choose(events,n),selected=b.chosen.filter(()=>rnd(2)).map(a=>a.r),extra=Array.from({length:rnd(3)},()=>BigInt(rnd(1<<n)));
  let U=bas([...selected,...extra]),p=U.length-rank(selected);
  for(let i=0;i<events.length;i++){
   let rows=events[i].rows,V=bas(rows),Ur=U.map(a=>a[1]),u=V.length+U.length-rank([...rows,...Ur]);
   let w=width(rows);ck(width(rows.map(r=>red(r,U)[0]))<=w+b.D[i]+p,"deficiency bound");
   for(let j=0;j<=rows.length;j++){let L=rows.slice(0,j),R=rows.slice(j),a=rank(L)+U.length-rank([...L,...Ur]),c=rank(R)+U.length-rank([...R,...Ur]);
    let wp=rank(L.map(r=>red(r,U)[0]))+rank(R.map(r=>red(r,U)[0]))-rank(rows.map(r=>red(r,U)[0]));
    ck(wp===rank(L)+rank(R)-V.length+u-a-c,"rank identity");
   }
  }stats.rankCases++;
  if(b.items.length<=12){
   let best=-1;for(let mask=0;mask<(1<<b.items.length);mask++){
    let q=b.items.filter((_,j)=>(mask>>j)&1);if(q.length===b.r&&rank(q.map(a=>a.r))===b.r)best=Math.max(best,q.reduce((s,a)=>s+a.s.filter(Boolean).length,0))
   }ck(best===b.chosen.reduce((s,a)=>s+a.s.filter(Boolean).length,0),"greedy optimum");stats.greedyOptima++;
  }
 }
 for(let t=0;t<100;t++){
  const n=3+rnd(4), events=Array.from({length:2},()=>({rows:Array.from({length:2+rnd(5)},()=>BigInt(rnd(1<<n))),labels:[],bad:Array.from({length:4},()=>Boolean(rnd(7)<3))}));
  events.forEach(e=>e.labels=e.rows.map(()=>1+rnd(3)));
  for(const e of events)for(let j=0;j<4;j++){const pins=Array.from({length:rnd(3)},()=>[BigInt(rnd(1<<n)),rnd(2)]),h=BigInt(rnd(1<<n));ck(moment(e,n,guard(pins),h)===ref(e,n,pins,h),"signed marginal")}
  let models=0;for(let x=0n;x<bit(n);x++)if(events.every(e=>!bad(e,x)))models++;
  if(models)stats.randomSAT++;else stats.randomUNSAT++;
  let res=solve(events,n,Array.from({length:1<<n},(_,j)=>BigInt(j))); // full small-spectrum control only
  if(res.label==="SAT"){ck(models>0,"false SAT");stats.certSAT++}else if(res.label==="UNSAT"){ck(!models,"false UNSAT");stats.certUNSAT++}else stats.unknown++;
 }
 // Reversed observation orders, each of n rows essential. Independent triples via six class parities.
 for(const n of [6,12,24,48]){
  const r=Array.from({length:n},(_,j)=>bit(j)),lab1=r.map((_,j)=>1<<(j%3)),lab2=r.map((_,j)=>j%6<3?(1<<(j%3))^(1<<((j+2)%3)):1<<(j%3));
  const tbl=Array.from({length:8},(_,j)=>par(BigInt(j))===0?j!==0:j===7); // bad iff Hamming weight >=2
  const e1={rows:r,labels:lab1,bad:tbl},e2={rows:r.slice().reverse(),labels:lab2.slice().reverse(),bad:tbl};
  function features(e){let a=[0n,0n,0n];e.rows.forEach((r,j)=>{for(let k=0;k<3;k++)if(e.labels[j]&(1<<k))a[k]^=r});return Array.from({length:8},(_,j)=>a.reduce((s,r,k)=>s^((j>>k)&1?r:0n),0n))}
  const fs=[...new Set([...features(e1),...features(e2)])];ck(fs.length===15,"independent triples");
  const good=solve([e1,e2],n,fs);ck(good.label==="SAT"&&good.credit===0.25&&good.maxw===0&&good.D.every(d=>!d),"reversed SAT");
  const opp={rows:r.slice().reverse(),labels:lab1.slice().reverse(),bad:tbl.map(v=>!v)};
  const no=solve([e1,opp],n,features(e1));ck(no.label!=="SAT"&&no.credit===0,"reversed UNSAT control");
  // All possible compatible interleavings have the n-observation cut with distinct coordinates on prefix.
  for(let j=0;j<=n;j++){let left=[...r.slice(0,j),...r.slice(j)];ck(rank(left)===n,"reverse global cut")}
  if(n<=12){let y=0,z=0;for(let x=0n;x<bit(n);x++){if(!bad(e1,x)&&!bad(e2,x))y++;if(!bad(e1,x)&&!bad(opp,x))z++}ck(y===2**(n-2)&&z===0,"exhaustive scale")}
  stats.scales.push({n,commonWidth:n,localWidth:good.maxw,deficiency:good.D,features:fs.length,credit:good.credit,negativeControl:no.label,negativeCredit:no.credit});
 }
 // Guard coupling necessity: pin x1+x2, local independent rows become equal.
 ck(width([1n,2n])===0&&width([1n,2n].map(r=>red(r,bas([3n]))[0]))===1,"cross guard");
 return stats;
};
console.log(JSON.stringify(run(),null,2));
