// P3RC02 deterministic audit; node audit.js
const Q=[[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0]];
function assert(x){if(!x)throw Error("assertion");}
function ring(k,relax){
 const colors=Array.from({length:k},(_,i)=>i%2);if(k%2)colors[k-1]=2;
 const T=[];
 for(let i=0;i<k;i++){const a=colors[(i+k-1)%k],b=colors[i],p=[a,b,3-a-b];for(let j=0;j<6;j++){const t=[];for(let c=0;c<3;c++)t[p[c]]=2*i+Q[j][c];T.push({id:6*i+j,t,block:i});}}
 for(let i=0;i<k;i++){const c=colors[i],u=T[6*i+3].t,v=T[6*((i+1)%k)].t;[u[c],v[c]]=[v[c],u[c]];}
 return T.filter(o=>o.id%6!==1||(relax&&o.id===1));
}
function valid(T,n,ids){const a=Array.from({length:3},()=>Array(n).fill(0));for(const o of T)if(ids.has(o.id))o.t.forEach((v,c)=>a[c][v]++);return a.every(r=>r.every(v=>v===1));}
function reference(T,n){const occ=Array.from({length:3*n},()=>[]);for(const o of T)for(let c=0;c<3;c++)occ[c*n+o.t[c]].push(o);const used=new Set(),ids=new Set();function dfs(){if(used.size===3*n)return true;let cand=null;for(let v=0;v<3*n;v++)if(!used.has(v)){const a=occ[v].filter(o=>o.t.every((x,c)=>!used.has(c*n+x)));if(cand===null||a.length<cand.length)cand=a;}for(const o of cand){o.t.forEach((x,c)=>used.add(c*n+x));ids.add(o.id);if(dfs())return true;ids.delete(o.id);o.t.forEach((x,c)=>used.delete(c*n+x));}return false;}return dfs();}
function closure(T,n){
 const pin=new Map();let calls=0,rounds=0;
 function match(a,b,force){calls++;const L=new Map();const covered=[new Set(),new Set(),new Set()];for(const o of T)if(pin.get(o.id)===1||o.id===force)for(let c=0;c<3;c++)covered[c].add(o.t[c]);
 for(let i=0;i<n;i++)if(!covered[a].has(i))L.set(i,[]);
 for(const o of T)if(!pin.has(o.id)&&o.id!==force&&!covered[a].has(o.t[a])&&!covered[b].has(o.t[b]))L.get(o.t[a]).push(o.t[b]);
 const mate=new Map();function aug(u,seen){for(const v of L.get(u))if(!seen.has(v)){seen.add(v);if(!mate.has(v)||aug(mate.get(v),seen)){mate.set(v,u);return true;}}return false;}
 for(const u of L.keys())if(!aug(u,new Set()))return false;return L.size===n-covered[b].size;
 }
 while(true){rounds++;let change=false;
 for(let c=0;c<3&&!change;c++)for(let v=0;v<n&&!change;v++){const os=T.filter(o=>o.t[c]===v),yes=os.filter(o=>pin.get(o.id)===1),free=os.filter(o=>!pin.has(o.id));if(yes.length>1||(!yes.length&&!free.length))return{no:true,pin,calls,rounds};if(yes.length&&free.length){pin.set(free[0].id,0);change=true;}else if(!yes.length&&free.length===1){pin.set(free[0].id,1);change=true;}}
 if(change)continue;
 for(const [a,b] of [[0,1],[0,2],[1,2]]){if(!match(a,b,-1))return{no:true,pin,calls,rounds};for(const o of T)if(!pin.has(o.id)&&!match(a,b,o.id)){pin.set(o.id,0);change=true;break;}if(change)break;}
 if(!change)return{no:false,pin,calls,rounds};
 }
}
function masks(T,k,pin){
 const tables=[];
 for(let i=0;i<k;i++){const os=T.filter(o=>o.block===i);const incoming=T.filter(o=>o.block!==i&&o.t.some(v=>Math.floor(v/2)===i));const tab=new Map();
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){if(incoming.some(o=>pin.has(o.id)&&pin.get(o.id)!==(o.block===(i+k-1)%k?a:b)))continue;for(let m=0;m<2**os.length;m++){const s=new Set(os.filter((o,j)=>(m>>j)&1).map(o=>o.id));if(os.some(o=>pin.has(o.id)&&pin.get(o.id)!==Number(s.has(o.id))))continue;if(Number(s.has(6*i))!==a||Number(s.has(6*i+3))!==b)continue;
 const count=Array(6).fill(0);
 for(const o of os)if(s.has(o.id))o.t.forEach((v,c)=>{if(Math.floor(v/2)===i)count[2*c+v%2]++;});
 for(const o of incoming){const bit=o.block===(i+k-1)%k?a:b;if(bit)o.t.forEach((v,c)=>{if(Math.floor(v/2)===i)count[2*c+v%2]++;});}
 if(count.every(x=>x===1)){tab.set(2*a+b,[...s]);break;}
 }}tables.push(tab);}return tables;
}
// 2-SAT by implication reachability with deterministic incremental pins.
// Every tentative bit is accepted only if SCC-equivalent reachability test stays feasible.
function solve(tabs){const k=tabs.length,edges=[];for(let i=0;i<k;i++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)if(!tabs[i].has(2*a+b)){const u=2*((i+k-1)%k)+a,v=2*i+b;edges.push([u,v^1],[v,u^1]);}
 function feasible(es){const g=Array.from({length:2*k},()=>[]);for(const [u,v] of es)g[u].push(v);function reach(u,v){const seen=new Set([u]),q=[u];for(let j=0;j<q.length;j++)for(const x of g[q[j]])if(!seen.has(x)){seen.add(x);q.push(x);}return seen.has(v);}for(let i=0;i<k;i++)if(reach(2*i,2*i+1)&&reach(2*i+1,2*i))return false;return true;}
 if(!feasible(edges))return null;const w=[];for(let i=0;i<k;i++){const p=[2*i+1,2*i];if(feasible([...edges,p])){edges.push(p);w.push(0);}else{edges.push([2*i,2*i+1]);w.push(1);}}return w;}
const results=[];
for(const k of [3,4,5,8,9,16,17,32,33,64,65])for(const relax of [false,true]){
 const T=ring(k,relax),n=2*k;assert(new Set(T.map(o=>o.t.join(","))).size===T.length);const expected=relax||k%2===0;
 const raw=masks(T,k,new Map());for(let i=0;i<k;i++)assert([...raw[i].keys()].sort().join(",")===(relax&&i===0?"0,1,2":"1,2"));
 const cl=closure(T,n);assert(!cl.no||!expected);
 const tab=cl.no?raw:masks(T,k,cl.pin),w=solve(tab);
 assert(Boolean(w)===expected);if(w){const ids=new Set();for(let i=0;i<k;i++)for(const id of tab[i].get(2*w[(i+k-1)%k]+w[i]))ids.add(id);assert(valid(T,n,ids));for(const [id,b] of cl.pin)assert(Number(ids.has(id))===b);}
 if(k<=9)assert(reference(T,n)===expected);
 results.push({k,relax,triples:T.length,sat:expected,closureNo:cl.no,pins:cl.pin.size,matchingCalls:cl.calls,rounds:cl.rounds,reference:k<=9});
}
console.log(JSON.stringify(results,null,2));
