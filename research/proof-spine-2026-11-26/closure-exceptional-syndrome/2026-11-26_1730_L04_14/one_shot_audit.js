function run(){
 let checks=0;const ck=(x,s="")=>{checks++;if(!x)throw Error("check "+checks+" "+s)},CAP=200000;
 const f=s=>"1".repeat(s.length)+"0"+s, key=x=>x.join(",");
 function make(n,E){let id=2,ready=Array.from({length:n},()=>id++),seek=Array.from({length:n},(_,v)=>Array.from({length:v+1},()=>id++)),ret=Array.from({length:n},()=>id++),verify=id++,R=[];
 const add=(u,a,v,c,d)=>R.push([u,a,0,v,c,0,d,2]),stay=(u,v)=>{for(let a of [1,2])add(u,a,v,a,2)};
 for(let v=0;v<n;v++)stay(0,seek[v][v]);
 for(let [u,v] of E)stay(ready[u],seek[v][v]);
 for(let u of [0,...ready])stay(u,verify);
 for(let v=0;v<n;v++){for(let r=v;r>0;r--)for(let a of [1,2])add(seek[v][r],a,seek[v][r-1],a,1);
 add(seek[v][0],1,ret[v],2,0);
 for(let a of [1,2])add(ret[v],a,ret[v],a,0);
 add(ret[v],0,ready[v],0,1)}
 add(verify,2,verify,2,1);add(verify,0,1,0,2);
 return {R,ready,seek,ret,verify,q:id}}
 function encode(R,n,t){return f(R.map(r=>r.map(x=>f(x.toString(2))).join("")).join(""))+f("0".repeat(n))+f(t.toString(2))}
 function decode(w){let p=0;function get(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||2*k+1-j>s.length)throw Error("frame");return[s.slice(k+1,2*k+1-j),2*k+1-j]}let raw,x,t;[raw,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);ck(/^0+$/.test(x)&&/^0*$/.test(w.slice(p))&&/^(0|1[01]*)$/.test(t));let T=Number(BigInt("0b"+t));ck(BigInt(T)<=BigInt(w.length)**4n);let R=[],j=0;while(j<raw.length){let a=[];for(let k=0;k<8;k++){let z;[z,j]=get(raw,j);ck(/^(0|1[01]*)$/.test(z));a.push(parseInt(z,2))}R.push(a)}return{w,n:x.length,t:T,R}}
 function acquire(F){let n=F.n,B=make(n,[]),actual=new Set(F.R.map(key)),E=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(actual.has(key([B.ready[u],1,0,B.seek[v][v],1,0,2,2])))E.push([u,v]);let expect=new Set(make(n,E).R.map(key));return actual.size===expect.size&&[...actual].every(r=>expect.has(r))?E:null}
 function raw(F){let idx=new Map(),cost=0;for(let r of F.R){let k=key(r.slice(0,3));if(!idx.has(k))idx.set(k,[]);idx.get(k).push(r)}
 let Q=[[0,0,0n,0]],seen=new Set(["0,0,0"]);for(let k=0;k<Q.length;k++){let [s,p,M,d]=Q[k];if(s===1)return{status:"YES",dist:d,cost};if(d>=F.t)continue;let a=p<0||p>=F.n?0:(M&(1n<<BigInt(p)))?2:1;
 for(let r of idx.get(key([s,a,0]))||[]){if(++cost>CAP)return{status:"UNKNOWN",cost:CAP};let z=M;if(p>=0&&p<F.n&&r[4]===2)z|=1n<<BigInt(p);let P=p+[-1,1,0][r[6]],v=key([r[3],P,z]);if(!seen.has(v)){seen.add(v);Q.push([r[3],P,z,d+1])}}}return{status:"NO",cost}}
 function dp(n,E){let adj=Array.from({length:n},()=>[]);for(let [u,v] of E)adj[u].push(v);let L=1<<n,F=Array.from({length:L},()=>new Map()),cost=0;for(let i=0;i<n;i++)F[1<<i].set(i,[-1,-1]);for(let m=1;m<L;m++)for(let [u] of F[m]){if(m===L-1){let path=[],M=m,U=u;while(U>=0){path.push(U);[M,U]=F[M].get(U)}return{status:"YES",path:path.reverse(),cost}}for(let v of adj[u]){if(++cost>CAP)return{status:"UNKNOWN",cost:CAP};if(!(m&(1<<v)))F[m|(1<<v)].set(v,[m,u])}}return{status:"NO",cost}}
 function dfs(n,E){let S=new Set(E.map(key)),cost=0;function search(path,left){if(!left.length)return path;for(let v of left){if(++cost>CAP)throw Error("cap");if(path.length&&!S.has(key([path.at(-1),v])))continue;let z=search([...path,v],left.filter(x=>x!==v));if(z)return z}return null}
 try{let p=search([],Array.from({length:n},(_,i)=>i));return p?{status:"YES",path:p,cost}:{status:"NO",cost}}catch(e){if(e.message==="cap")return{status:"UNKNOWN",cost:CAP};throw e}}
 let seed=297171;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 let data=[],mutants=0,summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}};
 for(let z=0;z<64;z++){let n=2+z%6,E=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(u!==v&&rnd()<.35)E.push([u,v]);if(z%4===0)for(let i=0;i<n-1;i++)if(!E.some(e=>e[0]===i&&e[1]===i+1))E.push([i,i+1]);let M=make(n,E),T=n*n+3*n+2;
 for(let t of [T-1,T]){let w=encode(M.R,n,t),Fs=Array.from({length:4},()=>decode(w)),Es=Fs.map(acquire);ck(Es.every(e=>e&&e.length===E.length&&e.every(a=>E.some(b=>key(a)===key(b)))));ck(Fs.every(x=>x.w===w));
 let A=t<T?{status:"NO",cost:0}:dp(n,Es[0]),B=t<T?{status:"NO",cost:0}:dfs(n,Es[1]),C=raw(Fs[2]),I=t<T?{status:"NO",cost:0}:dp(n,Es[3]);let vals={A,B,C,I};
 for(let [k,v] of Object.entries(vals)){ck(v.status==="UNKNOWN"||v.status===I.status);summary[k][v.status]++;if(v.path){ck(v.path.length===n&&new Set(v.path).size===n&&v.path.slice(1).every((x,i)=>E.some(([a,b])=>a===v.path[i]&&b===x)))}if(v.dist!==undefined)ck(v.dist===T)}
 data.push({n,N:w.length,t,T,edgeCount:E.length,...vals});
 }if(z<8){let R=M.R.slice();R.splice(0,1);ck(acquire(decode(encode(R,n,0)))===null);mutants++}}
 return{checks,cases:data.length,mutants,summary,data,scope:"sequential replicas, same numeric core candidate cap, different candidate types; original rule checks and preprocessing separately charged; no general lower bound"}
}
console.log(JSON.stringify(run(),null,2));
