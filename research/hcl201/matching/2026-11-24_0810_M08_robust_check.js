function run(){
let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
const st={random:0,baseUnsat:0,referenceFlows:0,referenceTuples:0,flowQueries:0,fixedArcs:0,blocks:0,interiorBlocks:0,parityQueries:0,tagChecks:0,sat:0,unsat:0,witnesses:0,scaling:[]};
const assert=(x,m)=>{if(!x)throw Error(m)};
function bal(n,E,x){let b=Array(n).fill(0);E.forEach(([u,v],i)=>{b[u]-=x[i];b[v]+=x[i]});return b}
function tag(E,x){return E.reduce((s,e,i)=>s^((x[i]%2)?e[3]:0n),0n)}
function flow(n,E,b,L=E.map(()=>0),U=E.map(e=>e[2])){
 st.flowQueries++;if(L.some((l,i)=>l>U[i]))return null;
 let d=b.map((v,i)=>v-bal(n,E,L)[i]);let A=Array.from({length:n+2},()=>[]),s=n,t=n+1;
 function add(u,v,c){if(u===v)return null;let a={v,c,r:A[v].length},r={v:u,c:0,r:A[u].length};A[u].push(a);A[v].push(r);return a}
 let arcs=E.map(([u,v],i)=>add(u,v,U[i]-L[i]));let goal=0;
 d.forEach((z,i)=>{if(z<0)add(s,i,-z);if(z>0){add(i,t,z);goal+=z}});
 if(d.reduce((a,b)=>a+b,0)!==0)return null;
 let sent=0;while(sent<goal){let prev=Array(n+2).fill(null),q=[s];prev[s]=[-1,-1];for(let k=0;k<q.length&&!prev[t];k++){let u=q[k];A[u].forEach((a,i)=>{if(a.c>0&&!prev[a.v]){prev[a.v]=[u,i];q.push(a.v)}})}if(!prev[t])return null;let h=goal-sent;for(let v=t;v!==s;){let [u,i]=prev[v];h=Math.min(h,A[u][i].c);v=u}for(let v=t;v!==s;){let [u,i]=prev[v],a=A[u][i];a.c-=h;A[v][a.r].c+=h;v=u}sent+=h}
 return arcs.map((a,i)=>a?U[i]-a.c:L[i])
}
function dsu(n){let p=Array.from({length:n},(_,i)=>i);const f=i=>p[i]===i?i:p[i]=f(p[i]);return [f,(i,j)=>p[f(i)]=f(j)]}
function partition(n,E){let [vfind,vunion]=dsu(n),[efind,eunion]=dsu(E.length),A=Array.from({length:n},()=>[]),cycles=[];
 E.forEach(([u,v],i)=>{if(vfind(u)!==vfind(v)){vunion(u,v);A[u].push([v,i]);A[v].push([u,i])}else{let path=[];if(u!==v){let q=[u],prev=Array(n).fill(null);prev[u]=[-1,-1];for(let k=0;k<q.length&&!prev[v];k++)for(let [w,e] of A[q[k]])if(!prev[w]){prev[w]=[q[k],e];q.push(w)}for(let w=v;w!==u;){let [p,e]=prev[w];path.push(e);w=p}}let C=[i,...path];for(let e of C)eunion(i,e);cycles.push(C)}});
 let m=new Map();E.forEach((_,i)=>{let k=efind(i);if(!m.has(k))m.set(k,{ids:[],cycles:[]});m.get(k).ids.push(i)});for(let C of cycles)m.get(efind(C[0])).cycles.push(C);
 return [...m.values()]
}
function spanAdd(B,v,mask){let x=v,m=mask;for(let [b,c] of B)if((x^b)<x){x^=b;m^=c}if(x)B.push([x,m]);}
function repr(B,v){let x=v,m=0n;for(let [b,c] of B)if((x^b)<x){x^=b;m^=c}return x?null:m}
function xorCycle(C){return C.reduce((s,i)=>s^(1n<<BigInt(i)),0n)}
function orient(n,E,mask){let A=Array.from({length:n},()=>[]),out=E.map(()=>0),used=new Set();E.forEach(([u,v],i)=>{if((mask>>BigInt(i))&1n){A[u].push([v,i,1]);A[v].push([u,i,-1])}});for(let s=0;s<n;s++){while(A[s].length){let u=s;while(A[u].length){let [v,i,sign]=A[u].pop();if(used.has(i))continue;used.add(i);out[i]=sign;u=v}assert(u===s,"not closed")}}return out}
function acquire(n,E,b){
 let f=flow(n,E,b);if(!f)return null;
 let ids=[];for(let i=0;i<E.length;i++){let U=E.map(e=>e[2]),L=E.map(()=>0);U[i]=f[i]-1;let lo=flow(n,E,b,L,U);U[i]=E[i][2];L[i]=f[i]+1;let hi=flow(n,E,b,L,U);if(lo||hi)ids.push(i);else st.fixedArcs++}
 let V=ids.map(i=>E[i]),parts=partition(n,V),W=[],tables=[],base=f.slice();
 for(let P of parts){st.blocks++;let I=P.ids.map(i=>ids[i]),G=I.map(i=>E[i]),x=I.map(i=>f[i]),b0=bal(n,G,x),map=new Map(P.ids.map((i,j)=>[i,j])),C=P.cycles.map(c=>c.map(i=>map.get(i)));
 let mid=flow(n,G,b0,G.map(()=>1),G.map(e=>e[2]-1));
 if(mid){st.interiorBlocks++;let B=[];for(let c of C){let mask=xorCycle(c),v=c.reduce((s,i)=>s^G[i][3],0n);spanAdd(B,v,mask)}let idx=W.length;for(let [v,m] of B)W.push({v,idx,m});I.forEach((i,j)=>base[i]=mid[j]);tables.push({I,G,b0,mid,B,idx,aff:true});}
 else{assert(C.length<=12,"test cap");let S=new Map();for(let z=0;z<2**C.length;z++){let mask=0n;C.forEach((c,i)=>{if((z>>i)&1)mask^=xorCycle(c)});let p=x.map((v,i)=>(v%2)^Number((mask>>BigInt(i))&1n)),bp=bal(n,G,p),bb=b0.map((v,i)=>(v-bp[i])/2);assert(bb.every(Number.isInteger),"parity balance");st.parityQueries++;let h=flow(n,G,bb,G.map(()=>0),G.map((e,i)=>Math.floor((e[2]-p[i])/2)));if(h){let y=h.map((v,i)=>2*v+p[i]);S.set(tag(G,y)^tag(G,x),y)}}tables.push({I,G,b0,x,S,aff:false})}
 }
 let B=[];W.forEach((w,i)=>spanAdd(B,w.v,1n<<BigInt(i)));let baseTag=tag(E,base);
 function solve(target){let D=target^baseTag,states=new Map([[0n,[]]]);for(let t of tables.filter(t=>!t.aff)){let next=new Map();for(let [a,path] of states)for(let [b,y] of t.S)if(!next.has(a^b))next.set(a^b,[...path,[t,y]]);states=next}for(let [v,path] of states){let m=repr(B,D^v);if(m===null)continue;let ans=base.slice();for(let [t,y] of path)t.I.forEach((i,j)=>ans[i]=y[j]);for(let t of tables.filter(t=>t.aff)){let mask=0n;t.B.forEach(([v,c],j)=>{if((m>>BigInt(t.idx+j))&1n)mask^=c});let d=orient(n,t.G,mask);t.I.forEach((i,j)=>ans[i]=t.mid[j]+d[j])}assert(ans.every((v,i)=>v>=0&&v<=E[i][2])&&String(bal(n,E,ans))===String(b)&&tag(E,ans)===target,"witness");st.witnesses++;return ans}return null}
 return {solve,tables,rank:B.length};
}
function brute(n,E,b){let S=new Set(),x=E.map(()=>0);function rec(i){if(i===E.length){st.referenceTuples++;if(String(bal(n,E,x))===String(b)){st.referenceFlows++;S.add(tag(E,x))}return}for(x[i]=0;x[i]<=E[i][2];x[i]++)rec(i+1)}rec(0);return S}
for(let k=0;k<180;k++){let n=2+rnd(5),m=2+rnd(7),E=Array.from({length:m},()=>[rnd(n),rnd(n),rnd(4),BigInt(rnd(16))]),x=E.map(e=>rnd(e[2]+1)),b=bal(n,E,x);if(k%7===0){b[0]+=2;b[1]-=2}let S=brute(n,E,b),R=acquire(n,E,b);assert(!!R===(S.size>0),"base");if(!R)st.baseUnsat++;st.random++;for(let i=0;i<16;i++){let a=R?.solve(BigInt(i));assert(!!a===S.has(BigInt(i)),"target");st.tagChecks++;if(a)st.sat++;else st.unsat++}}
for(let k of [4,16,64,128]){let E=[],n=2*k+1;for(let i=0;i<k;i++){let a=2*i+1,b=a+1;E.push([0,a,2,1n<<BigInt(i)],[a,b,2,0n],[b,0,2,0n])}let b=Array(n).fill(0),R=acquire(n,E,b),all=(1n<<BigInt(k))-1n;assert(R&&R.rank===k&&R.tables.length===k,"bouquet");assert(R.solve(all)&&!R.solve(all|(1n<<BigInt(k))),"bouquet control");st.scaling.push({kind:"one SCC bouquet",rank:k,edges:E.length,blocks:R.tables.length,affineRank:R.rank})}
for(let k of [6,10,16]){let E=[];for(let u=0;u<k;u++)for(let v=u+1;v<k;v++)E.push([u,v,2,1n<<BigInt(E.length)]);let b=bal(k,E,E.map(()=>1)),R=acquire(k,E,b),x=E.map(()=>1);x[0]=2;x[1]=0;let j=E.findIndex(e=>e[0]===1&&e[1]===2);x[j]=2;assert(String(bal(k,E,x))===String(b),"triangle");assert(R.solve(tag(E,x))&&!R.solve(tag(E,x)^1n),"dense control");st.scaling.push({kind:"interior dense",vertices:k,edges:E.length,blocks:R.tables.length,affineRank:R.rank})}
for(let k of [1,2,3]){let E=[[0,1,1,0n],[0,1,1,1n],[0,1,1,2n]],b=[-1,1],R=acquire(2,E,b);for(let t=0;t<4;t++)assert(!!R.solve(BigInt(t))===(t<3),'nonaffine parallel control');}return st
}
console.log(JSON.stringify(run(),null,2));
