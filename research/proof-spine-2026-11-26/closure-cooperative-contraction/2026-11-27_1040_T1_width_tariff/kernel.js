function sha(s){
 const K=[],H=[];for(let p=2;K.length<64;p++){let prime=true;for(let d=2;d*d<=p;d++)if(p%d===0){prime=false;break}if(!prime)continue;if(H.length<8)H.push((Math.sqrt(p)%1*4294967296)|0);K.push((Math.cbrt(p)%1*4294967296)|0)}
 const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("non ASCII");let n=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let i=7;i>=0;i--)a.push(Math.floor(n/256**i)%256);
 const rr=(x,n)=>(x>>>n)|(x<<(32-n));
 for(let o=0;o<a.length;o+=64){let w=[];for(let j=0;j<16;j++)w[j]=(a[o+4*j]<<24)|(a[o+4*j+1]<<16)|(a[o+4*j+2]<<8)|a[o+4*j+3];for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=((rr(x,7)^rr(x,18)^(x>>>3))+w[j-16]+(rr(y,17)^rr(y,19)^(y>>>10))+w[j-7])|0}let [A,B,C,D,E,F,G,J]=H;for(let j=0;j<64;j++){let t=(J+(rr(E,6)^rr(E,11)^rr(E,25))+((E&F)^(~E&G))+K[j]+w[j])|0,u=((rr(A,2)^rr(A,13)^rr(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,J]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,J].forEach((x,j)=>H[j]=(H[j]+x)|0)}
 return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}

function normalize(G){
 const n=4*G.types.length,A=Array.from({length:n},()=>[]),used=new Set(),edges=new Set();const add=(x,y,s)=>{A[x].push([y,s]);A[y].push([x,s])};
 for(const [x,y,s] of G.edges){let a=x>>2,b=y>>2,k=[Math.min(a,b),Math.max(a,b)].join(",");if(x<0||y<0||x>=n||y>=n||a===b||used.has(x)||used.has(y)||edges.has(k)||(s!==0&&s!==1))throw Error("bad network");used.add(x);used.add(y);edges.add(k);add(x,y,s)}
 if(used.size!==n)throw Error("degree");
 G.types.forEach((t,v)=>{if(t==="E"){for(let j=1;j<4;j++)add(4*v,4*v+j,0)}else if(t!=="B")throw Error("type")});
 let roots=new Int32Array(n).fill(-1),signs=new Uint8Array(n),arcs=0;
 for(let p=0;p<n;p++)if(roots[p]<0){roots[p]=p;let Q=[p];for(let i=0;i<Q.length;i++){let x=Q[i];for(let [y,s] of A[x]){arcs++;let z=signs[x]^s;if(roots[y]<0){roots[y]=p;signs[y]=z;Q.push(y)}else if(roots[y]!==p||signs[y]!==z)throw Error("transport")}}}
 let F=[],seen=new Set();
 G.types.forEach((t,v)=>{if(t!=="B")return;const ps=[0,1,2,3].map(j=>4*v+j),vs=[...new Set(ps.map(p=>roots[p]+1))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++){let count=0;for(let p of ps)count+=((w>>vs.indexOf(roots[p]+1))&1)^signs[p];if(count===2)ok.push(w)}let k=JSON.stringify([vs,ok]);if(!seen.has(k)){seen.add(k);F.push({vs,ok})}});
 return {F,arcs,roots,signs};
}

function solve(F,cap,limit,reverse=false){
 let order=[],tests=0,index=0,candidates=0,peak=F.reduce((s,f)=>s+f.ok.length,0),max=0,closure=0,pins=[];
 while(true){
  if(F.some(f=>!f.ok.length))return {status:"UNSAT",F,order,tests,index,candidates,peak,max,closure,pins};
  let forced=null;
  for(let f of F){for(let j=0;j<f.vs.length;j++){let a=(f.ok[0]>>j)&1;closure+=f.ok.length;if(f.ok.every(w=>((w>>j)&1)===a)){forced=[f.vs[j],a];break}}if(forced)break}
  if(forced){const [v,a]=forced;pins.push(forced);F=F.map(f=>{let j=f.vs.indexOf(v);if(j<0)return f;let vs=f.vs.filter(u=>u!==v),ok=f.ok.filter(w=>((w>>j)&1)===a).map(w=>(w&((1<<j)-1))|((w>>(j+1))<<j));return {vs,ok}}).filter(f=>f.ok.length!==2**f.vs.length);continue}
  let B=new Map();for(let i=0;i<F.length;i++)for(let v of F[i].vs){index++;if(!B.has(v))B.set(v,[]);B.get(v).push(i)}
  if(!B.size)return {status:"FEASIBLE",F,order,tests,index,candidates,peak,max,closure,pins};
  let best=null;for(let [v,ids] of B){let U=[...new Set(ids.flatMap(i=>F[i].vs))].sort((a,b)=>a-b);candidates++;if(U.length>cap)continue;if(!best||U.length<best.U.length||(U.length===best.U.length&&(reverse?v>best.v:v<best.v)))best={v,ids,U}}
  if(!best||tests+index+candidates+closure>limit)return {status:"UNKNOWN",F,order,tests,index,candidates,peak,max,closure,pins};
  let {v,ids,U}=best,vs=U.filter(u=>u!==v),ok=[],sets=ids.map(i=>new Set(F[i].ok)),ix=ids.map(i=>F[i].vs.map(u=>U.indexOf(u)));
  for(let w=0;w<2**U.length;w++){let yes=true;for(let j=0;j<ids.length;j++){tests++;let y=ix[j].reduce((s,k,i)=>s|(((w>>k)&1)<<i),0);if(!sets[j].has(y)){yes=false;break}}if(yes){let y=vs.reduce((s,u,j)=>s|(((w>>U.indexOf(u))&1)<<j),0);if(!ok.includes(y))ok.push(y)}}
  max=Math.max(max,U.length);order.push(v);let del=new Set(ids);F=F.filter((_,i)=>!del.has(i));if(ok.length!==2**vs.length)F.push({vs,ok});peak=Math.max(peak,F.reduce((s,f)=>s+f.ok.length,0));
 }
}

function compact(x){let {F,order,pins,...m}=x;return {...m,remaining:F.length,remainingVars:new Set(F.flatMap(f=>f.vs)).size,eliminated:order.length,forced:pins.length}}
module.exports={sha,normalize,solve,compact};
