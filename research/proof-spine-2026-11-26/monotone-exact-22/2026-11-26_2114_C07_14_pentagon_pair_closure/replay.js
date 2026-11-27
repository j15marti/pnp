function replay(data){
 const F=data.source,{D,P,certificates}=data.I,ok=(x,m)=>{if(!x)throw Error(m||"assert")};let h=2166136261;for(const c of JSON.stringify(F))h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;ok(h.toString(16)===data.finger);
 const V=F.owners.length,adj=Array.from({length:V},()=>[]);
 // Reconstruct source edge relation from the actual exclusion rows.
 F.edgeRows.forEach((ids,i)=>{const [u,v]=F.G.e[i];for(let c=0;c<3;c++){const row=F.rows[ids[c]];ok(row[0]===F.owners[u][c]&&row[1]===F.owners[v][c]&&row[2]===2)}adj[u].push(v);adj[v].push(u)});
 const z=Array(V).fill(-1);z[P[0]]=0;z[P[1]]=1;const words=[];let candidates=0;
 function enumerate(i){if(i===D.length){candidates++;if(F.G.e.every(([u,v])=>z[u]<0||z[v]<0||z[u]!==z[v]))words.push(D.map(v=>z[v]));return}
 const v=D[i];if(z[v]>=0){enumerate(i+1);return}for(let c=0;c<3;c++){z[v]=c;enumerate(i+1)}z[v]=-1}
 enumerate(0);
 const expected=new Set(certificates.map(t=>t.pins.join(",")));ok(expected.size===certificates.length&&words.length===expected.size&&words.every(w=>expected.has(w.join(","))),"cover mismatch");
 let nodes=0,scans=0,contradictions=0,cap=1000000,capped=false;const per=[];
 function closure(w){let changed=true;while(changed){changed=false;for(const r of F.rows){if(++scans>cap){capped=true;return null}let s=0,u=[];for(const i of r)if(w[i]<0)u.push(i);else s+=w[i];if(s>2||s+u.length<2){contradictions++;return null}if(s===2||s+u.length===2)for(const i of u){w[i]=s===2?0:1;changed=true}}}return w}
 function visit(w){nodes++;w=closure(w);if(!w)return !capped;
 let best=null,live=[];for(const owner of F.owners){if(owner.some(i=>w[i]===1))continue;const L=owner.filter(i=>w[i]!==0);if(!best||L.length<live.length){best=owner;live=L}}
 if(!best)return false;
 for(const i of live){const q=w.slice();q[i]=1;if(!visit(q))return false}return true
 }
 for(const pins of words){const w=Array(F.n).fill(-1);w[0]=w[1]=0;w[2]=w[3]=w[4]=1;D.forEach((v,i)=>F.owners[v].forEach((j,c)=>w[j]=c===pins[i]?1:0));const start=nodes,old=scans;ok(visit(w),"replay failed");per.push({pins,nodes:nodes-start,scans:scans-old})}
 return {finger:data.finger,candidates,cover:words.length,nodes,scans,contradictions,capped,per};
}
const fs=require('node:fs');
console.log(JSON.stringify(replay(JSON.parse(fs.readFileSync(process.argv[2]||'domination_results.json','utf8'))),null,2));
