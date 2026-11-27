function ck(x,m="check"){if(!x)throw Error(m)}

function range(n){return Array.from({length:n},(_,i)=>i)}

function family(s,p){let n=3*s,A=range(n).map(()=>[]),R=range(s).map(i=>[s+2*i,s+2*i+1]);function add(i,j){if(!A[i].includes(j))A[i].push(j)}for(let i=0;i<s;i++)for(let j=0;j<s;j++)if(i!==j)add(i,j);for(let i=0;i<s;i++){let [u,v]=R[i];add(u,v);add(v,u);add(i,u);add((i+1)%s,v);add(v,p[i]);add(u,p[(i+s-1)%s])}return {A,S:range(s),R,p}}

function cycles(p){let seen=new Set(),c=0;for(let i=0;i<p.length;i++)if(!seen.has(i)){c++;let j=i;while(!seen.has(j)){seen.add(j);j=p[j]}}return c}

function parity(p){return (p.length-cycles(p))%2}

function ref(A,cap=2000000){let p=[],used=new Set(),out=[],nodes=0;function rec(i){ck(++nodes<=cap,"reference cap");if(i===A.length){out.push({p:p.slice(),c:cycles(p)});return}for(let j of A[i])if(!used.has(j)){used.add(j);p.push(j);rec(i+1);p.pop();used.delete(j)}}rec(0);return {out,nodes}}

function sc(A){for(let rev of [false,true]){let st=[0],seen=new Set(st);while(st.length){let i=st.pop();let L=rev?range(A.length).filter(j=>A[j].includes(i)):A[i];for(let j of L)if(!seen.has(j)){seen.add(j);st.push(j)}}if(seen.size!==A.length)return false}return true}

function sup(A,C){return A.map((a,i)=>a.filter(j=>C.some(c=>c.p[i]===j)))}

function match(L,k){let owner=Array(k).fill(-1);function dfs(i,seen){for(let j of L[i])if(!seen.has(j)){seen.add(j);if(owner[j]===-1||dfs(owner[j],seen)){owner[j]=i;return true}}return false}return L.every((_,i)=>dfs(i,new Set()))}

function tables(A,S,R){return R.map(B=>{let out=new Map();function dfs(a,path){if(path.length===B.length){for(let b of S)if(A[path.at(-1)].includes(b)){let key=a+","+b;if(!out.has(key))out.set(key,{a,b,path:path.slice()})}return}for(let v of B)if(!path.includes(v)&&(path.length?A[path.at(-1)].includes(v):A[a].includes(v)))dfs(a,[...path,v])}for(let a of S)dfs(a,[]);return [...out.values()]})}

function hall(A,S,R){let T=R.map(B=>({in:S.filter(a=>B.some(v=>A[a].includes(v))),out:S.filter(b=>B.some(v=>A[v].includes(b)))}));let ids=new Map(S.map((s,i)=>[s,i]));return ["in","out"].every(k=>match(T.map(t=>t[k].map(x=>ids.get(x))),S.length))}

function gsolve(rows,n){rows=rows.map(([v,b])=>[v,b]);let r=0,piv=[];for(let j=0;j<n;j++){let k=r;while(k<rows.length&&!(rows[k][0]&(1n<<BigInt(j))))k++;if(k===rows.length)continue;[rows[r],rows[k]]=[rows[k],rows[r]];for(let i=0;i<rows.length;i++)if(i!==r&&(rows[i][0]&(1n<<BigInt(j)))){rows[i][0]^=rows[r][0];rows[i][1]^=rows[r][1]}piv.push(j);r++}if(rows.some(([v,b])=>!v&&b))return null;let x=0n,basis=[];for(let i=0;i<r;i++)if(rows[i][1])x|=1n<<BigInt(piv[i]);for(let j=0;j<n;j++)if(!piv.includes(j)){let v=1n<<BigInt(j);for(let i=0;i<r;i++)if(rows[i][0]&(1n<<BigInt(j)))v|=1n<<BigInt(piv[i]);basis.push(v)}return {x,basis,r}}

function chart(T,s){if(T.some(t=>!t.length))return {kind:"EMPTY"};if(T.some(t=>t.length>2))return {kind:"UNKNOWN"};let L=T.map(t=>t.length===1?[t[0],t[0]]:t),n=L.length;ck(n===s);let rows=[];for(let i=0;i<n;i++)if(T[i].length===1)rows.push([1n<<BigInt(i),0]);for(let side of ["a","b"])for(let j=0;j<s;j++){let mask=0n,c=0;for(let i=0;i<n;i++){let z=Number(L[i][0][side]===j),w=Number(L[i][1][side]===j);c^=z;if(z!==w)mask|=1n<<BigInt(i)}rows.push([mask,1^c])}let F=gsolve(rows,n);if(!F)return {kind:"EMPTY"};function perm(x){let p=Array(s).fill(-1);for(let i=0;i<n;i++){let {a,b}=L[i][Number((x>>BigInt(i))&1n)];ck(p[a]===-1);p[a]=b}ck(new Set(p).size===s);return p}let p0=perm(F.x),sg=parity(p0),d=F.basis.length,coeff=F.basis.map(v=>parity(perm(F.x^v))^sg);let mask=0n;for(let i=0;i<d;i++)if(coeff[i])mask|=1n<<BigInt(i);let H=gsolve([[mask,sg^((s-1)%2)]],d);return {kind:H?"PARITY-POSSIBLE":"WRONG-PARITY",F,H,sg,coeff,perm,rows,parityChecks:d+1}}

function words(T,cap=65536){let out=[],x=[];function rec(i){if(i===T.length){ck(out.length<cap);let a=x.map(z=>z.a),b=x.map(z=>z.b);if(new Set(a).size===T.length&&new Set(b).size===T.length){let p=[];for(let j=0;j<a.length;j++)p[a[j]]=b[j];out.push({x:x.map((z,j)=>T[j].indexOf(z)),p,c:cycles(p)})}return}for(let t of T[i]){x.push(t);rec(i+1);x.pop()}}rec(0);return out}

function prevClosure(G,R,mode){let A=G.A.map(a=>a.slice()),C=R.out.filter(c=>mode==="ordinary"||c.c%2),rounds=0,probes=0,deletions=0;while(true){rounds++;A=sup(A,C);if(!C.length||!sc(A)||!hall(A,G.S,G.R))return {kind:"NO",rounds,probes,deletions};let bad=[];for(let i=0;i<A.length;i++)for(let j of A[i]){probes++;ck(probes<=10000);let Q=C.filter(c=>c.p[i]===j),B=sup(A,Q);if(!Q.length||!sc(B)||!hall(B,G.S,G.R))bad.push([i,j])}if(!bad.length)return {kind:"UNKNOWN",rounds,probes,deletions};for(let [i,j] of bad)A[i]=A[i].filter(v=>v!==j);deletions+=bad.length;C=C.filter(c=>c.p.every((v,i)=>A[i].includes(v)))}}

function auditSmall(G){let R=ref(G.A),C=R.out.filter(c=>c.c%2),A=sup(G.A,C),T=tables(A,G.S,G.R),X=chart(T,G.S.length),W=words(T);ck(!R.out.some(c=>c.c===1),"misclassified");ck(sc(A)&&A.every((a,i)=>a.length===G.A[i].length),"initial closure");ck(hall(A,G.S,G.R));ck(T.every(t=>t.length===2));ck(X.kind==="WRONG-PARITY");ck(W.length===2&&W.every(w=>w.c%2===0));let old=prevClosure(G,R,"target"),ord=prevClosure(G,R,"ordinary");return {n:A.length,arcs:A.flat().length,covers:R.out.length,target:C.length,referenceNodes:R.nodes,allSupport:true,ordinary:ord,previous:old,tables:T,chart:{kind:X.kind,dim:X.F.basis.length,coeff:X.coeff,baseParity:X.sg},words:W}}

function run(){let small=auditSmall(family(4,[1,0,3,2])),large=[];for(let s of [6,8,12,24,48,96,192]){let G=family(s,range(s).map(i=>(i+4)%s)),T=tables(G.A,G.S,G.R),X=chart(T,s);ck(sc(G.A)&&hall(G.A,G.S,G.R));ck(T.every(t=>t.length===2)&&X.kind==="WRONG-PARITY"&&X.F.basis.length===1);let P=X.perm(X.F.x),Q=X.perm(X.F.x^X.F.basis[0]);ck(cycles(P)>1&&cycles(Q)>1);large.push({s,n:G.A.length,arcs:G.A.flat().length,chartDim:X.F.basis.length,cycles:[cycles(P),cycles(Q)],kind:X.kind,parityChecks:X.parityChecks})}
let G=family(15,range(15).map(i=>(i+5)%15)),T=tables(G.A,G.S,G.R),X=chart(T,15);ck(X.kind==="PARITY-POSSIBLE"&&X.F.basis.length===1);let hostile=[cycles(X.perm(X.F.x)),cycles(X.perm(X.F.x^X.F.basis[0]))];ck(hostile.every(c=>c>1&&c%2));
let control=family(4,[1,2,3,0]),Y=chart(tables(control.A,control.S,control.R),4),U=words(tables(control.A,control.S,control.R));ck(U.some(u=>u.c===1)&&Y.kind==="PARITY-POSSIBLE");let z=12345,rand=k=>{z=(Math.imul(z,1664525)+1013904223)>>>0;return z%k},tests=0,nonempty=0,parityWords=0;for(let s=2;s<=8;s++)for(let it=0;it<150;it++){let T=range(s).map(()=>range(2).map(()=>({a:rand(s),b:rand(s)}))),F=chart(T,s),W=words(T);tests++;ck((F.kind==="EMPTY")===!W.length);if(!W.length)continue;nonempty++;ck(BigInt(W.length)===(1n<<BigInt(F.F.basis.length)));for(let w of W){let a=F.sg; // evaluate linear parity via unique coefficient extraction from free-coordinate basis
let x=w.x.reduce((v,b,i)=>v|(BigInt(b)<<BigInt(i)),0n),delta=x^F.F.x;for(let i=F.F.basis.length-1;i>=0;i--){let v=F.F.basis[i]; // determine free coordinate from unit-column property by locating a column unused by other basis vectors and with zero particular bit; use exhaustive tiny coefficients instead below
}
let ok=false;for(let m=0;m<(1<<F.F.basis.length);m++){let y=F.F.x,sg=F.sg;for(let i=0;i<F.F.basis.length;i++)if(m&(1<<i)){y^=F.F.basis[i];sg^=F.coeff[i]}if(y===x){ck(sg===parity(w.p),"nonlinear parity");ok=true;break}}ck(ok);parityWords++}ck((F.kind==="PARITY-POSSIBLE")===W.some(w=>w.c%2))}
return {small,large,hostile:{n:45,cycles:hostile,parity:"UNKNOWN",boundedNullity:"NO"},yesControl:{n:12,tourCharts:U.filter(u=>u.c===1).length},random:{tests,nonempty,parityWords},execution:"sequential; prior closure simulated by exhaustive cover reference, not general RST algorithm; no full equal-bit cap"}}
console.log(JSON.stringify(run(),null,2));
