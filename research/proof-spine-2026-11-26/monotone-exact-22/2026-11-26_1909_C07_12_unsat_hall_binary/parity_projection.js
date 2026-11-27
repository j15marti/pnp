function audit(){
const ok=(x,s)=>{if(!x)throw Error(s)};
function build(t,k,type){
 let D=[],res=[],E=[];function add(rs){D.push(rs.map(r=>{res.push(r);return res.length-1}))}
 if(type==="tight"||type==="check"){for(let i=0;i<t;i++)add(Array.from({length:t},(_,j)=>"r"+j));for(let i=0;i<k;i++)add(["a"+i,"b"+i,"r0"]);for(let i=0;i<k-(type==="check"?1:0);i++)for(let c=0;c<2;c++)E.push([D[t+i][c],D[t+(i+1)%k][c]])}
 else if(type==="hall"){for(let i=0;i<=t;i++)add(Array.from({length:t},(_,j)=>"r"+j))}
 else {for(let i=0;i<11;i++)add([`${i}a`,`${i}b`,`${i}c`]);for(let i=0;i<5;i++){let j=(i+1)%5;for(const [u,v] of [[i,j],[i+5,j],[i,j+5],[i+5,10]])for(let c=0;c<3;c++)E.push([D[u][c],D[v][c]])}}
 let own=[];D.forEach((d,i)=>d.forEach(a=>own[a]=i));for(let a=0;a<res.length;a++)for(let b=a+1;b<res.length;b++)if(own[a]!==own[b]&&res[a]===res[b])E.push([a,b]);
 E=[...new Set(E.map(x=>x.slice().sort((a,b)=>a-b).join(",")))].map(x=>x.split(",").map(Number));
 let n=0,rows=[],alloc=()=>n++,row=(...r)=>{ok(new Set(r).size===4,"distinct");rows.push(r);return rows.length-1},nae=(a,b,c)=>row(a,b,c,alloc());
 let r0=alloc(),r1=alloc(),b=alloc(),u=alloc(),v=alloc();row(r0,b,r1,u);row(r0,b,u,v);row(r0,b,v,r1);
 let X=[],Y=[],cp=[];for(let i=0;i<3*res.length;i++){X.push(alloc());Y.push(alloc());cp.push(row(X[i],Y[i],r0,r1))}
 let S=[],paths=[],G=[],ctx=[];
 for(const d of D){let p=[r1,...d.slice(1).map(()=>alloc()),r0];paths.push(p);d.forEach((a,i)=>{let m=[alloc(),alloc()],rr=[];for(let j=0;j<2;j++)rr.push(nae(p[i],m[j],X[3*a+j]),nae(m[j],p[i+1],Y[3*a+j]));S[a]={a,s:p[i],t:p[i+1],m,rr}})}
 function clause(a,b){G.push([a,b]);let phys=l=>l>0?X[l-1]:Y[-l-1];ctx.push(nae(phys(a),phys(b),r0))}
 for(let a=0;a<res.length;a++){clause(3*a+1,3*a+3);clause(3*a+2,3*a+3)}for(const [a,b] of E)clause(-(3*a+3),-(3*b+3));
 return {t,k,type,D,own,n,rows,r0,r1,b,u,v,X,Y,cp,S,paths,G,ctx}
}
function src(F){return JSON.stringify({n:F.n,rows:F.rows,guards:[]})}
function hash(s){let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619)>>>0;return h.toString(16)}
function meter(N){return {v:0,cap:64*N*N,tick(n=1){this.v+=n;if(this.v>this.cap)throw Error("CAP")}}}
function pins(F){return [[F.r0,0],[F.r1,1],[F.b,0],[F.u,1],[F.v,1]]}
function gac(F,P,M){let w=Array(F.n).fill(-1);for(const [i,x] of P){if(w[i]!==-1&&w[i]!==x)return false;w[i]=x}let ch=true;while(ch){ch=false;for(const r of F.rows){M.tick();let s=0,U=[];for(const i of r)w[i]<0?U.push(i):s+=w[i];if(s>2||s+U.length<2)return false;if(s===2||s+U.length===2)for(const i of U){w[i]=s===2?0:1;ch=true}}}return true}
function check(F,M){let R=F.rows,used=new Set([0,1,2]);ok(R[0].join()===[F.r0,F.b,F.r1,F.u].join()&&R[1].join()===[F.r0,F.b,F.u,F.v].join()&&R[2].join()===[F.r0,F.b,F.v,F.r1].join(),"hub");
 function row(i,q){M.tick();ok(!used.has(i)&&R[i].slice(0,q.length).join()===q.join(),"row map");used.add(i)}
 F.X.forEach((x,i)=>row(F.cp[i],[x,F.Y[i],F.r0,F.r1]));
 F.D.forEach((d,i)=>{let p=F.paths[i];ok(p[0]===F.r1&&p.at(-1)===F.r0,"endpoints");d.forEach((a,j)=>{let s=F.S[a];ok(s.s===p[j]&&s.t===p[j+1]&&F.own[a]===i,"stage map");for(let z=0;z<2;z++){row(s.rr[2*z],[s.s,s.m[z],F.X[3*a+z]]);row(s.rr[2*z+1],[s.m[z],s.t,F.Y[3*a+z]])}})});
 let phys=l=>l>0?F.X[l-1]:F.Y[-l-1];F.G.forEach((c,i)=>row(F.ctx[i],[phys(c[0]),phys(c[1]),F.r0]));ok(used.size===R.length,"row coverage");
 let ids=[F.r0,F.r1,F.b,F.u,F.v,...F.X,...F.Y,...F.paths.flatMap(p=>p.slice(1,-1)),...F.S.flatMap(s=>s.m),...F.ctx.map(i=>R[i][3]),...F.S.flatMap(s=>s.rr.map(i=>R[i][3]))];ok(ids.length===F.n&&new Set(ids).size===F.n&&ids.every(i=>i>=0&&i<F.n),"private separation");
 ok(gac(F,pins(F),M),"initial occupancy closure");
}
let id=l=>2*(Math.abs(l)-1)+(l<0?1:0);
function close(n,G,M){let adj=Array.from({length:2*n},()=>[]);for(const [a,b] of G){adj[id(a)^1].push(id(b));adj[id(b)^1].push(id(a));M.tick(2)}
 let R=[];for(let i=0;i<2*n;i++){let r=new Uint8Array(2*n),q=[i];r[i]=1;M.tick(2*n);for(let j=0;j<q.length;j++)for(let v of adj[q[j]]){M.tick();if(!r[v]){r[v]=1;q.push(v)}}R.push(r)}
 let forced=[];for(let i=0;i<n;i++){M.tick();if(R[2*i][2*i+1]&&R[2*i+1][2*i])return {no:true,R,forced};if(R[2*i][2*i+1])forced.push([i,0]);if(R[2*i+1][2*i])forced.push([i,1])}return {no:false,R,forced}
}
function acquire(F,M){let c=close(F.X.length,F.G,M);ok(!c.no&&c.forced.length===0,"initial G");let p=F.own.length,B=Array.from({length:p},()=>new Uint8Array(p)),P=a=>[id(-(3*a+1)),id(-(3*a+2))];
 function bad(U){for(const a of U)for(const b of U){M.tick();if(c.R[a][b^1])return true}return false}
 let e=0;for(let a=0;a<p;a++){ok(!bad(P(a)),"single option");for(let b=a+1;b<p;b++)if(F.own[a]!==F.own[b]&&bad(P(a).concat(P(b)))){B[a][b]=B[b][a]=1;e++}}return {B,e,D:F.D.map(d=>d.slice())}
}
function binary(D,B,M){let d=D.filter(a=>a.length<=2);if(d.some(a=>!a.length))return true;let G=[];for(let i=0;i<d.length;i++){if(d[i].length===1)G.push([i+1,i+1]);for(let j=i+1;j<d.length;j++)for(let a=0;a<d[i].length;a++)for(let b=0;b<d[j].length;b++){M.tick();if(B[d[i][a]][d[j][b]])G.push([a===0?-(i+1):i+1,b===0?-(j+1):j+1])}}return close(d.length,G,M).no}
function arc(D,B,M){D=D.map(d=>d.slice());let ch=true,removed=0;while(ch){ch=false;for(let i=0;i<D.length;i++){let d=D[i].filter(a=>D.every((v,j)=>j===i||v.some(b=>{M.tick();return !B[a][b]})));if(d.length<D[i].length){removed+=D[i].length-d.length;D[i]=d;ch=true}if(!d.length)return {no:true,removed}}}return {no:binary(D,B,M),removed}}
function classes(F,B,M){let n=B.length,vis=new Uint8Array(n),cls=Array(n),groups=[];for(let i=0;i<n;i++)if(!vis[i]){let q=[i];vis[i]=1;for(let j=0;j<q.length;j++)for(let v=0;v<n;v++){M.tick();if(B[q[j]][v]&&!vis[v]){vis[v]=1;q.push(v)}}let good=true;for(let a of q)for(let b of q){M.tick();if(F.own[a]!==F.own[b]&&!B[a][b])good=false}for(let g of good?[q]:q.map(a=>[a])){let r=groups.length;groups.push(g);g.forEach(a=>cls[a]=r)}}return {cls,groups}}
function match(D,cls,M,pin=null){let r=new Map(),fix=pin?pin[0]:-1;if(pin)r.set(cls[pin[1]],fix);function aug(i,s){for(let a of D[i]){M.tick();let v=cls[a];if(s.has(v))continue;s.add(v);let j=r.get(v);if(j===undefined||(j!==fix&&aug(j,s))){r.set(v,i);return true}}return false}for(let i=0;i<D.length;i++)if(i!==fix&&!aug(i,new Set()))return false;return true}
function filter(F,Q,M){let {cls,groups}=classes(F,Q.B,M),D=Q.D;if(!match(D,cls,M))return {no:true,removed:[],groups:groups.length};let removed=[];D.forEach((d,i)=>d.forEach(a=>{if(!match(D,cls,M,[i,a]))removed.push(a)}));return {no:false,removed,groups:groups.length}}
function integrated(F,Q,M){let f=filter(F,Q,M);if(f.no)return {status:"NO",reason:"Hall deficiency",imports:0,groups:f.groups};let D=Q.D.map(d=>d.slice()),G=F.G.map(c=>c.slice()),imports=0;for(let a of f.removed){D[F.own[a]]=D[F.own[a]].filter(b=>b!==a);G.push([3*a+1,3*a+2]);imports++;let c=close(F.X.length,G,M);if(c.no)return {status:"NO",reason:"context",imports,groups:f.groups};if(!gac(F,pins(F).concat(c.forced.flatMap(([i,v])=>[[F.X[i],v],[F.Y[i],1-v]])),M))return {status:"NO",reason:"occupancy",imports,groups:f.groups}}
 let A=arc(D,Q.B,M);return {status:A.no?"NO":"UNKNOWN",reason:A.no?"binary core":"no contradiction",imports,groups:f.groups}
}
function native(F,M){
 let cases=0;for(let s of F.S)for(let A=0;A<2;A++)for(let B=0;B<2;B++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){let V=new Map([[s.s,A],[s.t,B],[F.X[3*s.a],x],[F.Y[3*s.a],1-x],[F.X[3*s.a+1],y],[F.Y[3*s.a+1],1-y]]),pass=false;
 for(let z=0;z<4;z++){V.set(s.m[0],z&1);V.set(s.m[1],z>>1);if(s.rr.every(i=>{M.tick();let n=F.rows[i].slice(0,3).reduce((a,b)=>a+V.get(b),0);return n===1||n===2}))pass=true}
 ok(pass===(A===B||(A===1?(!x&&!y):!!(x&&y))),`truth table ${F.type} ${A}${B}${x}${y} ${pass}`);cases++}
 let E=new Set();for(let i=0;i<F.own.length;i++){ok(F.G[2*i].join()===[3*i+1,3*i+3].join()&&F.G[2*i+1].join()===[3*i+2,3*i+3].join(),"proxy clauses")}
 for(let [a,b] of F.G.slice(2*F.own.length)){M.tick();ok(a<0&&b<0&&a%3===0&&b%3===0,"proxy conflict");E.add([(-a)/3-1,(-b)/3-1].sort((a,b)=>a-b).join(","))}
 let has=(a,b)=>{M.tick();return E.has([a,b].sort((a,b)=>a-b).join(","))},D=F.D,t=F.t,k=F.k;
 if(F.type==="tight"||F.type==="hall"){let h=F.type==="tight"?t:t+1;for(let r=0;r<t;r++)for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)ok(has(D[i][r],D[j][r]),"resource clique");if(F.type==="hall")return {status:"NO",cases,cert:"pigeonhole"};for(let i=0;i<k;i++){for(let j=0;j<t;j++)ok(has(D[t+i][2],D[j][0]),"blocked resource");for(let c=0;c<2;c++)ok(has(D[t+i][c],D[t+(i+1)%k][c]),"rim conflict")}ok(k%2===1,"odd rim");return {status:"NO",cases,cert:"conservation and odd parity"}}
 let trials=0;function rec(i,L){if(i===D.length)return L;for(let a of D[i]){trials++;M.tick();if(L.every(b=>!has(a,b))){let w=rec(i+1,L.concat(a));if(w)return w}}return null}let w=rec(0,[]);return {status:w?"POSSIBLE":"NO",cases,trials,choice:w}
}
function verifyWitness(F,C,M){let sel=new Set(C),w=Array(F.n).fill(-1);for(let [i,v] of pins(F))w[i]=v;for(let a=0;a<F.own.length;a++)for(let j=0;j<3;j++){let v=j===2?+sel.has(a):+!sel.has(a);w[F.X[3*a+j]]=v;w[F.Y[3*a+j]]=1-v}
 F.D.forEach((d,i)=>{let cut=d.findIndex(a=>sel.has(a));ok(cut>=0,"control choice");F.paths[i].forEach((a,j)=>w[a]=+(j<=cut));for(let a of d){let s=F.S[a];for(let j=0;j<2;j++){let v=0;for(;v<2;v++){w[s.m[j]]=v;if(s.rr.slice(2*j,2*j+2).every(r=>{let k=F.rows[r].slice(0,3).reduce((a,b)=>a+w[b],0);return k===1||k===2}))break}ok(v<2,"control middle")}}});
 for(let i of [...F.ctx,...F.S.flatMap(s=>s.rr)]){let r=F.rows[i];w[r[3]]=2-r.slice(0,3).reduce((a,b)=>a+w[b],0)}ok(w.every(v=>v===0||v===1)&&F.rows.every(r=>r.reduce((a,b)=>a+w[b],0)===2),"control full source");
}
function parityProjection(F,Q,M){
 const k=5,D=F.D,B=Q.B,proof=[];
 ok(D.length===11&&D.every(d=>d.length===3),"chart arity");
 for(let i=0;i<k;i++){
  let j=(i+1)%k,scope=[10,i,j,i+5,j+5],valid=0,checked=0;
  for(let w=0;w<243;w++){
   let x=w,c=[];for(let a=0;a<5;a++){c.push(x%3);x=Math.floor(x/3)}
   checked++;M.tick();let compatible=true;
   for(let a=0;a<5;a++)for(let b=a+1;b<5;b++){M.tick();if(B[D[scope[a]][c[a]]][D[scope[b]][c[b]]])compatible=false}
   if(!compatible)continue;valid++;
   let p=c[1]===c[0]?c[3]:c[1],q=c[2]===c[0]?c[4]:c[2];
   ok(p!==c[0]&&q!==c[0]&&p!==q,"failed local recoloring certificate");
  }
  proof.push({i,j,scope,checked,valid})
 }
 ok(k%2===1,"odd parity");return {status:"NO",proof,conclusion:"all edges force inequality on the same two colors other than the apex color; odd cycle impossible"}
}
let jobs=[];
for(let [t,k,type] of [[0,0,"hostile"]]){
 let F=build(t,k,type),N=8*src(F).length,H=hash(src(F)),Ms=Array.from({length:4},()=>meter(N)),copies=Ms.map(()=>JSON.parse(JSON.stringify(F)));for(let i=0;i<4;i++){ok(hash(src(copies[i]))===H,"hash");check(copies[i],Ms[i])}
 let QA=acquire(copies[0],Ms[0]),A=arc(QA.D,QA.B,Ms[0]),B=filter(copies[1],acquire(copies[1],Ms[1]),Ms[1]),C=native(copies[2],Ms[2]),QI=acquire(copies[3],Ms[3]),I=integrated(copies[3],QI,Ms[3]);
 if(type==="check"){ok(C.status==="POSSIBLE"&&I.status==="UNKNOWN","control status");verifyWitness(F,C.choice,Ms[2])}else ok(C.status==="NO"&&(type==="hostile"?I.status==="UNKNOWN":I.status==="NO"),"NO status "+type+" "+JSON.stringify(I));
 let extra=parityProjection(copies[3],QI,Ms[3]);jobs.push({extra,t,k,type,N,n:F.n,rows:F.rows.length,options:F.own.length,hash:H,A:A.no?"NO":"UNKNOWN",Aremoved:A.removed,B:B.no?"NO":"UNKNOWN",Bremoved:B.removed.length,C:C.status,Ccases:C.cases,Ctrials:C.trials??null,I:I.status,reason:I.reason,imports:I.imports,groups:I.groups,edges:QI.e,meters:Ms.map(m=>({ticks:m.v,cap:m.cap}))})
}
return {jobs}
}
console.log(JSON.stringify(audit(),null,2));
