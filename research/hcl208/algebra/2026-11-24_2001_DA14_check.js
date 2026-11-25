function experiment(){
const stats={assertions:0,matching_calls:0,closure_passes:0,cycles:0,peels:0,reference_matchings:0,random:{SAT:0,UNSAT:0,UNKNOWN:0},native:{SAT:0,UNSAT:0,UNKNOWN:0,NONBIPARTITE:0}};
function check(b){stats.assertions++;if(!b)throw Error("assertion "+stats.assertions)}
function basis(){const a=[];return {a,reduce(x){for(const [v] of a){if((x^v)<x)x^=v}return x},add(x,id){let y=this.reduce(x);if(!y)return false;a.push([y,id,x]);a.sort((p,q)=>p[0]>q[0]?-1:1);return true}}}
function xor(xs){return xs.reduce((a,b)=>a^b,0n)}
function prepare(n,E){
stats.matching_calls++;const adj=Array.from({length:n},()=>[]);E.forEach((e,i)=>adj[e[0]].push(i));const R=Array(n).fill(-1);
function aug(u,seen){for(const i of adj[u]){let v=E[i][1];if(seen[v])continue;seen[v]=1;if(R[v]<0||aug(E[R[v]][0],seen)){R[v]=i;return true}}return false}
for(let u=0;u<n;u++)if(!aug(u,Array(n).fill(0)))return null;
const M=Array(n);R.forEach(i=>M[E[i][0]]=i);
const D=Array.from({length:n},()=>[]);
E.forEach((e,i)=>{if(i!==M[e[0]])D[e[0]].push({u:e[0],v:E[R[e[1]]][0],i,t:e[2]^E[M[e[0]]][2]})});
function paths(r){const p=Array(n).fill(null),q=[r];p[r]=[];for(let k=0;k<q.length;k++)for(const a of D[q[k]])if(p[a.v]===null){p[a.v]=p[q[k]].concat(a);q.push(a.v)}return p}
const pathsAll=Array.from({length:n},(_,i)=>paths(i)),seen=new Set(),blocks=[];
for(let r=0;r<n;r++){if(seen.has(r))continue;const C=Array.from({length:n},(_,i)=>i).filter(v=>pathsAll[r][v]!==null&&pathsAll[v][r]!==null);C.forEach(v=>seen.add(v));const cycles=[],B=basis();
function walk(w){if(!w.length)return;let vertices=[w[0].u],edges=[];for(const a of w){check(vertices.at(-1)===a.u);let j=vertices.indexOf(a.v);if(j>=0){let cy=edges.slice(j).concat(a),t=xor(cy.map(x=>x.t));stats.cycles++;if(B.add(t,cycles.length))cycles.push({t,cy});vertices=vertices.slice(0,j+1);edges=edges.slice(0,j)}else{vertices.push(a.v);edges.push(a)}}check(edges.length===0)}
for(const v of C){walk(pathsAll[r][v].concat(pathsAll[v][r]));for(const a of D[v])if(pathsAll[a.v][r]!==null)walk(pathsAll[r][v].concat(a,pathsAll[a.v][r]))}
blocks.push({C,cycles});
}
return {M,blocks,base:xor(M.map(i=>E[i][2]))};
}
function decide(n,E,P,target){
if(!P)return {status:"UNSAT"};
const W=basis(),choices=[],remaining=P.blocks.slice(),delta=target^P.base;
let global=basis();for(const block of remaining)for(const c of block.cycles)global.add(c.t,0);
function closure(){stats.closure_passes++;const B=basis();for(const c of choices)B.add(c.t,0);for(const block of remaining)for(const c of block.cycles)B.add(c.t,0);return B.reduce(delta)===0n}
if(!closure())return {status:"UNSAT",rank:global.a.length};
let change=true;while(change){change=false;for(let j=0;j<remaining.length;j++){const local=basis(),block=remaining[j];for(const c of block.cycles)local.add(W.reduce(c.t),0);if(local.a.length>1)continue;remaining.splice(j,1);if(local.a.length){let c=block.cycles.find(c=>W.reduce(c.t)!==0n);check(W.add(c.t,choices.length));choices.push(c)}stats.peels++;check(closure());change=true;break}}
check(closure());if(W.reduce(delta)!==0n)return {status:"UNKNOWN",rank:global.a.length,peeledRank:W.a.length};
const M=P.M.slice();let d=delta;for(let j=choices.length-1;j>=0;j--){let B=basis();for(let i=0;i<j;i++)B.add(choices[i].t,0);if(B.reduce(d)!==0n){d^=choices[j].t;for(const a of choices[j].cy)M[a.u]=a.i}}
check(d===0n);check(new Set(M.map(i=>E[i][1])).size===n);check(M.every((i,u)=>E[i][0]===u));check(xor(M.map(i=>E[i][2]))===target);
return {status:"SAT",rank:global.a.length,peeledRank:W.a.length,M};
}
function reference(n,E){let s=new Set(),adj=Array.from({length:n},()=>[]);E.forEach(e=>adj[e[0]].push(e));function go(u,used,t){if(u===n){s.add(t);stats.reference_matchings++;return}for(const e of adj[u])if(!used.has(e[1])){used.add(e[1]);go(u+1,used,t^e[2]);used.delete(e[1])}}go(0,new Set(),0n);return s}
let seed=20261124;function rnd(m){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%m}
for(let z=0;z<150;z++){let n=2+rnd(4),E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(rnd(100)<55)E.push([i,j,BigInt(rnd(16))]);let P=prepare(n,E),S=reference(n,E);check(!!P===(S.size>0));if(P){let A=basis(),B=basis();for(const t of S)A.add(t^P.base,0);for(const b of P.blocks)for(const c of b.cycles)B.add(c.t,0);check(A.a.length===B.a.length&&A.a.every(([v])=>B.reduce(v)===0n))}
for(let t=0;t<16;t++){let r=decide(n,E,P,BigInt(t));stats.random[r.status]++;check(r.status==="UNKNOWN"||((r.status==="SAT")===S.has(BigInt(t))))}}
function hostile(extra){let E=[[0,0,0n],[1,1,0n],[2,2,0n],[0,1,1n],[1,0,0n],[0,2,2n],[2,0,0n]];if(extra)E.push([3,3,0n],[4,4,0n],[3,4,1n],[4,3,0n]);let n=extra?5:3,P=prepare(n,E),S=reference(n,E),r=decide(n,E,P,3n);check(S.has(3n)===extra);check(r.status===(extra?"SAT":"UNKNOWN"));return {support:[...S].map(String),status:r.status,rank:r.rank,peeledRank:r.peeledRank}}
const obstruction=hostile(false),unlock=hostile(true);
const scale=[];for(let k of [8,32,128]){let E=[];for(let j=0;j<k;j++){let a=2*j,b=a+1;E.push([a,a,0n],[b,b,0n],[a,b,1n<<BigInt(j)],[b,a,0n])}let P=prepare(2*k,E),r=decide(2*k,E,P,(1n<<BigInt(k))-1n),s=decide(2*k,E,P,1n<<BigInt(k));check(r.status==="SAT"&&s.status==="UNSAT");scale.push({blocks:k,rank:r.rank,SAT:r.status,UNSAT:s.status})}
// I19 two native degree-four vertices, four signed parallel wires.
function native(types,sign,pin){let edges=[],N=8,dim=0;const add=(u,v,t=0n)=>edges.push([u,v,t]);for(let q=0;q<2;q++){let o=4*q;if(types[q]==="E"){let t=1n<<BigInt(dim++);add(o,o+1,t);add(o+2,o+3,t)}else{for(let j=0;j<2;j++){let d=N++;for(let i=0;i<4;i++)add(o+i,d)}}}let target=0n;for(let i=0;i<4;i++){let tag=0n;if(pin&&pin[0]===i){tag=1n<<BigInt(dim++);if(pin[1])target^=tag}if(sign>>i&1){let d=N++;add(i,d,tag);add(d,4+i)}else add(i,4+i,tag)}
let adj=Array.from({length:N},()=>[]);for(const [u,v] of edges){adj[u].push(v);adj[v].push(u)}let col=Array(N).fill(-1);for(let u=0;u<N;u++)if(col[u]<0){col[u]=0;let q=[u];for(let j=0;j<q.length;j++)for(const v of adj[q[j]]){if(col[v]===col[q[j]])return null;if(col[v]<0){col[v]=1-col[q[j]];q.push(v)}}}
let L=[],R=[];col.forEach((c,i)=>(c?R:L).push(i));if(L.length!==R.length)return {status:"UNSAT"};
let E=edges.map(([u,v,t])=>col[u]?[L.indexOf(v),R.indexOf(u),t]:[L.indexOf(u),R.indexOf(v),t]);return decide(L.length,E,prepare(L.length,E),target)}
function legal(t,x){let w=x.toString(2).replaceAll("0","").length;return t==="E"?(w===0||w===4):w===2}
for(const types of ["EE","EB","BB"])for(let s=0;s<16;s++)for(const pin of [null,[0,0],[0,1]]){let ok=false;for(let x=0;x<16;x++)if(legal(types[0],x)&&legal(types[1],x^s)&&(!pin||((x>>pin[0]&1)===pin[1])))ok=true;let r=native(types,s,pin);if(!r){stats.native.NONBIPARTITE++;continue}stats.native[r.status]++;check(r.status==="UNKNOWN"||(r.status==="SAT")===ok)}
return {seed:20261124,...stats,obstruction,unlock,scale,limitations:"No Fano or K5 source adapter; bipartite matching only; no full portfolio, no target-conditioned semantic closure, no physical CM measurements."}
}
console.log(JSON.stringify(experiment(),null,2));
