// Node.js: node signed_audit.js
function signedAudit(){
let seed=20261126,checks=0;function ok(x){checks++;if(!x)throw Error("check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
function build(k,yes){let F=[[],[],[],[]];for(let i=0;i<k;i++)for(let j=0;j<4;j++)for(let l=0;l<3;l++){let c=AG[j][l].map(v=>9*i+v);if(j===0&&(l===0||(yes&&l===1)))c[2]=9*((i+1)%k)+AG[j][l][2];F[j].push({c,s:0})}return F}
const evalClause=(c,x)=>(x(c[0])^x(c[1]))+2*(x(c[0])^x(c[2]));
const valid=(F,x)=>F.flat().every(({c,s})=>evalClause(c,v=>x[v])!==s);
function solve(F,n){
let adj=Array.from({length:n},()=>[]);for(let {c} of F.slice(1).flat())for(let v of c)for(let u of c)if(u!==v)adj[v].push(u);
let B=[],id=Array(n).fill(-1);for(let v=0;v<n;v++)if(id[v]<0){let i=B.length,Q=[v];id[v]=i;for(let j=0;j<Q.length;j++)for(let u of adj[Q[j]])if(id[u]<0){id[u]=i;Q.push(u)}B.push(Q)}
let k=B.length,local=B.map(()=>[]),cross=B.map(()=>[]),out=B.map(()=>[]),next=Array(k).fill(-1),prev=Array(k).fill(-1);
for(let f of F.flat()){let a=f.c.map(v=>id[v]);if(a.every(z=>z===a[0]))local[a[0]].push(f);else{let q=a.findIndex(z=>a.filter(y=>y===z).length===1);ok(q>=0);let src=a.find((_,j)=>j!==q),dst=a[q];ok(next[src]===-1||next[src]===dst);ok(prev[dst]===-1||prev[dst]===src);next[src]=dst;prev[dst]=src;cross[src].push(f);out[dst].push(f.c[q])}}
out.forEach(a=>a.sort((x,y)=>x-y));let h=out[0].length,K=2**h;ok(h===1||h===2);ok(out.every(a=>a.length===h&&new Set(a).size===h));let order=[0];for(let i=1;i<k;i++)order.push(next[order[i-1]]);ok(new Set(order).size===k&&next[order[k-1]]===0);
let tables=B.map((V,i)=>{ok(V.length===9);let pos=new Map(V.map((v,j)=>[v,j])),other=new Map(out[next[i]].map((v,j)=>[v,j])),T=Array.from({length:K},()=>Array(K).fill(-1));for(let w=0;w<512;w++){let x=v=>w>>pos.get(v)&1;if(!local[i].every(({c,s})=>evalClause(c,x)!==s))continue;let a=out[i].reduce((a,v,j)=>a+(x(v)<<j),0);for(let b=0;b<K;b++)if(cross[i].every(({c,s})=>evalClause(c,v=>id[v]===i?x(v):b>>other.get(v)&1)!==s))T[a][b]=w}return T});
for(let a=0;a<K;a++){let reachable=Array(K).fill(false);reachable[a]=true;let history=[];for(let i of order){let p=Array(K).fill(-1);for(let u=0;u<K;u++)if(reachable[u])for(let v=0;v<K;v++)if(tables[i][u][v]>=0)p[v]=u;history.push(p);reachable=p.map(u=>u>=0)}if(!reachable[a])continue;let x=Array(n),v=a;for(let j=k-1;j>=0;j--){let i=order[j],u=history[j][v],w=tables[i][u][v];B[i].forEach((z,l)=>x[z]=w>>l&1);v=u}ok(v===a&&valid(F,x));return x}
return null}
function brute(F,n){let C=F.flat();for(let w=0;w<2**n;w++)if(C.every(({c,s})=>evalClause(c,v=>w>>v&1)!==s))return true;return false}
function relabel(F,n){let p=shuffle(Array.from({length:n},(_,i)=>i));return F.map(P=>shuffle(P.map(({c,s})=>({c:c.map(v=>p[v]),s}))))}
let results=[];for(let k of [2,4,16,64,256])for(let yes of [false,true]){let n=9*k,stats={k,yes,n,checked:0,sat:0,unsat:0,exhaustive:0};for(let q=0;q<12;q++){let F=build(k,yes);if(q>0&&q<6)for(let f of F.flat())f.s=rnd(4);if(q>=6){let x=Array.from({length:n},()=>rnd(2));for(let f of F.flat()){let a=evalClause(f.c,v=>x[v]);f.s=(a+1+rnd(3))%4}ok(valid(F,x))}F=relabel(F,n);let x=solve(F,n);if(q===0)ok((x!==null)===yes);if(q>=6)ok(x!==null);if(k===2){ok((x!==null)===brute(F,n));stats.exhaustive++}stats.checked++;if(x)stats.sat++;else stats.unsat++}results.push(stats)}return{seed:20261126,checks,results}}
console.log(JSON.stringify(signedAudit(),null,2));
