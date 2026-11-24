function main(){
 const counts={bag_words:0,local_edge_checks:0,separator_lookups:0,table_cells:0,peak_retained_cells:0,closure_edge_scans:0,reconstructed_edges:0,discovery_bag_tests:0};
 const assert=(b,s)=>{if(!b)throw Error(s)};
 let seed=921208;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
 function graph(k){let E=[],bags=[[0,1,2,3,4]],T=[],n=5;for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E.push([i,j]);let edge=[0,1],oldBag=0;for(let j=1;j<k;j++){let [u,v]=edge;let newV=n;let B=[u,n,n+1,n+2,n+3];n+=4;let b1=bags.length,b2=b1+1;bags.push([u,v,newV],B);T.push([oldBag,b1],[b1,b2]);let i=E.findIndex(([a,b])=>(a===u&&b===v)||(a===v&&b===u));assert(i>=0,"join edge");E.splice(i,1);for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)if(a!==0||b!==1)E.push([B[a],B[b]]);E.push([v,newV]);edge=[newV,newV+1];oldBag=b2}return {n,E,bags,T}}
 function balanced(n,E){let A=Array.from({length:n},()=>[]),v=Array(n).fill(-1);for(let [a,b,s] of E){A[a].push([b,s]);A[b].push([a,s])}for(let i=0;i<n;i++)if(v[i]<0){v[i]=0;let q=[i];for(let j=0;j<q.length;j++)for(let [w,s] of A[q[j]]){let x=v[q[j]]^s;if(v[w]<0){v[w]=x;q.push(w)}else if(v[w]!==x)return false}}return true}
 function solve(G,E){let {n,bags,T}=G;
 // Unconditional scoped closure: self-loop rejection and exact parallel-mask merge; no external pins.
 let masks=new Map();for(let [a,b,s] of E){counts.closure_edge_scans++;if(a===b){if(!s)return null;continue}let key=[Math.min(a,b),Math.max(a,b)].join(",");let mask=(masks.get(key)||0)|(1<<s);masks.set(key,mask);if(mask===15)return null}
 // Authenticate tree, running intersection, and exact edge ownership.
 let adj=bags.map(()=>[]);for(let [a,b] of T){adj[a].push(b);adj[b].push(a)}let par=Array(bags.length).fill(-2),order=[0];par[0]=-1;for(let i=0;i<order.length;i++)for(let v of adj[order[i]])if(par[v]===-2){par[v]=order[i];order.push(v)}assert(order.length===bags.length&&T.length===bags.length-1,"tree");
 for(let v=0;v<n;v++){let B=bags.map((b,i)=>b.includes(v)?i:-1).filter(i=>i>=0);assert(B.length&&B.filter(i=>par[i]<0||!bags[par[i]].includes(v)).length===1,"running intersection")}
 let local=bags.map(()=>[]);for(let e of E){let i=bags.findIndex(b=>{counts.discovery_bag_tests++;return b.includes(e[0])&&b.includes(e[1])});assert(i>=0,"edge covered");local[i].push(e)}
 let sep=bags.map((b,i)=>par[i]<0?[]:b.filter(v=>bags[par[i]].includes(v)).sort((a,b)=>a-b));let tab=bags.map(()=>new Map()),cells=0;
 const key=(B,w,S)=>S.map(v=>w[B.indexOf(v)]).join("");
 for(let i of order.slice().reverse()){let B=bags[i],children=adj[i].filter(v=>par[v]===i);for(let z=0;z<4**B.length;z++){counts.bag_words++;let w=B.map((_,j)=>z>>(2*j)&3),ok=true;for(let [a,b,s] of local[i]){counts.local_edge_checks++;if((w[B.indexOf(a)]^w[B.indexOf(b)])===s){ok=false;break}}if(!ok)continue;for(let c of children){counts.separator_lookups++;if(!tab[c].has(key(B,w,sep[c]))){ok=false;break}}if(!ok)continue;let k=key(B,w,sep[i]);if(!tab[i].has(k)){tab[i].set(k,w);cells++;counts.table_cells++}}}
 counts.peak_retained_cells=Math.max(counts.peak_retained_cells,cells);if(!tab[0].has(""))return null;let x=Array(n).fill(-1);for(let i of order){let B=bags[i],k=sep[i].map(v=>x[v]).join(""),w=tab[i].get(k);assert(w,"lift record");B.forEach((v,j)=>{assert(x[v]<0||x[v]===w[j],"lift agreement");x[v]=w[j]})}for(let [a,b,s] of E){counts.reconstructed_edges++;assert((x[a]^x[b])!==s,"lift source")}return x
 }
 let out=[];for(let k of [1,2,4,8,16,32]){let G=graph(k),{n,E,bags}=G;let sat=0,unsat=0,deletions=0,perturb=0,random=0;function test(signed,expected){let x=solve(G,signed);assert(!!x===expected,"Hajos theorem");if(x)sat++;else unsat++}
 let zero=E.map(([a,b])=>[a,b,0]);test(zero,false);
 let gauge=Array.from({length:n},()=>rnd(4)),bal=E.map(([a,b])=>[a,b,gauge[a]^gauge[b]]);assert(balanced(n,bal),"gauge");test(bal,false);
 for(let j=0;j<20;j++){let Z=E.map(([a,b])=>[a,b,rnd(4)]);test(Z,!balanced(n,Z));random++}
 if(k<=8)for(let i=0;i<E.length;i++){test(zero.filter((_,j)=>j!==i),true);deletions++;for(let s=1;s<4;s++){let Z=zero.map((e,j)=>j===i?[e[0],e[1],s]:e);assert(!balanced(n,Z),"nonbridge");test(Z,true);perturb++}}
 else for(let i of [0,Math.floor(E.length/2),E.length-1]){test(zero.filter((_,j)=>j!==i),true);deletions++;for(let s=1;s<4;s++){let Z=zero.map((e,j)=>j===i?[e[0],e[1],s]:e);assert(!balanced(n,Z),"nonbridge");test(Z,true);perturb++}}
 out.push({blocks:k,n,m:E.length,cycle_rank:E.length-n+1,syndrome_dimension:2*(E.length-n+1),bags:bags.length,max_bag:Math.max(...bags.map(b=>b.length)),sat,unsat,deletions,perturb,random})}
 return {seed:921208,scales:out,counters:counts};
}
console.log(JSON.stringify(main(),null,2));
