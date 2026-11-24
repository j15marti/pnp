const BS05=require('./2026-11-24_1150_BS05_check.js');
const BS04=require('./2026-11-24_1050_BS04_check.js');
function projectWheels(graph, gadgets) {
 const A=(v,m)=>{if(!v)throw Error(m);}, {n,edges}=graph;
 const vertex=x=>Number.isSafeInteger(x)&&x>=0&&x<n, sign=x=>Number.isInteger(x)&&x>=0&&x<4;
 A(Number.isSafeInteger(n)&&n>=0&&edges.every(([u,v,s])=>vertex(u)&&vertex(v)&&u!==v&&sign(s)),"graph schema");
 A(gadgets.every(z=>vertex(z.h)&&vertex(z.b)&&z.h!==z.b&&Array.isArray(z.rim)&&z.rim.length===3&&z.rim.every(vertex)&&sign(z.a)),"manifest schema");
 const rims=new Set(gadgets.flatMap(z=>z.rim)), ports=new Map(gadgets.map(z=>[z.b,z]));
 A(rims.size===3*gadgets.length&&ports.size===gadgets.length,"overlap");
 for(const z of gadgets)A(!rims.has(z.h)&&!rims.has(z.b)&&!ports.has(z.h),"root/port overlap");
 const key=([u,v,s])=>`${Math.min(u,v)}/${Math.max(u,v)}/${s}`, mult=new Map();
 for(const e of edges)mult.set(key(e),(mult.get(key(e))??0)+1);
 const rem=new Set();
 for(const {h,b,rim,a} of gadgets)for(let i=0;i<3;i++)for(const e of [[h,rim[i],0],[b,rim[i],a],[rim[i],rim[(i+1)%3],0]]){const k=key(e);A(mult.get(k)===1&&!rem.has(k),"unauthenticated wheel edge");rem.add(k);}
 const roots=Array.from({length:n},(_,i)=>i).filter(i=>!rims.has(i)&&!ports.has(i)), ix=new Map(roots.map((v,i)=>[v,i])),out=[];
 let impossible=false;
 for(const e of edges){if(rem.has(key(e)))continue;const [u,v,s]=e;A(!rims.has(u)&&!rims.has(v),"exterior rim edge");const a=ports.get(u),b=ports.get(v),x=a?a.h:u,y=b?b.h:v,z=s^(a?a.a:0)^(b?b.a:0);if(x===y){if(z===0)impossible=true;}else out.push([ix.get(x),ix.get(y),z]);}
 return {impossible,graph:{n:roots.length,edges:out},lift(w){const x=Array(n);roots.forEach((v,i)=>x[v]=w[i]);for(const {h,b,rim,a} of gadgets){x[b]=x[h]^a;const colors=[0,1,2,3].filter(c=>c!==x[h]);rim.forEach((v,i)=>x[v]=colors[i]);}A(x.every(v=>v!==undefined)&&edges.every(([u,v,s])=>(x[u]^x[v])!==s),"original wheel lift");return x;}};
}
function graphRows(graph){const {n,edges}=graph;return {K:edges.flatMap(()=>[1,1,1,1]),factors:Array.from({length:n},(_,i)=>[0,1,2,3].map(x=>({c:edges.flatMap(([u,v,s])=>[0,1,2,3].map(a=>Number(i===u&&x===a)+Number(i===v&&x===(a^s))))})))};}
function cooperative(input, options={}){
 const A=(v,m)=>{if(!v)throw Error(m);};let P=null, x=input, rejected=null;
 A(!input.allGuards,"decision only");
 if(input.graph){A(!input.q&&!BigInt(input.b??0)&&!BigInt(input.h??0),"graph input has no separate hidden guards");
  if(input.wheels){try{P=projectWheels(input.graph,input.wheels);if(P.impossible)return {status:"UNSAT",backend:"verified-wheel-projection",w:null};x={graph:P.graph};}catch(e){P=null;rejected=String(e);x={graph:input.graph};}}}
 const z=BS05(x,options);let result=z, backend="block-cut";
 if(z.status==="UNKNOWN"){const old=BS04(x.graph?graphRows(x.graph):x);result={status:old.result===null?"UNSAT":"SAT",w:old.result,counters:old.counters};backend="BS04-fallback";}
 if(result.status==="SAT"){let w=result.w;if(P)w=P.lift(w);
  if(input.graph)A(w.length===input.graph.n&&input.graph.edges.every(([u,v,s])=>(w[u]^w[v])!==s),"graph witness");
  if(input.cnf)A(w.length===input.cnf.n&&input.cnf.clauses.every(c=>c.some(l=>w[Math.abs(l)-1]===Number(l>0))),"CNF witness");
  if(!input.graph&&!input.cnf){const K=input.K.map(BigInt);let t=0n,g=0n,c=K.map(()=>0n);for(let i=0;i<input.factors.length;i++){const r=input.factors[i][w[i]];A(r,"row witness");t^=BigInt(r.t??0);g^=BigInt(r.g??0);c=c.map((v,j)=>v+BigInt(r.c?.[j]??0));}A(t===BigInt(input.b??0)&&g===BigInt(input.h??0)&&c.every((v,j)=>v<=K[j]),"original row witness");}
  result={...result,w};
 }
 return {...result,backend,blockAttempt:z.counters,manifestRejected:rejected};
}
function affineClosure(input, options={}){
 const A=(v,m)=>{if(!v)throw Error(m);};A(!input.cnf&&!input.graph&&!input.allGuards,"explicit row decision input");
 const root=BS05(input,options), out={status:root.status,w:root.w,calls:1,support:null,rank:null,anchor:null,basis:null,counters:{...root.counters}};
 if(root.status!=="SAT")return out;
 const F=input.factors, offsets=[];let d=0;for(const f of F){offsets.push(d);d+=f.length;}
 const word=w=>w.reduce((v,id,i)=>v|(1n<<BigInt(offsets[i]+id)),0n);
 const anchor=word(root.w), piv=new Map(), high=x=>x.toString(2).length-1;
 const parity=x=>{let v=0n;while(x){x&=x-1n;v^=1n;}return v;};
 function put(x){while(x){const k=high(x);if(piv.has(k))x^=piv.get(k);else{piv.set(k,x);return true;}}return false;}
 function run(x){const z=BS05(x,options);out.calls++;for(const [k,v] of Object.entries(z.counters))if(typeof v==="number")out.counters[k]=k==="peakMessage"?Math.max(out.counters[k]??0,v):(out.counters[k]??0)+v;return z;}
 const support=F.map(f=>f.map(()=>false));
 for(let i=0;i<F.length;i++)for(let j=0;j<F[i].length;j++){
  const z=run({...input,factors:F.map((f,k)=>k===i?[f[j]]:f)});
  if(z.status==="UNKNOWN"){out.status="UNKNOWN";return out;}
  if(z.status==="SAT"){support[i][j]=true;const w=z.w.slice();w[i]=j;put(word(w)^anchor);}
 }
 out.support=support;
 const q=input.q??0;
 while(true){
  let grew=false;const keys=[...piv.keys()].sort((a,b)=>a-b);
  for(let j=0;j<d;j++)if(!piv.has(j)){
   let a=1n<<BigInt(j);for(const k of keys)if(parity(a&piv.get(k)))a|=1n<<BigInt(k);
   const F2=F.map((f,i)=>f.map((r,l)=>({...r,g:String(BigInt(r.g??0)|(parity(a&(1n<<BigInt(offsets[i]+l)))<<BigInt(q)))})));
   const z=run({...input,factors:F2,q:q+1,h:String(BigInt(input.h??0)|((parity(a&anchor)^1n)<<BigInt(q)))});
   if(z.status==="UNKNOWN"){out.status="UNKNOWN";return out;}
   if(z.status==="SAT"){A(put(word(z.w)^anchor),"probe did not expand");grew=true;break;}
  }
  if(!grew)break;
 }
 out.rank=piv.size;out.anchor=String(anchor);out.basis=[...piv.values()].map(String);return out;
}
function supplemental(){
 const A=(v,m)=>{if(!v)throw Error(m);}, results={nonflow:[],wheel:[],fallback:[],support:[],parityRank:[],errors:0};
 const fanoLines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],clauses=fanoLines.flatMap(c=>[c,c.map(x=>-x)]);
 for(let i=-1;i<14;i++){const x={cnf:{n:7,clauses:clauses.filter((_,j)=>j!==i)}},z=cooperative(x,{blockCap:4});A(z.status===(i<0?"UNSAT":"SAT")&&z.backend==="BS04-fallback","fallback "+JSON.stringify(z));results.fallback.push({removed:i,status:z.status,backend:z.backend});}
 for(const k of [4,16,64,128]){
  const B=1n<<80n, factors=Array.from({length:2*k},(_,i)=>[0,1].map(x=>({g:x?(i%2?2:1):0,c:Array.from({length:2*k+1},(_,j)=>String((!x&&(j===0||j===1+2*Math.floor(i/2))||x&&j===2+2*Math.floor(i/2))?B:0n))})));
  for(const [d,h,want] of [[0n,0,true],[0n,1,false],[-1n,0,false]]){
   const x={factors,K:[String(BigInt(k)*B+d),...Array(2*k).fill(String(B))],q:2,h},z=cooperative(x);
   A(z.status===(want?"SAT":"UNSAT")&&z.backend==="block-cut","nonflow");results.nonflow.push({k,budgetDelta:String(d),guard:h,status:z.status,...z.counters});
  }
  const f2=Array.from({length:2*k},(_,i)=>[0,1].map(x=>({t:x?String((1n<<BigInt(1+Math.floor(i/2)))|(i%2===0?1n:0n)):"0",c:Array.from({length:k},(_,j)=>String(j===Math.floor(i/2)&&x?B:0n)),g:x?1:0})));
  for(const h of [k%2,1-k%2]){
   const x={factors:f2,K:Array(k).fill(String(B)),b:String(((1n<<BigInt(k+1))-2n)|1n),q:1,h};
   const z=cooperative(x);A(z.status===(h===k%2?"SAT":"UNSAT"),"base rank");results.parityRank.push({k,guard:h,status:z.status,...z.counters});
  }
 }
 const E=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E.push([i,j,0]);
 function shard(edges){let n=5,es=[],wheels=[];for(const [u,v,s] of edges){const tips=[];for(const h of [u,v]){const b=n++,rim=[n++,n++,n++],a=(h+b)%4;wheels.push({h,b,rim,a});tips.push([b,a]);for(let i=0;i<3;i++)es.push([h,rim[i],0],[b,rim[i],a],[rim[i],rim[(i+1)%3],0]);}es.push([tips[0][0],tips[1][0],s^tips[0][1]^tips[1][1]]);}return {graph:{n,edges:es},wheels};}
 for(let i=-1;i<10;i++){const x=shard(E.filter((_,j)=>j!==i)),z=cooperative(x);A(z.status===(i<0?"UNSAT":"SAT")&&z.backend==="block-cut","wheel");results.wheel.push({removed:i,n:x.graph.n,edges:x.graph.edges.length,status:z.status,verifiedLift:z.status==="SAT",...z.counters});}
 const bad={graph:{n:5,edges:[[0,2,0],[1,2,1],[0,3,0],[1,3,1],[0,4,0],[1,4,1],[2,3,0],[3,4,0],[4,2,0]].slice(1)},wheels:[{h:0,b:1,rim:[2,3,4],a:1}]};
 const b=cooperative(bad);A(b.status==="SAT"&&b.manifestRejected,"bad manifest");results.invalidManifest={status:b.status,rejected:b.manifestRejected};
 let seed=91231;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);};
 const inputs=[];for(let j=0;j<60;j++){const n=2+rnd(4),m=1+rnd(3),factors=Array.from({length:n},()=>Array.from({length:2+rnd(2)},()=>({t:rnd(4),g:rnd(4),c:Array.from({length:m},()=>rnd(4))})));let x={factors,K:Array.from({length:m},()=>2+rnd(8)),b:rnd(4),q:2,h:rnd(4)};if(j%2===0){const rows=factors.map(f=>f[rnd(f.length)]);x.b=rows.reduce((a,r)=>a^r.t,0);x.h=rows.reduce((a,r)=>a^r.g,0);x.K=x.K.map((_,k)=>rows.reduce((a,r)=>a+r.c[k],0)+rnd(2));}inputs.push(x);}
 for(let i=-1;i<14;i++){const cls=clauses.filter((_,j)=>j!==i);inputs.push({K:cls.map(()=>2),factors:Array.from({length:7},(_,j)=>[0,1].map(x=>({c:cls.map(c=>c.filter(l=>Math.abs(l)===j+1&&x!==Number(l>0)).length)})))});}
 for(const x of inputs){const z=affineClosure(x);const F=x.factors,K=x.K.map(BigInt);let d=0,offsets=F.map(f=>{let z=d;d+=f.length;return z;}), models=[], sup=F.map(f=>f.map(()=>false));
  function rec(i,t,g,c,w,ids){if(i===F.length){if(t===BigInt(x.b??0)&&g===BigInt(x.h??0)&&c.every((v,j)=>v<=K[j])){models.push(w);ids.forEach((id,j)=>sup[j][id]=true);}return;}F[i].forEach((r,id)=>rec(i+1,t^BigInt(r.t??0),g^BigInt(r.g??0),c.map((v,j)=>v+BigInt(r.c?.[j]??0)),w|(1n<<BigInt(offsets[i]+id)),ids.concat(id)));}
  rec(0,0n,0n,K.map(()=>0n),0n,[]);A(z.status===(models.length?"SAT":"UNSAT"),"support label");
  if(models.length){const P=new Map();for(let w of models){w^=models[0];while(w){let k=w.toString(2).length-1;if(P.has(k))w^=P.get(k);else{P.set(k,w);break;}}}A(z.rank===P.size&&JSON.stringify(z.support)===JSON.stringify(sup),"support/rank");}
  results.support.push({models:models.length,status:z.status,calls:z.calls,rank:z.rank,verifiedRows:z.counters.verified});
 }
 return results;
}
module.exports={cooperative,affineClosure,projectWheels};
if(require.main===module){const fs=require('fs'),arg=process.argv[2];console.log(JSON.stringify(arg?cooperative(JSON.parse(fs.readFileSync(arg,'utf8'))):supplemental(),null,2));}
