function BW14(){
 const stats={closurePasses:0,forcedPins:0,matchingAugmentations:0,cycleFactors:0,referenceWords:0,nativeWitnessChecks:0,decisions:0,assertions:0}, results={random:{SAT:0,UNSAT:0,UNKNOWN:0},fano:[],scaling:[],hostile:[]};
 const assert=(x,m)=>{stats.assertions++;if(!x)throw Error(m)};
 const rng=(()=>{let s=20261124;return n=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s%n}})();
 // star [a,b,c,sa,sb,sc,t], high equation h_b xor h_c=t when active
 function native(s,x){const [a,b,c,sa,sb,sc,t]=s;return [x[a]^sa,x[a]^sa^2,x[b]^sb^1,x[c]^sc^3^(2*(1^t))]}
 function highs(n,S,lo,partial=false){const adj=Array.from({length:n},()=>[]);for(const [a,b,c,sa,sb,sc,t] of S){if(lo[a]<0||lo[b]<0||lo[c]<0)continue;if((lo[a]^sa)===(lo[b]^sb)&&(lo[a]^sa)===(lo[c]^sc)){adj[b].push([c,t]);adj[c].push([b,t])}}
 const h=Array(n).fill(-1);for(let a=0;a<n;a++)if(h[a]<0){h[a]=0;const q=[a];for(let i=0;i<q.length;i++){let u=q[i];for(const [v,t] of adj[u]){let z=h[u]^t;if(h[v]<0){h[v]=z;q.push(v)}else if(h[v]!==z)return null}}}return h}
 function cycles(n,S){const tree=Array.from({length:n},()=>[]),p=Array.from({length:n},(_,i)=>i),used=new Set(),out=[];function root(i){while(p[i]!==i)i=p[i];return i}
 for(let k=0;k<S.length;k++){const [,b,c]=S[k],u=root(b),v=root(c);if(u!==v){p[u]=v;tree[b].push([c,k]);tree[c].push([b,k]);continue}
 const q=[b],prev=new Map([[b,[-1,-1]]]);for(let j=0;j<q.length&&!prev.has(c);j++)for(const [w,e] of tree[q[j]])if(!prev.has(w)){prev.set(w,[q[j],e]);q.push(w)}
 let z=c,es=[k];while(z!==b){const [w,e]=prev.get(z);es.push(e);z=w}if(es.some(e=>used.has(e)))return null;for(const e of es)used.add(e);out.push(es)}
 return out}
 function factor(n,S,es){if(es.reduce((p,e)=>p^S[e][6],0)===0)return null;const adj=Array.from({length:n},()=>[]),vars=new Set();for(const e of es){const [a,b,c,sa,sb,sc]=S[e];vars.add(a);vars.add(b);vars.add(c);adj[a].push([b,sa^sb],[c,sa^sc]);adj[b].push([a,sa^sb]);adj[c].push([a,sa^sc])}
 const root=vars.values().next().value,alpha=new Map([[root,0]]),q=[root];for(let i=0;i<q.length;i++)for(const [v,t] of adj[q[i]]){const z=alpha.get(q[i])^t;if(!alpha.has(v)){alpha.set(v,z);q.push(v)}else if(alpha.get(v)!==z)return null}
 assert(alpha.size===vars.size,"connected cycle activation");return [...alpha.entries()]}
 function solve(n,S,pins){stats.decisions++;const deg=Array(n).fill(0);for(const [a,b,c,sa,sb,sc,t] of S){assert(new Set([a,b,c]).size===3,"distinct ports");deg[a]+=2;deg[b]++;deg[c]++}
 const lo=pins.slice();stats.closurePasses++;if(!highs(n,S,lo,true))return {label:"UNSAT"};if(deg.some(d=>d>4))return {label:"UNKNOWN"};
 const cs=cycles(n,S);if(cs===null)return {label:"UNKNOWN"};const F=cs.map(es=>factor(n,S,es)).filter(Boolean);stats.cycleFactors+=F.length;const occ=Array(n).fill(0);for(const f of F)for(const [v] of f)occ[v]++;assert(occ.every((v,i)=>2*v<=deg[i]),"owner incidence charge");
 let rows;while(true){stats.closurePasses++;if(!highs(n,S,lo,true))return {label:"UNSAT"};rows=[];let pin=null;for(const f of F){const known=new Set(),free=[];for(const [v,s] of f){if(lo[v]<0)free.push([v,s]);else known.add(lo[v]^s)}
 if(known.size===2)continue;
 if(!known.size){assert(free.length>=3,"NAE arity");rows.push({nae:true,lits:free});continue}
 const k=known.values().next().value;if(!free.length)return {label:"UNSAT"};
 const lits=free.map(([v,s])=>[v,s^k]); // at least one signed bit is 1
 if(lits.length===1){pin=[lits[0][0],1^lits[0][1]];break}rows.push({nae:false,lits})}
 if(!pin)break;lo[pin[0]]=pin[1];stats.forcedPins++}
 // Bipartite augmenting-path matching, distinct pivot per remaining owner.
 const owner=Array(n).fill(-1),pivot=Array(rows.length).fill(-1);
 function aug(i,seen){for(const [v] of rows[i].lits)if(!seen[v]){seen[v]=true;if(owner[v]<0||aug(owner[v],seen)){owner[v]=i;pivot[i]=v;return true}}return false}
 for(let i=0;i<rows.length;i++){assert(aug(i,Array(n).fill(false)),"Hall");stats.matchingAugmentations++}
 // Assign OR pivots first and all unmatched vertices. NAE pivots follow a decreasing distance dependency.
 const reverse=Array.from({length:n},()=>[]),dist=Array(n).fill(-1),next=Array(n).fill(-1),q=[];
 for(let v=0;v<n;v++)if(owner[v]<0||!rows[owner[v]].nae){if(lo[v]<0)lo[v]=owner[v]<0?0:1^rows[owner[v]].lits.find(x=>x[0]===v)[1];dist[v]=0;q.push(v)}
 for(let i=0;i<rows.length;i++)if(rows[i].nae){const v=pivot[i];for(const [w] of rows[i].lits)if(w!==v)reverse[w].push(v)}
 for(let i=0;i<q.length;i++)for(const v of reverse[q[i]])if(dist[v]<0){dist[v]=dist[q[i]]+1;next[v]=q[i];q.push(v)}
 assert(dist.every(d=>d>=0),"acyclic escape");for(const v of q)if(next[v]>=0){const R=rows[owner[v]].lits,w=next[v];lo[v]=1^lo[w]^R.find(x=>x[0]===w)[1]^R.find(x=>x[0]===v)[1]}
 const h=highs(n,S,lo);assert(h!==null,"high reconstruction");const x=lo.map((l,i)=>l+2*h[i]);const centers=S.map(s=>[0,1,2,3].find(c=>!native(s,x).includes(c)));assert(centers.every(c=>c!==undefined),"center reconstruction");assert(pins.every((p,i)=>p<0||(x[i]&1)===p),"pins preserved");for(let i=0;i<S.length;i++){assert(!native(S[i],x).includes(centers[i]),"source verify");stats.nativeWitnessChecks++}return {label:"SAT",x,centers}}
 function brute(n,S,pins){const x=Array(n).fill(0);function dfs(i){if(i===n){stats.referenceWords++;return S.every(s=>new Set(native(s,x)).size<4)}for(let c=0;c<4;c++)if(pins[i]<0||(c&1)===pins[i]){x[i]=c;if(dfs(i+1))return true}return false}return dfs(0)}
 // Random strict-degree cactus, up to 8 terminals, random signs and pins.
 for(let trial=0;trial<160;trial++){const n=6+rng(3),deg=Array(n).fill(0),S=[],add=(a,b,c)=>{if(a===b||a===c||b===c||deg[a]>2||deg[b]>3||deg[c]>3)return false;deg[a]+=2;deg[b]++;deg[c]++;S.push([a,b,c,rng(2),rng(2),rng(2),rng(2)]);return true};
 // one two-edge cycle plus either bridge or second disjoint two-edge cycle
 add(2,0,1);add(3,0,1);if(trial%2===0){add(0,4,5);add(1,4,5)}else add(4,1,5);if(n>6&&trial%3===0)add(5,0,6);
 // force genuine random bits using higher bits of PRNG via larger modulus
 for(const s of S)for(let j=3;j<7;j++)s[j]=rng(256)>>7;
 const pins=Array.from({length:n},()=>{let z=rng(256);return z<96?-1:(z>>7)});const a=solve(n,S,pins),b=brute(n,S,pins);assert(a.label!=="UNKNOWN","random eligibility");assert((a.label==="SAT")===b,"random reference");results.random[a.label]++}
 // Signed Fano root, sign neighbors and one-budget neighbors. Each owner has its own actual port copies,
 // supplied low chart is pinned, and every query charged. No free physical synchronization claim.
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const variants=[{name:"root"}];for(let i=0;i<7;i++)for(let j=0;j<3;j++)variants.push({name:`sign-${i}-${j}`,i,j});for(let i=0;i<7;i++)for(let b=0;b<2;b++)variants.push({name:`budget-${i}-${b}`,i,b});
 for(const v of variants){let count=0;for(let w=0;w<128;w++){const S=[],pins=[];let ref=true;for(let i=0;i<7;i++){let vals=lines[i].map(x=>(w>>x)&1),sign=[0,0,0];if(v.i===i&&v.j!==undefined)sign[v.j]=1;let signed=vals.map((x,j)=>x^sign[j]);let base=pins.length;if(v.i===i&&v.b!==undefined){let sg=v.b; pins.push(vals[0],vals[1],vals[2],0);S.push([base,base+2,base+3,sg,sg,0,0],[base+1,base+2,base+3,sg,sg,0,1]);ref&&=vals.some(x=>(x^sg)===1)}else{pins.push(...vals);S.push([base,base+1,base+2,...sign,0],[base,base+1,base+2,...sign,1]);ref&&=new Set(signed).size>1}}
 const a=solve(pins.length,S,pins);assert((a.label==="SAT")===ref,"Fano fiber");if(ref)count++}assert(count===(v.name==="root"?0:v.j!==undefined?10:5),"Fano model count");results.fano.push({name:v.name,models:count})}
 // Coupled cycles sharing pivot variables with opposite low signs, all endpoint lows pinned.
 for(const k of [4,16,64,256]){let S=[],pins=Array(3*k).fill(-1);for(let i=0;i<2*k;i++)pins[i]=0;for(let i=0;i<k;i++){let a=2*k+i,b=2*k+(i+1)%k;S.push([a,2*i,2*i+1,0,0,0,0],[b,2*i,2*i+1,1,0,0,1])}
 let a=solve(3*k,S,pins);assert(a.label==="SAT","large coupled cycles");let pinBad=pins.slice();pinBad[2*k]=0;pinBad[3*k-1]=1;let b=solve(3*k,S,pinBad);assert(b.label==="UNSAT","large pin contradiction");results.scaling.push({cycles:k,terminals:3*k,SAT:a.label,UNSAT:b.label})}
 // A theta/three parallel edges is outside cactus; degree-bounded by distributing pivots.
 const theta=[[2,0,1,0,0,0,0],[3,0,1,0,0,0,1],[4,0,1,0,0,0,0]];
 const th=solve(5,theta,Array(5).fill(-1));assert(th.label==="UNKNOWN","theta declined");results.hostile.push({name:"three parallel endpoint edges",label:th.label,reference:brute(5,theta,Array(5).fill(-1))});
 return {seed:20261124,stats,results};
}
console.log(JSON.stringify(BW14(),null,2));
