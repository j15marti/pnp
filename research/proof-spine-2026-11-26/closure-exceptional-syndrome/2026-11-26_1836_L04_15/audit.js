function run(){
 const ck=(b,s)=>{if(!b)throw Error(s||"assert")};let checks=0;const ok=(b,s)=>{checks++;ck(b,s)};
 const bits=x=>{let a=[];while(x){let b=x&-x;x^=b;a.push(31-Math.clz32(b))}return a},key=x=>x.join(","),f=s=>"1".repeat(s.length)+"0"+s;
 function native(n,E){let id=2,ready=Array.from({length:n},()=>id++),seek=Array.from({length:n},(_,v)=>Array.from({length:v+1},()=>id++)),ret=Array.from({length:n},()=>id++),verify=id++,R=[];
 const add=(u,a,v,c,d)=>R.push([u,a,0,v,c,0,d,2]),stay=(u,v)=>{for(let a of [1,2])add(u,a,v,a,2)};
 for(let v=0;v<n;v++)stay(0,seek[v][v]);for(let [u,v] of E)stay(ready[u],seek[v][v]);for(let u of [0,...ready])stay(u,verify);
 for(let v=0;v<n;v++){for(let r=v;r>0;r--)for(let a of [1,2])add(seek[v][r],a,seek[v][r-1],a,1);add(seek[v][0],1,ret[v],2,0);for(let a of [1,2])add(ret[v],a,ret[v],a,0);add(ret[v],0,ready[v],0,1)}add(verify,2,verify,2,1);add(verify,0,1,0,2);return{R,ready,seek}}
 function encode(n,E){let t=n*n+3*n+2;return f(native(n,E).R.map(r=>r.map(x=>f(x.toString(2))).join("")).join(""))+f("0".repeat(n))+f(t.toString(2))}
 function decode(w){let p=0;function read(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||2*k+1-j>s.length)throw Error("frame");return[s.slice(k+1,2*k+1-j),2*k+1-j]}let raw,x,t;[raw,p]=read(w,p);[x,p]=read(w,p);[t,p]=read(w,p);let n=x.length,T=Number(BigInt("0b"+t));ok(n>=2&&/^0+$/.test(x)&&/^0*$/.test(w.slice(p))&&T===n*n+3*n+2&&BigInt(T)<=BigInt(w.length)**4n);let R=[],j=0;while(j<raw.length){let a=[];for(let k=0;k<8;k++){let z;[z,j]=read(raw,j);ok(/^(0|1[01]*)$/.test(z));a.push(parseInt(z,2))}R.push(a)}
 let B=native(n,[]),actual=new Set(R.map(key)),E=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(actual.has(key([B.ready[u],1,0,B.seek[v][v],1,0,2,2])))E.push([u,v]);let expected=new Set(native(n,E).R.map(key));ok(expected.size===actual.size&&[...actual].every(a=>expected.has(a)));return {w,n,T,R,E}}
 function augment(F){let n=F.n,G=Array(n+1).fill(1);G[0]=(1<<(n+1))-2;for(let [u,v] of F.E)if(u!==v)G[u+1]|=1<<(v+1);return G}
 function fromG(G){return encode(G.length-1,G.flatMap((a,i)=>i?bits(a).filter(j=>j>0).map(j=>[i-1,j-1]):[]))}
 function counter(cap){return{ops:0,cap,tick(n=1){this.ops+=n;if(this.ops>this.cap)throw Error("cap")}}}
 function reach(G,S,C){let n=G.length,V=((1<<n)-1)^S,A=G.map((a,i)=>(V>>i&1)?(a&V)|(1<<i):0);for(let k=0;k<n;k++)if(V>>k&1)for(let i=0;i<n;i++){C.tick();if(A[i]>>k&1)A[i]|=A[k]}return[A,V]}
 function cut(G,C){let n=G.length,[A,V]=reach(G,0,C);if(A.some(x=>x!==V))return{S:[],type:"disconnected"};for(let k=0;k<n;k++){[A,V]=reach(G,1<<k,C);for(let i=0;i<n;i++)if(i!==k)for(let j=0;j<i;j++)if(j!==k){C.tick();if(!(A[i]>>j&1)&&!(A[j]>>i&1))return{S:[k],pair:[i,j]}}}return null}
 const pin=(G,i,j,C)=>{C.tick(G.length);return G.map((a,k)=>k===i?1<<j:a&~(1<<j))};
 function unit(G,C){let n=G.length;for(;;){let old=G.join(),F=[];for(let i=0;i<n;i++){C.tick(n);if(!G[i])return null;let b=bits(G[i]);if(b.length===1)F.push([i,b[0]])}
 for(let j=0;j<n;j++){let v=[];for(let i=0;i<n;i++){C.tick();if(G[i]>>j&1)v.push(i)}if(!v.length)return null;if(v.length===1)F.push([v[0],j])}
 for(let [i,j] of F){if(!(G[i]>>j&1))return null;G=pin(G,i,j,C)}if(G.join()===old)return G}}
 function support(G,C){let n=G.length,M=Array(n).fill(-1),seen=0;function aug(i){for(let j of bits(G[i])){C.tick();if(seen>>j&1)continue;seen|=1<<j;if(M[j]<0||aug(M[j])){M[j]=i;return true}}return false}
 for(let i=0;i<n;i++){seen=0;if(!aug(i))return null}
 let H=G.map(a=>bits(a).reduce((x,j)=>x|(1<<M[j]),0)),[A]=reach(H,0,C);return G.map((a,i)=>bits(a).reduce((x,j)=>{C.tick();return A[M[j]]>>i&1?x|(1<<j):x},0))}
 function lane(F,mode){let C=counter(F.w.length**2),G=augment(F),rounds=[],terminal;try{for(;;){G=unit(G,C);if(G===null){terminal="degree";break}if(mode!=="B"){let H=support(G,C);if(H===null){terminal="matching";break}G=H;G=unit(G,C);if(G===null){terminal="degree";break}}if(mode!=="A"&&(terminal=cut(G,C)))break;if(mode==="A")return{status:"UNKNOWN",ops:C.ops,rounds};let bad=[];for(let i=0;i<G.length;i++)for(let j of bits(G[i])){let H=unit(pin(G,i,j,C),C),why=H===null?"degree":null;if(H!==null&&mode==="I"){H=support(H,C);if(H===null)why="matching";else {H=unit(H,C);if(H===null)why="degree"}}
 if(H!==null)why=cut(H,C);if(why)bad.push({edge:[i,j],why})}
 if(!bad.length)return{status:"UNKNOWN",ops:C.ops,rounds};rounds.push(bad);for(let {edge:[i,j]} of bad)G[i]&=~(1<<j)}
 return{status:"NO",terminal,ops:C.ops,rounds}}catch(e){if(e.message!=="cap")throw e;return{status:"UNKNOWN",ops:C.cap,rounds,cap:true}}}
 function dp(F,cap){let n=F.n,C=counter(cap),D=new Map(),A=augment(F).slice(1).map(x=>x>>1);try{for(let i=0;i<n;i++)D.set(1<<i,1<<i);for(let m=1;m<1<<n;m++){C.tick();for(let i of bits(D.get(m)||0))for(let j of bits(A[i]&~m)){C.tick();D.set(m|(1<<j),(D.get(m|(1<<j))||0)|(1<<j))}}return{status:D.get((1<<n)-1)?"WITNESS_EXISTS":"NO",ops:C.ops}}catch(e){if(e.message!=="cap")throw e;return{status:"UNKNOWN",ops:C.cap}}}
 function raw(F){let C=counter(F.w.length**2),I=new Map();for(let r of F.R){let k=key(r.slice(0,3));if(!I.has(k))I.set(k,[]);I.get(k).push(r)}let Q=[[0,0,0,0]],seen=new Set(["0,0,0"]);try{for(let k=0;k<Q.length;k++){let [s,p,M,d]=Q[k];C.tick();if(s===1)return{status:"WITNESS_EXISTS",ops:C.ops};if(d>=F.T)continue;let a=p<0||p>=F.n?0:M>>p&1?2:1;for(let r of I.get(key([s,a,0]))||[]){C.tick();let z=M;if(p>=0&&p<F.n&&r[4]===2)z|=1<<p;let P=p+[-1,1,0][r[6]],v=key([r[3],P,z]);if(!seen.has(v)){seen.add(v);Q.push([r[3],P,z,d+1])}}}return{status:"NO",ops:C.ops}}catch(e){if(e.message!=="cap")throw e;return{status:"UNKNOWN",ops:C.cap}}}
 const seed=[1022,133,203,579,129,773,545,81,33,69],seed2=[126,5,11,35,65,9,21]; // second list is not used
 let out=[],excluded=0,attempts=0;
 function job(G,kind,proof=false){let w=fromG(G),F=Array.from({length:4},()=>decode(w));ok(F.every(x=>x.w===w));ok(augment(F[0]).join()===G.join());let C=proof?{status:"NO",certificate:"universal separator; lobe count exceeds separator size in augmented graph"}:dp(F[2],w.length**2);if(C.status!=="NO"){excluded++;return}let A=lane(F[0],"A"),B=lane(F[1],"B"),I=lane(F[3],"I"),R=proof?{status:"NOT_RUN"}:raw(F[2]);ok(R.status==="NO"||R.status==="UNKNOWN"||R.status==="NOT_RUN");let hash=2166136261;for(let c of w){hash=Math.imul(hash^c.charCodeAt(0),16777619)>>>0}out.push({kind,n:F[0].n,N:w.length,clock:F[0].T,rows:G,fnv32:hash.toString(16),A,B,C,R,I})}
 job(seed,"postclosure seed");
 let R=123421;const rnd=()=>((R=(Math.imul(R,1664525)+1013904223)>>>0)/4294967296);for(let z=0;z<140;z++){let n=6+z%4,G=Array.from({length:n+1},(_,i)=>i===0?(1<<(n+1))-2:1);for(let i=1;i<=n;i++)for(let j=1;j<=n;j++)if(i!==j&&rnd()<.23)G[i]|=1<<j;attempts++;job(G,"candidate")}
 function lobes(s,b){let n=s+(s+1)*b;return Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>j).reduce((x,j)=>i!==j&&(i<s||j<s||Math.floor((i-s)/b)===Math.floor((j-s)/b))?x|(1<<j):x,0))}
 job(lobes(4,3),"separator hostile",true);job(lobes(4,4),"separator hostile",true);
 let counts={};for(let a of out)for(let k of ["A","B","C","I"]){let z=counts[k]||{NO:0,UNKNOWN:0};z[a[k].status]++;counts[k]=z}
 return{checks,attempts,excluded,counts,seed:out[0],hostile:out.filter(x=>x.kind==="separator hostile"),records:out.map(x=>({...x,A:{...x.A,rounds:x.A.rounds.map(r=>r.length)},B:{...x.B,rounds:x.B.rounds.map(r=>r.length)},I:{...x.I,rounds:x.I.rounds.map(r=>r.length)}})),scope:"all four copies exact same framed native bytes, FNV32 diagnostic only; common N^2 instrumented high-level probe cap, not bit-equivalent; raw TM separately checked on small NO; candidates with witness excluded, no SAT analysis; no universal completeness"};
}
console.log(JSON.stringify(run(),null,2));
