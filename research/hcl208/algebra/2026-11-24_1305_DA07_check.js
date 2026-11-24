"use strict";
function experiment(){
 const out={seed:20261124,random:0,randomSAT:0,randomUNSAT:0,guarded:0,guardedSAT:0,guardedUNSAT:0,sourceCases:0,sourceSAT:0,sourceUNSAT:0,sourceWords:0,verifiedLifts:0,assertions:0,gaussianCalls:0,pivotXors:0,collisionEvents:0,closurePasses:0,domainDeletes:0,treeTransitions:0,bruteWords:0,scales:[]};
 let seed=out.seed;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;};
 const assert=(b,msg)=>{out.assertions++;if(!b)throw Error(msg);};
 const colors=[0,1,2,3],pop=m=>colors.filter(c=>m&(1<<c)).length;
 const parity=x=>{let b=0;while(x){x&=x-1n;b^=1;}return b;};
 const eq=(a,b)=>[a[0]^b[0],a[1]^b[1]];
 const xor=(a,b)=>eq(a,b);
 const con=(d,c)=>[c&1?1n<<BigInt(d):0n,c&2?1n<<BigInt(d):0n];
 const value=(d,a,z)=>parity(a[0]&(z|(1n<<BigInt(d))))+2*parity(a[1]&(z|(1n<<BigInt(d))));
 function gauss(d,rows){
  out.gaussianCalls++;const C=1n<<BigInt(d),basis=Array(d).fill(0n);let rank=0;
  for(let row of rows){for(let i=0;i<d;i++)if(row&(1n<<BigInt(i))){if(basis[i]){row^=basis[i];out.pivotXors++;}else{basis[i]=row;rank++;row=0n;break;}}if(row===C)return null;}
  let x=0n;for(let i=d-1;i>=0;i--)if(basis[i]&&parity(basis[i]&(x|C)))x|=1n<<BigInt(i);
  return {x,rank,rows:basis.filter(Boolean)};
 }
 function shape(parent){
  const n=parent.length,children=Array.from({length:n},()=>[]);
  for(let v=1;v<n;v++)children[parent[v]].push(v);
  const ports=children.map((ch,v)=>4-ch.length-(v?1:0));
  assert(ports.every(p=>p>=0),"degree");return {n,parent,children,ports};
 }
 function compile(T,d,ext,shift){
  const msg=[],events=[];
  for(let v=T.n-1;v>=0;v--){
   const ins=ext[v].concat(T.children[v].map(w=>xor(msg[w],con(d,shift[w]))));
   assert(ins.length===(v?3:4),"port count");
   for(let i=0;i<ins.length;i++)for(let j=i+1;j<ins.length;j++){events.push(eq(ins[i],ins[j]));out.collisionEvents++;}
   msg[v]=ins.reduce(xor,[0n,0n]);
  }
  assert(events.length===3*T.n+3,"size");return events;
 }
 function evalEvents(d,events,z){const word=z|(1n<<BigInt(d));return events.some(e=>e.every(r=>!parity(r&word)));}
 function solveGuard(d,events,guard){
  let G=gauss(d,guard);if(!G)return null;
  let live=[];
  for(const e of events){const h=gauss(d,G.rows.concat(e));if(!h)continue;if(h.rank===G.rank)return h.x;live.push({e,h});}
  if(!live.length)return null;
  if(live.length===1){G=gauss(d,G.rows.concat(live[0].e));assert(!!G,"forced guard");return G.x;}
  return live[0].h.x;
 }
 function actual(T,d,ext,z){return ext.map(a=>a.map(e=>value(d,e,z)));}
 function verify(T,ext,shift,x){return x.length===T.n&&x.every((c,v)=>!ext[v].includes(c)&&(v===0||(c^x[T.parent[v]])!==shift[v]));}
 function lift(T,ext,shift){
  const dom=ext.map(a=>15^a.reduce((m,c)=>m|(1<<c),0));
  let change=true;while(change){out.closurePasses++;change=false;for(let v=1;v<T.n;v++){const u=T.parent[v];for(const [a,b] of [[u,v],[v,u]])if(pop(dom[a])===1){const c=colors.find(c=>dom[a]&(1<<c));const old=dom[b];dom[b]&=~(1<<(c^shift[v]));if(old!==dom[b]){out.domainDeletes+=pop(old)-pop(dom[b]);change=true;}}}if(dom.some(x=>!x))return null;}
  for(let v=T.n-1;v>=0;v--)for(const c of colors)if(dom[v]&(1<<c))for(const w of T.children[v]){out.treeTransitions++;if(!(dom[w]&~(1<<(c^shift[w])))){dom[v]&=~(1<<c);break;}}
  if(!dom[0])return null;const x=[];for(let v=0;v<T.n;v++){let c=colors.find(c=>(dom[v]&(1<<c))&&(v===0||(c^x[T.parent[v]])!==shift[v]));assert(c!==undefined,"lift");x.push(c);}
  assert(verify(T,ext,shift,x),"verify");out.verifiedLifts++;return x;
 }
 function brute(T,ext,shift){const x=[];function visit(v){out.bruteWords++;if(v===T.n)return true;for(const c of colors)if(!ext[v].includes(c)&&(v===0||(c^x[T.parent[v]])!==shift[v])){x[v]=c;if(visit(v+1))return true;}return false;}return visit(0);}
 function randomTree(n){const p=[-1],deg=[0];for(let v=1;v<n;v++){const avail=deg.map((d,i)=>d<4?i:-1).filter(i=>i>=0);const u=avail[rnd(avail.length)];p.push(u);deg[u]++;deg.push(1);}return shape(p);}
 for(let k=0;k<240;k++){
  const T=randomTree(1+rnd(8)),d=0,ext=T.ports.map(p=>Array.from({length:p},()=>con(d,rnd(4)))),shift=T.parent.map(()=>rnd(4));const E=compile(T,d,ext,shift),a=actual(T,d,ext,0n),ans=evalEvents(d,E,0n),w=lift(T,a,shift);
  assert(ans===!!w&&ans===brute(T,a,shift),"random");out.random++;out[ans?"randomSAT":"randomUNSAT"]++;
 }
 for(let k=0;k<100;k++){
  const T=randomTree(1+rnd(6)),d=1+rnd(7),limit=1<<(d+1),ext=T.ports.map(p=>Array.from({length:p},()=>[BigInt(rnd(limit)),BigInt(rnd(limit))])),shift=T.parent.map(()=>rnd(4));const E=compile(T,d,ext,shift),G=Array.from({length:rnd(d+1)},()=>BigInt(rnd(limit))),w=solveGuard(d,E,G);
  let count=0;for(let z=0;z<1<<d;z++){const Z=BigInt(z);if(G.every(r=>!parity(r&(Z|(1n<<BigInt(d)))))){const a=actual(T,d,ext,Z),b=brute(T,a,shift);assert(b===evalEvents(d,E,Z),"fiber");if(b)count++;}}
  assert((w!==null)===(count>0),"guard");if(w!==null){assert(G.every(r=>!parity(r&(w|(1n<<BigInt(d))))),"guard lift");assert(!!lift(T,actual(T,d,ext,w),shift),"guard tree lift");}out.guarded++;out[count?"guardedSAT":"guardedUNSAT"]++;
 }
 for(const n of [1,8,32,128,512]){
  const T=shape(Array.from({length:n},(_,i)=>i-1)),d=0,shift=T.parent.map(()=>1),ext=T.ports.map((p,v)=>{
   const a=v===0?(n===1?[0,1,2,3]:[0,2,3]):(v===n-1?[1,2,3]:[2,3]);assert(a.length===p,"scale");return a.map(c=>con(d,c));
  });
  let E=compile(T,d,ext,shift);assert(!evalEvents(d,E,0n)&&!lift(T,actual(T,d,ext,0n),shift),"scale UNSAT");
  ext[0][0]=con(d,2);E=compile(T,d,ext,shift);assert(evalEvents(d,E,0n)&&!!lift(T,actual(T,d,ext,0n),shift),"scale SAT");out.scales.push({n,events:E.length,boundaryPorts:2*n+2});
 }
 const T=shape([-1]);
 function cnf(n,F,expected=null){
  const d=n,rows=F.map(cl=>{assert(cl.length===3,"clause width");const ext=[con(d,0)];for(let j=0;j<3;j++){const l=cl[j],b=1n<<BigInt(Math.abs(l)-1),f=b^(l>0?1n<<BigInt(d):0n);ext.push([j+1&1?f:0n,j+1&2?f:0n]);}return {ext:[ext],E:compile(T,d,[ext],[0])};});
  let count=0;
  for(let z=0;z<1<<n;z++){
   out.sourceWords++;const Z=BigInt(z);const sat=F.every(cl=>cl.some(l=>!!(z&(1<<(Math.abs(l)-1)))===(l>0)));const a=rows.every(r=>evalEvents(d,r.E,Z));assert(sat===a,"star source");
   if(a){count++;for(const r of rows)assert(!!lift(T,actual(T,d,r.ext,Z),[0]),"star lift");}
  }
  if(expected!==null)assert(count===expected,"source count");out.sourceCases++;out[count?"sourceSAT":"sourceUNSAT"]++;
 }
 const cube=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>(i>>j)&1?v:-v));
 for(let m=0;m<256;m++)cnf(3,cube.filter((_,j)=>m>>j&1));
 const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],fano=lines.flatMap(e=>[e,e.map(x=>-x)]);
 cnf(7,fano,0);for(let j=0;j<14;j++)cnf(7,fano.filter((_,i)=>i!==j),5);
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
