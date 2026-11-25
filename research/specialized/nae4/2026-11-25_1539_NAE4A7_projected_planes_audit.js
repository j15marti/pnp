// NAE4A7: exact dual-plane messages, deterministic small-instance audit.
// Run node <file>. Bit masks limited to small audit instances.
let seed=20261125, checks=0;
function rand(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function ok(v){++checks;if(!v)throw Error("assertion "+checks)}
const hi=x=>31-Math.clz32(x);
function par(x){let p=0;while(x){p^=1;x&=x-1}return p}
function basis(xs){let b=Array(30).fill(0);for(let x of xs){while(x){let i=hi(x);if(b[i])x^=b[i];else{b[i]=x;break}}}for(let i=0;i<30;i++)if(b[i])for(let j=i+1;j<30;j++)if(b[j]&(1<<i))b[j]^=b[i];return b.filter(Boolean).reverse()}
function coords(x,B){let k=0;for(let i=0;i<B.length;i++)if(x&(1<<hi(B[i]))){x^=B[i];k|=1<<i}if(x)throw Error("not in span");return k}
function meet(A,B){let e=Array(30).fill(0),t=Array(30).fill(0),out=[];for(let [v,tag] of [...A.map(a=>[a,a]),...B.map(b=>[b,0])]){while(v){let i=hi(v);if(e[i]){v^=e[i];tag^=t[i]}else{e[i]=v;t[i]=tag;break}}if(!v&&tag)out.push(tag)}return basis(out)}
function project(x,A,B){return B.reduce((m,b,i)=>m|(par(x&coords(b,A))<<i),0)}
function solve(rows){let B=Array(30).fill(null);for(let [v,r] of rows){while(v){let i=hi(v);if(B[i]){v^=B[i][0];r^=B[i][1]}else{B[i]=[v,r];break}}if(!v&&r)return null}let x=0;for(let i=0;i<30;i++)if(B[i]&&(par(x&B[i][0])!==B[i][1]))x|=1<<i;return x}
function truth(c,x){return c.f.reduce((m,a,i)=>m|(par(x&a)<<i),0)!==c.bad}
function oracle(n,cs){let words=[];for(let x=0;x<(1<<n);x++)if(cs.every(c=>truth(c,x)))words.push(x);return words}
function graph(cs,shuffle){let m=cs.length,g=Array.from({length:m},()=>[]),q=Array.from({length:m},(_,i)=>i);if(shuffle)for(let i=q.length-1;i>0;i--){let j=rand(i+1);[q[i],q[j]]=[q[j],q[i]]}while(q.length>1){let r=[];for(let i=0;i<q.length;i+=2){if(i+1===q.length){r.push(q[i]);continue}let v=g.length,a=q[i],b=q[i+1];g.push([a,b]);g[a].push(v);g[b].push(v);r.push(v)}q=r}return {g,root:q[0]}}
function dp(cs,shuffle=false){let m=cs.length,{g,root}=graph(cs,shuffle),S=new Map,M=new Map,width=0,visits=0;
function span(v,p){let key=v+","+p;if(S.has(key))return S.get(key);let s=basis(v<m?cs[v].f:g[v].filter(w=>w!==p).flatMap(w=>span(w,v)));S.set(key,s);return s}
function message(v,p){let key=v+","+p;if(M.has(key))return M.get(key);let U=span(v,p),W=p<0?[]:meet(U,span(p,v)),T=new Map; width=Math.max(width,W.length);if(v<m){for(let x=0;x<(1<<U.length);x++){let c=cs[v],z=c.f.reduce((a,f,i)=>a|(par(x&coords(f,U))<<i),0);if(z!==c.bad){let k=project(x,U,W);if(!T.has(k))T.set(k,{x})}}}else{let children=g[v].filter(w=>w!==p).map(w=>[w,message(w,v)]),J=basis(children.flatMap(([,a])=>a.W));let maps=children.map(([,a])=>a.W.map(b=>coords(b,J))),wm=W.map(b=>coords(b,J));for(let x=0;x<(1<<J.length);x++){visits++;let keys=maps.map(a=>a.reduce((k,c,i)=>k|(par(c&x)<<i),0));if(!children.every(([,a],i)=>a.T.has(keys[i])))continue;let k=wm.reduce((a,c,i)=>a|(par(c&x)<<i),0);if(!T.has(k))T.set(k,{children:children.map(([w],i)=>[w,keys[i]])})}}
let obj={W,U,T};M.set(key,obj);return obj}
let ans=message(root,-1),witness=null;
if(ans.T.has(0)){let rows=[];function rec(v,p,k){let a=message(v,p),r=a.T.get(k);if(v<m){a.U.forEach((b,i)=>rows.push([b,(r.x>>i)&1]));return}for(let [c,z] of r.children)rec(c,v,z)}rec(root,-1,0);witness=solve(rows);ok(witness!==null&&cs.every(c=>truth(c,witness)))}
let deletions=[],projections=[];for(let v=0;v<m;v++){let U=basis(cs[v].f),comp=g[v].length?message(g[v][0],v):{W:[],T:new Map([[0,{}]])};deletions.push(comp.T.size>0);let allowed=[];for(let x=0;x<(1<<U.length);x++){let z=cs[v].f.reduce((a,f,i)=>a|(par(x&coords(f,U))<<i),0);if(z!==cs[v].bad&&comp.T.has(project(x,U,comp.W)))allowed.push(x)}projections.push(allowed)}return {sat:ans.T.has(0),witness,deletions,projections,width,visits}}
function clause(a,b,c){return {f:[(1<<a)^(1<<b),(1<<a)^(1<<c)],bad:0}}
function plane(){let cs=[];for(let j=0;j<3;j++)cs.push(clause(j,3+j,6+j));for(let i=0;i<3;i++)cs.push(clause(3*i,3*i+1,3*i+2));for(let j=0;j<3;j++){cs.push(clause(j,3+(j+1)%3,6+(j+2)%3));cs.push(clause(j,3+(j+2)%3,6+(j+1)%3))}return cs}
function cyclic(p){let cs=[];for(let j=0;j<4;j++)for(let i=0;i<p;i++)cs.push(clause(i,p+(i+j)%p,2*p+(i+2*j)%p));return cs}
function test(n,cs){let words=oracle(n,cs),r=dp(cs),q=dp(cs,true);ok(r.sat===(words.length>0));ok(q.sat===r.sat);for(let i=0;i<cs.length;i++){let d=oracle(n,cs.filter((_,j)=>i!==j)).length>0;ok(r.deletions[i]===d&&q.deletions[i]===d);let U=basis(cs[i].f),p=[...new Set(words.map(x=>U.reduce((a,b,j)=>a|(par(x&b)<<j),0)))].sort((a,b)=>a-b);ok(JSON.stringify(r.projections[i])===JSON.stringify(p));ok(JSON.stringify(q.projections[i])===JSON.stringify(p))}return {count:words.length,width:r.width,rewiredWidth:q.width,visits:r.visits}}
let controls=[];for(let k=0;k<3;k++)controls.push({name:"affine_plane_minus_"+k,...test(9,plane().slice(k))});controls.push({name:"single_triple",...test(3,[clause(0,1,2)])});
let sat=0,unsat=0,random=0;for(let n=2;n<=8;n++)for(let job=0;job<50;job++){let cs=[];for(let i=0,m=1+rand(9);i<m;i++){let a=1+rand((1<<n)-1),b=1+rand((1<<n)-1);if(a===b)b=0;cs.push({f:b?[a,b]:[a],bad:rand(b?4:2)})}let r=test(n,cs);if(r.count)sat++;else unsat++;random++}
function distinctPlanes(cs){let p=new Map;for(let c of cs){let B=basis(c.f);if(B.length===2)p.set(B.join(","),[B[0],B[1],B[0]^B[1]])}return [...p.values()]}
function coordTest(P){let count=new Map;for(let p of P)for(let x of p)count.set(x,(count.get(x)||0)+1);let F=[...count].filter(([,n])=>n>=2).map(([x])=>x);if(basis(F).length!==F.length)return false;let chosen=[...F];for(let p of P){let a=p.filter(x=>F.includes(x));if(a.length>2)return false;for(let x of p)if(a.length<2&&!a.includes(x)){a.push(x);chosen.push(x)}}return basis(chosen).length===chosen.length}
function coordOracle(P){function rec(i,A){if(basis(A).length!==A.length)return false;if(i===P.length)return true;let p=P[i];return [0,1,2].some(j=>rec(i+1,[...new Set([...A,...p.filter((_,k)=>k!==j)])]))}return rec(0,[])}
let coordJobs=0,coordYes=0;for(let n=2;n<=6;n++)for(let job=0;job<100;job++){let cs=[];for(let i=0,m=1+rand(7);i<m;i++){let a=1+rand((1<<n)-1),b=1+rand((1<<n)-1);if(a!==b)cs.push({f:[a,b]})}let P=distinctPlanes(cs),r=coordTest(P);ok(r===coordOracle(P));coordJobs++;coordYes+=r}
function quotient(x,W){for(let a of W)if(x&(1<<hi(a)))x^=a;return x}
let backdoorJobs=0;for(let n=9;n<=9;n++)for(let k=0;k<=2;k++)for(let job=0;job<150;job++){let W=[];while(W.length<k)W=basis([...W,1+rand((1<<n)-1)]);let P=distinctPlanes(plane().map(c=>({f:c.f.map(x=>quotient(x,W))})));ok(!coordTest(P));backdoorJobs++}
let big=dp(cyclic(7));ok(big.sat&&big.deletions.every(Boolean));controls.push({name:"cyclic_p7_genuine",sat:big.sat,width:big.width,visits:big.visits,witness:big.witness,bruteForce:false});
console.log(JSON.stringify({seed:20261125,checks,controls,random,sat,unsat,coordJobs,coordYes,backdoorJobs}));