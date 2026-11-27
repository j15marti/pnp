const R=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));
function upper(r){
 let live=new Map();for(let i=0;i<r.hybrid.log.length;i++){for(const [j,f] of live)if(f.s.includes(r.hybrid.log[i].v))live.delete(j);live.set(i,r.hybrid.log[i])}
 const fs=[...live.values()],vs=[...new Set(fs.flatMap(f=>f.s))].sort((a,b)=>a-b);
 const val=(f,x)=>f.t[f.s.reduce((k,v,j)=>k|(x.get(v)<<j),0)];
 let state=12345,reads=0,tries=0,best=Infinity,bestx=null;
 function rng(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0}
 const E=x=>fs.reduce((a,f)=>{reads++;return a+val(f,x)},0);
 for(let restart=0;restart<100&&best>2;restart++){tries++;let x=new Map(vs.map(v=>[v,rng()&1])),e=E(x);
 for(let step=0;step<100&&e>2;step++){let target=null,ee=e;for(const v of vs){x.set(v,1-x.get(v));let c=E(x);x.set(v,1-x.get(v));if(c<ee){target=v;ee=c}}if(target===null)break;x.set(target,1-x.get(target));e=ee}
 if(e<best){best=e;bestx=new Map(x)}}
 let full=new Map(bestx),reconstructed=0;
 for(let j=r.hybrid.log.length-1;j>=0;j--){let a=r.hybrid.log[j],w=a.s.reduce((k,v,i)=>{if(!full.has(v))throw Error("missing bit");return k|(full.get(v)<<i)},0);let costs=a.costs[w],b=costs[0]<=costs[1]?0:1;if(costs[b]!==a.t[w])throw Error("bad argmin");full.set(a.v,b);reconstructed++}
 return {id:r.id,upperBound:best,tableReads:reads,restarts:tries,reconstructed,remainingAssignment:[...bestx],rootAssignment:[...full],anchor:[r.anchor,0]};
}
console.log(JSON.stringify(R.map(upper),null,2));
