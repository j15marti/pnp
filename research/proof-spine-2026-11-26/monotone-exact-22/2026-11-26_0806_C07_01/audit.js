function audit(){
let checks=0,seed=26112607;
const assert=(x,msg="")=>{checks++;if(!x)throw Error("audit failure "+checks+" "+msg)};
const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const valid=(F,x)=>F.every(r=>r.reduce((s,v)=>s+x[v],0)===2);
function compiler(F,n){
 let next=0,occ=Array.from({length:n},()=>[]),A=[],B=[],links=[];
 for(const row of F){A.push(row.map(v=>{let i=next++;occ[v].push(i);return i}))}
 for(const o of occ)for(let j=0;j+1<o.length;j++){const p=[next++,next++,next++];A.push([o[j],...p]);B.push([o[j+1],...p]);links.push([o[j],o[j+1],p])}
 return {A,B,F:[...A,...B],n:next,occ,links}
}
function lift(C,x){let y=Array(C.n).fill(-1);C.occ.forEach((o,v)=>o.forEach(i=>y[i]=x[v]));for(const [a,b,p] of C.links){assert(y[a]===y[b]);p.forEach((v,j)=>y[v]=+(j<2-y[a]))}assert(valid(C.F,y));return y}
function forest(F){let parent=new Map(),size=new Map();function find(x){if(!parent.has(x)){parent.set(x,x);size.set(x,1)}while(parent.get(x)!==x)x=parent.get(x);return x}for(let i=0;i<F.length;i++)for(const v of F[i]){let a=find("f"+i),b=find("v"+v);assert(a!==b);parent.set(b,a);size.set(a,size.get(a)+size.get(b))}return Math.max(0,...[...parent.keys()].filter(x=>parent.get(x)===x).map(x=>size.get(x)))}
function closure(F,n,pin=-1,b=0){let x=Array(n).fill(-1);if(pin>=0)x[pin]=b;let change=true;while(change){change=false;for(const r of F){let s=0,u=[];for(const v of r){if(x[v]<0)u.push(v);else s+=x[v]}if(s>2||s+u.length<2)return null;if(u.length&&(s===2||s+u.length===2))for(const v of u){x[v]=+(s!==2);change=true}}}return x}
function quotient(F,n){
 let p=Array.from({length:n},(_,i)=>i);function root(a){while(p[a]!==a){p[a]=p[p[a]];a=p[a]}return a}
 let merges=0,rounds=0;
 for(;;){rounds++;let seen=new Map(),change=false;
 for(const row of F){let r=row.map(root);if(new Set(r).size!==4)continue;for(let i=0;i<4;i++){let k=r.filter((_,j)=>j!==i).sort((a,b)=>a-b).join(",");let v=r[i];if(seen.has(k)){let a=root(v),b=root(seen.get(k));if(a!==b){p[a]=b;change=true;merges++}}else seen.set(k,v)}}if(!change)break}
 let rows=[...new Map(F.map(r=>{let t=r.map(root).sort((a,b)=>a-b);return [t.join(","),t]})).values()];
 return {root,rows,merges,rounds}
}
function privateTerminal(F,n){
 let q=quotient(F,n),rows=q.rows,stack=[],vals=new Map();
 function word(r,ext,priv,z,w){return r.reduce((s,v)=>s+(ext.includes(v)?(z>>ext.indexOf(v))&1:(w>>priv.indexOf(v))&1),0)}
 for(;;){
 let occ=new Map();for(const r of rows)for(const v of new Set(r))occ.set(v,(occ.get(v)||0)+1);
 let next=[],removed=0,used=new Set();
 for(const r of rows){let ids=[...new Set(r)],priv=ids.filter(v=>occ.get(v)===1),ext=ids.filter(v=>occ.get(v)>1),table=[],any=false,all=true;
 for(let z=0;z<1<<ext.length;z++){let witness=-1;for(let w=0;w<1<<priv.length;w++){if(word(r,ext,priv,z,w)===2){witness=w;break}}if(witness>=0)any=true;else all=false;table.push(witness)}
 if(!any)return {status:"NO",merges:q.merges,rounds:q.rounds,peeled:stack.length};
 if(all){stack.push({ext,priv,table});removed++;}else next.push(r)
 }
 rows=next;if(!rows.length)break;if(!removed)return {status:"UNKNOWN",merges:q.merges,rounds:q.rounds,peeled:stack.length};
 }
 while(stack.length){let {ext,priv,table}=stack.pop();let z=0;ext.forEach((v,i)=>{if(!vals.has(v))vals.set(v,0);z|=vals.get(v)<<i});let w=table[z];assert(w>=0);priv.forEach((v,i)=>{assert(!vals.has(v)||vals.get(v)===((w>>i)&1));vals.set(v,(w>>i)&1)})}
 let x=Array.from({length:n},(_,v)=>vals.get(q.root(v))??0);assert(valid(F,x));return {status:"YES",merges:q.merges,rounds:q.rounds,peeled:q.rows.length}
}
function grid(k,bad){let n=2*k*k,F=[],h=(i,j)=>i*k+j,v=(i,j)=>k*k+i*k+j;
 function eq(a,b){let p=[n++,n++,n++];F.push([a,...p],[b,...p])}
 for(let i=0;i<k;i++)for(let j=0;j<k;j++){if(j+1<k)eq(h(i,j),h(i,j+1));if(i+1<k)eq(v(i,j),v(i+1,j));F.push([h(i,j),v(i,j),n++,n++])}
 if(bad)F.push([0,1,2,3]);return {F,n}
}
function minCut(F){let m=F.length,ids=[...new Set(F.flat())],n=ids.length,vi=new Map(ids.map((v,i)=>[v,i])),S=m+2*n,T=S+1,L=T+1,M=n+1,best=n+1;
 for(let a=0;a<m;a++)for(let b=a+1;b<m;b++)for(let c=0;c<m;c++)for(let d=c+1;d<m;d++){
 if(a===c||a===d||b===c||b===d)continue;let g=Array.from({length:L},()=>Array(L).fill(0));for(let i=0;i<n;i++)g[m+2*i][m+2*i+1]=1;
 for(let i=0;i<m;i++)for(const v of F[i]){let j=vi.get(v);g[i][m+2*j]=M;g[m+2*j+1][i]=M}
 g[S][a]=g[S][b]=g[c][T]=g[d][T]=M;let flow=0;
 for(;;){let prev=Array(L).fill(-1),q=[S];prev[S]=S;for(let z=0;z<q.length&&prev[T]<0;z++)for(let v=0;v<L;v++)if(prev[v]<0&&g[q[z]][v]>0){prev[v]=q[z];q.push(v)}if(prev[T]<0){let A=F.filter((_,i)=>prev[i]>=0),B=F.filter((_,i)=>prev[i]<0);let u=new Set(A.flat()),w=new Set(B.flat());assert(A.length>=2&&B.length>=2);assert([...u].filter(x=>w.has(x)).length===flow);break}let f=M;for(let v=T;v!==S;v=prev[v])f=Math.min(f,g[prev[v]][v]);for(let v=T;v!==S;v=prev[v]){g[prev[v]][v]-=f;g[v][prev[v]]+=f}flow+=f}
 best=Math.min(best,flow)}
 return best
}
function bruteCut(F){let best=Infinity;for(let z=0;z<1<<F.length;z++){let A=F.filter((_,i)=>(z>>i)&1),B=F.filter((_,i)=>!((z>>i)&1));if(A.length<2||B.length<2)continue;let u=new Set(A.flat()),v=new Set(B.flat());best=Math.min(best,[...u].filter(x=>v.has(x)).length)}return best}
let cutCases=0,tariff=0,grids=[],gadgetWords=0,randomCases=0;
for(let i=0;i<80;i++){let m=4+rnd(4),F=[];for(let j=0;j<m;j++){let s=new Set();while(s.size<1+(j%4))s.add(rnd(9));F.push([...s])}assert(minCut(F)===bruteCut(F));cutCases++}
for(let c=2;c<=12;c++)for(let a=2;a<=24;a++)for(let b=a;b<=60;b++){let A=BigInt(a),B=BigInt(b),m=A+B,d=BigInt(c),q=(A-1n)*m**(d-1n)/A**d;if(q<1n)continue;assert(q*A**d+(B+1n)**d<m**d);tariff++}
for(let i=0;i<32;i++){let F=[];for(let j=0;j<1+rnd(7);j++){let s=new Set();while(s.size<4)s.add(rnd(7));F.push([...s])}let C=compiler(F,7);assert(forest(C.A)<=21);assert(forest(C.B)<=5);let q=quotient(C.F,C.n);for(let z=0;z<128;z++){let x=Array.from({length:7},(_,v)=>(z>>v)&1);if(valid(F,x)){lift(C,x);gadgetWords++}}for(const o of C.occ)for(const a of o)assert(q.root(a)===q.root(o[0]));randomCases++}
for(let k of [4,6,8,12,20])for(let bad of [false,true]){let G=grid(k,bad),C=compiler(G.F,G.n),a=forest(C.A),b=forest(C.B);assert(a<=21&&b<=5);let x=closure(C.F,C.n);assert(x&&x.every(z=>z<0));let probes=0;if(k<=6)for(let v=0;v<C.n;v++)for(let s=0;s<2;s++){let y=closure(C.F,C.n,v,s);assert(y&&y.filter(t=>t>=0).length===1);probes++}
 let out=privateTerminal(C.F,C.n);assert(out.status===(bad?"NO":"YES"),JSON.stringify({k,bad,out}));grids.push({k,bad,sourceVars:G.n,sourceClauses:G.F.length,compiledVars:C.n,compiledClauses:C.F.length,forestMax:[a,b],probes,...out})}
return {checks,cutCases,tariff,randomCases,gadgetWords,grids};
}
console.log(JSON.stringify(audit(),null,2));
