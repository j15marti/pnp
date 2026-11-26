function audit(){
let seed=20261125;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let checks=0;
const ck=(v,msg)=>{checks++;if(!v)throw Error(msg)};
function flowRoof(F){
 const {c,l,q}=F,n=l.length,s=2*n,t=s+1,N=t+1;let C=2*c,L=Array(2*n).fill(0),P=Array.from({length:N},()=>Array(N).fill(0));
 const pair=(i,j,w)=>{ck(w<=0,"submodular");if(i>j)[i,j]=[j,i];P[i][j]-=w;L[i]+=w};
 for(let i=0;i<n;i++){C+=l[i];L[i]+=l[i];L[n+i]-=l[i]}
 for(const [i,j,w] of q){if(w<=0){C+=w;L[n+i]-=w;L[n+j]-=w;pair(i,j,w);pair(n+i,n+j,w)}else{L[i]+=w;L[j]+=w;pair(i,n+j,-w);pair(n+i,j,-w)}}
 for(let i=0;i<2*n;i++){if(L[i]>=0)P[i][t]+=L[i];else{P[s][i]-=L[i];C+=L[i]}}
 const R=P.map(r=>r.slice());let value=0,seen;
 while(true){let parent=Array(N).fill(-1),Q=[s];parent[s]=s;for(let k=0;k<Q.length;k++){let i=Q[k];for(let j=0;j<N;j++)if(parent[j]===-1&&R[i][j]>0){parent[j]=i;Q.push(j)}}if(parent[t]<0){seen=new Set(Q);break}let f=Infinity;for(let j=t;j!==s;j=parent[j])f=Math.min(f,R[parent[j]][j]);for(let j=t;j!==s;j=parent[j]){R[parent[j]][j]-=f;R[j][parent[j]]+=f}value+=f}
 const LB=C+value,pins=[];for(let i=0;i<n;i++){ck(!(seen.has(i)&&seen.has(n+i)),"minimal cut symmetry");if(seen.has(i)!==seen.has(n+i))pins.push([i,+seen.has(i)])}
 let min=Infinity,minResidual=Infinity,zero=0,zeroResidual=0,optCompatible=false,vals=[];
 for(let x=0;x<2**n;x++){let b=i=>(x>>>i)&1;let E=c+l.reduce((a,w,i)=>a+w*b(i),0)+q.reduce((a,[i,j,w])=>a+w*b(i)*b(j),0);let A=i=>i===s||i<n&&b(i)===1||i>=n&&i<2*n&&b(i-n)===0;let excess=0,cap=0;for(let i=0;i<N;i++)if(A(i))for(let j=0;j<N;j++)if(!A(j)){excess+=R[i][j];cap+=P[i][j]}
 ck(C+cap===2*E,"consistent doubled energy");ck(excess===2*E-LB,"residual exactness");ck(excess>=0,"nonnegative capacity");min=Math.min(min,E);minResidual=Math.min(minResidual,excess);if(E===0)zero++;if(excess<=-LB)zeroResidual++;vals.push([x,E])}
 for(const [x,E] of vals)if(E===min&&pins.every(([i,v])=>((x>>>i)&1)===v))optCompatible=true;
 ck(optCompatible,"weak persistency");ck(minResidual===2*min-LB,"gap identity");if(min>=0)ck(zero===zeroResidual,"zero support equivalence");
 return {n,LB,min,zero,pins:pins.length};
}
const fixtures=[
{name:"MF_U",b:[-1,1,0],d:[[2,-1,-1],[-1,1,0],[-1,1,0],[0,0,0],[0,-1,1],[0,-1,1],[1,1,-2]],arcs:[[1,0],[2,0],[3,2],[3,1],[3,0],[4,3],[5,3],[6,5],[6,4],[6,3]]},
{name:"MF_V",b:[0,0,0],d:[[-1,1,0],[2,-1,-1],[-1,1,0],[-1,1,0],[1,-1,0],[0,-1,1],[0,-1,1],[1,1,-2],[-1,1,0]],arcs:[[1,0],[2,1],[3,1],[4,3],[4,2],[4,0],[5,4],[6,4],[7,5],[7,4],[7,6],[8,0],[8,1],[8,4]]}];
const result=[];
for(const {name,b,d,arcs} of fixtures){let n=d.length,R=Array.from({length:n},()=>Array(n).fill(false));for(const [i,j] of arcs)R[i][j]=true;for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)R[i][j]||=R[i][k]&&R[k][j];let dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),c=dot(b,b),l=d.map(v=>2*dot(b,v)+dot(v,v)),q=new Map();for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let w=2*dot(d[i],d[j]);if(R[i][j])l[i]+=w;else if(R[j][i])l[j]+=w;else q.set(i*n+j,w)}const B=2*(Math.abs(c)+l.reduce((s,v)=>s+Math.abs(v),0)+[...q.values()].reduce((s,v)=>s+Math.abs(v),0))+1;for(const [i,j] of arcs){l[i]+=B;let k=Math.min(i,j)*n+Math.max(i,j);q.set(k,(q.get(k)||0)-B)}const x=flowRoof({c,l,q:[...q].map(([k,v])=>[Math.floor(k/n),k%n,v])});ck(x.zero===(name==="MF_U"?0:3),"actual cover count");result.push({name,...x})}
for(let k=0;k<200;k++){const n=1+rnd(7),c=rnd(9)-4,l=Array.from({length:n},()=>rnd(11)-5),q=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)q.push([i,j,rnd(11)-5]);flowRoof({c,l,q})}
return {seed:20261125,checks,randomQUBOs:200,fixtures:result};
}
console.log(JSON.stringify(audit(),null,2));
