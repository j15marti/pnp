'use strict';
function auditFP14(){
 const p=(a,b)=>a<b?[a,b]:[b,a], key=E=>JSON.stringify(E.map(e=>p(...e)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]));
 function table(bad){
  const wires=bad?[3,2,5,4]:[2,3,4,5], out={};
  for(let i=0;i<4;i++){
   const adj=Array.from({length:12},()=>[]);
   const add=(a,b)=>{adj[a].push(b);adj[b].push(a)};
   for(let j=0;j<4;j++)add(j+2,6+wires[j]);
   for(let side=0;side<2;side++){let b=(i>>side)&1;for(let j=b;j<6;j+=2)add(6*side+j,6*side+(j+1)%6)}
   const seen=new Set(),pairs=[];
   for(const u of [0,1,6,7])if(!seen.has(u)){let v=u,prev=-1;do{seen.add(v);let w=adj[v].find(x=>x!==prev);prev=v;v=w}while(adj[v].length!==1);seen.add(v);pairs.push([u,v])}
   out[i]=key(pairs);
  }
  return out;
 }
 const good=table(false), bad=table(true);
 if(new Set(Object.values(good)).size!==2||new Set(Object.values(bad)).size!==1)throw Error('pair table');
 // Independent raw edge-subset enumeration for both 14-vertex source fixtures.
 function source(bad){
  const E=[];for(let v=0;v<12;v+=6)for(let i=0;i<6;i++)E.push([v+i,v+(i+1)%6]);E.push([12,13]);
  (bad?[3,2,5,4]:[2,3,4,5]).forEach((w,j)=>E.push([j+2,w+6]));E.push([12,0],[12,1],[13,6],[13,7]);
  const masks=Array(14).fill(0);E.forEach(([u,v],i)=>{masks[u]|=1<<i;masks[v]|=1<<i});const full=(1<<E.length)-1,a=4095,z=4096;
  function pop(n){let c=0;while(n){n&=n-1;c++}return c}
  const F=[];for(let x=0;x<=full;x++)if(masks.every(d=>!(pop(d&x)&1)))F.push(x);
  const proper=F.some(x=>F.some(y=>(x|y)===full));const charts=F.filter(b=>(full^(a|b))===z);
  const extending=charts.filter(x=>F.some(y=>(x|y)===full));
  if(!proper||charts.length!==4||(extending.length>0)===bad)throw Error('raw source control');
  return {proper,flows:F.length,partners:charts,extending};
 }
 // For each multigraph with a fixed root 0, enumerate all rewrite sequences from singletons.
 let checked=0,states=0,nonconfluent=0;
 for(let n=3;n<=5;n++){
  const pairs=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)pairs.push([i,j]);
  for(let m=0;m<(1<<pairs.length);m++){
   const E=pairs.filter((_,i)=>(m>>i)&1).flatMap(e=>[e,e]);
   const cut=S=>E.reduce((a,[u,v])=>a+((((S>>u)^(S>>v))&1)?1:0),0);
   let ok=true;for(let S=2;S<(1<<n);S+=2)if(cut(S)<4){ok=false;break}if(!ok)continue;
   const memo=new Map();
   function rec(P){const k=P.join(',');if(memo.has(k))return memo.get(k);let F=new Set();
    for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++)if(cut(P[i]|P[j])<=4){
      const Q=P.filter((_,h)=>h!==i&&h!==j).concat(P[i]|P[j]).sort((a,b)=>a-b);
      for(const f of rec(Q))F.add(f)
    }
    if(!F.size)F.add(k);memo.set(k,F);return F;
   }
   const out=rec(Array.from({length:n-1},(_,i)=>2<<i));checked++;states+=memo.size;if(out.size!==1)nonconfluent++;
  }
 }
 if(nonconfluent)throw Error('confluence failure');
 return {good,bad,sourceGood:source(false),sourceBad:source(true),checked,states,nonconfluent};
}
console.log(JSON.stringify(auditFP14(),null,2));
