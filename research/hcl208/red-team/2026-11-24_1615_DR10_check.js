'use strict';
function run(){
 let checks=0,edgeScans=0,closureScans=0,closureCalls=0,pins=0,frontierTransitions=0,frontierCandidates=0,evals=0;
 function ok(t){checks++;if(!t)throw Error("assertion "+checks);}
 // Layers have local integer vertex IDs. Each edge is [tail,head,variable,value]; -1 means mandatory.
 function graph(){return {w:[1],e:[]};}
 function step(g,w,e){g.w.push(w);g.e.push(e);}
 function edge(u,v,b=-1,c=0){return [u,v,b,c];}
 function neutral(k){
  let g=graph(),w=4*k;step(g,w,Array.from({length:w},(_,j)=>edge(0,j)));
  for(let b=0;b<2*k;b++)step(g,w,Array.from({length:w},(_,j)=>Math.floor(j/4)===Math.floor(b/2)?edge(j,j,b,(j%4>>(b%2))&1):edge(j,j)));
  let cut=g.e.length;
  let es=[];for(let j=0;j<w;j++)for(let t=0;t<=j%4;t++)es.push(edge(j,j));step(g,w,es);
  for(let i=0;i<2*k;i++){let es=[];for(let j=0;j<w;j++){es.push(edge(j,j));if(i<2*Math.floor(j/4))es.push(edge(j,j));}step(g,w,es);}
  step(g,1,Array.from({length:w},(_,j)=>edge(j,0)));return {g,cut};
 }
 function core(k,b){
  let g=graph(),w=2*k+2,p=2*k;
  step(g,w,[...Array.from({length:p},(_,j)=>edge(0,j)),edge(0,p)]);
  for(let t=0;t<2*k;t++){
   let e=[];for(let j=0;j<p;j++){let own=Math.floor(j/2)===Math.floor(t/2);e.push(own?edge(j,j,t,(j%2)^(t%2)):edge(j,j));}
   for(let q=0;q<2;q++)for(let a=0;a<2;a++)e.push(edge(p+q,p+(q^a),t,a));step(g,w,e);
  }
  for(let i=0;i<k;i++){let e=[];for(let j=0;j<w;j++){e.push(edge(j,j));if(j<p&&i<=Math.floor(j/2))e.push(edge(j,j));}step(g,w,e);}
  step(g,1,[...Array.from({length:p},(_,j)=>edge(j,0)),edge(p+b,0)]);return g;
 }
 function reverse(g){return {w:g.w.slice().reverse(),e:g.e.slice().reverse().map(es=>es.map(([u,v,b,c])=>edge(v,u,b,c)))};}
 function shift(g,d){return {w:g.w.slice(),e:g.e.map(es=>es.map(([u,v,b,c])=>edge(u,v,b<0?b:b+d,c)))};}
 function join(...gs){return {w:gs.flatMap((g,i)=>i?g.w.slice(1):g.w),e:gs.flatMap(g=>g.e)};}
 function bit(z,b){return (z>>b)&1;}
 function count(g,z){evals++;let a=[1n];for(let i=0;i<g.e.length;i++){let n=Array(g.w[i+1]).fill(0n);for(let [u,v,b,c] of g.e[i]){edgeScans++;if(b<0||bit(z,b)===c)n[v]+=a[u];}a=n;}return a[0];}
 function closure(g,initial={}){
  let p={...initial};while(true){closureCalls++;let f=[new Set([0])],possible=new Set([0]);const status=(b,c)=>b<0?1:Object.hasOwn(p,b)?(p[b]===c?1:0):2;
   for(let es of g.e){let m=new Set(),v2=new Set();for(let [u,v,b,c] of es){closureScans++;let s=status(b,c);if(s===1&&f.at(-1).has(u))m.add(v);if(s!==0&&possible.has(u))v2.add(v);}f.push(m);possible=v2;}
   if(f.at(-1).has(0))return {status:"UNSAT",p};if(!possible.has(0))return {status:"SAT",p};
   let r=Array(g.w.length);r[r.length-1]=new Set([0]);for(let i=g.e.length-1;i>=0;i--){r[i]=new Set();for(let [u,v,b,c] of g.e[i]){closureScans++;if(status(b,c)===1&&r[i+1].has(v))r[i].add(u);}}
   let change=false;outer:for(let i=0;i<g.e.length;i++)for(let [u,v,b,c] of g.e[i]){closureScans++;if(status(b,c)===2&&f[i].has(u)&&r[i+1].has(v)){p[b]=1-c;pins++;change=true;break outer;}}
   if(!change)return {status:"UNKNOWN",p};
  }
 }
 function frontier(g,cut){
  let masks=[new Set([0])],peak=1;for(let i=0;i<cut;i++){let es=g.e[i],vars=[...new Set(es.filter(e=>e[2]>=0).map(e=>e[2]))];ok(vars.length<=1);let next=new Map();
   for(let m of masks)for(let a=0;a<(1<<vars.length);a++){frontierTransitions++;let s=new Set();for(let [u,v,b,c] of es){frontierCandidates++;if(m.has(u)&&(b<0||a===c))s.add(v);}let key=[...s].sort((a,b)=>a-b).join(",");next.set(key,s);}
   masks=[...next.values()];ok(masks.every(m=>m.size===masks[0].size));peak=Math.max(peak,masks.length);
  }return {size:masks.length,peak};
 }
 function clauseGraph(n,cs){let g=graph(),w=cs.length;step(g,w,cs.map((_,j)=>edge(0,j)));for(let i=0;i<n;i++){let es=[];cs.forEach((c,j)=>{let ls=c.filter(l=>Math.abs(l)===i+1);if(!ls.length)es.push(edge(j,j));else if(ls.every(l=>l===ls[0]))es.push(edge(j,j,i,ls[0]>0?0:1));});step(g,w,es);}step(g,1,cs.map((_,j)=>edge(j,0)));return g;}
 function bad(cs,z){return cs.filter(c=>!c.some(l=>bit(z,Math.abs(l)-1)===(l>0?1:0))).length;}
 let suite={SAT:0,UNSAT:0,sourceWords:0,verifiedWitnesses:0},fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)]);
 const cube=Array.from({length:8},(_,j)=>[1,2,3].map((x,i)=>bit(j,i)?x:-x));
 const cases=[...Array.from({length:256},(_,j)=>[3,cube.filter((_,i)=>bit(j,i))]),[7,fano],...fano.map((_,i)=>[7,fano.filter((_,j)=>i!==j)])];
 let fanoModels=[];
 for(let ci=0;ci<cases.length;ci++){let [n,cs]=cases[ci],g=clauseGraph(n,cs),cl=closure(g),models=[];for(let z=0;z<1<<n;z++){suite.sourceWords++;let b=bad(cs,z);ok(count(g,z)===BigInt(b));if(!b){models.push(z);ok(Object.entries(cl.p).every(([i,a])=>bit(z,+i)===a));}}ok(cl.status!=="UNSAT"||!models.length);ok(cl.status!=="SAT"||models.length>0);if(models.length){suite.SAT++;suite.verifiedWitnesses++;ok(bad(cs,models[0])===0);}else suite.UNSAT++;if(ci>=256){fanoModels.push(models.length);ok(models.length===(ci===256?0:5));}}
 let scales=[];
 for(let k=1;k<=5;k++){
  let {g:ng,cut}=neutral(k),r=frontier(ng,cut);ok(r.size===4**k);
  let left=new Set(),even=core(k,1),odd=core(k,0),m0=Array(k+2).fill(0n),m1=Array(k+2).fill(0n),v0=new Set(),v1=new Set(),zeros=[0,0];
  for(let z=0;z<1<<(2*k);z++){
   let x=0,p=0;for(let i=0;i<k;i++){let b=bit(z,2*i)^bit(z,2*i+1);x+=b*(1<<i);p^=b;}
   let a=count(even,z),b=count(odd,z);ok(a===BigInt(2*x+p));ok(b===BigInt(2*x+1-p));if(a===0n)zeros[0]++;else v0.add(a.toString());if(b===0n)zeros[1]++;else v1.add(b.toString());
   for(let j=0;j<=k+1;j++){m0[j]+=a**BigInt(j);m1[j]+=b**BigInt(j);}
   let n=count(ng,z);ok(n===BigInt(z+((4**k-1)/3)));left.add(n.toString());
  }
  ok(left.size===4**k);ok(zeros[0]===2**k&&zeros[1]===0);ok(v0.size===2**k-1&&v1.size===2**k);
  for(let j=0;j<=k;j++)ok(m0[j]===m1[j]);ok(m0[k+1]!==m1[k+1]);
  let neutralMom=Array(k+2).fill(0n);for(let z=0;z<1<<(2*k);z++){let v=BigInt(z+(4**k-1)/3);for(let j=0;j<=k+1;j++)neutralMom[j]+=v**BigInt(j);}
  // Reverse terminal has precisely the same frontier when traversed backwards.
  let ge=join(ng,shift(even,2*k),shift(reverse(ng),4*k)),go=join(ng,shift(odd,2*k),shift(reverse(ng),4*k));
  let rr=frontier(reverse(go),cut);ok(rr.size===4**k);
  for(let g of [ge,go]){let cl=closure(g);ok(cl.status==="UNKNOWN"&&Object.keys(cl.p).length===0);}
  let prodChecks=0;for(let z=0;z<64;z++){let a=(z*17+3)%(4**k),b=(z*23+1)%(4**k),c=(z*31+2)%(4**k),word=a+(b<<(2*k))+(c<<(4*k));let l=count(ng,a),rr=count(ng,c);ok(count(ge,word)===l*count(even,b)*rr);ok(count(go,word)===l*count(odd,b)*rr);prodChecks+=2;}
  ok(count(ge,0)===0n&&count(go,0)>0n);
  let n=6*k,models=(2n**BigInt(5*k)).toString(); // 2^k core zero assignments, 4k free padding bits.
  scales.push({k,selectorBits:n,vertices:ge.w.reduce((a,b)=>a+b,0),edges:ge.e.reduce((a,b)=>a+b.length,0),forwardMasks:r.size,reverseMasks:rr.size,positiveCoreEven:v0.size,positiveCoreOdd:v1.size,neutralDistinct:left.size,positiveFullLowerBound:4**k,matchedMomentOrder:k,firstDifferentMoment:k+1,evenMoments:m0.map((v,j)=>(v*neutralMom[j]**2n).toString()),oddMoments:m1.map((v,j)=>(v*neutralMom[j]**2n).toString()),coreZeros:zeros,fullSATModels:models,fullUNSATModels:"0",productChecks:prodChecks});
 }
 return {suite,fanoModels,scales,ledger:{checks,edgeScans,closureScans,closureCalls,pins,frontierTransitions,frontierCandidates,evals},limitations:"Exact rank-one edge closure; no semantic closure, no full physical compiler, no full portfolio, no measured peak bytes/CM; product moments computed from separately enumerated independent factors, not full-word enumeration."};
}
console.log(JSON.stringify(run(),null,2));
