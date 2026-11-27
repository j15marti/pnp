// C08-18 adaptive affine-direction audit; node audit.js
function audit(){
let seed=20261126,checks=0,sccCalls=0,baseCalls=0,guardCalls=0,rankImports=0;
function ok(t,msg){checks++;if(!t)throw Error(msg||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function par(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return(0x6996>>>(x&15))&1}
function gauss(d,rows=[]){let A=Array(d).fill(null),r=0,bad=false;function reduce(a,b=0){for(let i=d-1;i>=0&&a;i--)if(A[i]&&((a>>>i)&1)){a^=A[i][0];b^=A[i][1]}return[a,b]}function add(a,b=0){[a,b]=reduce(a,b);if(!a){if(b)bad=true;return b?-1:0}A[31-Math.clz32(a)]=[a,b];r++;return 1}for(let [a,b] of rows)add(a,b);function solve(x=0,hom=false){for(let i=0;i<d;i++)if(A[i]&&((hom?0:A[i][1])^par(A[i][0]&x)))x^=1<<i;return x}function kernel(){let K=[];for(let i=0;i<d;i++)if(!A[i])K.push(solve(1<<i,true));return K}return{add,reduce,solve,kernel,get rank(){return r},get bad(){return bad},get rows(){return A.filter(Boolean)}}}
function obs(M,z){return M.a.map((a,i)=>par(a&z)^M.b[i])}
function valid(M,z){let y=obs(M,z);return M.B.every(([a,b])=>y[a>>1]===(a&1)||y[b>>1]===(b&1))}
function hull2(p,B){sccCalls++;let adj=Array.from({length:2*p},()=>[]),rev=Array.from({length:2*p},()=>[]);
function edge(u,v){adj[u].push(v);rev[v].push(u)}for(let [u,v] of B){edge(u^1,v);edge(v^1,u)}
let order=[],vis=new Uint8Array(2*p);
function dfs(u){vis[u]=1;for(let v of adj[u])if(!vis[v])dfs(v);order.push(u)}for(let i=0;i<2*p;i++)if(!vis[i])dfs(i);
let C=new Int32Array(2*p).fill(-1),k=0;for(let u of order.reverse())if(C[u]<0){let q=[u];C[u]=k;for(let i=0;i<q.length;i++)for(let v of rev[q[i]])if(C[v]<0){C[v]=k;q.push(v)}k++}
for(let i=0;i<p;i++)if(C[2*i]===C[2*i+1])return{bad:true};
let D=Array.from({length:k},()=>new Set);for(let u=0;u<2*p;u++)for(let v of adj[u])if(C[u]!==C[v])D[C[u]].add(C[v]);let seen=new Int32Array(k),s=0;function reach(u,v){if(u===v)return true;if(u>v)return false;s++;seen[u]=s;let q=[u];for(let i=0;i<q.length;i++)for(let w of D[q[i]]){if(w===v)return true;if(w<v&&seen[w]!==s){seen[w]=s;q.push(w)}}return false}
let rows=[],x=[],groups=new Map;for(let i=0;i<p;i++){let a=C[2*i],b=C[2*i+1];x[i]=+(b>a);if(reach(a,b))rows.push([i,-1,1]);else if(reach(b,a))rows.push([i,-1,0]);let key=Math.min(a,b);if(groups.has(key)){let j=groups.get(key);rows.push([i,j,+(C[2*j+1]!==b)])}else groups.set(key,i)}
return{rows,x,bad:false}}
function close(M,rows=[],B=M.B){baseCalls++;let H=gauss(M.d,rows),rounds=0;if(H.bad)return{status:"NO",H};
for(;;){rounds++;let sig=M.a.map((a,i)=>H.reduce(a,M.b[i])),L=B.slice(),rep=new Map;
for(let i=0;i<sig.length;i++){let [r,b]=sig[i];if(!r)L.push([2*i+b,2*i+b]);else if(rep.has(r)){let j=rep.get(r),t=b^sig[j][1];L.push([2*i,2*j+(1^t)],[2*i+1,2*j+t])}else rep.set(r,i)}
let T=hull2(M.a.length,L);if(T.bad)return{status:"NO",H,rounds};let old=H.rank;
for(let [i,j,t] of T.rows)if(H.add(M.a[i]^(j<0?0:M.a[j]),t^M.b[i]^(j<0?0:M.b[j]))<0)return{status:"NO",H,rounds};
if(H.rank!==old)continue;
let z=H.solve();if(valid({...M,B},z))return{status:"YES",H,z,rounds};let J=gauss(M.d,H.rows);for(let i=0;i<M.a.length;i++)J.add(M.a[i],T.x[i]^M.b[i]);if(!J.bad){z=J.solve();ok(valid({...M,B},z));return{status:"YES",H,z,rounds}}
return{status:"OPEN",H,rounds}}
}
function merge(d,A,B){if(A.status==="NO")return B.status==="NO"?null:B.H;if(B.status==="NO")return A.H;let u=A.H.solve(),v=B.H.solve(),D=gauss(d);for(let x of [...A.H.kernel(),...B.H.kernel(),u^v])D.add(x);let H=gauss(d);for(let h of D.kernel())H.add(h,par(h&u));return H}
function directions(M,H){let a=M.a.map(a=>H.reduce(a)[0]),S=new Set(a.filter(Boolean));for(let i=0;i<a.length;i++)for(let j=0;j<i;j++)if(a[i]^a[j])S.add(a[i]^a[j]);return [...S].sort((a,b)=>a-b)}
function adaptive(M,initial=[],maxRounds=M.d+1){let rows=initial.slice(),rounds=[],total=0;for(let pass=0;pass<maxRounds;pass++){let A=close(M,rows);if(A.status!=="OPEN")return{status:A.status,rounds,total,z:A.z};let H=A.H;let cand=directions(M,H),changed=false,log={rank:H.rank,candidates:cand.length,probes:0};for(let h of cand){guardCalls+=2;total+=2;log.probes+=2;let a=close(M,H.rows.concat([[h,0]])),b=close(M,H.rows.concat([[h,1]]));if(a.status==="YES"||b.status==="YES"){rounds.push({...log,winning:h,kind:"witness"});return{status:"YES",rounds,total,z:a.status==="YES"?a.z:b.z}}let J=merge(M.d,a,b);if(!J){rounds.push({...log,winning:h,kind:"two contradictions"});return{status:"NO",rounds,total}}if(J.rank>H.rank){rankImports+=J.rank-H.rank;rounds.push({...log,winning:h,kind:"merged",newRank:J.rank});rows=J.rows;changed=true;break}}
if(!changed){rounds.push(log);return{status:"OPEN",rounds,total}}}return{status:"OPEN",rounds,total}}
function old(M){let B=M.B.slice(),keys=new Set(B.map(([a,b])=>[Math.min(a,b),Math.max(a,b)].join(","))),rows=[],n=M.a.length,total=0;function put(a,b){if(a===(b^1))return false;let k=[Math.min(a,b),Math.max(a,b)].join(",");if(keys.has(k))return false;keys.add(k);B.push([a,b]);return true}
for(let r=0;r<=2*n*n+2;r++){let A=close(M,rows,B);if(A.status!=="OPEN")return{status:A.status,total,z:A.z};rows=A.H.rows;let changed=false;for(let i=0;i<n;i++)for(let b of [0,1]){total++;guardCalls++;let q=close(M,rows.concat([[M.a[i],b^M.b[i]]]),B);if(q.status==="YES")return{status:"YES",total,z:q.z};if(q.status==="NO"){changed=put(2*i+(b^1),2*i+(b^1))||changed;continue}for(let j=0;j<n;j++){let [r,t]=q.H.reduce(M.a[j],M.b[j]);if(!r)changed=put(2*i+(b^1),2*j+t)||changed}}if(!changed)return{status:"OPEN",total}}throw Error("old cap")}
function exact(M){let r=[];for(let z=0;z<(1<<M.d);z++)if(valid(M,z))r.push(z);return r}
function verify(M,result,W){if(result.status==="YES")ok(valid(M,result.z)&&W.length>0);if(result.status==="NO")ok(!W.length)}
// Independent check of projection criterion for every affine direction, and merge containment.
let projectionCases=0,projectionChecks=0,mergeChecks=0;for(let t=0;t<100;t++){let d=3+rnd(5),p=3+rnd(8),M={d,a:Array.from({length:p},()=>rnd(1<<d)),b:Array.from({length:p},()=>rnd(2)),B:Array.from({length:1+rnd(2*p)},()=>[rnd(2*p),rnd(2*p)])},H=gauss(d);let z=rnd(1<<d),q=rnd(d);while(H.rank<q){let a=1+rnd((1<<d)-1);H.add(a,par(a&z))}let cand=new Set(directions(M,H)),base=M.a.map((a,i)=>H.reduce(a,M.b[i]));for(let h=1;h<(1<<d);h++){if(H.reduce(h)[0]!==h)continue;let J=gauss(d,H.rows.concat([[h,0]]));let s=M.a.map((a,i)=>J.reduce(a,M.b[i]));let visible=s.some(([a],i)=>!a&&base[i][0])||s.some(([a],i)=>s.slice(0,i).some(([b],j)=>a===b&&base[i][0]!==base[j][0]));ok(visible===cand.has(h));projectionChecks++}
let A=close(M,H.rows);if(A.status!=="NO"){let D=directions(M,A.H);if(D.length){let h=D[0],a=close(M,A.H.rows.concat([[h,0]])),b=close(M,A.H.rows.concat([[h,1]])),J=merge(d,a,b);for(let x=0;x<1<<d;x++)if(H.rows.every(([a,b])=>par(a&x)===b)&&valid(M,x)){ok(J&&J.rows.every(([a,b])=>par(a&x)===b));mergeChecks++}if(!J)ok(!exact(M).some(x=>H.rows.every(([a,b])=>par(a&x)===b)))}}projectionCases++}
// Actual native raw AG9 and cyclic source; observations are exact cuts of anchored original graph.
function native(F,n){let S=new Set,a=[],B=[];function get(u,v){let h=(u?1<<(u-1):0)^(v?1<<(v-1):0),i=a.indexOf(h);if(i<0){i=a.length;a.push(h)}return i}
for(let part of F){let deg=Array(n).fill(0);for(let c of part){ok(new Set(c).size===3);c.forEach(v=>deg[v]++);let L=[];for(let [i,j] of [[0,1],[0,2],[1,2]]){let u=c[i],v=c[j],key=Math.min(u,v)*n+Math.max(u,v);ok(!S.has(key));S.add(key);L.push(2*get(u,v)+1)}B.push([L[0],L[1]],[L[0],L[2]],[L[1],L[2]])}ok(deg.every(v=>v===1))}
ok(F.length===4);return{d:n-1,a,b:a.map(()=>0),B}}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const cyclic=p=>Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[i,p+(i+s)%p,2*p+(i+3*s)%p]));
let nativeResults=[];for(let [name,F,n] of [["AG9",AG,9],["cyclic15",cyclic(5),15]]){let M=native(F,n),W=exact(M),a=close(M),b=old(M),c=adaptive(M);verify(M,a,W);verify(M,b,W);verify(M,c,W);nativeResults.push({name,n,actualModelsUpToComplement:W.length,base:a.status,old:b,new:c})}
// Search small affine/2CNF controls under explicit same model; not native NAE4.
let randomStats={cases:0,unsat:0,oldOpenNo:0,newRefutedOldOpen:0,newSolvedOldOpen:0};let example=null,examples=[];
for(let t=0;t<1800;t++){let d=4+rnd(4),p=8+2*rnd(4),M={d,a:Array.from({length:p},()=>1+rnd((1<<d)-1)),b:Array.from({length:p},()=>rnd(2)),B:[]};if(t%3===0)for(let i=0;i<p;i+=2)M.B.push([2*i+1,2*i+3]);else for(let j=0;j<p+4+rnd(p);j++)M.B.push([rnd(2*p),rnd(2*p)]);let W=exact(M);randomStats.cases++;randomStats.unsat+=!W.length;let a=old(M);verify(M,a,W);if(a.status!=="OPEN")continue;if(!W.length)randomStats.oldOpenNo++;let b=adaptive(M);verify(M,b,W);if(b.status!=="OPEN"){randomStats.newSolvedOldOpen++;if(!W.length&&b.status==="NO"){randomStats.newRefutedOldOpen++;if(!example)example={M,actualModels:W,old:a,new:b}}if(examples.length<6)examples.push({d,p,actualModels:W.length,old:a.status,new:b.status,rounds:b.rounds});}
if(example&&randomStats.cases>=300)break}
function mul(a,b){let r=0;while(b){if(b&1)r^=a;b>>>=1;a<<=1;if(a&64)a^=67}return r}
let col=Array.from({length:64},(_,t)=>1|(t<<1)|(mul(mul(t,t),t)<<7)),M={d:13,a:col,b:col.map((_,i)=>((i<32?648477357:3348622548) >>> (i%32))&1),B:Array.from({length:32},(_,i)=>[4*i+1,4*i+3])};ok(exact(M).length===0);let H=close(M);ok(H.status==="OPEN"&&H.H.rank===0);let C=directions(M,H.H);ok(C.length===2080);let all=new Set(C),visible=0,silent=0,guardFailures=0,commonGain=0,branchRanks={};for(let h=1;h<8192;h++){if(!all.has(h)){let a=gauss(13,[[h,0]]),s=col.map(c=>a.reduce(c)[0]);ok(s.every(Boolean)&&new Set(s).size===64);silent++;continue}
visible++;guardCalls+=2;let a=close(M,[[h,0]]),b=close(M,[[h,1]]);ok(a.status==="OPEN"&&b.status==="OPEN");let J=merge(13,a,b);ok(J.rank===0);branchRanks[a.H.rank+","+b.H.rank]=(branchRanks[a.H.rank+","+b.H.rank]||0)+1}
return{seed:20261126,checks,sccCalls,baseCalls,guardCalls,rankImports,projectionCases,projectionChecks,mergeChecks,nativeResults,randomStats,example,examples,barrier:{latent:13,observations:64,clauses:32,exactModels:0,visible,silent,guardFailures,commonGain,branchRanks}};
}
console.log(JSON.stringify(audit(),null,2));
