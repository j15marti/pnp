// Run: node audit.js
const audit=function audit(){
const assert=(b,s)=>{if(!b)throw Error(s)};
let seed=261126;const rand=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return (seed>>>8)%n};
const bits=i=>[(i>>2)&1,(i>>1)&1,i&1];
function grid(l){
 let k=l*l,id=(i,j)=>i+l*j,T=[],E=[],O=[],I=[];
 for(let a=0;a<k;a++)for(let i=0;i<8;i++)T.push(bits(i).map(v=>2*a+v));
 for(let i=0;i<l;i++)for(let j=0;j<l;j++){if(i+1<l)E.push([id(i,j),0,id(i+1,j),0]);if(j+1<l)E.push([id(i,j),1,id(i,j+1),1]);}
 for(let i=0;i<l;i++)O.push([id(i,l-1),1]);for(let j=l-1;j>=0;j--)O.push([id(l-1,j),0]);
 for(let i=l-1;i>=0;i--)I.push([id(i,0),1]);for(let j=0;j<l;j++)I.push([id(0,j),0]);
 I.reverse();O.forEach((x,i)=>E.push([...x,...I[i]]));
 for(let [a,p,b,q] of E)T[8*a+p][0]=2*b;
 return {n:2*k,T};
}
function prism(k){
 let L=2*k,n=2*k,T=Array.from({length:2*L},()=>[-1,-1,-1]),c=[0,0,0];
 for(let j=0;j<2;j++)for(let i=0;i<L;i++){let p=i%2,x=j*L+i,y=j*L+(i+1)%L;T[x][p]=T[y][p]=c[p]++}
 for(let i=0;i<L;i++)T[i][2]=T[L+i][2]=c[2]++;
 assert(c.every(x=>x===n),"prism balance");
 T.push(...Array.from({length:8},(_,i)=>bits(i).map(x=>x+n)));
 let a=0,b=2*L;[T[a][0],T[b][0]]=[T[b][0],T[a][0]];
 return {n:n+2,T};
}
function getRows(F){let R=Array.from({length:3*F.n},()=>[]);F.T.forEach((t,i)=>t.forEach((x,c)=>R[c*F.n+x].push(i)));return R}
function valid(F,W,P={}){let S=new Set(W),R=getRows(F);return S.size===W.length&&R.every(row=>row.filter(i=>S.has(i)).length===1)&&Object.entries(P).every(([i,b])=>S.has(+i)===!!b)}
function matching(A,n){
 let r=Array(n).fill(-1),l=Array(A.length).fill(-1);
 function aug(i,seen){for(let j of A[i])if(!seen[j]){seen[j]=1;if(r[j]<0||aug(r[j],seen)){r[j]=i;l[i]=j;return true}}return false}
 for(let i=0;i<A.length;i++)aug(i,new Uint8Array(n));
 return {l,r,size:l.filter(x=>x>=0).length};
}
function closure(F,P={}){
 const R=getRows(F),m=F.T.length,n=F.n,x=Array(m).fill(-1);let changed=true;
 function pin(i,b){if(x[i]>=0)return x[i]===b;x[i]=b;changed=true;return true}
 for(let [i,b] of Object.entries(P))if(!pin(+i,b))return null;
 while(changed){
  changed=false;
  for(let row of R){let yes=row.filter(i=>x[i]===1).length,free=row.filter(i=>x[i]<0);
   if(yes>1||(!yes&&!free.length))return null;
   if(yes){for(let i of free)if(!pin(i,0))return null}
   else if(free.length===1&&!pin(free[0],1))return null;
  }
  if(changed)continue;
  let bas=new Map(),bad=false;
  for(let row of R){let b=1,mask=0n;for(let i of row){if(x[i]===1)b^=1;else if(x[i]<0)mask^=1n<<BigInt(i)}
   while(mask){let p=mask.toString(2).length-1;if(!bas.has(p)){bas.set(p,[mask,b]);break}let [v,w]=bas.get(p);mask^=v;b^=w}
   if(!mask&&b){bad=true;break}
  }
  if(bad)return null;
  let ks=[...bas.keys()].sort((a,b)=>a-b);
  for(let p of ks){let [v,b]=bas.get(p);for(let q of ks){if(q>=p)break;if((v>>BigInt(q))&1n){let [w,t]=bas.get(q);v^=w;b^=t}}
   bas.set(p,[v,b]);if(v===(1n<<BigInt(p))&&!pin(p,b))return null;
  }
  if(changed)continue;
  for(let [a,b] of [[0,1],[0,2],[1,2]]){
   let L=Array.from({length:n},(_,j)=>j).filter(j=>!R[a*n+j].some(i=>x[i]===1)),B=Array.from({length:n},(_,j)=>j).filter(j=>!R[b*n+j].some(i=>x[i]===1));
   if(L.length!==B.length)return null;
   let lm=new Map(L.map((v,i)=>[v,i])),bm=new Map(B.map((v,i)=>[v,i])),A=L.map(()=>[]);
   let live=[];for(let i=0;i<m;i++)if(x[i]<0){let u=lm.get(F.T[i][a]),v=bm.get(F.T[i][b]);assert(u!==undefined&&v!==undefined,"covered row");A[u].push(v);live.push([i,u,v])}
   let M=matching(A,B.length);if(M.size!==L.length)return null;
   let adj=A.map(v=>v.map(j=>M.r[j])),rev=L.map(()=>[]),seen=new Uint8Array(L.length),order=[];
   adj.forEach((v,i)=>v.forEach(j=>rev[j].push(i)));
   function dfs(i){if(seen[i])return;seen[i]=1;for(let j of adj[i])dfs(j);order.push(i)}
   for(let i=0;i<L.length;i++)dfs(i);
   let cc=Array(L.length).fill(-1),z=0;function dfs2(i){if(cc[i]>=0)return;cc[i]=z;for(let j of rev[i])dfs2(j)}
   for(let i of order.reverse())if(cc[i]<0){dfs2(i);z++}
   for(let [i,u,v] of live)if(cc[u]!==cc[M.r[v]]&&!pin(i,0))return null;
   if(changed)break;
  }
 }
 return x;
}
function cover(F,x){
 let R=getRows(F),bad=R.map((r,i)=>[r.filter(j=>x[j]<0),i]).filter(([r,i])=>r.length>0&&r.length!==2),A=bad.map(([r])=>r),M=matching(A,F.T.length),seenL=new Set(),seenR=new Set(),Q=[];
 for(let i=0;i<A.length;i++)if(M.l[i]<0){seenL.add(i);Q.push(i)}
 for(let i of Q)for(let j of A[i])if(j!==M.l[i]&&!seenR.has(j)){seenR.add(j);let t=M.r[j];if(t>=0&&!seenL.has(t)){seenL.add(t);Q.push(t)}}
 let O=bad.filter((_,i)=>!seenL.has(i)).map(x=>x[1]),C=[...seenR].sort((a,b)=>a-b);
 assert(O.length+C.length===M.size,"Konig size");
 let os=new Set(O),cs=new Set(C);
 for(let [r,i] of bad)for(let j of r)assert(os.has(i)||cs.has(j),"uncovered conflict");
 return {O,C,k:M.size};
}
function solve(F,P={},cap=15){
 let x=closure(F,P);if(!x)return {count:"0",k:null,states:0,W:null};
 let K=cover(F,x),{O,C,k}=K;if(k>cap)return {count:null,k,states:0,W:null};
 const R=getRows(F),Oset=new Set(O),ob=new Map(O.map((r,i)=>[r,1n<<BigInt(i)]));
 let total=0n,W=null,states=0;
 for(let mask=0;mask<(1<<C.length);mask++){
  let pins={...P};x.forEach((v,i)=>{if(v>=0)pins[i]=v});C.forEach((j,i)=>pins[j]=(mask>>i)&1);
  let y=closure(F,pins);if(!y)continue;
  let fixed=y.flatMap((v,i)=>v===1?[i]:[]),target=0n,ad=F.T.map(()=>[]),ok=true;
  for(let r=0;r<R.length;r++){let row=R[r],one=row.filter(i=>y[i]===1).length,free=row.filter(i=>y[i]<0);
   if(Oset.has(r)){if(!one)target|=ob.get(r)}
   else if(!one){assert(free.length===2,"nonbinary outside cover");let[a,b]=free;ad[a].push(b);ad[b].push(a)}
  }
  let col=Array(F.T.length).fill(-1),comps=[];
  for(let i=0;i<y.length;i++)if(y[i]<0&&col[i]<0){
   let q=[i];col[i]=0;for(let j of q)for(let a of ad[j]){if(col[a]<0){col[a]=1-col[j];q.push(a)}else if(col[a]===col[j])ok=false}
   comps.push(q);
  }
  if(!ok)continue;
  let dp=new Map([[0n,[1n,[]]]]);
  for(let q of comps){
   let opts=[];
   for(let ph=0;ph<2;ph++){
    let sel=q.filter(i=>col[i]===ph),word=0n,pass=true;
    for(let i of sel)F.T[i].forEach((v,c)=>{let bit=ob.get(c*F.n+v)||0n;if(bit){if((word&bit)||!(target&bit))pass=false;word|=bit}});
    if(pass)opts.push([word,sel]);
   }
   let next=new Map();
   for(let [a,[count,w]] of dp)for(let [b,sel] of opts)if(!(a&b)){let t=a|b,old=next.get(t);next.set(t,[count+(old?old[0]:0n),old?old[1]:w.concat(sel)]);states++}
   dp=next;
  }
  if(dp.has(target)){let [num,w]=dp.get(target);total+=num;if(!W){W=fixed.concat(w);assert(valid(F,W,P),"bad lift")}}
 }
 return {count:total.toString(),k,states,W};
}
function brute(F,P={}){
 let R=getRows(F),x=Array(F.T.length).fill(-1),count=0n;
 for(let [i,b] of Object.entries(P))x[+i]=b;
 function rec(y){let best=null;for(let row of R){let one=row.filter(i=>y[i]===1),free=row.filter(i=>y[i]<0);
  if(one.length>1||(!one.length&&!free.length))return;
  if(one.length){for(let i of free)y[i]=0}else if(!best||free.length<best.length)best=free;
 }
 if(!best){if(valid(F,y.flatMap((v,i)=>v===1?[i]:[]),P))count++;return}
 for(let i of best)if(y[i]<0){let z=y.slice();z[i]=1;for(let r of R)if(r.includes(i)){for(let j of r)if(j!==i){if(z[j]===1){z=null;break}z[j]=0}if(!z)break}if(z)rec(z)}
 }
 rec(x);return count.toString();
}
let small=[],guardChecks=0,yes=0,no=0,declines=0,states=0;
for(let F of [grid(1),grid(2),prism(2),prism(3)]){
 for(let j=0;j<70;j++){
 let D=F.T.map((_,i)=>i).filter(i=>j===0||rand(10)>1),G={n:F.n,T:D.map(i=>F.T[i])},P={};
 if(j%3===1&&G.T.length)P[rand(G.T.length)]=rand(2);
 if(j%3===2&&G.T.length){P[rand(G.T.length)]=0;P[rand(G.T.length)]=1}
 let r=solve(G,P),b=brute(G,P);guardChecks++;states+=r.states;
 if(r.count===null){declines++;continue}assert(r.count===b,"reference discrepancy "+JSON.stringify({G,P,r,b}));if(b==="0")no++;else yes++;
 }
 let c=cover(F,Array(F.T.length).fill(-1));small.push({n:F.n,m:F.T.length,raw_k:c.k,count:brute(F),solved:solve(F).count});
}
let scale=[];for(let k of [2,4,8,16,32,64,128,256]){
 let F=prism(k),r=solve(F),a=solve(F,{0:0}),b=solve(F,{0:1});assert(r.count==="4"&&a.count==="3"&&b.count==="1","prism cube splice count "+JSON.stringify({k,r:r.count,a:a.count,b:b.count}));
 scale.push({k,triples:F.T.length,defects:r.k,count:r.count,states:r.states,guards:[a.count,b.count]});
}
let gridScale=[];for(let l of [1,2,4,8,12]){
 let F=grid(l),x=closure(F);assert(x&&x.every(v=>v===-1),"grid closure");let c=cover(F,x);assert(c.k===6*l*l,"grid mincover");gridScale.push({l,triples:F.T.length,defects:c.k});
}
let F=grid(2),D=new Set([1,6,15,16,21,25,28,30,31]),G={n:F.n,T:F.T.filter((_,i)=>!D.has(i))},J={n:F.n,T:F.T.filter((_,i)=>!D.has(i)&&i!==26)};
let nei=[G,J].map(F=>({triples:F.T.length,count:brute(F),solver:solve(F).count}));assert(nei[0].count==="8"&&nei[1].count==="0","neighbor reference");
return {seed:261126,small,guardChecks,yes,no,declines,states,scale,gridScale,neighbor:nei};
};
console.log(JSON.stringify(audit(),null,2));
