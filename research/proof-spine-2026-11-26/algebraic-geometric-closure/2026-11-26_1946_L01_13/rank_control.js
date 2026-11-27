function ck(x,m="assert"){if(!x)throw Error(m)}

function base(){const L=[[2,3,5],[6,7],[3,5],[1,4,6],[3,6,8],[0,8],[2,7],[1,6],[0,2,4]],neg=new Set(["2,5","6,7","7,6","8,2","8,4"]);return {n:9,E:L.flatMap((a,i)=>a.map(j=>[i,j,neg.has(i+","+j)?-1:1]))}}

function cy(p){let out=[],seen=new Set();for(let i=0;i<p.length;i++)if(!seen.has(i)){let c=[],j=i;while(!seen.has(j)){seen.add(j);c.push(j);j=p[j]}out.push(c)}return out}

function ref(G){let adj=Array.from({length:G.n},()=>[]);for(let [u,v,s] of G.E)adj[u].push([v,s]);let p=[],out=[],calls=0;function dfs(i,M,s){ck(++calls<=2000000,"cap");if(i===G.n){let C=cy(p);out.push({p:p.slice(),cy:C,signed:s*((G.n-C.length)%2?-1:1)});return}for(let [v,z] of adj[i])if(!(M&(1n<<BigInt(v)))){p.push(v);dfs(i+1,M|(1n<<BigInt(v)),s*z);p.pop()}}dfs(0,0n,1);return {out,calls}}

function switchGraph(k){let g=base(),n=9+2*k,a=i=>9+2*i,b=i=>10+2*i;let E=g.E.map(([u,v,s])=>[u===0?a(k-1):u===2?b(k-1):u,v,s]);E.push([0,a(0),1],[2,b(0),1]);for(let i=0;i<k-1;i++)E.push([a(i),a(i+1),1],[b(i),b(i+1),1],[a(i),b(i+1),-1],[b(i),a(i+1),1]);return {n,E}}

function lift(p,k,w){let r=p.slice(),a=i=>9+2*i,b=i=>10+2*i;r[0]=a(0);r[2]=b(0);for(let i=0;i<k-1;i++){r[a(i)]=w[i]?b(i+1):a(i+1);r[b(i)]=w[i]?a(i+1):b(i+1)}r[a(k-1)]=p[0];r[b(k-1)]=p[2];return r}

function bits(x,k){return Array.from({length:k},(_,i)=>Number((x>>BigInt(i))&1n))}

function evenWord(x,k){let w=bits(x,k-2);w.push(w.reduce((a,b)=>a^b,0));return w}

function strong(G){for(let rev of [0,1]){let seen=new Set([0]),stack=[0];while(stack.length){let u=stack.pop();for(let e of G.E)if(e[rev]===u&&!seen.has(e[1-rev])){seen.add(e[1-rev]);stack.push(e[1-rev])}}if(seen.size!==G.n)return false}return true}

function run(){let B=ref(base()).out,same=c=>c.cy.some(S=>S.includes(0)&&S.includes(2));ck(B.length===9&&B.filter(c=>c.cy.length===2).every(same));let P=B.find(c=>c.cy.length===3&&!same(c));ck(P);let all=[];
for(let k of [3,4,6,8,16,32,64]){let G=switchGraph(k);ck(strong(G));let bound=1n<<BigInt(k-2),sample=Number(bound<64n?bound:64n),rows=[],sets=[],arcMap=new Map(G.E.map(([u,v,s])=>[u+","+v,s]));let checks=0;
for(let i=0;i<sample;i++){let p=lift(P.p,k,evenWord(BigInt(i),k)),C=cy(p);ck(C.length===3);let S=C.find(c=>c.includes(2));ck(!S.includes(0));for(let u=0;u<p.length;u++)ck(arcMap.has(u+","+p[u]));rows.push(p);sets.push(S);checks+=p.length}
for(let i=0;i<sample;i++)for(let j=0;j<sample;j++){let S=new Set(sets[i]);ck([...S].every(u=>S.has(rows[j][u]))===(i===j),"minor");checks++}
let full=null;if(k<=8){let R=ref(G),T=R.out.filter(c=>c.cy.length%2);ck(R.out.length===9*2**(k-1));ck(new Set(R.out.map(c=>c.signed)).size===1&&R.out.every(c=>c.cy.length>1));ck(T.every(c=>c.cy.length<=5));let sup=G.E.every(([u,v])=>T.some(c=>c.p[u]===v));ck(sup);full={total:R.out.length,target:T.length,cycleHistogram:T.reduce((a,c)=>(a[c.cy.length]=(a[c.cy.length]||0)+1,a),{}),calls:R.calls,allTargetSupported:sup}}
all.push({k,n:G.n,arcs:G.E.length,identityRankLowerBound:bound,executedIdentitySide:sample,checkedEntries:sample*sample,checks,fullReference:full,strong:true})}
return {baseCycleLists:B.map(c=>c.cy),selectedBase:P,all,mode:"independent serial reconstruction; exhaustive reference at k<=8; polynomial sampled submatrix at larger k"}}
console.log(JSON.stringify(run(),(_,v)=>typeof v==='bigint'?v.toString():v,2));
