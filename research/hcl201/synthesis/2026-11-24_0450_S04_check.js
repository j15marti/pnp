// Node.js, dependency free.
function run(){
const seedEdges=[[0,7],[0,13],[0,18],[0,19],[1,8],[1,15],[1,17],[1,19],[2,9],[2,10],[2,19],[2,20],[3,9],[3,11],[3,14],[3,18],[4,10],[4,12],[4,13],[4,15],[5,11],[5,13],[5,17],[5,20],[6,12],[6,14],[6,16],[6,19],[7,14],[7,15],[7,20],[8,16],[8,18],[8,20],[9,15],[9,16],[10,17],[10,18],[11,19],[12,20],[13,16],[14,17]];
let rng=0x2010450;const rnd=()=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng/4294967296};
const eq=(a,b,u,v)=>(a===u&&b===v)||(a===v&&b===u);
function decomp(n,edges,stats){
const bags=[],links=[];
function split(V,E){
const adj=new Map(V.map(v=>[v,[]]));for(const [u,v] of E){adj.get(u).push(v);adj.get(v).push(u)}
function separate(S){stats.cuts++;const seen=new Set(S),start=V.find(v=>!seen.has(v));if(start===undefined)return null;const A=[start];seen.add(start);for(let j=0;j<A.length;j++)for(const u of adj.get(A[j]))if(!seen.has(u)){seen.add(u);A.push(u)}const B=V.filter(v=>!seen.has(v));return B.length?[A,B,S]:null}
let cut=null;
if(V.length>3){cut=separate([]);for(const u of V){if(cut)break;cut=separate([u])}for(let i=0;i<V.length&&!cut;i++)for(let j=i+1;j<V.length&&!cut;j++)cut=separate([V[i],V[j]])}
if(!cut){let i=bags.length;bags.push(V);return [i]}
const [A,B,S]=cut;
function child(X){const W=X.concat(S).sort((a,b)=>a-b),set=new Set(W),F=E.filter(([u,v])=>set.has(u)&&set.has(v));if(S.length===2&&!F.some(([u,v])=>eq(u,v,...S)))F.push(S.slice());return split(W,F)}
const L=child(A),R=child(B),a=L.find(i=>S.every(v=>bags[i].includes(v))),b=R.find(i=>S.every(v=>bags[i].includes(v)));if(a===undefined||b===undefined)throw Error("missing separator bag");links.push([a,b]);return L.concat(R)
}
split(Array.from({length:n},(_,i)=>i),edges);const nb=bags.map(()=>[]);for(const [a,b] of links){nb[a].push(b);nb[b].push(a)}
for(let v=0;v<n;v++){const containing=bags.map((b,i)=>b.includes(v)?i:-1).filter(i=>i>=0),seen=new Set([containing[0]]),q=[containing[0]];for(let j=0;j<q.length;j++)for(const x of nb[q[j]])if(bags[x].includes(v)&&!seen.has(x)){seen.add(x);q.push(x)}if(seen.size!==containing.length)throw Error("running intersection")}
if(!edges.every(([u,v])=>bags.some(b=>b.includes(u)&&b.includes(v))))throw Error("missing edge");
stats.bags=bags.length;stats.maxBag=Math.max(...bags.map(b=>b.length));return {bags,nb};
}
function feat(w){let f=1n,k=1;const b=w.flatMap(c=>[c&1,(c>>1)&1]);for(let i=0;i<b.length;i++){if(b[i])f|=1n<<BigInt(k);k++}for(let i=0;i<b.length;i++)for(let j=i+1;j<b.length;j++){if(b[i]&&b[j])f|=1n<<BigInt(k);k++}return f}
function add(B,w){let f=feat(w);while(f){const k=f.toString(2).length-1;if(B.has(k))f^=B.get(k).f;else{B.set(k,{f,w});return}}}
const witnesses=B=>[...B.values()].map(x=>x.w);
function contains(B,w){let f=feat(w);while(f){const k=f.toString(2).length-1;if(!B.has(k))return false;f^=B.get(k).f}return true}
function solve(n,edges,features=false){
const stats={cuts:0,bags:0,maxBag:0,bagNodes:0,products:0,tableCells:0,closureEmpty:0,closureForced:0};
const {bags,nb}=decomp(n,edges,stats);
function visit(i,parent){
const V=bags[i],S=parent<0?[]:V.filter(v=>bags[parent].includes(v)),local=edges.filter(([u,v])=>V.includes(u)&&V.includes(v)),children=nb[i].filter(j=>j!==parent).map(j=>visit(j,i)),T=new Map();
const key=(w,P)=>P.map(v=>w[v]).join("");
const order=V.filter(v=>!S.includes(v)).sort((a,b)=>local.filter(e=>e.includes(b)).length-local.filter(e=>e.includes(a)).length);
function forPin(w,j){
if(j<S.length){for(let c=1;c<=3;c++){w[S[j]]=c;forPin(w,j+1)}w[S[j]]=0;return}
let result=features?new Map():null;
function dfs(k){
stats.bagNodes++;
if(local.some(([u,v])=>w[u]&&w[v]&&w[u]===w[v]))return false;
for(const ch of children)if(ch.S.every(v=>w[v])&&!ch.T.has(key(w,ch.S)))return false;
if(k<order.length){const v=order[k];for(let c=1;c<=3;c++){w[v]=c;if(dfs(k+1)&&!features){w[v]=0;return true}}w[v]=0;return false}
let B=features?new Map():null,one=w.slice();if(features)add(B,one);
for(const ch of children){const cell=ch.T.get(key(w,ch.S));if(!cell)throw Error("missing compatible cell");if(features){const next=new Map();for(const a of witnesses(B))for(const b of witnesses(cell)){stats.products++;add(next,a.map((c,j)=>c||b[j]))}B=next}else one=one.map((c,j)=>c||cell[j])}
if(features){for(const a of witnesses(B))add(result,a);return false}result=one;return true
}
dfs(0);const q=key(w,S);stats.tableCells++;if(features?result.size:result)T.set(q,result);else stats.closureEmpty++;
}
forPin(Array(n).fill(0),0);
if(S.length===2){const same=[...T.keys()].some(k=>k[0]===k[1]),diff=[...T.keys()].some(k=>k[0]!==k[1]);if(same!==diff)stats.closureForced++}
return {S,T};
}
const root=visit(0,-1),cell=root.T.get(""),ws=cell?(features?witnesses(cell):[cell]):[];
for(const w of ws)if(w.some(c=>!c)||edges.some(([u,v])=>w[u]===w[v]))throw Error("invalid witness");
return {sat:!!cell,ws,stats};
}
function reference(n,E){const B=new Map(),w=Array(n).fill(0);let count=0;function rec(i){if(i===n){if(E.every(([u,v])=>w[u]!==w[v])){count++;add(B,w.slice())}return}for(let c=1;c<=3;c++){w[i]=c;rec(i+1)}}rec(0);return {B,count}}
const small={graphs:0,sat:0,unsat:0,assignments:0,basisWitnesses:0,products:0,maxBag:0,cutChecks:0,forcedMessages:0,emptyCells:0};function check(n,E){const a=solve(n,E,true),b=reference(n,E),B=new Map();a.ws.forEach(w=>add(B,w));if(a.sat!==(b.count>0)||B.size!==b.B.size||!witnesses(b.B).every(w=>contains(B,w))||!witnesses(B).every(w=>contains(b.B,w)))throw Error("span mismatch");small.graphs++;small[a.sat?"sat":"unsat"]++;small.assignments+=3**n;small.basisWitnesses+=B.size;small.products+=a.stats.products;small.maxBag=Math.max(small.maxBag,a.stats.maxBag);small.cutChecks+=a.stats.cuts;small.forcedMessages+=a.stats.closureForced;small.emptyCells+=a.stats.closureEmpty}
for(let n=1;n<=4;n++){const all=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)all.push([i,j]);for(let mask=0;mask<2**all.length;mask++)check(n,all.filter((_,i)=>mask&(1<<i)))}
for(let t=0;t<90;t++){const n=5+(t%3),E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rnd()<(.12+.7*(t%9)/8))E.push([i,j]);check(n,E)}
function chain(h){let n=21,E=seedEdges.map(e=>e.slice()),out=[1,8];for(let i=1;i<h;i++){const [a,b]=out,map=[a,...Array.from({length:20},(_,j)=>n+j)];E=E.filter(([u,v])=>!eq(u,v,a,b));for(const [u,v] of seedEdges)if(!eq(u,v,0,7))E.push([map[u],map[v]]);E.push([b,map[7]]);out=[map[1],map[8]];n+=20}return {n,E,out}}
const scaling=[];for(const h of [1,2,4,8,16]){const {n,E,out}=chain(h),a=solve(n,E),b=solve(n,E.filter(([u,v])=>!eq(u,v,...out)));if(a.sat||!b.sat||Math.max(a.stats.maxBag,b.stats.maxBag)>21)throw Error("chain mismatch");scaling.push({h,n,m:E.length,unsat:a.stats,sat:b.stats,witnessVerified:true})}
return {seed:0x2010450,small,scaling};
}
console.log(JSON.stringify(run(),null,2));
