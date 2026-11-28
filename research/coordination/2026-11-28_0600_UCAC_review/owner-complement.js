// Source-only owner complement quotient; runner uses pinned compiler and registry; study exported for reproduction.
function study(g,cap=512){
 const n=g.types.length*4,p=Array.from({length:n},(_,i)=>i),s=Array(n).fill(0),size=Array(n).fill(1);
 const cost={uf:0,rankTests:0,xor:0,localWords:0,joins:0,member:0};
 function find(i){let b=0;while(p[i]!==i){cost.uf++;b^=s[i];i=p[i]}return [i,b]}
 function join(i,j,b){let [a,x]=find(i),[c,y]=find(j);if(a===c)return (x^y)===b;if(size[a]<size[c])[a,c]=[c,a];p[c]=a;s[c]=x^y^b;size[a]+=size[c];return true}
 for(const [i,j,b] of g.edges)if(!join(i,j,b))return {status:"NO",reason:"signed equality",cost};
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="E")for(let j=1;j<4;j++)if(!join(4*v,4*v+j,0))return {status:"NO",reason:"E equality",cost};
 const owners=[],occ=new Map(),portMap=Array.from({length:n},(_,i)=>find(i));
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="B"){
  let id=owners.length,ports=portMap.slice(v*4,v*4+4),opts=[];
  for(let x=0;x<16;x++){cost.localWords++;let a=ports.map(([r,b],j)=>((x>>j)&1)^b),seen=new Map();if([0,1,2,3].reduce((z,j)=>z+((x>>j)&1),0)!==2)continue;if(a.every((b,j)=>!seen.has(ports[j][0])?(seen.set(ports[j][0],b),true):seen.get(ports[j][0])===b))opts.push({x,a})}
  if(!opts.length)return {status:"NO",reason:"local balance",cost};
  owners.push({v,ports,opts,masks:Array(4).fill(0n)});
  ports.forEach(([r],j)=>{if(!occ.has(r))occ.set(r,[]);occ.get(r).push([id,j])});
 }
 let dim=0;for(const a of occ.values())for(let j=1;j<a.length;j++){const [u,k]=a[0],[v,l]=a[j],b=1n<<BigInt(dim++);owners[u].masks[k]^=b;owners[v].masks[l]^=b}
 const S=owners.map(o=>o.opts.map(({a,x})=>({x,v:a.reduce((z,b,j)=>b?z^o.masks[j]:z,0n)})));
 const low=x=>x&-x;
 function add(B,x){while(x){cost.rankTests++;let b=low(x);if(!B.has(b)){B.set(b,x);return true}x^=B.get(b);cost.xor++}return false}
 function reduce(B,x){for(const [b,v] of B){cost.rankTests++;if(x&b){x^=v;cost.xor++}}return x}
 function sorted(B){return new Map([...B].sort((a,b)=>a[0]<b[0]?-1:1))}
 const span=A=>{let B=new Map();for(const L of A){let a=L[0];for(const v of L)add(B,v^a)}return sorted(B)};
 const raw=S.map(L=>[...new Set(L.map(x=>x.v))]);
 const K=new Map(),periods=owners.map(o=>o.masks.reduce((a,b)=>a^b,0n));
 for(let i=0;i<raw.length;i++){const set=new Set(raw[i]);if(!raw[i].every(x=>set.has(x^periods[i])))throw Error("period");add(K,periods[i])}
 const B=sorted(K),quot=raw.map(L=>[...new Set(L.map(x=>reduce(B,x)))]);
 const par=owners.map((_,i)=>i);function root(i){while(par[i]!==i)i=par[i];return i}
 for(const a of occ.values())for(let j=1;j<a.length;j++)par[root(a[j][0])]=root(a[0][0]);
 const comps=new Set(owners.map((_,i)=>root(i))).size;if(K.size!==owners.length-comps)throw Error("owner rank");
 function widths(A,order){const all=span(A),vals=[];function go(lo,hi){if(hi-lo<=1)return;let mid=(lo+hi)>>1;for(const [l,h] of [[lo,mid],[mid,hi]]){let left=order.slice(l,h).map(i=>A[i]),right=order.filter((_,j)=>j<l||j>=h).map(i=>A[i]);vals.push(span(left).size+span(right).size-all.size);if(h-l>1)go(l,h)}}go(0,order.length);return {max:Math.max(0,...vals),sum:vals.reduce((a,b)=>a+b,0),rank:all.size}}
 const order=owners.map((_,i)=>i);
 // source-only deterministic incidence BFS order, no imported labels.
 const adj=owners.map(()=>new Set());for(const a of occ.values()){let u=a[0][0];for(const [v] of a)if(u!==v){adj[u].add(v);adj[v].add(u)}}
 let seen=new Set(),bfs=[];for(const i of order)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++){let u=q[j];bfs.push(u);for(const v of [...adj[u]].sort((a,b)=>a-b))if(!seen.has(v)){seen.add(v);q.push(v)}}}
 // fixed representative target test, exact target-conditioned sequential DP, stores selected local options.
 function dp(A,ord){let target=0n,center=A.map(L=>{target^=L[0];return L.map(x=>x^L[0])});let suffix=Array(ord.length+1);suffix[ord.length]=new Map();for(let i=ord.length-1;i>=0;i--){let b=new Map(suffix[i+1]);for(const x of center[ord[i]])add(b,x);suffix[i]=sorted(b)}
 if(reduce(suffix[0],target))return {status:"NO",peak:0,reason:"affine hull"};
 let cur=new Map([[0n,[]]]),peak=1;
 for(let i=0;i<ord.length;i++){let nxt=new Map();for(const [x,h] of cur)for(let j=0;j<center[ord[i]].length;j++){cost.joins++;let y=x^center[ord[i]][j];if(nxt.has(y))continue;cost.member++;if(!reduce(suffix[i+1],target^y)){nxt.set(y,h.concat(j));if(nxt.size>cap)return {status:"UNKNOWN",peak:nxt.size,stage:i}}}cur=nxt;peak=Math.max(peak,cur.size);if(!cur.size)return {status:"NO",peak,stage:i}}
 let h=cur.get(target);if(!h)return {status:"NO",peak};let a=Array(A.length);ord.forEach((u,i)=>a[u]=h[i]);return {status:"YES",peak,choices:a}
 }
 function lift(res,A,isQ){if(res.status!=="YES")return null;let words=res.choices.map((j,i)=>S[i].find(x=>(isQ?reduce(B,x.v):x.v)===A[i][j]));let delta=words.reduce((a,x)=>a^x.v,0n);
 if(isQ){const tag=new Map();for(let i=0;i<periods.length;i++){let x=periods[i],t=1n<<BigInt(i);while(x){let b=low(x);if(!tag.has(b)){tag.set(b,[x,t]);break}let [v,u]=tag.get(b);x^=v;t^=u}}let t=0n;while(delta){let b=low(delta);if(!tag.has(b))throw Error("lift");let [v,u]=tag.get(b);delta^=v;t^=u}words=words.map((x,i)=>t>>BigInt(i)&1n?S[i].find(y=>y.x===(x.x^15)):x)}
 let assigned=new Map();owners.forEach((o,i)=>o.ports.forEach(([r,b],j)=>{let x=(words[i].x>>j&1)^b;if(assigned.has(r)&&assigned.get(r)!==x)throw Error("carrier lift");assigned.set(r,x)}));const vals=portMap.map(([r,b])=>(assigned.get(r)??0)^b);
 if(!g.edges.every(([i,j,b])=>(vals[i]^vals[j])===b)||!g.types.every((t,i)=>{let a=vals.slice(4*i,4*i+4);return t==="E"?a.every(x=>x===a[0]):a.reduce((x,y)=>x+y,0)===2}))throw Error("native check");return true}
 const arms=[];for(const [name,A,o] of [["raw/source",raw,order],["quot/source",quot,order],["quot/incidence",quot,bfs]]){let res=dp(A,o);let valid=lift(res,A,name.startsWith("quot"));delete res.choices;arms.push({name,...res,verified:valid,width:widths(A,o)})}
 return {owners:owners.length,carriers:occ.size,dim,comps,periodRank:K.size,rawRows:raw.reduce((a,b)=>a+b.length,0),quotRows:quot.reduce((a,b)=>a+b.length,0),arms,cost};
}
module.exports={study};
