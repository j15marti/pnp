'use strict';
function experiment(){
let stats={closurePasses:0,rowTests:0,deletions:0,guardEdges:0,messagePairs:0,branchNodes:0,forestCalls:0,referenceTuples:0,witnessChecks:0,maxMessageStates:0}; const ok=(x)=>{if(!x)throw Error("assertion");};
let seed=2081125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
const row=(g,c)=>({g,c:c.map(BigInt)});
function check(F,K,h,w){stats.witnessChecks++;if(!w||w.length!==F.length)return false;let a=K.map(()=>0n),g=0;for(let i=0;i<F.length;i++){const r=F[i][w[i]];if(!r)return false;g^=r.g;for(let j=0;j<K.length;j++)a[j]+=r.c[j];}return g===h&&a.every((v,j)=>v<=K[j]);}
function brute(F,K,h){let found=false;function rec(i,g,c){if(i===F.length){stats.referenceTuples++;if(g===h&&c.every((x,j)=>x<=K[j]))found=true;return;}for(const r of F[i])rec(i+1,g^r.g,c.map((x,j)=>x+r.c[j]));}rec(0,0,K.map(()=>0n));return found;}
function solve(F,K,h,q,cap=65536){
const H=1<<q,n=F.length,m=K.length;
function closure(D){D=D.map(a=>a.slice());for(;;){stats.closurePasses++;if(D.some(a=>!a.length)||K.some(x=>x<0n))return null;
let mins=D.map((a,i)=>K.map((_,j)=>a.reduce((v,k)=>v===null||F[i][k].c[j]<v?F[i][k].c[j]:v,null)));
let total=K.map((_,j)=>mins.reduce((s,a)=>s+a[j],0n));if(total.some((x,j)=>x>K[j]))return null;
let changed=false;
outer:for(let i=0;i<n;i++){
 let reach=new Set([0]);for(let z=0;z<n;z++)if(z!==i){let nxt=new Set();for(const a of reach)for(const k of D[z]){stats.guardEdges++;nxt.add(a^F[z][k].g);}reach=nxt;}
 for(const k of D[i]){stats.rowTests++;let r=F[i][k];if(!reach.has(h^r.g)||r.c.some((x,j)=>total[j]-mins[i][j]+x>K[j])){D[i]=D[i].filter(a=>a!==k);stats.deletions++;changed=true;break outer;}}
}if(!changed)return D;}}
function normalize(D){let min=D.map((a,i)=>K.map((_,j)=>a.reduce((v,k)=>v===null||F[i][k].c[j]<v?F[i][k].c[j]:v,null)));
let B=K.map((v,j)=>v-min.reduce((s,a)=>s+a[j],0n));let R=D.map((a,i)=>a.map(k=>({id:k,g:F[i][k].g,c:F[i][k].c.map((x,j)=>x-min[i][j])})));
let adj=Array.from({length:n+m},()=>[]),edges=[];for(let i=0;i<n;i++)for(let j=0;j<m;j++)if(R[i].some(r=>r.c[j]>0n)){adj[i].push(n+j);adj[n+j].push(i);edges.push([i,n+j]);}
return {B,R,adj,edges};}
function cutset(edges){let par=Array.from({length:n+m},(_,i)=>i),C=new Set();function root(x){while(par[x]!==x){x=par[x];}return x;}for(const [a,b] of edges){let x=root(a),y=root(b);if(x===y)C.add(a);else par[x]=y;}return [...C].sort((a,b)=>a-b);}
function forest(A){stats.forestCalls++;const {B,R,adj}=A,seen=new Set();
function put(M,g,c,w){let old=M[g];if(!old||c<old.c)M[g]={c,w};}
function combine(X,Y,limit=null){let Z=Array(H).fill(null);for(let a=0;a<H;a++)if(X[a])for(let b=0;b<H;b++)if(Y[b]){stats.messagePairs++;let c=X[a].c+Y[b].c;if(limit===null||c<=limit)put(Z,a^b,c,X[a].w.concat(Y[b].w));}stats.maxMessageStates=Math.max(stats.maxMessageStates,Z.filter(Boolean).length);return Z;}
function identity(g=0,c=0n,w=[]){let X=Array(H).fill(null);X[g]={c,w};return X;}
function visit(v,p){ok(!seen.has(v));seen.add(v);let ch=adj[v].filter(x=>x!==p).map(x=>[x,visit(x,v)]);
if(v>=n){let X=identity();for(let [,M] of ch)X=combine(X,M,B[v-n]);return X;}
let out=Array(H).fill(null);for(let r of R[v]){let X=identity(r.g,0n,[[v,r.id]]);for(let [u,M] of ch){let Y=M.map(x=>x&&x.c+r.c[u-n]<=B[u-n]?{c:0n,w:x.w}:null);X=combine(X,Y);}let c=p<0?0n:r.c[p-n];for(let a=0;a<H;a++)if(X[a])put(out,a,c,X[a].w);}stats.maxMessageStates=Math.max(stats.maxMessageStates,out.filter(Boolean).length);return out;}
let X=identity();for(let i=0;i<n;i++)if(!seen.has(i))X=combine(X,visit(i,-1));if(!X[h])return null;
let w=Array(n);for(let [i,k] of X[h].w)w[i]=k;ok(check(F,K,h,w));return w;}
let D=closure(F.map(a=>a.map((_,i)=>i)));if(!D)return {status:"UNSAT",cut:0,volume:0};
let A=normalize(D),C=cutset(A.edges),vol=C.reduce((p,i)=>p*BigInt(D[i].length),1n);if(vol>BigInt(cap))return {status:"UNKNOWN",cut:C.length,volume:vol.toString()};
function branch(D,j,initial=false){stats.branchNodes++;if(!initial)D=closure(D);if(!D)return null;let A=normalize(D);if(!cutset(A.edges).length)return forest(A);while(j<C.length&&D[C[j]].length===1)j++;ok(j<C.length);
let i=C[j];for(let k of D[i]){let X=D.slice();X[i]=[k];let w=branch(X,j+1);if(w)return w;}return null;}
let w=branch(D,0,true);return {status:w?"SAT":"UNSAT",cut:C.length,volume:Number(vol)};}
let results={randomForest:{SAT:0,UNSAT:0},randomCyclic:{SAT:0,UNSAT:0},controls:[],scales:[]};
for(let it=0;it<240;it++){let n=2+rnd(6),q=rnd(4),m=n-1+(it>=120?2:0),adj=Array.from({length:n},()=>Array(m).fill(false));
for(let j=0;j<n-1;j++){adj[j+1][j]=true;adj[rnd(j+1)][j]=true;}for(let j=n-1;j<m;j++){adj[rnd(n)][j]=true;adj[rnd(n)][j]=true;adj[rnd(n)][j]=true;}
let F=adj.map(a=>Array.from({length:2+rnd(2)},()=>row(rnd(1<<q),a.map(x=>x?rnd(4):0))));let K=Array.from({length:m},()=>BigInt(rnd(7))),h=rnd(1<<q);let b=brute(F,K,h),z=solve(F,K,h,q);ok(z.status===(b?"SAT":"UNSAT"));if(it<120)ok(z.cut===0);results[it<120?"randomForest":"randomCyclic"][z.status]++;}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function nae(es,n,relax=-1){let K=Array(es.length*2).fill(2n);if(relax>=0)K[relax]=3n;let F=Array.from({length:n},(_,i)=>[0,1].map(x=>row(0,es.flatMap(e=>e.includes(i)?[x,1-x]:[0,0]))));return [F,K];}
for(let j=-1;j<14;j++){let [F,K]=nae(fano,7,j),z=solve(F,K,0,0);ok(z.status===(j<0?"UNSAT":"SAT")&&brute(F,K,0)===(j>=0));results.controls.push({name:"Fano "+j,...z});}
function color(es,n){let K=Array(es.length*4).fill(1n),F=Array.from({length:n},(_,i)=>[0,1,2,3].map(x=>row(0,es.flatMap(e=>[0,1,2,3].map(y=>e.includes(i)&&x===y?1:0)))));return [F,K];}
let edges=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)edges.push([a,b]);
for(let j=-1;j<10;j++){let [F,K]=color(edges.filter((_,i)=>i!==j),5),z=solve(F,K,0,0);ok(z.status===(j<0?"UNSAT":"SAT")&&brute(F,K,0)===(j>=0));results.controls.push({name:"K5 "+j,...z});}
for(let n of [8,32,128]){let A=1n<<80n,F=Array.from({length:n},(_,i)=>[row(0,[A,...Array(n).fill(0)]),row(i%2?1:2,[A+1n,...Array.from({length:n},(_,j)=>i===j?1:0)])]);for(let off of [1,2]){let K=[BigInt(n)*A+BigInt(off),...Array(n).fill(1n)];let z=solve(F,K,3,2);ok(z.status===(off===1?"UNSAT":"SAT")&&z.cut===0);results.scales.push({n,off,capacity:K[0].toString(),...z});}}
for(let a of [3,4]){let F=Array.from({length:4},()=>[row(0,[2,0]),row(0,[0,2])]),K=[BigInt(a),BigInt(8-a)],z=solve(F,K,0,0);ok(z.status===(a===4?"SAT":"UNSAT"));results.controls.push({name:"partition "+a,...z});}
return {seed:2081125,results,stats};
}
console.log(JSON.stringify(experiment(),null,2));
