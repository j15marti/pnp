/* TMR-5/047 independent deterministic V8 verification; no external dependencies. */
function run(){
 let assertions=0; const A=(cond,msg)=>{assertions++;if(!cond)throw Error(msg)};
 const ev=(n,G,x)=>{let v=x.slice();for(const [op,a,b] of G)v.push(op==="NOT" ? 1-v[a] : op==="AND" ? v[a]&v[b] : v[a]|v[b]);return v};
 const prune=(n,G)=>{let needed=new Set([n+G.length-1]);for(let j=G.length-1;j>=0;j--){if(!needed.has(n+j))continue;let [op,a,b]=G[j];needed.add(a);if(op!=="NOT")needed.add(b)}let indices=[...Array(G.length).keys()].filter(j=>needed.has(n+j)), map=new Map([...Array(n).keys()].map(i=>[i,i]));indices.forEach((j,i)=>map.set(n+j,n+i));return indices.map(j=>{let[op,a,b]=G[j];return[op,map.get(a),op==="NOT"?null:map.get(b)]})};
 const cnf=(n,G)=>{let cls=[];const add=(...a)=>cls.push([...new Set(a)].sort((x,y)=>x-y));for(let j=0;j<G.length;j++){let[op,a,b]=G[j],z=n+j+1,u=a+1,v=b===null?0:b+1;if(op==="AND"){add(-z,u);add(-z,v);add(z,-u,-v)}else if(op==="OR"){add(z,-u);add(z,-v);add(-z,u,v)}else{add(-z,-u);add(z,u)}}add(n+G.length);let used=new Set(cls.flat().map(Math.abs));for(let i=1;i<=n;i++)if(!used.has(i))add(i,-i);return [...new Map(cls.map(c=>[c.join(","),c])).values()]};
 const sat=(cls,a)=>cls.every(c=>c.some(l=>l>0?a[l-1]:1-a[-l-1]));
 const ass=(n)=>Array.from({length:1<<n},(_,i)=>Array.from({length:n},(_,j)=>(i>>j)&1));
 let caseCount=0, fullAssignments=0;
 for(let n=1;n<=4;n++)for(let g=1;g<=4;g++)for(let typ=0;typ<5;typ++){
  let base=[["NOT",0,null],["AND",0,0],["OR",0,0],["AND",0,Math.min(1,n-1)],["OR",0,Math.min(1,n-1)]];
  let G=[];for(let j=0;j<g;j++){let [op,a,b]=base[(typ+j)%5];if(j>=1&&typ%2===1)a=n+j-1;G.push([op,a,b])}
  let P=prune(n,G),C=cnf(n,G),CP=cnf(n,P);
  A(C.length>=2*g+1,"min clauses");A(C.length<=3*g+n+1,"max clauses");A(CP.length>=2*P.length+1,"pruned min");
  A(C.every(c=>c.length<=3),"width");A(new Set(C.flat().map(Math.abs)).size===n+g,"every var");A(new Set(C.map(c=>c.join(","))).size===C.length,"nodup");
  for(let x of ass(n)){let y=ev(n,G,x);A(y.at(-1)===ev(n,P,x).at(-1),"prune");A(!!sat(C,y)===!!y.at(-1),"ext orig");let yy=ev(n,P,x);A(!!sat(CP,yy)===!!yy.at(-1),"ext prune")}
  if(n<=3){for(let w of ass(n+g)){if(sat(C,w)){let z=ev(n,G,w.slice(0,n));A(w.every((v,i)=>v===z[i]),"unique extension")};fullAssignments++}}
  caseCount++;
 }
 let padding=[];for(let n of [4,8,16,32,64,128]){let g=n*n;let G=Array.from({length:g-1},()=>["AND",0,1]);G.push(["OR",0,0]);let P=prune(n,G);A(P.length===1,"dead prune");padding.push({n,g_original:g,g_live:P.length,V_raw:n+g,V_live:n+1,satisfying_inputs:"2^"+(n-1)})}
 const gf2rank=(rows)=>{let b={};for(let x0 of rows){let x=x0;while(x){let p=Math.floor(Math.log2(x));if(b[p]!==undefined)x^=b[p];else{b[p]=x;break}}}return Object.keys(b).length};
 const disj=(x)=>{for(let i=0;i<x.length/2;i++)if(x[2*i]&&x[2*i+1])return 0;return 1};
 const dRows=[];for(let k=1;k<=4;k++){let rows=[];for(let i=0;i<(1<<k);i++){let row=0;for(let j=0;j<(1<<k);j++)if([...Array(k).keys()].every(h=>!((i>>h&1)&&(j>>h&1))))row|=(1<<j);rows.push(row)}let r=gf2rank(rows);A(r===(1<<k),"DISJ rank");dRows.push({k,rankGF2:r,satisfying_assignments:3**k})}
 const perm=(arr)=>{if(arr.length===0)return [[]];return arr.flatMap((v,i)=>perm(arr.filter((_,j)=>j!==i)).map(p=>[v,...p]))};
 const bdd=(ord)=>{let U=new Map(),next=2;function v(p,x){if(p===6)return disj(x);let a=x.slice();a[ord[p]]=0;let lo=v(p+1,a);a[ord[p]]=1;let hi=v(p+1,a);if(lo===hi)return lo;let key=ord[p]+":"+lo+":"+hi;if(!U.has(key))U.set(key,next++);return U.get(key)}v(0,[0,0,0,0,0,0]);return U.size};
 const rankCut=(ord,p)=>{let rows=[];for(let i=0;i<(1<<p);i++){let row=0;for(let j=0;j<(1<<(6-p));j++){let x=Array(6).fill(0);for(let t=0;t<p;t++)x[ord[t]]=(i>>t)&1;for(let t=p;t<6;t++)x[ord[t]]=(j>>(t-p))&1;if(disj(x))row|=1<<j}rows.push(row)}return gf2rank(rows)};
 let res=perm([0,1,2,3,4,5]).map(order=>({nodes:bdd(order),rank:Math.max(...Array.from({length:7},(_,p)=>rankCut(order,p)))}));
 let obdd={orders:res.length,min_nodes:Math.min(...res.map(r=>r.nodes)),max_nodes:Math.max(...res.map(r=>r.nodes)),min_peak_rank:Math.min(...res.map(r=>r.rank)),max_peak_rank:Math.max(...res.map(r=>r.rank)),node_optimal_orders:res.filter(r=>r.nodes===6).length};
 A(obdd.orders===720&&obdd.min_nodes===6&&obdd.max_nodes===14&&obdd.min_peak_rank===2&&obdd.max_peak_rank===8&&obdd.node_optimal_orders===48,"OBDD peer");
 for(let T=1;T<=2000;T++){let v=Infinity;for(let b=1;b<=T;b++)v=Math.min(v,Math.max(b,Math.ceil(T/b)));A(v===Math.ceil(Math.sqrt(T)),"tree materialized protocol")}
 let rows=[];for(let n of [256,1024,4096,16384,65536]){let L=Math.log2(n);for(let [kind,g] of [["logpow045",Math.floor(n*L**0.45)],["rootlog_over_loglog",Math.floor(n*Math.sqrt(L)/Math.log2(L))],["rootlog",Math.floor(n*Math.sqrt(L))],["quadratic",n*n]]){let V=n+g,m=3*g+n+1,Em=3*m/Math.sqrt(Math.log2(m)),Ev=9*V*Math.log2(Math.log2(V))/Math.sqrt(Math.log2(V));rows.push({n,kind,g,V,m_upper:m,Em_per_n:+(Em/n).toFixed(6),Ev_per_n:+(Ev/n).toFixed(6),envelope_per_n:+(Math.min(Em,Ev)/n).toFixed(6)})}}
 return {version:"tmr5_livegate_threshold047.v1",timezone:"America/Los_Angeles",date:"2026-11-15",seed:null,assertions,circuit_cases:caseCount,fully_enumerated_aux_assignments:fullAssignments,zero_failures:true,padded_deadgate:padding,DISJ:dRows,OBDD_DISJ3:obdd,graph_protocol:{tested_T:2000,optimum:"ceil(sqrt(T))",model:"physically materialized ceil(T/b) graph guess plus b-bit register"},source_envelope:rows,source_revision:"anthropics/formal-math@16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc",scope:"finite tests computational; symbolic live-gate bound conditional on pinned MainTheorem; no general SAT runtime lower bound"};
}
const output=run();
if(typeof console!=="undefined")console.log(JSON.stringify(output,null,2));
