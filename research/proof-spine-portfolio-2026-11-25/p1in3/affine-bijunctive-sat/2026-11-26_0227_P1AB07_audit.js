function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m)};const mod=x=>((x%3)+3)%3;
 const combos=(a,h)=>{let o=[[]];function f(s,j){if(s.length===h)return;for(let i=j;i<a.length;i++){let t=[...s,a[i]];o.push(t);f(t,i+1)}}f([],0);return o};
 const all=d=>Array.from({length:2**d},(_,s)=>Array.from({length:d},(_,i)=>(s>>i)&1));
 const sat=(F,x)=>F.every(c=>c.some(l=>x[Math.abs(l)-1]===+(l>0)));
 const stats={samples:0,rankComparisons:0,guardTests:0,gauss:0,matching:0,probes:0,closure:0};
 function model2(F,d){
   function feas(G){let a=Array.from({length:2*d},()=>new Set());let j=l=>2*(Math.abs(l)-1)+ +(l<0);for(let c of G){if(!c.length)return false;assert(c.length<=2,"not 2cnf");let u=j(c[0]),v=j(c[c.length-1]);a[u^1].add(v);a[v^1].add(u)}
     let reach=(u,v)=>{let seen=new Set([u]),s=[u];while(s.length){let k=s.pop();for(let w of a[k]){if(w===v)return true;if(!seen.has(w)){seen.add(w);s.push(w)}}}return false};for(let i=0;i<d;i++)if(reach(2*i,2*i+1)&&reach(2*i+1,2*i))return false;return true}
   if(!feas(F))return null;let G=F.slice(),x=[];for(let i=0;i<d;i++){let l=-(i+1);if(!feas([...G,[l]]))l=-l;G.push([l]);x.push(+(l>0))}assert(sat(F,x),"2sat lift");return x;
 }
 function hornClosure(F,d,seed){let x=Array(d).fill(0);for(let i of seed)x[i]=1;for(let change=true;change;){change=false;for(let c of F){let pos=c.filter(l=>l>0);assert(pos.length<=1,"not horn");if(c.filter(l=>l<0).every(l=>x[-l-1])){if(!pos.length)return null;if(!x[pos[0]-1]){x[pos[0]-1]=1;change=true}}}}return x}
 function sample2(F,d,h){let a=model2(F,d);if(!a)return [];let G=F.map(c=>c.map(l=>a[Math.abs(l)-1]?-l:l));let out=new Map();for(let J of combos(Array.from({length:d},(_,i)=>i),h)){let x=hornClosure(G,d,J);if(x){x=x.map((v,i)=>v^a[i]);out.set(x.join(""),x)}}return [...out.values()]}
 function samples(F,d,h,half,flip=Array(d).fill(0)){
   let G=F.map(c=>c.map(l=>flip[Math.abs(l)-1]?-l:l)),B=half,H=Array.from({length:d},(_,i)=>i).filter(i=>!B.includes(i)),Bset=new Set(B),HH=[],BB=[];
   for(let c of G){let b=c.filter(l=>Bset.has(Math.abs(l)-1)),k=c.filter(l=>!Bset.has(Math.abs(l)-1));if(b.length){assert(b.length<=2&&k.every(l=>l<0),"bad mixed qhorn certificate");BB.push([k,b])}else{assert(k.filter(l=>l>0).length<=1,"bad horn cert");HH.push(k)}}
   let reps=new Map();for(let J of combos(H,h)){let a=hornClosure(HH,d,J);if(a){let k=a.join("");if(!reps.has(k)||reps.get(k)[1]>J.length)reps.set(k,[a,J.length])}}
   let out=new Map();for(let [a,r] of reps.values()){let K=BB.filter(([k])=>k.every(l=>a[-l-1])).map(([,b])=>b.map(l=>Math.sign(l)*(B.indexOf(Math.abs(l)-1)+1)));for(let w of sample2(K,B.length,h-r)){let x=a.slice();B.forEach((i,j)=>x[i]=w[j]);x=x.map((v,i)=>v^flip[i]);assert(sat(F,x),"bad qhorn sample");out.set(x.join(""),x)}}
   assert(out.size<=combos(Array.from({length:d},(_,i)=>i),h).length,"sample bound");stats.samples+=out.size;return [...out.values()]
 }
 function rank(M,p=3){if(!M.length)return 0;M=M.map(r=>r.map(v=>(v%p+p)%p));let k=0;for(let j=0;j<M[0].length&&k<M.length;j++){let i=M.findIndex((r,i)=>i>=k&&r[j]);if(i<0)continue;[M[i],M[k]]=[M[k],M[i]];let t=M[k][j]===2?2:1;M[k]=M[k].map(v=>v*t%p);for(i=k+1;i<M.length;i++){t=M[i][j];M[i]=M[i].map((v,c)=>(v-t*M[k][c]+2*p)%p)}k++}return k}
 function compare(F,d,h,B,flip){let W=samples(F,d,h,B,flip),V=all(d).filter(x=>sat(F,x)),mon=combos(Array.from({length:d},(_,i)=>i),h),ev=S=>S.map(x=>mon.map(J=>J.every(i=>x[i])?1:0));assert(rank(ev(W))===rank(ev(V)),"rank gap");assert(!!W.length===!!V.length,"SAT mismatch");stats.rankComparisons++}
 let seed=720726;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 for(let t=0;t<160;t++){let d=3+rand(5),B=Array.from({length:d},(_,i)=>i).filter(()=>rand(5)<2),H=Array.from({length:d},(_,i)=>i).filter(i=>!B.includes(i)),F=[],flip=Array.from({length:d},()=>rand(2));for(let j=0;j<12;j++){let k=H.filter(()=>rand(4)===0).map(i=>-i-1);let b=B.filter(()=>rand(3)===0).slice(0,2).map(i=>(rand(2)?1:-1)*(i+1));if(!b.length&&H.length&&rand(2)){let i=H[rand(H.length)];k=k.filter(l=>l!==-i-1);k.push(i+1)}let c=k.concat(b);if(c.length)F.push(c.map(l=>flip[Math.abs(l)-1]?-l:l))}
   compare(F,d,2,B,flip);let i=rand(d);compare([...F,[(rand(2)?1:-1)*(i+1)]],d,2,B,flip)
 }
 const C0=[[3,14,17],[1,4,6],[0,2,5],[0,3,5],[1,4,12],[2,5,7],[2,7,8],[6,9,13],[6,9,10],[3,7,8],[0,8,10],[11,15,16],[9,12,13],[4,12,13],[11,14,15],[10,14,15],[1,16,17],[11,16,17]];
 const C1=[[1,3,14],[4,6,9],[0,2,5],[3,5,14],[4,9,12],[2,7,8],[2,5,7],[1,6,13],[4,6,12],[3,7,13],[0,8,10],[10,15,16],[8,13,17],[1,9,12],[0,10,15],[11,15,16],[11,16,17],[11,14,17]];
 const R0=[[32,21,35],[19,22,24],[18,20,23],[23,21,18],[30,22,19],[20,25,23],[25,20,26],[31,27,24],[24,27,28],[21,25,26],[26,18,28],[29,34,33],[27,31,30],[22,30,31],[32,29,33],[28,32,33],[34,35,19],[35,34,29],[10,2,3],[4,1,16],[2,6,5],[3,9,0],[1,4,13],[5,3,2],[7,8,1],[9,5,6],[6,10,9],[8,7,12],[10,15,8],[14,17,11],[12,13,4],[13,12,7],[15,0,14],[11,15,14],[11,17,16],[16,17,0]];
 // R0 prior report indexes clauses first; convert to variables first.
 const R0v=R0.slice(18).concat(R0.slice(0,18)).map(r=>r.map(i=>(i+18)%36));
 const R1=[[20,32,28],[18,25,31],[20,23,24],[21,27,18],[19,26,22],[24,21,20],[25,26,19],[23,27,24],[30,23,28],[22,31,19],[28,32,29],[33,35,34],[31,22,26],[25,27,30],[35,21,18],[29,32,33],[34,29,33],[34,35,30],[3,1,14],[6,4,9],[0,2,5],[5,3,14],[4,12,9],[2,8,7],[7,5,2],[1,13,6],[12,4,6],[13,3,7],[8,0,10],[10,15,16],[13,8,17],[9,12,1],[15,10,0],[15,11,16],[11,17,16],[17,11,14]];
 function auth(C,R){let n=C.length,A=Array.from({length:2*n},()=>[]);for(let i=0;i<n;i++){assert(new Set(C[i]).size===3,"bad clause");for(let v of C[i]){A[v].push(n+i);A[n+i].push(v)}}assert(A.every((a,i)=>a.length===3&&[...a].sort((a,b)=>a-b).join()===[...R[i]].sort((a,b)=>a-b).join()),"bad rotation");let seen=new Set(),f=0;for(let i=0;i<2*n;i++)for(let j of R[i]){let u=i,v=j;if(seen.has(u+","+v))continue;f++;while(!seen.has(u+","+v)){seen.add(u+","+v);let w=R[v][(R[v].indexOf(u)+1)%3];u=v;v=w}assert(u===i&&v===j,"face orbit")}assert(2*n-3*n+f===2,"nonplanar rotation");let V=new Set([0]),Q=[0];while(Q.length)for(let w of A[Q.pop()])if(!V.has(w)){V.add(w);Q.push(w)}assert(V.size===2*n,"disconnected");return f}
 const faces=[auth(C0,R0v),auth(C1,R1)];
 function chart(C,pins,p){stats.gauss++;let n=C.length,M=C.map(c=>Array.from({length:n+1},(_,i)=>i===n?1:+c.includes(i)));pins.forEach((v,i)=>{if(v>=0)M.push(Array.from({length:n+1},(_,j)=>j===n?v:+(i===j)))});
   let piv=[],k=0;for(let j=0;j<n;j++){let i=M.findIndex((r,i)=>i>=k&&r[j]);if(i<0)continue;[M[i],M[k]]=[M[k],M[i]];let t=M[k][j]===2?2:1;M[k]=M[k].map(v=>v*t%p);for(i=0;i<M.length;i++)if(i!==k){t=M[i][j];M[i]=M[i].map((v,c)=>(v-t*M[k][c]+2*p)%p)}piv.push(j);k++}
   if(M.slice(k).some(r=>r[n]))return null;let F=Array.from({length:n},(_,i)=>i).filter(i=>!piv.includes(i)),D=Array.from({length:n},(_,i)=>F.map(j=>+(i===j))),a=Array(n).fill(0);piv.forEach((j,i)=>{a[j]=M[i][n];D[j]=F.map(v=>(p-M[i][v])%p)});return {F,D,a}
 }
 function necessary(C,p){stats.matching++;let n=C.length,L=C.filter(c=>!c.some(v=>p[v]===1)),owner=Array(3*n).fill(-1);function aug(i,seen){for(let v of L[i])if(p[v]!==0)for(let k=0;k<3;k++){let w=3*v+k;if(seen.has(w))continue;seen.add(w);if(owner[w]===-1||aug(owner[w],seen)){owner[w]=i;return true}}return false}return L.every((_,i)=>aug(i,new Set()))}
 function close(C,p){stats.closure++;p=p.slice();for(;;){let old=p.join();for(let c of C){let t=c.filter(i=>p[i]===1).length,u=c.filter(i=>p[i]<0);if(t>1||(!t&&!u.length))return null;if(t)u.forEach(i=>p[i]=0);else if(u.length===1)p[u[0]]=1}
   for(let f of [2,3]){let q=chart(C,p,f);if(!q)return null;for(let i=0;i<p.length;i++)if(q.D[i].every(v=>!v)){let a=q.a[i];if(a>1||p[i]>=0&&p[i]!==a)return null;p[i]=a}}
   if(!necessary(C,p))return null;if(old===p.join())return p}}
 function fullClose(C,p){p=close(C,p);if(!p)return null;for(;;){let old=p.join();for(let i=0;i<p.length;i++)if(p[i]<0){let valid=[];for(let v=0;v<2;v++){stats.probes++;let q=p.slice();q[i]=v;valid.push(!!close(C,q))}if(!valid[0]&&!valid[1])return null;if(valid[0]!==valid[1]){p[i]=+valid[1];p=close(C,p);if(!p)return null}}if(old===p.join())return p}}
 const lift=(q,z)=>q.a.map((a,i)=>mod(a+q.D[i].reduce((s,v,j)=>s+v*z[j],0)));
 function identity(q,W){let f=q.a.map((_,i)=>W.map(z=>+(lift(q,z)[i]===2)));let rr=rank(f);return {exact:f.every(r=>r.every(v=>!v)),contradiction:W.length>0&&rank([...f,W.map(()=>1)])===rr}}
 function labels(F,d){if(F.every(c=>c.length<=2))return {B:Array.from({length:d},(_,i)=>i),flip:Array(d).fill(0)};let G=[];for(let c of F)for(let i=0;i<c.length;i++)for(let j=i+1;j<c.length;j++)G.push([c[i],c[j]]);let flip=model2(G,d);return flip?{B:[],flip}:null}
 const key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)).join(",");
 function compact(F){let D=[...new Map(F.map(c=>[key(c),c])).values()];return D.filter(c=>!D.some(b=>b.length<c.length&&b.every(l=>c.includes(l))))}
 function solve(C,p){p=fullClose(C,p);if(!p)return {status:"NO_CLOSURE"};let q=chart(C,p,3),d=q.F.length,H=[];assert(d<=10,"audit cap");for(let i=0;i<C.length;i++){let J=q.D[i].map((v,j)=>v?j:-1).filter(j=>j>=0);if(J.length>2)continue;for(let x of all(J.length)){if(mod(q.a[i]+J.reduce((s,j,k)=>s+q.D[i][j]*x[k],0))===2)H.push(J.map((j,k)=>(x[k]?-1:1)*(j+1)))}}
   H=compact(H);let initial=H.map(c=>c.slice());for(let step=0;step<1+8*d**3;step++){let L=labels(H,d);if(!L)return {status:"OPEN_RECOGNIZER"};let W=samples(H,d,2,L.B,L.flip);if(!W.length)return {status:"NO_QHORN"};let I=identity(q,W);if(I.contradiction)return {status:"NO_IDENTITY"};if(I.exact){let x=lift(q,W[0]);assert(C.every(c=>c.reduce((s,i)=>s+x[i],0)===1)&&p.every((v,i)=>v<0||v===x[i]),"invalid lift");return {status:"EXACT",d,F:q.F,initial,H,flip:L.flip,step,witness:x,models:all(d).filter(z=>sat(H,z)).length}}
     let deck=[];for(let J of combos(Array.from({length:d},(_,i)=>i),3)){if(!J.length)continue;for(let b of all(J.length)){let guard=J.map((j,k)=>(b[k]?1:-1)*(j+1));let V=samples([...H,...guard.map(l=>[l])],d,2,L.B,L.flip);stats.guardTests++;if(V.length&&identity(q,V).contradiction)deck.push(guard.map(l=>-l))}}
     let K=compact([...H,...deck]);if(!deck.length||!labels(K,d)){fullClose(C,p);return {status:"OPEN",d,deck:K}}H=K;let forced=close(C,p);assert(forced&&forced.join()===p.join(),"unexpected source closure change");
   }throw Error("iteration cap")}
 function brute(C,p){let n=C.length,out=[];for(let x of all(n)){if(p.every((v,i)=>v<0||v===x[i])&&C.every(c=>c.reduce((s,i)=>s+x[i],0)===1))out.push(x)}return out}
 // independent exact-cover reference avoids full word arrays
 function ref(C,p){let n=C.length,out=[];function dfs(x){let best=null;for(let c of C){let t=c.filter(i=>x[i]===1).length,u=c.filter(i=>x[i]<0);if(t>1||!t&&!u.length)return;if(t&&u.length){let y=x.slice();u.forEach(i=>y[i]=0);return dfs(y)}if(!t&&(!best||u.length<best.length))best=u}
   if(!best){out.push(x.map(v=>Math.max(0,v)));return}for(let i of best){let y=x.slice();for(let j of best)y[j]=+(i===j);dfs(y)}}dfs(p.slice());return out}
 let controls=[],root;for(let C of [C0,C1]){let P=[Array(18).fill(-1)];for(let i of [8,12,16,17])for(let v=0;v<2;v++){let p=Array(18).fill(-1);p[i]=v;P.push(p)}for(let p of P){let R=ref(C,p),s=solve(C,p);if(C===C0&&controls.length===0)root=s;assert(s.status==="EXACT"?R.length>0&&s.models===R.length:s.status.startsWith("NO")?R.length===0:true,"native mismatch");controls.push({source:C===C0?"SAT":"UNSAT",pins:p.map((v,i)=>v>=0?[i,v]:null).filter(Boolean),ref:R.length,status:s.status,d:s.d??null})}}
 assert(root.status==="EXACT"&&root.models===9,"AB06 rescue failed");
 // Products are admitted by component factorization; no global model enumeration.
 let products=[];for(let k of [1,2,4,8,16]){let witnesses=[],ok=true;for(let j=0;j<k;j++){let s=solve(C0,Array(18).fill(-1));ok&&=s.status==="EXACT";witnesses.push(...s.witness)}assert(ok&&witnesses.length===18*k,"product lift");let C=Array.from({length:k},(_,j)=>C0.map(c=>c.map(i=>i+18*j))).flat();assert(C.every(c=>c.reduce((s,i)=>s+witnesses[i],0)===1),"product occupancy");let no=solve(C1,Array(18).fill(-1));assert(no.status.startsWith("NO"),"negative product factor");products.push({n:18*k,models:String(9n**BigInt(k)),sat:true,unsatReplacement:true})}
 return {seed:720726,faces,stats,root,controls,products,limitations:"General q-Horn recognition not executed; mixed samples use explicit generated certificates; native recognition uses all-half or acquired Horn renaming. Products are disconnected. Planar rotations explicitly checked. Coupled affine guards and general higher-degree closure unexecuted."}
}
console.log(JSON.stringify(audit(),null,2));
