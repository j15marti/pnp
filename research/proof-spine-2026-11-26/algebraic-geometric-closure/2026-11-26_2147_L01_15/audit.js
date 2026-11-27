function assert(x,m){if(!x)throw Error(m||"assert")}

function fixture(yes=false){let A=[[1,2,3,5,7,9],[3,4,6,10],[0,3,5,6,7,8],[2,4,5],[0,1,2,5],[1,2,3],[0,1,7],[1,6],[0,1,9,10],[1,8],[2,8]];if(yes)A[0].push(10);return {A,S:[0,1,2],R:[[3,4,5],[6,7],[8,9,10]]}}

function matching(rows){let M=new Map();function f(i,s){for(let j of rows[i])if(!s.has(j)){s.add(j);if(!M.has(j)||f(M.get(j),s)){M.set(j,i);return true}}return false}let k=0;for(let i=0;i<rows.length;i++)if(f(i,new Set()))k++;return k}

function cycles(p){let seen=new Set(),c=0;for(let i=0;i<p.length;i++)if(!seen.has(i)){c++;let j=i;while(!seen.has(j)){seen.add(j);j=p[j]}}return c}

function enumeration(A,ledger){let n=A.length,order=Array.from({length:n},(_,i)=>i).sort((i,j)=>A[i].length-A[j].length||i-j),p=Array(n).fill(-1),used=new Set(),out=[];function dfs(k){assert(++ledger.nodes<=1000000,"reference node cap");if(k===n){out.push({p:p.slice(),c:cycles(p)});return}let i=order[k];for(let j of A[i])if(!used.has(j)){p[i]=j;used.add(j);dfs(k+1);used.delete(j)}}dfs(0);return out}

function support(A,L,par){let T=L.filter(x=>!par||x.c%2);if(!T.length)return null;return A.map((_,i)=>Array.from(new Set(T.map(x=>x.p[i]))).sort((a,b)=>a-b))}

function connected(A){if(!A)return false;let n=A.length;for(let rev of [false,true]){let q=[0],s=new Set(q);for(let i of q){let row=rev?A.map((r,j)=>r.includes(i)?j:-1).filter(j=>j>=0):A[i];for(let j of row)if(!s.has(j)){s.add(j);q.push(j)}}if(s.size!==n)return false}return true}

function hall(A,S,R,ledger){ledger.hall++;let d=R.map(r=>Math.max(1,r.length-matching(r.map(i=>A[i].filter(j=>r.includes(j))))));let total=d.reduce((a,b)=>a+b,0);let ok=total<=S.length,cert=null;
 for(let rev of [false,true]){let N=R.map(r=>S.filter(s=>r.some(v=>rev?A[v].includes(s):A[s].includes(v))));let rows=N.flatMap((z,i)=>Array.from({length:d[i]},()=>z));let good=matching(rows)===rows.length;
 // Independent weighted Hall subset check for small region count.
 let witness=null;assert(R.length<=12);for(let mask=1;mask<2**R.length;mask++){let u=new Set(),need=0,regions=[];for(let i=0;i<R.length;i++)if(mask&(1<<i)){need+=d[i];regions.push(i);for(let x of N[i])u.add(x)}ledger.hallSubsets++;if(need>u.size&&!witness)witness={rev,regions,need,neighbors:[...u]}}
 assert(good===!witness,"Hall equivalence");if(!good&&!cert)cert=witness;ok=ok&&good;
 }return {ok,d,cert}}

function pin(A,i,j){return A.map((r,u)=>r.filter(v=>u===i?v===j:v!==j))}

function close(f,mode){let {S,R}=f,A=f.A.map(r=>r.slice().sort((a,b)=>a-b));let par=mode!=="H",h=mode!=="P",ledger={nodes:0,guard:0,hall:0,hallSubsets:0,passes:0},steps=[];let before=JSON.stringify(A);
 while(true){assert(++ledger.passes<=A.length*A.length+1);let C=enumeration(A,ledger);let B=support(A,C,par);if(!connected(B))return {status:"NO",terminal:"support",steps,ledger};
 let delta=A.reduce((s,r,i)=>s+r.length-B[i].length,0);A=B;if(delta)steps.push({supportDeleted:delta});
 if(h){let H=hall(A,S,R,ledger);if(!H.ok)return {status:"NO",terminal:H,steps,ledger}}
 let bad=[];for(let i=0;i<A.length;i++)for(let j of A[i]){assert(++ledger.guard<=10000,"guard cap");let F=pin(A,i,j),Q=support(F,C.filter(x=>x.p[i]===j),par);if(!connected(Q)){bad.push({i,j,why:"support"});continue}if(h){let H=hall(Q,S,R,ledger);if(!H.ok)bad.push({i,j,why:"Hall",d:H.d,cert:H.cert})}}
 if(!bad.length)return {status:"UNKNOWN",steps,ledger,residual:A};steps.push({guards:bad});let set=new Set(bad.map(e=>e.i+","+e.j));A=A.map((r,i)=>r.filter(j=>!set.has(i+","+j)));assert(JSON.stringify(A)!==before);before=JSON.stringify(A);
 }}

function run(){let f=fixture(),ledger={nodes:0},C=enumeration(f.A,ledger),T=C.filter(x=>x.c%2);assert(C.length===60&&T.length===34&&!C.some(x=>x.c===1));assert(JSON.stringify(support(f.A,C,true))===JSON.stringify(f.A));let lanes=Object.fromEntries(["H","P","I"].map(m=>[m,close(f,m)]));assert(lanes.H.status==="UNKNOWN"&&lanes.P.status==="UNKNOWN"&&lanes.I.status==="NO");let y=fixture(true),ly={nodes:0},Y=enumeration(y.A,ly);assert(Y.some(x=>x.c===1));let yes=close(y,"I");assert(yes.status!=="NO");let guards=[];for(let i=0;i<f.A.length;i++)for(let j of f.A[i]){let z={...f,A:pin(f.A,i,j)},r=close(z,"I");guards.push({i,j,status:r.status,ledger:r.ledger})}return {fixture:f,total:C.length,target:T.length,cyclesHistogram:Object.fromEntries([...new Set(C.map(x=>x.c))].map(k=>[k,C.filter(x=>x.c===k).length])),initialReferenceNodes:ledger.nodes,lanes,yes:{added:[0,10],total:Y.length,tours:Y.filter(x=>x.c===1),result:yes.status,ledger:yes.ledger},guards}}
console.log(JSON.stringify(run(),null,2));
