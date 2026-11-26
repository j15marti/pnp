function audit(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const canon=w=>{const m=new Map();return w.map(x=>{if(!m.has(x))m.set(x,m.size);return m.get(x)}).join("")};
 const words=n=>Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**j)%3)).filter(w=>[0,1,2].every(c=>w.filter(x=>x===c).length%2===n%2)).map(canon);
 const S=[...new Set(words(6))].sort(),ix=new Map(S.map((s,i)=>[s,i])),all=2**31-1,bit=s=>2**ix.get(s),ids=m=>S.map((_,i)=>i).filter(i=>m&(2**i)),mask=ss=>[...new Set(ss)].reduce((m,s)=>m|bit(s),0),decode=m=>ids(m).map(i=>S[i]);
 check(S.length===31,"universe");
 const fuse=(s,i,j)=>s[i]===s[j]?null:canon([...s].map(Number).filter((_,k)=>k!==i&&k!==j).concat(3-Number(s[i])-Number(s[j])));
 const type=s=>[...s].map((c,i)=>[...s].filter(x=>x===c).length===1?i:-1).filter(i=>i>=0).join("");
 const rows=[];for(let j=1;j<6;j++){const D=new Map();for(const s of S){const f=fuse(s,0,j);if(f!==null){if(!D.has(f))D.set(f,[]);D.get(f).push(s)}}check(D.size===10,"five fiber");for(const a of D.values()){check(a.length===2,"preimages");rows.push(a)}}
 const rank=R=>{const p=101,A=R.map(r=>r.map(x=>x%p));let n=0;for(let j=0;j<31&&n<A.length;j++){let i=A.findIndex((r,i)=>i>=n&&r[j]);if(i<0)continue;[A[n],A[i]]=[A[i],A[n]];for(let k=n+1;k<A.length;k++)if(A[k][j]){const a=A[n][j],b=A[k][j];A[k]=A[k].map((v,t)=>((a*v-b*A[n][t])%p+p)%p)}n++}return n};
 const R=rows.map(a=>S.map(s=>+a.includes(s))),extra=S.map(s=>+["001001","010001"].includes(s)),glue=S.map(s=>s[0]===s[1]?(s==="000000"?3:6):0);
 check(rank(R)===29&&rank([...R,extra])===30&&rank([...R,extra,glue])===31,"rank");
 function pairings(a){if(!a.length)return [[]];let out=[];for(let j=1;j<a.length;j++)for(const P of pairings(a.filter((_,i)=>i!==0&&i!==j)))out.push([[a[0],a[j]],...P]);return out}
 const rules=S.map(s=>[[0,1],[0,2],[1,2]].map(([a,b])=>pairings([...s].map(Number).map((x,i)=>x===a||x===b?i:-1).filter(i=>i>=0)).map(P=>{let m=0;for(let k=0;k<1<<P.length;k++){const t=[...s].map(Number);P.forEach(([u,v],j)=>{if(k>>j&1){t[u]=a+b-t[u];t[v]=a+b-t[v]}});m|=bit(canon(t))}return m})));
 function close(m){for(;;){let n=0;for(const i of ids(m))if(rules[i].every(r=>r.some(o=>(o&m)===o)))n|=2**i;if(n===m)return m;m=n}}
 const E=[[0,2],[1,3],[2,4],[2,5],[3,4],[3,5]],F=[[0,7],[1,2],[1,4],[2,7],[2,5],[3,6],[3,5],[4,6],[6,7]],P=[0,1,1,0,4,5],Q=[0,1,1,4,0,5],B=[4,3,1,5,0,0];
 function support(E,p){let n=Math.max(...E.flat(),...p)+1,k=E.length,inc=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});p.forEach((v,i)=>inc[v].push(k+i));check(inc.every(a=>a.length===3),"degrees");const adj=Array.from({length:k+p.length},()=>new Set());for(const l of inc)for(const i of l)for(const j of l)if(i!==j)adj[i].add(j);const x=Array(adj.length).fill(-1);x[0]=0;let W=new Set(),nodes=0;function dfs(){nodes++;let u=-1,opt=null;for(let i=0;i<x.length;i++)if(x[i]<0){let d=[0,1,2].filter(c=>[...adj[i]].every(j=>x[j]!==c));if(!d.length)return;if(opt===null||d.length<opt.length){u=i;opt=d}}if(u<0){W.add(canon(x.slice(k)));return}for(const c of opt){x[u]=c;dfs();x[u]=-1}}dfs();return {support:[...W].sort(),nodes}}
 const a=support(E,P),b=support(E,Q),c=support(F,B);check(a.support.length===10&&b.support.length===10&&c.support.length===12,"supports");const projection=s=>Array.from({length:5},(_,j)=>[...new Set(s.map(w=>fuse(w,0,j+1)).filter(x=>x!==null))].sort());check(JSON.stringify(projection(a.support))===JSON.stringify(projection(b.support)),"identical five full support tables");check(!a.support.some(s=>c.support.includes(s))&&b.support.some(s=>c.support.includes(s)),"different contexts");
 const cycleSet=new Set();function perm(a,k,p=[]){if(!k){let e=p.map((v,i)=>[v,p[(i+1)%p.length]].sort().join("")).sort().join(",");cycleSet.add(e);return}for(const v of a)perm(a.filter(x=>x!==v),k-1,[...p,v])}for(let k=3;k<=5;k++)perm([0,1,2,3,4],k);check(cycleSet.size===37,"cycle caps");
 const F4=[...new Set(words(4))].sort();check(F4.length===4,"four states");
 const capQueries=[];for(let j=1;j<6;j++)for(const C of cycleSet){const T=C.split(",");capQueries.push(mask(S.filter(w=>{let f=fuse(w,0,j);return f!==null&&T.includes(type(f))})))}
 const equalQueries=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)equalQueries.push(mask(S.filter(w=>w[i]===w[j]&&[F4[u],F4[v]].includes(canon([...w].filter((_,k)=>k!==i&&k!==j))))));
 function bound(s,qs){const m=mask(s);let U=all,W=0,yes=0;for(const q of qs){const h=m&q;if(h){W|=h&-h;yes++}else U&=all^q}U=close(U);return {yes,W:decode(W),upper:decode(U),certifiesExactCap:(W&m)===m&&!(close(all^m)&U)}}
 const joined=(p)=>support([...E,...F.map(e=>e.map(v=>v+6)),...p.map((u,i)=>[u,B[i]+6])],[]);
 const u=joined(P),v=joined(Q);check(!u.support.length&&v.support.length===1,"direct joined graph comparison");
 return {rank:[29,30,31],a,b,c,projection:projection(a.support),joined:{U:u,V:v},queries:{A_five:bound(a.support,capQueries),B_five:bound(b.support,capQueries),A_combined:bound(a.support,[...capQueries,...equalQueries]),B_combined:bound(b.support,[...capQueries,...equalQueries])}};
}
console.log(JSON.stringify(audit(),null,2));
