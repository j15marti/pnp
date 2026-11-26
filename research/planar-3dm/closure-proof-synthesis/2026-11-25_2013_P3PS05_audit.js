// Standalone Node.js audit. Seed and data returned by audit().
function audit(){
 let seed=5505;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
 const modes=Array.from({length:8},(_,i)=>[1,...[0,1,2].map(j=>(i>>j&1)?-1:1)]);
 const prod=(s,I)=>I.reduce((p,i)=>p*s[i],1);
 const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],all=[0,1,2,3];
 function wal(f,I){return modes.reduce((v,s,i)=>v+f[i]*prod(s,I),0)/8}
 function energy(s,E){return E.reduce((v,[i,j,w])=>v+w*s[i]*s[j],0)}
 function table(n,E,B){let f=Array(8).fill(Infinity),wit=Array(8);for(let mask=0;mask<2**n;mask++){let s=Array.from({length:n},(_,i)=>(mask>>i&1)?-1:1);if(s[B[0]]!==1)continue;let j=B.slice(1).reduce((a,v,k)=>a+((s[v]===-1)?1<<k:0),0);let e=energy(s,E);if(e<f[j]){f[j]=e;wit[j]=s}}return {f,wit}}
 let checks=0;function check(x){checks++;if(!x)throw Error("failed assertion "+checks)}
 function compress(f){let C=wal(f,[]),A=wal(f,[0,2]),B=wal(f,[1,3]),q=wal(f,all),h=Math.min(Math.abs(A),Math.abs(B));check(2*q===Math.abs(A+B)-Math.abs(A-B));let a=Math.abs(A)+h,b=Math.abs(B)+h;let g=[1,1,A>0?-1:1,B>0?-1:1],w=[a,b,a*g[2],b*g[3]];let star=modes.map(s=>-Math.abs(s.reduce((t,x,i)=>t+x*w[i],0)));let K=C-wal(star,[]),rim=[[0,1],[1,2],[2,3],[0,3]].map(I=>[...I,wal(f,I)-wal(star,I)]);
 for(const I of [[0,2],[1,3],all])check(wal(star,I)===wal(f,I));
 for(let i=0;i<8;i++)check(K+star[i]+energy(modes[i],rim)===f[i]);
 return {q,A,B,K,w,rim}}
 let disk=0,nonzero=0,zero=0,external=0;
 for(let trial=0;trial<240;trial++){let h=3,w=trial%2?3:4,E=[];for(let i=0;i<h;i++)for(let j=0;j<w;j++){let u=i*w+j;if(i+1<h)E.push([u,u+w,rnd(15)-7]);if(j+1<w)E.push([u,u+1,rnd(15)-7]);if(i+1<h&&j+1<w&&rnd(2))E.push([u,u+w+1,rnd(15)-7])}let B=[0,w-1,h*w-1,(h-1)*w],{f,wit}=table(h*w,E,B);let c=compress(f);disk++;if(c.q===0)zero++;else nonzero++;
 let exterior=pairs.map(I=>[...I,rnd(11)-5]),best=Infinity,newbest=Infinity,bi=-1;for(let i=0;i<8;i++){let x=f[i]+energy(modes[i],exterior);if(x<best){best=x;bi=i}let y=c.K-Math.abs(modes[i].reduce((v,s,j)=>v+s*c.w[j],0))+energy(modes[i],c.rim)+energy(modes[i],exterior);newbest=Math.min(newbest,y)}check(best===newbest);check(energy(wit[bi],E)+energy(modes[bi],exterior)===best);external++;}
 let starTests=0;for(let i=0;i<256;i++){let E=Array.from({length:4},(_,j)=>[j,4,((i>>(2*j))&3)-1]);compress(table(5,E,[0,1,2,3]).f);starTests++}
 const crossing=table(4,[[0,2,1],[1,3,1]],[0,1,2,3]).f;check(wal(crossing,all)===0);check(2*wal(crossing,all)!==Math.abs(wal(crossing,[0,2])+wal(crossing,[1,3]))-Math.abs(wal(crossing,[0,2])-wal(crossing,[1,3])));
 let matchingCalls=0;
 function matching(T,n,a,b,force=-1){matchingCalls++;let adj=Array.from({length:n},()=>[]),blockedL=force<0?-1:T[force][a],blockedR=force<0?-1:T[force][b];for(let j=0;j<T.length;j++){let u=T[j][a],v=T[j][b];if(u!==blockedL&&v!==blockedR)adj[u].push(v)}let mate=Array(n).fill(-1);function dfs(u,seen){for(let v of adj[u])if(!seen[v]){seen[v]=1;if(mate[v]<0||dfs(mate[v],seen)){mate[v]=u;return true}}return false}for(let u=0;u<n;u++)if(u!==blockedL&&!dfs(u,Array(n).fill(0)))return false;return true}
 function cover(T,n,ids){return ids.length===n&&[0,1,2].every(c=>new Set(ids.map(i=>T[i][c])).size===n)}
 function fullPrism(m){return Array.from({length:m},(_,i)=>{let t=[];for(let j of [(i+m-1)%m,i,(i+1)%m])t[j%3]=Math.floor(j/3);return t})}
 function periodic(T,orig,m){return [0,1,2].map(r=>orig.map((x,i)=>x%3===r?i:-1).filter(i=>i>=0)).filter(ids=>cover(T,m/3,ids))}
 function close(T,n){let ids=T.map((_,i)=>i),chosen=[],live=Array.from({length:3},()=>Array(n).fill(true)),rounds=0;while(true){rounds++;let forced=-1;for(let c=0;c<3;c++)for(let v=0;v<n;v++)if(live[c][v]){let a=ids.filter(i=>T[i][c]===v);if(a.length===0)return {status:"NO",rounds,chosen};if(a.length===1)forced=a[0]}
 if(forced>=0){chosen.push(forced);for(let c=0;c<3;c++)live[c][T[forced][c]]=false;ids=ids.filter(i=>[0,1,2].every(c=>T[i][c]!==T[forced][c]));continue}if(!ids.length)return {status:cover(T,n,chosen)?"YES":"NO",rounds,chosen};
 let maps=live.map(x=>new Map(x.flatMap((v,i)=>v?[i]:[]).map((v,i)=>[v,i]))),R=ids.map(i=>T[i].map((v,c)=>maps[c].get(v))),nn=n-chosen.length,keep=Array(R.length).fill(true);
 for(let [a,b] of [[0,1],[0,2],[1,2]]){if(!matching(R,nn,a,b))return {status:"NO",rounds,chosen};for(let j=0;j<R.length;j++)if(!matching(R,nn,a,b,j))keep[j]=false}
 if(keep.every(Boolean))return {status:"OPEN",rounds,chosen,live:ids.length};ids=ids.filter((_,i)=>keep[i]);}}
 let prism=[];for(let m of [18,24,48,96,192,384]){let T=fullPrism(m);let all=T.map((_,i)=>i);check(new Set(T.map(t=>t.join(","))).size===m);let sols=periodic(T,all,m);check(sols.length===3);check(new Set(sols.flat()).size===m);let c=close(T,m/3);check(c.status==="OPEN"&&c.live===m);
 let del=new Set([0,7,14]);let orig=all.filter(i=>!del.has(i)),U=orig.map(i=>T[i]);for(let v=0;v<m/3;v++)for(let k=0;k<3;k++)check([2,3].includes(U.filter(t=>t[k]===v).length));check(periodic(U,orig,m).length===0);let d=close(U,m/3);check(d.status!=="YES");prism.push({m,SAT:sols.length,SATClosure:c.status,UNSAT:0,UNSATClosure:d.status,deleted:[0,7,14]})}
 const U=[[0,0,0],[0,1,1],[1,0,1],[1,1,0]],V=[...U,[1,1,1]];function smallCount(T){let n=0;for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++)if(cover(T,2,[i,j]))n++;return n}check(smallCount(U)===0);check(smallCount(V)===1);let uc=close(U,2),vc=close(V,2);check(uc.status!=="YES"&&vc.status!=="NO");
 let sourceStar=compress(table(5,[[0,4,4],[1,4,4],[2,4,4],[3,4,6]],[0,1,2,3]).f);check(sourceStar.q!==0);
 return {seed:5505,checks,disk,zero,nonzero,external,starTests,crossingRejected:true,sourceStar:{q:sourceStar.q,A:sourceStar.A,B:sourceStar.B},smallNeighbor:{U,V,counts:[0,1],closure:[uc.status,vc.status]},prism,matchingCalls,scope:"Exhaustive local reference tables; abstract planar grids by construction; prism planarity and solution formula symbolic; no production T-join or disk separator acquisition executed."}
}
console.log(JSON.stringify(audit(),null,2));
