'use strict';
function runDA05(){
 const Q=[0,1,2,3], out={seed:20805,local_words:0,graph_cases:0,sat:0,unsat:0,source_words:0,physical_lifts:0,source_edge_checks:0,closure_passes:0,arc_checks:0,deleted_colors:0,root_hub_deletions:0,cut_checks:0,subspace_checks:0,guard_minima:[],benchmarks:[],discrepancies:0}; let seed=out.seed;
 function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 function ck(b,m){if(!b)throw Error(m)}
 function choices(mask){return Q.filter(x=>mask>>x&1)}
 function ac(D,E){let change=true;while(change){change=false;out.closure_passes++;for(const [u,v,s] of E){for(const [i,j] of [[u,v],[v,u]]){out.arc_checks++;let old=D[i],keep=0;for(const a of choices(old))if(choices(D[j]).some(b=>(a^b)!==s))keep|=1<<a;if(keep!==old){out.deleted_colors+=choices(old).length-choices(keep).length;D[i]=keep;change=true}if(!keep)return false}}}return true}
 function compile(n,E){let P=[];let r=n,t=n+1,z=n+2;for(const [u,v,s] of E){for(const h of [0,2]){P.push([z,r,h],[z,t,h],[z,u,0],[z,v,s^1]);z++}}return {N:z,P,r,t}}
 function rank(A){let b=[];for(let x of A){for(let j=31;j>=0&&x;j--)if((x>>>j)&1){if(b[j])x^=b[j];else{b[j]=x;break}}}return b.filter(Boolean).length}
 function spanForms(E,n,star){let a=[];for(const [u,v] of E){let A=1<<u,B=1<<v,C=(1<<(n+u))^(1<<(n+v));a.push(A^B,C);if(star)a.push(A)}return a}
 function vc(E){let V=[...new Set(E.flatMap(e=>e.slice(0,2)))];let c=0,seen=new Set();for(const v of V)if(!seen.has(v)){c++;let q=[v];seen.add(v);while(q.length){let x=q.pop();for(const [u,w] of E){let y=u===x?w:w===x?u:-1;if(y>=0&&!seen.has(y)){seen.add(y);q.push(y)}}}}return [V.length,c]}
 for(const r of Q)for(const s of Q)for(const u of Q)for(const v of Q){let ok=true;for(const h of [0,2]){let forbidden=[r^h,r^1^h,u,v^s^1];let avail=Q.filter(z=>!forbidden.includes(z));let direct=Q.some(z=>z!==(r^h)&&z!==(r^1^h)&&z!==u&&z!==(v^s^1));ck(direct===(avail.length>0),"local");ok&&=direct;}ck(ok===((u^v)!==s),"pair projection");out.local_words++}
 function graph(n,E,name){let {N,P,r,t}=compile(n,E),base=Array(N).fill(15);base[r]=1;base[t]=2;ck(ac(base,P),"root closure");for(let i=0;i<n;i++)if(base[i]!==15)out.root_hub_deletions++;ck(base.slice(0,n).every(x=>x===15),"root hub pruning");
 let models=0;
 for(let word=0;word<4**n;word++){let x=Array.from({length:n},(_,i)=>(word>>(2*i))&3);let valid=true;for(const [u,v,s] of E){out.source_edge_checks++;if((x[u]^x[v])===s)valid=false}
 let D=base.slice();for(let i=0;i<n;i++)D[i]=1<<x[i];let phys=ac(D,P);ck(phys===valid,"source physical projection");out.source_words++;if(phys){models++;let y=D.map(m=>choices(m)[0]);for(const [u,v,s] of P){ck((y[u]^y[v])!==s,"lift");out.source_edge_checks++}out.physical_lifts++}}
 if(E.length<=12)for(let mask=0;mask<2**E.length;mask++){let L=E.filter((_,i)=>(mask>>i)&1),R=E.filter((_,i)=>!((mask>>i)&1));let [vl,cl]=vc(L),[vr,cr]=vc(R),[ve,ce]=vc(E);let a=spanForms(L,n,true),b=spanForms(R,n,true),c=spanForms(E,n,true);let w=rank(a)+rank(b)-rank(c);let raw=rank(spanForms(L,n,false))+rank(spanForms(R,n,false))-rank(spanForms(E,n,false));ck(rank(a)===2*vl-cl&&rank(b)===2*vr-cr&&rank(c)===2*ve-ce,"span rank");ck(w===raw+cl+cr-ce&&w>=raw,"cut formula");out.cut_checks++}
 out.graph_cases++;out[models?"sat":"unsat"]++;if(name)out.benchmarks.push({name,n,edges:E.length,physical_vertices:N,physical_edges:P.length,source_models:models})}
 const K=Array.from({length:5},(_,u)=>Q.concat(4).filter(v=>v>u).map(v=>[u,v,0])).flat();
 graph(5,K,"K5");for(let i=0;i<K.length;i++)graph(5,K.filter((_,j)=>j!==i),"K5-e"+i);
 for(let i=0;i<10;i++)graph(5,K.map((e,j)=>j===i?[e[0],e[1],1]:e),"K5 sign "+i);
 for(let i=0;i<48;i++){let n=3+rnd(3),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(7)<4)E.push([u,v,rnd(4)]);graph(n,E)}
 // Enumerate every binary subspace in dimensions 4 and 6, independently minimize rank.
 for(const n of [2,3]){let size=1<<(2*n),spaces=[[0]],keys=new Set(["0"]);for(let i=0;i<spaces.length;i++){let H=spaces[i],has=new Set(H);for(let v=1;v<size;v++)if(!has.has(v)){let T=H.concat(H.map(x=>x^v)).sort((a,b)=>a-b),key=T.join(",");if(!keys.has(key)){keys.add(key);spaces.push(T)}}}
 let edges=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)edges.push([i,j,0]);for(let mask=1;mask<1<<edges.length;mask++){let E=edges.filter((_,i)=>mask>>i&1),opt=2*n;let planes=E.map(e=>{let [u,v]=e,A=1<<u,B=1<<v,C=(1<<(n+u))^(1<<(n+v));return Array.from({length:8},(_,i)=>((i&1)?A:0)^((i&2)?B:0)^((i&4)?C:0))});for(const H of spaces){let d=Math.log2(H.length);out.subspace_checks++;if(planes.every(P=>P.filter(x=>H.includes(x)).length>=4))opt=Math.min(opt,d)}let [v]=vc(E);ck(opt===v,"guard rank optimum");out.guard_minima.push({n,mask,subspaces:spaces.length,minimum:opt})}}
 return out;
}
console.log(JSON.stringify(runDA05(),null,2));
