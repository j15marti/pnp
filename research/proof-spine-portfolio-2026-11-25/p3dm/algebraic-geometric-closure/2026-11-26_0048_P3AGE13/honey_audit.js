console.log(JSON.stringify((function honeyAudit(){
const ok=(x,m)=>{if(!x)throw Error(m)},bit=i=>1n<<BigInt(i),range=n=>Array.from({length:n},(_,i)=>i),rank=(a)=>{let B=new Map;for(let v of a){while(v){let p=v.toString(2).length-1;if(!B.has(p)){B.set(p,v);break}v^=B.get(p)}}return B.size};
const T0=[[0,0,0],[1,1,1],[0,0,1],[1,1,0],[0,1,0],[1,0,1]],faces=[[0,8,2,6],[0,10,3,7,5,8],[0,6,4,10],[1,11,5,7],[1,9,4,6,2,11],[1,7,3,9],[2,8,5,11],[3,10,4,9]];
let R0=range(12).map(()=>new Map);
for(let f of faces)for(let i=0;i<f.length;i++)R0[f[i]].set(f[(i+f.length-1)%f.length],f[(i+1)%f.length]);
R0=R0.map(M=>{let x=M.keys().next().value,a=[x];for(let v=M.get(x);v!==x;v=M.get(v))a.push(v);ok(a.length===M.size,"base rotation");return a});
let seed=19903;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
let rows=[];
for(let k of [1,2,3,4,6,8,12]){
const h=2*k*k,host=[],at=(i,j,s)=>2*(i*k+j)+s;
for(let i=0;i<k;i++)for(let j=0;j<k;j++){host.push([at(i,j,0),at(i,j,1),0]);if(i+1<k)host.push([at(i,j,0),at(i+1,j,1),1]);if(j+1<k)host.push([at(i,j,0),at(i,j+1,1),2])}
let T=range(h).flatMap(u=>T0.map(t=>t.map(x=>x+2*u))),R=range(h).flatMap(u=>R0.map(a=>a.map(v=>12*u+v))),port=[[1,1],[2,2],[4,1]],phase=range(h).map(()=>Array(3).fill(-1)),edges=[];
function rep(p,q,r){let i=R[p].indexOf(q);ok(i>=0,"edge replacement");R[p][i]=r}
for(let [u,v,c] of host){let [t,col]=port[c],p=12*u+6+t,r=12*v+6+t,q=12*u+2*col+T0[t][col],s=12*v+2*col+T0[t][col];rep(p,q,s);rep(q,p,r);rep(r,s,q);rep(s,r,p);[T[6*u+t][col],T[6*v+t][col]]=[T[6*v+t][col],T[6*u+t][col]];phase[u][c]=phase[v][c]=edges.length;edges.push([u,v])}
for(let u=0;u<h;u++)for(let c=0;c<3;c++)if(phase[u][c]<0){phase[u][c]=edges.length;edges.push([u,h])}
let visited=new Set(),F=0;for(let u=0;u<R.length;u++)for(let v of R[u])if(!visited.has(u+","+v)){F++;let a=u,b=v;do{let key=a+","+b;ok(!visited.has(key),"face repeat");visited.add(key);let j=R[b].indexOf(a);ok(j>=0,"reciprocal");let z=R[b][(j+1)%R[b].length];a=b;b=z}while(a!==u||b!==v)}
ok(visited.size===36*h&&12*h-18*h+F===2,"planarity rotation "+k);
let A=T.map(t=>t.reduce((p,x,c)=>p|bit(c*2*h+x),0n)),b=(1n<<BigInt(6*h))-1n;
for(let c=0;c<3;c++){let z=0n;for(let u=0;u<h;u++)for(let i of [2*c,2*c+1]){let a=A[6*u+i];ok(!(z&a),"uniform phase overlap");z|=a}ok(z===b,"uniform phase coverage")}
let P=edges.map(([u,v])=>bit(u)^bit(v)),reps=Array(edges.length).fill(-1),J=edges.map(()=>0n);
for(let u=0;u<h;u++)for(let c=0;c<3;c++){let e=phase[u][c];reps[e]=6*u+2*c;J[e]^=A[6*u+2*c]^A[6*u+2*c+1]}
let rA=rank(A),rP=rank(P),rJ=rank(J);ok(A.length-rA===P.length-rP,"nullity");ok(rank(P.map((p,e)=>p|(J[e]<<BigInt(h+1))))===rP,"lift of every graph cycle");ok(rJ===rP,"reverse kernel");
let trials=32;for(let j=0;j<trials;j++){let S=range(P.length).filter(()=>rnd(2)),s=new Set(S.map(i=>reps[i])),r1=S.length+rank(A.filter((_,i)=>!s.has(i)))-rA,ss=new Set(S),r2=S.length+rank(P.filter((_,i)=>!ss.has(i)))-rP;ok(r1===r2,"cographic rank identity")}
rows.push({k,hostVertices:h,tuples:A.length,faces:F,phaseEdges:P.length,sourceNullity:A.length-rA,graphNullity:P.length-rP,dualRestrictionChecks:trials,uniformCovers:3,gridMinorOrder:k})
}
return rows
})(),null,2));
