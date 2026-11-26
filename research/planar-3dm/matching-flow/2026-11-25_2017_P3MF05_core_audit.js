function audit(){
const fixtures=[
{name:"U",T:"000 002 010 011 021 022 100 101 111 201 202 221",b:[-1,1,0],d:[[2,-1,-1],[-1,1,0],[-1,1,0],[0,0,0],[0,-1,1],[0,-1,1],[1,1,-2]],arcs:[[1,0],[2,0],[3,2],[3,1],[3,0],[4,3],[5,3],[6,5],[6,4],[6,3]]},
{name:"V",T:"000 002 010 011 021 022 100 101 111 201 202 221 110",b:[0,0,0],d:[[-1,1,0],[2,-1,-1],[-1,1,0],[-1,1,0],[1,-1,0],[0,-1,1],[0,-1,1],[1,1,-2],[-1,1,0]],arcs:[[1,0],[2,1],[3,1],[4,3],[4,2],[4,0],[5,4],[6,4],[7,5],[7,4],[7,6],[8,0],[8,1],[8,4]]}];
let result=[];
for(const f of fixtures){const {b,d,arcs}=f,n=d.length,R=Array.from({length:n},()=>Array(n).fill(false));for(const [i,j] of arcs)R[i][j]=true;for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)R[i][j]||=R[i][k]&&R[k][j];const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),l=d.map(v=>2*dot(b,v)+dot(v,v)),q=[],cover=new Set();for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){const c=2*dot(d[i],d[j]);if(R[i][j])l[i]+=c;else if(R[j][i])l[j]+=c;else{q.push([i,j,c]);if(c>0&&!cover.has(i)&&!cover.has(j)){cover.add(i);cover.add(j);}}}
let hist={},nIdeals=0;const feasible=[];for(let x=0;x<1<<n;x++){const bit=i=>(x>>i)&1;if(arcs.some(([i,j])=>bit(i)>bit(j)))continue;const c=b.map((v,k)=>v+d.reduce((s,r,i)=>s+r[k]*bit(i),0)),E=dot(c,c),Q=dot(b,b)+l.reduce((s,v,i)=>s+v*bit(i),0)+q.reduce((s,[i,j,v])=>s+v*bit(i)*bit(j),0);if(E!==Q)throw Error("quadratic");hist[E]=(hist[E]??0)+1;nIdeals++;feasible.push(x);}
const T=f.T.split(" ").map(s=>[...s].map(Number));let source={};for(const a of T.filter(x=>x[0]===0))for(const b of T.filter(x=>x[0]===1))for(const c of T.filter(x=>x[0]===2)){const M=[a,b,c];if(new Set(M.map(x=>x[1])).size!==3)continue;const E=[0,1,2].reduce((s,z)=>s+(M.filter(x=>x[2]===z).length-1)**2,0);source[E]=(source[E]??0)+1;}
if(JSON.stringify(hist)!==JSON.stringify(source))throw Error("hist");
let tests=0,violations=0;for(const x of feasible)for(const y of feasible){const energy=a=>dot(b,b)+l.reduce((s,v,i)=>s+v*((a>>i)&1),0)+q.reduce((s,[i,j,v])=>s+v*((a>>i)&1)*((a>>j)&1),0);if(energy(x)+energy(y)<energy(x|y)+energy(x&y))violations++;tests++;}
for(const [i,j,c] of q)if(c>0&&!cover.has(i)&&!cover.has(j))throw Error("cover");
result.push({name:f.name,ideals:nIdeals,hist,cover:[...cover],submodularityTests:tests,violations,positivePairs:q.filter(x=>x[2]>0)});
}return result;
}
console.log(JSON.stringify(audit(),null,2));
