const fs=require('node:fs');
const audit=function audit(R){
 const A=(t,m)=>{if(!t)throw Error(m)},sat=(C,a)=>C.every(c=>c.some(l=>a.get(Math.abs(l))===+(l>0)));
 let out=[];for(let f of R.family.filter(f=>!f.yes)){
 let m=f.m,N=2*m,patterns=0,edges=0,clauseTests=0,checkLits=0,seed=271128,examples=[];
 function check(ids){let adj=Array.from({length:N+2},()=>[]);for(let i of ids){let j=Math.floor(i/m),k=i%m,u=2+j*m+k,v=k===m-1?2+j*m:u+1,b=+(k===m-1);adj[u].push([v,b]);adj[v].push([u,b]);edges++}let a=new Map();for(let v=1;v<=N+1;v++)if(!a.has(v)){a.set(v,0);let q=[v];for(let t=0;t<q.length;t++)for(let [w,b] of adj[q[t]]){let z=a.get(q[t])^b;if(a.has(w))A(a.get(w)===z,"odd cycle");else{a.set(w,z);q.push(w)}}}
 let C=ids.flatMap(i=>f.factors[i].map(j=>f.phase[j])),b=new Map([...a].map(([v,z])=>[v,1-z]));A(sat(C,a)&&sat(C,b),"regional complement");patterns++;clauseTests+=2*C.length;checkLits+=2*C.reduce((s,c)=>s+c.length,0);if(examples.length<3)examples.push({ids,word:[...a]})}
 if(m<=6){for(let mask=0;mask<2**N;mask++){let ids=[];for(let i=0;i<N;i++)if(mask>>i&1)ids.push(i);if(ids.length<m)check(ids)}}else{for(let t=0;t<1024;t++){let order=Array.from({length:N},(_,i)=>i);for(let i=N-1;i>0;i--){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let j=seed%(i+1);[order[i],order[j]]=[order[j],order[i]]}check(order.slice(0,m-1))}}
 // Full path phase equations force opposite selector; verify by two possible uniform chain states.
 let endTests=0;for(let j=0;j<2;j++){let C=f.factors.slice(j*m,(j+1)*m).flatMap(i=>i.map(x=>f.phase[x]));for(let s of [0,1])for(let z of [0,1]){let a=new Map([[1,s]]);for(let i=2+j*m;i<2+(j+1)*m;i++)a.set(i,z);A(sat(C,a)===(s===(j===0?1:0)),"complete path");endTests+=C.length}}
 out.push({instance:f.instance,mode:m<=6?"exhaustive":"1024 deterministic samples",regionFactorCap:m-1,patterns,edges,clauseTests,checkLits,endTests,examples})
 }return out;
};
console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
