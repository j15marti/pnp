function audit(){
const chk=(x,m)=>{if(!x)throw Error(m)};
const canon=w=>{const d=new Map();return w.map(x=>{if(!d.has(x))d.set(x,d.size);return d.get(x)}).join("")};
const S=[...new Set(Array.from({length:729},(_,i)=>Array.from({length:6},(_,j)=>Math.floor(i/3**j)%3)).filter(w=>[0,1,2].every(x=>w.filter(y=>y===x).length%2===0)).map(canon))].sort();
const all=2**31-1,idx=new Map(S.map((w,i)=>[w,i])),bit=w=>2**idx.get(w),mask=ws=>ws.reduce((m,s)=>m|bit(s),0),decode=m=>S.filter((_,i)=>m&2**i);
const E=[[0,4],[0,5],[1,2],[1,6],[2,3],[2,7],[3,8],[4,9],[5,7],[6,8],[6,9],[7,9]],p=[3,4,5,8,0,1],q=[3,4,5,8,1,0],F=[[0,2],[0,5],[1,2],[1,7],[1,3],[3,4],[4,6],[5,7],[5,6]],r=[3,0,2,6,4,7],t=[3,0,2,6,7,4];
function color(E,p){const n=Math.max(...E.flat(),...p)+1,k=E.length,inc=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});p.forEach((u,i)=>inc[u].push(k+i));chk(inc.every(v=>v.length===3),"degrees");const adj=Array.from({length:k+p.length},()=>new Set());for(const l of inc)for(const i of l)for(const j of l)if(i!==j)adj[i].add(j);const a=Array(adj.length).fill(-1);a[0]=0;let W=new Map(),nodes=0;function dfs(){nodes++;let u=-1,d=null;for(let i=0;i<a.length;i++)if(a[i]<0){let v=[0,1,2].filter(c=>[...adj[i]].every(j=>a[j]!==c));if(!v.length)return;if(d===null||v.length<d.length){u=i;d=v}}if(u<0){const s=canon(a.slice(k));if(!W.has(s))W.set(s,a.slice());return}for(const c of d){a[u]=c;dfs();a[u]=-1}}dfs();return {support:[...W.keys()].sort(),nodes,witness:W.get("")??null}}
const A=color(E,p),B=color(E,q),C=color(F,r),D=color(F,t);
const a=mask(A.support),b=mask(B.support),c=mask(C.support),d=mask(D.support);
chk(a&c,"A+C SAT");chk(!(b&c),"B+C UNSAT");chk(!(a&d),"A+D UNSAT");
function pairings(v){if(!v.length)return [[]];let out=[];for(let j=1;j<v.length;j++)for(const P of pairings(v.filter((_,i)=>i!==0&&i!==j)))out.push([[v[0],v[j]],...P]);return out}
const rules=S.map(s=>[[0,1],[0,2],[1,2]].map(([x,y])=>pairings([...s].map(Number).map((v,i)=>v===x||v===y?i:-1).filter(i=>i>=0)).map(P=>{let m=0;for(let k=0;k<1<<P.length;k++){let z=[...s].map(Number);P.forEach(([u,v],j)=>{if(k>>j&1){z[u]=x+y-z[u];z[v]=x+y-z[v]}});m|=bit(canon(z))}return m})));
function K(m){for(;;){let n=0;for(let i=0;i<31;i++)if((m&2**i)&&rules[i].every(R=>R.some(o=>(o&m)===o)))n|=2**i;if(m===n)return m;m=n}}
const dual=m=>K(all^m);
chk(K(all^d)===a&&K(all^c)===b,"single extra query exact closure");
for(const m of [a,b,c,d])chk((dual(dual(m))&m)===m&&dual(dual(dual(m)))===dual(m),"dual identity");
const cycles=new Set();function perm(v,k,P=[]){if(k===0){cycles.add(P.map((u,i)=>[u,P[(i+1)%P.length]].sort().join("")).sort().join(","));return}for(const u of v)perm(v.filter(x=>x!==u),k-1,[...P,u])}for(let k=3;k<=5;k++)perm([0,1,2,3,4],k);chk(cycles.size===37,"cycle caps");
const type=s=>[...s].map((x,i)=>[...s].filter(y=>y===x).length===1?i:-1).filter(i=>i>=0).join("");
const f4=["0000","0011","0101","0110"];let queries=[];
for(let i=0;i<6;i++)for(let j=i+1;j<6;j++){
for(const cyc of cycles){const T=cyc.split(",");const states=S.filter(w=>{if(w[i]===w[j])return false;const v=[...w].map(Number).filter((_,k)=>k!==i&&k!==j);v.push(3-Number(w[i])-Number(w[j]));return T.includes(type(canon(v)))});queries.push(mask(states));}
for(let u=0;u<4;u++)for(let v=u+1;v<4;v++){const states=S.filter(w=>w[i]===w[j]&&[f4[u],f4[v]].includes(canon([...w].filter((_,k)=>k!==i&&k!==j))));queries.push(mask(states));}
}
chk(queries.length===645,"queries");const Aanswers=queries.map(m=>!!(m&a)),Banswers=queries.map(m=>!!(m&b));chk(JSON.stringify(Aanswers)===JSON.stringify(Banswers)&&Aanswers.filter(Boolean).length===642,"identical");
const U=K(queries.reduce((m,h,i)=>Aanswers[i]?m:m&(all^h),all));chk(decode(U).length===26,"uncertainty");
const joined=(P,R)=>[...E,...F.map(e=>e.map(v=>v+10)),...P.map((u,i)=>[u,R[i]+10])];
let graphs=[joined(p,r),joined(q,r),joined(p,t)];for(const G of graphs)chk(new Set(G.map(e=>e.slice().sort((a,b)=>a-b).join(","))).size===G.length,"simple");
let exact=graphs.map(G=>color(G,[]));chk(exact[0].support.length===1&&exact[1].support.length===0&&exact[2].support.length===0,"direct graph outcomes");
for(const m of [12303921,12566066,2125820352])chk(K(m)===m,"abstract gaps consistent");
return {states:S,ports:{p,q,r,t},A:A.support,B:B.support,C:C.support,D:D.support,query_count:645,positive:642,upper_before:decode(U),after_negative:{A:decode(K(all^d)),B:decode(K(all^c))},dual_A:decode(dual(a)),dual_B:decode(dual(b)),graphs,exact,abstract_gaps:[12303921,12566066,2125820352].map(decode)};
}
console.log(JSON.stringify(audit(),null,2));
