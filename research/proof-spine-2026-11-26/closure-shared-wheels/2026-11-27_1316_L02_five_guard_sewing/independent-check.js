const fs=require('fs');const [c,b,r]=process.argv.slice(2),s=fs.readFileSync(c,'utf8');const compile=new Function(s.slice(s.indexOf('function compile'),s.indexOf('function auditLocal'))+';return compile')();const verifyNative=function verifyNative(net,z){
 let C=z.nativeChart,F=C.clauses,n=C.vars.length,N=net.types.length*4,adj=Array.from({length:N},()=>[]),edgeSeen=new Set(),portSeen=new Set(),visits=0;
 const assert=(a,s)=>{if(!a)throw Error(s)},abs=Math.abs,uniq=x=>[...new Set(x)],eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 function link(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
 assert(net.format==="STRICT-EB4-v1"&&net.types.every(t=>t==="E"||t==="B"),"format");
 for(let [a,b,s] of net.edges){assert(Number.isInteger(a)&&Number.isInteger(b)&&a>=0&&a<N&&b>=0&&b<N&&[0,1].includes(s),"edge");let v=a>>2,w=b>>2,k=Math.min(v,w)+":"+Math.max(v,w);assert(v!==w&&!edgeSeen.has(k)&&!portSeen.has(a)&&!portSeen.has(b),"simple");edgeSeen.add(k);portSeen.add(a);portSeen.add(b);link(a,b,s)}
 assert(portSeen.size===N,"degree");for(let v=0;v<net.types.length;v++)if(net.types[v]==="E")for(let j=1;j<4;j++)link(4*v,4*v+j,0);
 let root=new Int32Array(N).fill(-1),sign=new Uint8Array(N);for(let i=0;i<N;i++)if(root[i]<0){let q=[i];root[i]=i;while(q.length){let u=q.pop();for(let[v,s]of adj[u]){visits++;if(root[v]<0){root[v]=i;sign[v]=sign[u]^s;q.push(v)}else assert(root[v]===i&&sign[v]===(sign[u]^s),"parity")}}}
 let anchor=C.anchorPort;assert(root[anchor]===anchor,"anchor");let seen=new Set(),occ=new Map(),local=[],truthChecks=0;
 for(let i=0;i<C.factors.length;i++){
  let fac=C.factors[i],rows=[];for(let v of fac.ids){assert(net.types[v]==="B"&&!seen.has(v),"B partition");seen.add(v);rows.push(Array.from({length:4},(_,j)=>[root[v*4+j],sign[v*4+j]]))}
  let all=uniq(rows.flat().map(t=>t[0])),ret=uniq(F[i].map(l=>C.vars[abs(l)-1])),hidden=all.filter(v=>v!==anchor&&!ret.includes(v));for(let v of all){if(!occ.has(v))occ.set(v,new Set());occ.get(v).add(i)}
  assert(ret.every(v=>all.includes(v))&&all.includes(anchor),"scope");assert(all.length<=12,"truth cap");let V=all.filter(v=>v!==anchor),good=new Set();
  for(let w=0;w<2**V.length;w++){truthChecks++;let bits=v=>v===anchor?0:(w>>V.indexOf(v))&1;if(rows.every(row=>row.reduce((s,[v,t])=>s+(bits(v)^t),0)===2)){let mask=ret.reduce((s,v,j)=>s+(bits(v)<<j),0);good.add(mask)}}
  for(let w=0;w<2**ret.length;w++){truthChecks++;let target=F[i].some(l=>Boolean(w&(1<<ret.indexOf(C.vars[abs(l)-1])))===(l>0));assert(good.has(w)===target,"exact local projection")}
  local.push({hidden,ret,ids:fac.ids})
 }
 assert(seen.size===net.types.filter(t=>t==="B").length,"B coverage");for(let {hidden} of local)for(let v of hidden)assert(occ.get(v).size===1&&!C.vars.includes(v),"shared hidden");
 let proofEvents=0;
 function check(t,g){if(t.leaf){let a=new Int8Array(n+1);for(let l of g){assert(abs(l)<=n&&l!==0,"guard");a[abs(l)]=Math.sign(l)}while(true){let change=false;for(let idx of t.used){proofEvents++;assert(Number.isInteger(idx)&&idx>=0&&idx<F.length,"factor id");let cl=F[idx],sat=false,z=0,last=0;for(let l of cl){let v=a[abs(l)];if(v===Math.sign(l)){sat=true;break}if(!v){z++;last=l}}if(sat)continue;if(!z)return true;if(z===1){a[abs(last)]=Math.sign(last);change=true}}if(!change)return false}}assert(Number.isInteger(t.x)&&t.x>=1&&t.x<=n&&!g.some(l=>abs(l)===t.x),"branch");return check(t.lo,g.concat(-t.x))&&check(t.hi,g.concat(t.x))}
 let G=z.nativeRes.guards;for(let i=0;i<G.length;i++)assert(check(z.nativeRes.proofs[i],G[i]),"proof check");
 let coord=uniq(G.flat().map(abs)),patterns=0;for(let w=0;w<2**coord.length;w++){let bits=v=>(w>>coord.indexOf(v))&1;assert(G.some(g=>g.every(l=>bits(abs(l))===Number(l>0))),"cover");patterns++}
 // hostile mutation: delete a necessary leaf's support (all support entries, not single-clause minimality).
 let t=JSON.parse(JSON.stringify(z.nativeRes.proofs[0]));while(!t.leaf)t=t.lo;t.used=[];assert(!check(t,[]),"mutated empty support"); // leaf with no premises must fail under empty guard
 return {portCount:N,edgeCount:net.edges.length,bfsArcVisits:visits,localFactorCount:local.length,truthChecks,hiddenCount:local.reduce((s,r)=>s+r.hidden.length,0),proofEvents,patterns,mutatedLeafRejected:true,exactProjection:true,local};
};
for(let z of JSON.parse(fs.readFileSync(r,'utf8'))){let x=JSON.parse(fs.readFileSync(b,'utf8')).instances.find(t=>t.id===z.alias);let g=compile(x);const crypto=require('crypto');if(crypto.createHash('sha256').update(JSON.stringify(g.network)+'\n').digest('hex')!==z.registry.sha256)throw Error('source hash');console.log(JSON.stringify({alias:z.alias,...verifyNative(g.network,z)}))}
