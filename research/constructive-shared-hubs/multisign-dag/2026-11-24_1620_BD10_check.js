"use strict";
function run(){
 const stats={rankCalls:0,xors:0,exchangeTests:0,augmentations:0,closureSweeps:0,pins:0,referenceWords:0,verifiedLifts:0,peakGround:0,peakExchangeVertices:0};
 const bit=i=>1n<<BigInt(i);
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 const pivot=x=>x.toString(2).length-1;
 function reduce(row,b){let [x,y]=row;for(const [a,c] of b){if(x&bit(pivot(a))){x^=a;y^=c;stats.xors++}}return [x,y]}
 function basis(rows){stats.rankCalls++;let b=[];for(const row of rows){let [x,y]=reduce(row,b);if(!x){if(y)return null;continue}let p=pivot(x);b=b.map(([a,c])=>a&bit(p)?[a^x,c^y]:[a,c]);b.push([x,y]);b.sort((a,b)=>pivot(b[0])-pivot(a[0]))}return b}
 function rank(rows){return basis(rows.map(a=>[a,0])).length}
 function evalRows(rows,z){return rows.every(([a,b])=>parity(a&z)===b)}
 function witness(rows){const b=basis(rows);if(!b)return null;let z=0n;for(const [a,c] of [...b].reverse())if(parity(a&z)!==c)z^=bit(pivot(a));return z}
 function key(rows){return rows.map(([a,b])=>a.toString(16)+":"+b).join(",")}
 function closure(G,events){let g=basis(G);if(!g)return {unsat:true};for(;;){stats.closureSweeps++;let f=[],seen=new Set(),changed=false;for(const e of events){let b=basis(e.map(row=>reduce(row,g)));if(!b)continue;if(!b.length)return {unsat:true};if(b.length===1){g=basis([...g,[b[0][0],b[0][1]^1]]);stats.pins++;if(!g)return {unsat:true};changed=true;break}let k=key(b);if(!seen.has(k)){seen.add(k);f.push(b)}}if(!changed)return {g,f}}}
 function select(G,W,E){
  const q=basis([...G.map(([a])=>[a,0]),...W.map(a=>[a,0])]);let e=[];
  E.forEach((rows,i)=>rows.forEach(([a,b])=>{let v=reduce([a,0],q)[0];if(v)e.push({i,a,b,v})}));
  stats.peakGround=Math.max(stats.peakGround,e.length);let I=new Set();
  const linear=A=>{stats.exchangeTests++;return rank(A.map(j=>e[j].v))===A.length};
  const partition=A=>{stats.exchangeTests++;return new Set(A.map(j=>e[j].i)).size===A.length};
  while(true){let inA=[...I],out=e.map((_,j)=>j).filter(j=>!I.has(j));let prev=new Map(),queue=[];
   for(const j of out)if(partition([...inA,j])){prev.set(j,-1);queue.push(j)}
   let end=-1;
   for(let t=0;t<queue.length;t++){let j=queue[t];if(!I.has(j)&&linear([...inA,j])){end=j;break}
    if(I.has(j)){for(const k of out)if(!prev.has(k)&&partition([...inA.filter(a=>a!==j),k])){prev.set(k,j);queue.push(k)}}
    else{for(const k of inA)if(!prev.has(k)&&linear([...inA.filter(a=>a!==k),j])){prev.set(k,j);queue.push(k)}}
   }
   stats.peakExchangeVertices=Math.max(stats.peakExchangeVertices,prev.size);
   if(end<0)break;
   for(let j=end;j!==-1;j=prev.get(j)){if(I.has(j))I.delete(j);else I.add(j)}
   stats.augmentations++;
   if(!linear([...I])||!partition([...I]))throw Error("invalid exchange");
  }
  return [...I].map(j=>e[j]);
 }
 function verify(G,W,E,s,z0){let z=witness([...G,...W.map(a=>[a,parity(a&z0)]),...s.map(({a,b})=>[a,b^1])]);if(z===null||!evalRows(G,z)||W.some(a=>parity(a&z)!==parity(a&z0))||E.some(e=>evalRows(e,z)))throw Error("bad lift");stats.verifiedLifts++;return z}
 function brute(n,G,E){let count=0;for(let z=0n;z<bit(n);z++){stats.referenceWords++;if(evalRows(G,z)&&E.every(e=>!evalRows(e,z)))count++}return count}
 let controls={cube:{sat:0,unsat:0,cert:0,closureUnsat:0},fano:{sat:0,unsat:0,cert:0,closureUnsat:0},random:{sat:0,unsat:0,cert:0,closureUnsat:0}};
 function control(name,n,E,G=[]){let C=controls[name],count=brute(n,G,E);C[count?"sat":"unsat"]++;let v=closure(G,E);if(v.unsat){C.closureUnsat++;if(count)throw Error("closure false");return count}let s=select(v.g,[],v.f);if(s.length===v.f.length){C.cert++;if(!count)throw Error("false certificate");let z=verify(v.g,[],v.f,s,0n);if(!evalRows(G,z)||E.some(e=>evalRows(e,z)))throw Error("source");}return count}
 const cube=Array.from({length:8},(_,z)=>[0,1,2].map(i=>[bit(i),(z>>i)&1]));for(let i=0;i<256;i++)control("cube",3,cube.filter((_,j)=>(i>>j)&1));
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];const fano=triples.flatMap(t=>[0,1].map(b=>t.map(i=>[bit(i),b])));if(control("fano",7,fano)!==0)throw Error("fano");for(let i=0;i<14;i++)if(control("fano",7,fano.filter((_,j)=>i!==j))!==5)throw Error("neighbor");
 let seed=1731;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};for(let t=0;t<100;t++){let n=5,E=[];for(let j=0;j<1+rnd(12);j++){let z=BigInt(rnd(32)),rows=[];for(let k=0;k<1+rnd(3);k++){let a=BigInt(1+rnd(31));rows.push([a,parity(a&z)])}E.push(rows)}control("random",n,E)}
 let scaling=[];for(let m of [4,8,16,32,64]){let W=Array.from({length:m},(_,i)=>bit(m+i));let E=W.map((w,i)=>[[w^bit(i),0],[w^bit((i+1)%m),0]]);let c=closure([],E);let s=select(c.g,W,c.f);if(s.length!==m)throw Error("scale");for(let z of [0n,W.reduce((a,b)=>a^b,0n),W.filter((_,i)=>i%2).reduce((a,b)=>a^b,0n)])verify(c.g,W,c.f,s,z);
 scaling.push({m,exteriorRank:m,selected:s.length,unionBoundNumerator:m,unionBoundDenominator:4,flatKeysAnalytical:(1n<<BigInt(m)).toString(),supportKeys:1});}
 // Actual canonical expansion of scaling family for m<=8, including cancellation.
 let flat=[];for(let m of [4,8]){let E=Array.from({length:m},(_,i)=>[[bit(m+i)^bit(i),0],[bit(m+i)^bit((i+1)%m),0]]);let M=new Map([["",{b:[],c:1}]]);let pairs=0;for(let e of E){let Q=new Map(M);for(let {b,c} of M.values()){pairs++;let a=basis([...b,...e]);if(a){let k=key(a),v=(Q.get(k)?.c??0)-c;if(v)Q.set(k,{b:a,c:v});else Q.delete(k)}}M=Q}if(M.size!==2**m)throw Error("flat");flat.push({m,keys:M.size,pairs})}
 const tiny=cube.slice(0,3).map((_,i)=>[0,1].map(j=>[bit(j),(i>>j)&1]));let c=closure([],tiny),s=select(c.g,[],c.f);let counter={selected:s.length,events:tiny.length,models:brute(2,[],tiny),neighborModels:brute(2,[],[...tiny,[[1n,1],[2n,1]]])};if(counter.selected!==2||counter.models!==1||counter.neighborModels!==0)throw Error("counter");
 // Exhaustively validate all-fiber certificate on random small guarded charts.
 let fiber={certificates:0,fibers:0,declines:0};for(let t=0;t<100;t++){let n=5,G=[[BigInt(1+rnd(31)),rnd(2)]],W=[BigInt(1+rnd(31)),BigInt(1+rnd(31))],E=[];for(let i=0;i<1+rnd(5);i++){let z=BigInt(rnd(32));E.push(Array.from({length:2},()=>{let a=BigInt(1+rnd(31));return [a,parity(a&z)]}))}let c=closure(G,E);if(c.unsat){fiber.declines++;continue}let s=select(c.g,W,c.f);if(s.length!==c.f.length){fiber.declines++;continue}fiber.certificates++;for(let z=0n;z<bit(n);z++)if(evalRows(c.g,z)){verify(c.g,W,c.f,s,z);fiber.fibers++}}
 return {controls,scaling,flat,counter,fiber,stats,seed:1731};
}
console.log(JSON.stringify(run(),null,2));
