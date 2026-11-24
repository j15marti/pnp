// Run with node. Exact terminal-pairing reference backend, not blossom.
console.log(JSON.stringify((function run(){
let seed=0x2010610;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
const INF=Infinity;const stats={random:0,sat:0,unsat:0,referenceRows:0,referenceTuples:0,oracleCalls:0,patterns:0,verified:0,scaling:[],hostile:[]};
function tj(n,edges,T){ // exact shortest paths + terminal pairing reference; costs safe integer
 stats.oracleCalls++;let terminals=[];for(let v=0;v<n;v++)if((T>>BigInt(v))&1n)terminals.push(v);
 if(terminals.length%2)return null;if(!terminals.length)return {cost:0,mask:0n};
 let dist=[],paths=[];
 for(const s of terminals){let d=Array(n).fill(INF),p=Array(n).fill(0n),done=Array(n).fill(false);d[s]=0;
 for(let k=0;k<n;k++){let v=-1;for(let i=0;i<n;i++)if(!done[i]&&(v<0||d[i]<d[v]))v=i;if(v<0||d[v]===INF)break;done[v]=true;
 for(const e of edges){let u=e.u===v?e.v:e.v===v?e.u:-1;if(u<0||done[u])continue;if(d[v]+e.w<d[u]){d[u]=d[v]+e.w;p[u]=p[v]^(1n<<BigInt(e.id));}}}
 dist.push(terminals.map(v=>d[v]));paths.push(terminals.map(v=>p[v]));}
 const memo=new Map([[0,{cost:0,mask:0n}]]);
 function pair(mask){if(memo.has(mask))return memo.get(mask);let i=0;while(!(mask&(1<<i)))i++;let best=null;for(let j=i+1;j<terminals.length;j++)if(mask&(1<<j)){if(!Number.isFinite(dist[i][j]))continue;let a=pair(mask^(1<<i)^(1<<j));if(a&&(!best||a.cost+dist[i][j]<best.cost))best={cost:a.cost+dist[i][j],mask:a.mask^paths[i][j]};}memo.set(mask,best);return best;}
 if(terminals.length>24)throw Error("reference pairing limit");return pair((1<<terminals.length)-1);
}
const bd=e=>(1n<<BigInt(e.u))^(1n<<BigInt(e.v));
function verify(bs,K,ms){if(!ms)return false;let c=K.map(()=>0);for(let b=0;b<bs.length;b++){let t=0n;for(const e of bs[b].edges)if(ms[b]&(1n<<BigInt(e.id))){t^=bd(e);c[e.o]+=e.w;}if(t!==bs[b].T)return false;}return c.every((x,i)=>x<=K[i]);}
function solve(bs,K){ // exact forest, q=0, no tags; each block supplied with local boundary
 let inc=K.map(()=>[]);for(let b=0;b<bs.length;b++){let owners=[...new Set(bs[b].edges.map(e=>e.o))];for(let o of owners)inc[o].push(b);}
 let seenO=new Set(),seenB=new Set(),answers=Array(bs.length).fill(0n);
 function own(o,parent){if(seenO.has(o))throw Error("not forest");seenO.add(o);let cost=0,rows=[];for(let b of inc[o])if(b!==parent){let x=block(b,o);if(!x)return null;cost+=x.cost;rows.push(...x.rows);}if(cost>K[o])return null;return {cost,rows};}
 function block(b,parent){if(seenB.has(b))throw Error("not forest");seenB.add(b);let B=bs[b],groups=new Map();for(let e of B.edges){if(!groups.has(e.o))groups.set(e.o,[]);groups.get(e.o).push(e);}
 let dom=[...groups.keys()].sort((a,b)=>groups.get(b).length-groups.get(a).length||a-b)[0];let slack=new Map(),childRows=[];
 for(let o of groups.keys())if(o!==parent){let v=own(o,b);if(!v)return null;slack.set(o,K[o]-v.cost);childRows.push(...v.rows);}
 // parent owner budget is also safe to use as an upper bound.
 slack.set(parent,K[parent]);let fixed=[],free=[];for(let [o,es] of groups){if(o===dom){free.push(...es.filter(e=>e.w<=slack.get(o)));continue;}if(es.length===1&&o!==parent){if(es[0].w<=slack.get(o))free.push({...es[0],w:0});}else fixed.push(...es);}
 // Every free edge outside dominant has zero objective: its child budget has already been checked.
 let best=null;function rec(i,mask,t,c){if(i<fixed.length){let e=fixed[i];rec(i+1,mask,t,c);let w=(c.get(e.o)||0)+e.w;if(w<=slack.get(e.o)){let d=new Map(c);d.set(e.o,w);rec(i+1,mask|(1n<<BigInt(e.id)),t^bd(e),d);}return;}
 stats.patterns++;let x=tj(B.n,free,t);if(!x||x.cost>slack.get(dom))return;let pc=parent===dom?x.cost:(c.get(parent)||0);
 if(!best||pc<best.cost)best={cost:pc,rows:[[b,mask^x.mask],...childRows]};}
 rec(0,0n,B.T,new Map());return best;}
 for(let o=0;o<K.length;o++)if(!seenO.has(o)){let x=own(o,-1);if(!x)return null;for(let [b,m] of x.rows)answers[b]=m;}if(seenB.size!==bs.length)throw Error("missing block");return answers;}
 function brute(bs,K){let tables=bs.map(B=>{let a=[];for(let mask=0;mask<2**B.edges.length;mask++){stats.referenceRows++;let t=0n,c=K.map(()=>0);for(let e of B.edges)if(mask&(1<<e.id)){t^=bd(e);c[e.o]+=e.w;}if(t===B.T&&c.every((v,i)=>v<=K[i]))a.push(c);}return a;});
 function rec(i,c){if(i===tables.length)return true;for(let a of tables[i]){stats.referenceTuples++;let d=c.map((x,j)=>x+a[j]);if(d.every((x,j)=>x<=K[j])&&rec(i+1,d))return true;}return false;}return rec(0,K.map(()=>0));}
 function check(bs,K,expected){let m=solve(bs,K),got=m!==null;if(got!==expected)throw Error("decision mismatch "+JSON.stringify(K));if(m){if(!verify(bs,K,m))throw Error("witness mismatch");stats.verified++;}return got;}
 function B(n,edges,T){return {n,edges:edges.map((e,id)=>({...e,id})),T};}
 // Incidence forest: each block is attached to one existing owner and introduces new owners.
 for(let k=0;k<180;k++){let bs=[],K=[rnd(7)],h=1+rnd(4);for(let b=0;b<h;b++){let n=3+rnd(3),parent=rnd(K.length),owner1=K.length;K.push(rnd(7));let owner2=K.length;K.push(rnd(7));let es=[];for(let u=0;u<n;u++)es.push({u,v:(u+1)%n,o:[parent,owner1,owner2][rnd(3)],w:rnd(5)}); // guarantee actual attachment
 es[0].o=parent;es[1].o=owner1;es[2].o=owner2;
 for(let j=0;j<rnd(4);j++){let u=rnd(n),v=(u+1+rnd(n-1))%n;es.push({u,v,o:[parent,owner1,owner2][rnd(3)],w:rnd(5)});}
 let T=0n;for(let e of es)if(rnd(5)<2)T^=bd(e);if(k%11===0)T^=1n;bs.push(B(n,es,T));}
 let expected=brute(bs,K);check(bs,K,expected);stats.random++;stats[expected?"sat":"unsat"]++;}
 // Hostile: multi-edge child owner budget cannot be checked edgewise; required path uses both.
 let bs=[B(3,[{u:0,v:1,o:1,w:1},{u:1,v:2,o:1,w:1},{u:0,v:2,o:0,w:4},{u:0,v:2,o:0,w:5},{u:0,v:1,o:0,w:5}],5n)];
 for(let K of [[0,1],[0,2]]){let exp=brute(bs,K);check(bs,K,exp);stats.hostile.push({K,sat:exp});}
 // Dense high-rank blocks, path owner incidence, all leaf minority groups singleton.
 for(let h of [4,8,16,32,64]){let n=8+Math.floor(Math.log2(h)),bs=[],K=Array(h+1).fill(1);K[0]=0;let p=0,ell=0;
 for(let b=0;b<h;b++){let es=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)es.push({u,v,o:b,w:1});es.push({u:0,v:1,o:b+1,w:1});for(let u=2;u<n;u++)for(let v=u+1;v<n;v++){let o=K.length;K.push(1);es.push({u,v,o,w:1});}p+=es.length-n*(n-1)/2;ell=Math.max(ell,es.length-n+1);bs.push(B(n,es,3n));}
 let before=stats.oracleCalls,pat=stats.patterns;check(bs,K,true);let sc=stats.oracleCalls-before,sp=stats.patterns-pat;K[h]=0;before=stats.oracleCalls;check(bs,K,false);stats.scaling.push({blocks:h,verticesPerBlock:n,globalMinority:p,maxNullity:ell,localEnumeratedBits:0,satOracleCalls:sc,satPatterns:sp,unsatOracleCalls:stats.oracleCalls-before});}
 return stats;
})(),null,2));
