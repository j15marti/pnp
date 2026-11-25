// M27: node checker.js BS19_results.json BS20_results.json RT26_results.json
function run(bs,peer,rt){
 let assertions=0;function ck(b,s){assertions++;if(!b)throw Error(s)}
 const bit=(w,i)=>(w>>>i)&1,pc=x=>{let c=0;while(x){x&=x-1;c++}return c},par=x=>pc(x)&1, id=l=>Math.abs(l), sg=l=>+(l<0), vmask=l=>1<<(id(l)-1);
 function bad(c,w){let b=bit(w,id(c[0])-1)^sg(c[0]);return c.every(l=>(bit(w,id(l)-1)^sg(l))===b)}
 function packet(c){return c.slice(1).map(l=>[vmask(c[0])^vmask(l),sg(c[0])^sg(l)])}
 function pbad(p,w){return p.every(([a,b])=>par(a&w)===b)}
 function expand(p){let t=new Map([[0,1]]);for(let [a,b] of p){let old=[...t];for(let [k,v] of old){let q=k^a;ck(!t.has(q),"independent rows");t.set(q,b?-v:v)}}return t}
 function liftPacket(p,Y){return p.map(([m,b])=>{let a=0;for(let j=1;j<Y.length;j++)if(bit(m,j-1))a^=1<<(Y[j]-1);if(pc(a)&1)a^=1<<(Y[0]-1);return [a,b]})}
 function signature(C,P){
   let sets=[...C.map(packet),...P],maxRank=Math.max(...sets.map(p=>p.length)),D=2**maxRank,total=new Map(),occ=new Map(),nonquad=[];
   for(let i=0;i<sets.length;i++){let p=sets[i],t=expand(p),scale=D/2**p.length,degree=Math.max(...[...t.keys()].map(pc));if(degree>2)nonquad.push(i);for(let [k,v] of t){total.set(k,(total.get(k)||0)+v*scale);if(!occ.has(k))occ.set(k,[]);occ.get(k).push([i,v])}}
   let high=[...total].filter(([k,v])=>v&&pc(k)>2),unique=[...occ].filter(([k,a])=>pc(k)>2&&a.length===1).map(([k,a])=>({mask:k,owner:a[0][0],sign:a[0][1]}));
   let allsame=[...occ].filter(([k,a])=>pc(k)>2&&a.every(x=>x[1]===a[0][1])).length;
   let edges=[...total].filter(([k,v])=>v&&pc(k)===2).length;
   return {D,total,stat:{maxRank,nonquadraticOwners:nonquad.length,highTerms:high.length,uniqueHighTerms:unique.length,firstUnique:unique[0]||null,sameSignHighTerms:allsame,pairEdges:edges,degree:Math.max(...[...total].filter(([k,v])=>v).map(([k])=>pc(k)))}};
 }
 function closure(C,P){let n=0;for(let c of C){ck(new Set(c.map(id)).size===c.length&&c.length>=2,"distinct literals");let seen=[new Set(),new Set()];for(let b=0;b<2**c.length;b++){let vals=c.map((l,j)=>bit(b,j)^sg(l));if(vals.every(x=>x===vals[0]))continue;for(let j=0;j<c.length;j++)seen[bit(b,j)].add(j)}ck(seen.every(a=>a.size===c.length),"both values per owner");n++}for(let p of P){let terms=expand(p);ck(p.length>1,"no rank-one packet");let span=new Set(terms.keys());ck(![...span].some(k=>pc(k)===1),"complement invariance");n++}return n}
 function hasPrivate(C,Y,w,P){
   const fixed=new Map(Y.map((x,j)=>[x,j===0?0:bit(w,j-1)])),ix=new Map(P.map((x,j)=>[x,j])),g=Array.from({length:2*P.length},()=>[]);
   function add(a,b){g[a].push(b)}
   for(let c of C)for(let neg=0;neg<2;neg++){
      let l=[];let sat=false;
      for(let z of c){let s=sg(z)^neg,x=id(z);if(fixed.has(x)){if(fixed.get(x)^s){sat=true;break}}else l.push(2*ix.get(x)+(1^s))}
      if(sat)continue;if(l.length===0)return false;ck(l.length<=2,"parametric arity");if(l.length===1)add(l[0]^1,l[0]);else{add(l[0]^1,l[1]);add(l[1]^1,l[0])}
   }
   const reach=(a,b)=>{let q=[a],s=new Set(q);for(let j=0;j<q.length;j++){if(q[j]===b)return true;for(let z of g[q[j]])if(!s.has(z)){s.add(z);q.push(z)}}return false};
   for(let i=0;i<P.length;i++)if(reach(2*i,2*i+1)&&reach(2*i+1,2*i))return false;return true;
 }
 const raw=bs.source.O.map(o=>o.t.map(x=>x+1)),wide=bs.common.find(o=>o.K===16).residual.C;
 let out={};
 for(let [key,C,g] of [["raw",raw,peer.raw.gauge],["wide",wide,peer.wide.gauge]]){
   let Y=g.exterior,P=g.private,packets=g.packets.map(p=>liftPacket(p,Y));
   let scans=closure(C,[])+closure(C,packets),base=signature(C,[]),all=signature(C,packets),low=signature(C,packets.filter(p=>p.length===2));
   let degree=packets.map(p=>Math.max(...[...expand(p).keys()].map(pc))),covered=0,accepted=0;
   for(let w=0;w<2**(Y.length-1);w++){let x=0;for(let j=1;j<Y.length;j++)if(bit(w,j-1))x|=1<<(Y[j]-1);let cover=packets.some(p=>pbad(p,x));let ok=hasPrivate(C,Y,w,P);if(cover){covered++;ck(!ok,"peer packet replay")}if(ok)accepted++}
   let V=[...new Set(C.flat().map(id))].sort((a,b)=>a-b),words=key==="wide"?2**V.length:512,models=0;let seed=271125;
   for(let i=0;i<words;i++){let w=0;if(key==="wide"){V.forEach((x,j)=>{if(bit(i,j))w|=1<<(x-1)})}else{seed=(Math.imul(seed,1664525)+1013904223)>>>0;w=seed&((1<<24)-1)}
     let v=C.filter(c=>bad(c,w)).length+packets.filter(p=>pbad(p,w)).length;
     let f=0;for(let [m,z] of all.total)if(z)f+=par(m&w)?-z:z;ck(f===v*all.D,"Fourier exact energy");if(v===0)models++;
   }
   let E=new Set();for(let c of C)for(let i=0;i<c.length;i++)for(let j=i+1;j<c.length;j++)E.add(vmask(c[i])^vmask(c[j]));
   let sourceWitness=Object.entries(g.firstWitness).reduce((w,[x,b])=>w|(b<<(Number(x)-1)),0);ck(C.every(c=>!bad(c,sourceWitness))&&packets.every(p=>!pbad(p,sourceWitness)),"peer witness");
   out[key]={n:V.length,owners:C.length,closureScans:scans,forcedPins:0,packetDegrees:degree,packetRanks:packets.map(p=>p.length),liftedPackets:packets,base:base.stat,combined:all.stat,rankTwoOnly:low.stat,exteriorWords:2**(Y.length-1),covered,accepted,energyWords:words,modelsInEnergyWords:models,sourceWitness,primalEdges:E.size,genusLowerIfSimpleConnected:Math.max(0,Math.ceil((E.size-3*V.length+6)/6))};
 }
 // Fixed disk wheel on vertices 0..3, center 4. All 5^4 choices (absent or 4 sign classes).
 const tris=[[0,1,4],[1,2,4],[2,3,4],[3,0,4]],edges=[[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]],fac=[[0,4,5],[1,5,6],[2,6,7],[3,7,4]];
 let disk={charts:0,sat:0,unsat:0,crossoverPremise:0,exactCrossovers:0,dualComparisons:0};
 for(let q=0;q<625;q++){
   let t=q,C=[];for(let k=0;k<4;k++){let a=t%5;t=Math.floor(t/5);if(a)C.push(tris[k].map((x,j)=>(x+1)*(j&&bit(a-1,j-1)?-1:1)))}
   let supports=new Set(),min=Infinity;
   for(let w=0;w<32;w++){let f=C.filter(c=>bad(c,w)).length;min=Math.min(min,f);if(!f)supports.add(w&15)}
   // pair cost = number of equal signed endpoints. Face-even edge words are cuts.
   let paircost=edges.map(([u,v])=>[0,1].map(b=>C.reduce((s,c)=>{let a=c.find(l=>id(l)===u+1),d=c.find(l=>id(l)===v+1);return s+(a&&d?+(b===(sg(a)^sg(d))):0)},0)));
   let dual=Infinity;for(let z=0;z<256;z++){if(fac.some(F=>F.reduce((p,i)=>p^bit(z,i),0)))continue;let cost=paircost.reduce((s,p,i)=>s+p[bit(z,i)],0);dual=Math.min(dual,cost)}
   ck(dual===C.length+2*min,"disk dual minimum");disk.dualComparisons++;disk.charts++;disk[min?"unsat":"sat"]++;
   if(supports.has(0)&&supports.has(10)){disk.crossoverPremise++;ck([...supports].some(w=>![0,5,10,15].includes(w)),"noncrossing support")}
   if(supports.size===4&&[0,5,10,15].every(w=>supports.has(w)))disk.exactCrossovers++;
 }
 // RT26 exact opposite-label controls; source bad words as supplied.
 let critical=[];
 for(let r of rt.controls){let C=r.registry;let m=0;for(let w=0;w<2**r.n;w++){if(C.every(o=>!o.bad.includes(o.t.reduce((s,x,j)=>s|(bit(w,x)<<j),0))))m++}ck(m===0,"RT26 UNSAT root");let sat=0;
   for(let i=0;i<C.length;i++)for(let j=0;j<3;j++){let yes=false;for(let w=0;w<2**r.n;w++){if(C.every((o,k)=>!o.bad.includes(o.t.reduce((s,x,h)=>s|(bit(w,x)<<h),0)^(k===i?1<<j:0)))){yes=true;break}}ck(yes,"RT26 sign neighbor");sat++}
   critical.push({n:r.n,owners:C.length,rootModels:m,satNeighbors:sat});
 }
 return {assertions,out,disk,critical};
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('fs');console.log(JSON.stringify(run(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2))}
