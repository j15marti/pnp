const fs=require('node:fs'),crypto=require('node:crypto');
const verify=function(a,b){
 const ck=(x,m)=>{if(!x)throw Error(m)},C=a.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),p=a.proof,D=p.demand.map(x=>x.c),bins=p.bins,B=p.boundary,d=D.length,q=bins.length,binOf=new Map(),demands=new Map();
 let checks=0;
 D.forEach((row,i)=>row.forEach(v=>{ck(!demands.has(v),"disjoint");demands.set(v,i)}));bins.forEach((row,j)=>row.forEach(v=>{ck(demands.has(v)&&!binOf.has(v),"bin");binOf.set(v,j)}));ck(binOf.size===demands.size,"coverage");
 let canon=c=>c.slice().sort((a,b)=>a-b).join(","),allowed=new Set(D.map(canon)),consumer=new Set(p.consumer.map(x=>x.i)),seen=new Set();
 for(let [j,bin] of bins.entries()){for(let i=0;i<bin.length;i++)for(let k=i+1;k<bin.length;k++)allowed.add(canon([-bin[i],-bin[k]]));let v=p.blockers[j];if(v!==null){ck(B.includes(v)&&!seen.has(v),"injectivity");seen.add(v);for(let w of bin)allowed.add(canon([-v,-w]))}}
 ck(seen.size===B.length,"all selectors");let actual=new Set(C.filter((_,i)=>!consumer.has(i)).map(canon));ck(actual.size===allowed.size&&[...actual].every(k=>{checks++;return allowed.has(k)}),"exact region");
 const neighbors=D.map(row=>[...new Set(row.map(v=>binOf.get(v)))].sort((a,b)=>a-b));ck(JSON.stringify(neighbors)===JSON.stringify(b.neighbors),"neighbors");
 ck(b.cuts.length===d&&new Set(b.cuts.map(x=>x.force)).size===d,"all forced rows");
 for(let cut of b.cuts){let s=0,t=1+d+q,n=t+1,inf=d+q+1,edges=new Map(),balance=Array(n).fill(0);ck(cut.force>=0&&cut.force<d,"force");for(let i=0;i<d;i++){edges.set(s+","+String(1+i),i===cut.force?inf:1);for(let j of neighbors[i])edges.set((1+i)+","+(1+d+j),inf)}for(let j=0;j<q;j++)edges.set((1+d+j)+","+t,1);ck(cut.arcs.length===edges.size,"arc count");for(let e of cut.arcs){let k=e.u+","+e.v;ck(edges.has(k)&&edges.get(k)===e.c&&Number.isInteger(e.f)&&e.f>=0&&e.f<=e.c,"flow");edges.delete(k);balance[e.u]-=e.f;balance[e.v]+=e.f;checks++}ck(balance[s]===-q&&balance[t]===q&&balance.slice(1,-1).every(v=>v===0),"flow value q");ck(cut.value===q,"flow value")}
 return {verified:true,checks,threshold:q-d,flows:d,exactShell:true,interpretation:"Every boundary assignment of weight <=q-d has a matching lift, every assignment of greater weight is impossible; no boundary mask enumeration in this proof."}
};
const bytes=fs.readFileSync(process.argv[2]);const a=JSON.parse(bytes),b=JSON.parse(fs.readFileSync(process.argv[3]));if(b.parents[0]!=='CERT-v1:sha256:'+crypto.createHash('sha256').update(bytes).digest('hex')||a.instance_id!==b.instance_id||a.instance_id!=='DIMACS-CNF-v1:sha256:'+crypto.createHash('sha256').update(a.dimacs).digest('hex'))throw Error('identity');console.log(JSON.stringify(verify(a,b.proof)));
