function audit(){
const assert=(b,m)=>{if(!b)throw Error(m)};
const E=[[0,7],[0,9],[0,19],[1,3],[1,14],[1,18],[2,11],[2,13],[2,16],[3,5],[3,19],[4,7],[4,13],[4,15],[5,6],[5,9],[6,8],[6,16],[7,11],[8,10],[8,12],[9,18],[10,11],[10,15],[12,14],[12,15],[13,17],[14,16],[17,18],[17,19]],n=20,M=74474769;
const A=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{A[u].push([v,i]);A[v].push([u,i])});
const count=x=>{let a=0;while(x){x&=x-1;a++}return a};
function* match(V,m=0){if(!V){yield m;return}const u=31-Math.clz32(V&-V);for(const [v,i] of A[u])if(V>>v&1)yield* match(V^(1<<u)^(1<<v),m|1<<i)}
function cycles(m){const seen=new Set(),C=[];for(let u=0;u<n;u++)if(!seen.has(u)){let c=[u],prev=-1,v=u;for(;;){let [w]=A[v].find(([w,i])=>!(m>>i&1)&&w!==prev);if(w===u)break;c.push(w);prev=v;v=w}c.forEach(v=>seen.add(v));C.push(c)}return C}
const Ms=[...match((1<<n)-1)],C=cycles(M),even=Ms.filter(m=>cycles(m).every(c=>!(c.length%2))),hist={},dHist={};let scans=0,minEven=99,witness=null;
for(let x=0;x<1<<n;x+=2){let d=0;E.forEach(([u,v],i)=>{if(!((x>>u^x>>v)&1))d|=1<<i});if(count(d&~M)!==2)continue;scans++;const b=Math.min(...Ms.map(m=>count(d&~m)));hist[b]=(hist[b]||0)+1;for(const m of even){const k=count(d&~m);dHist[k]=(dHist[k]||0)+1;if(k<minEven){minEven=k;witness={x,m}}}}
assert(scans===140&&hist[2]===140&&minEven===2&&Ms.length===31&&even.length===18,"strict plateau");
const col=E.map((_,i)=>witness.m>>i&1?2:-1);for(const c of cycles(witness.m))c.forEach((u,i)=>{const v=c[(i+1)%c.length];col[A[u].find(([w])=>w===v)[1]]=i%2});assert(A.every(l=>new Set(l.map(([v,i])=>col[i])).size===3),"lift");
function cyclic(S){let U=S;while(U){let b=U&-U,vertices=0,degree=0;const todo=[31-Math.clz32(b)];U^=b;for(let i=0;i<todo.length;i++){let u=todo[i];vertices++;for(const [v] of A[u])if(S>>v&1){degree++;if(U>>v&1){U^=1<<v;todo.push(v)}}}if(degree>=2*vertices)return true}return false}
let minCut=31,side=0;const all=(1<<n)-1;
for(let S=1;S<1<<(n-1);S++){let t=0;for(const [u,v] of E)t+=(S>>u^S>>v)&1;if(t>=minCut)continue;if(cyclic(S)&&cyclic(all^S)){minCut=t;side=S}}
assert(minCut===4,"cyclic cut");
let g=99;for(let u=0;u<n;u++)for(const [v,k] of A[u]){const d=Array(n).fill(-1),q=[u];d[u]=0;for(let i=0;i<q.length;i++)for(const [w,j] of A[q[i]])if(j!==k&&d[w]<0){d[w]=d[q[i]]+1;q.push(w)}if(d[v]>=0)g=Math.min(g,d[v]+1)}
assert(g===4,"girth");
return {edges:E,old_matching:M,old_cycles:C,perfect_matchings:Ms.length,even_matchings:even.length,all_optimal_cuts:scans,best_response_hist:hist,even_matching_cost_hist:dHist,min_cost_to_even:minEven,witness,edge_colors:col,cyclic_cut:minCut,cut_side_mask:side,girth:g};
}
console.log(JSON.stringify(audit(),null,2));
