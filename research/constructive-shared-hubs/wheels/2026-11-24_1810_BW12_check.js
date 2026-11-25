function run(){
const R={seed:2081212,assertions:0,randomGraphs:0,pairQueries:0,componentGreedy:0,tightQueries:0,referenceModels:0,verifiedLifts:0,closureScans:0,closurePins:0,sourceChecks:0,sharp:[],closed:[],fano:[],scaling:[]};let seed=R.seed;const rnd=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};const ok=(x,m)=>{R.assertions++;if(!x)throw Error(m)};
const deg=(n,E)=>{let d=Array(n).fill(0);for(const [u,v] of E){d[u]++;d[v]++}return d};
const valid=(E,x)=>{for(const [u,v,s] of E){R.sourceChecks++;if((x[u]^x[v])===s)return false}return true};
function comp(n,E,excluded=[]){let seen=new Set(excluded),out=[];for(let i=0;i<n;i++)if(!seen.has(i)){let a=[i];seen.add(i);for(let j=0;j<a.length;j++)for(const [u,v] of E){let w=u===a[j]?v:v===a[j]?u:-1;if(w>=0&&!seen.has(w)){seen.add(w);a.push(w)}}out.push(a)}return out}
function greedy(n,E,C,root,initial){let x=initial.slice(),a=[root],seen=new Set(a),cs=new Set(C);for(let j=0;j<a.length;j++)for(const [u,v] of E){let w=u===a[j]?v:v===a[j]?u:-1;if(cs.has(w)&&!seen.has(w)){seen.add(w);a.push(w)}}ok(a.length===C.length,"connected");for(const u of a.reverse()){let bad=new Set;for(const [v,w,s] of E){let t=v===u?w:w===u?v:-1;if(t>=0&&x[t]>=0)bad.add(x[t]^s)}let c=[0,1,2,3].find(k=>!bad.has(k));ok(c!==undefined,"slack greedy");x[u]=c}R.componentGreedy++;return x}
function brute(n,E,vars,initial,all=false){let x=initial.slice(),out=[];function rec(i){if(i===vars.length){out.push(x.slice());return !all}let u=vars[i];for(let k=0;k<4;k++){x[u]=k;let good=true;for(const [v,w,s] of E){if((v===u||w===u)&&x[v]>=0&&x[w]>=0&&(x[v]^x[w])===s){good=false;break}}if(good&&rec(i+1))return true}x[u]=-1;return false}if(validPartial(E,x))rec(0);return out}
function validPartial(E,x){return E.every(([u,v,s])=>x[u]<0||x[v]<0||(x[u]^x[v])!==s)}
function analyze(n,E,name){
let D=deg(n,E),T=D.map((d,i)=>d<4?i:-1).filter(i=>i>=0);ok(D.every(d=>d<=4)&&comp(n,E).length===1&&T.length>0,"domain");let base=greedy(n,E,Array.from({length:n},(_,i)=>i),T[0],Array(n).fill(-1));ok(valid(E,base),"base");let init=Array(n).fill(-1);init[0]=0;let models=brute(n,E,Array.from({length:n-1},(_,i)=>i+1),init,true);R.referenceModels+=models.length;ok(models.length>0,"models");let use=T.map(()=>new Set),def=T.map(()=>0),equations=[],pair=[];
for(let ai=0;ai<T.length;ai++)for(let bi=ai+1;bi<T.length;bi++){
let a=T[ai],b=T[bi],components=comp(n,E,[a,b]),allocA=new Set,allocB=new Set,active=[];
for(let j=0;j<E.length;j++){let [u,v]=E[j];if((u===a&&v===b)||(u===b&&v===a)){allocA.add(j);allocB.add(j)}}
for(let C of components){let S=new Set(C),EA=[],EB=[];for(let j=0;j<E.length;j++){let [u,v]=E[j];if((u===a&&S.has(v))||(v===a&&S.has(u)))EA.push(j);if((u===b&&S.has(v))||(v===b&&S.has(u)))EB.push(j)}let slack=C.find(v=>D[v]<4),hard=slack===undefined&&EA.length>0&&EB.length>0;if(hard){EA.forEach(j=>allocA.add(j));EB.forEach(j=>allocB.add(j))}active.push({C,S,EA,EB,slack,hard})}
for(let [idx,A] of [[ai,allocA],[bi,allocB]])for(let j of A){ok(!use[idx].has(j),"disjoint allocation");use[idx].add(j)}
let actual=new Set(models.map(x=>x[a]^x[b])),pred=[];
for(let d=0;d<4;d++){R.pairQueries++;let x=Array(n).fill(-1);x[a]=0;x[b]=d;let good=validPartial(E,x);
if(good)for(let {C,S,EA,EB,slack,hard} of active){let local=E.filter(([u,v])=>S.has(u)||S.has(v));if(slack!==undefined)x=greedy(n,local,C,slack,x);else if(!hard){let shift=EA.length?base[a]:EB.length?base[b]^d:0;for(let v of C)x[v]=base[v]^shift}else{R.tightQueries++;let w=brute(n,local,C,x)[0];if(!w){good=false;break}x=w}}
ok(good===actual.has(d),"pair support");if(good){ok(valid(E,x)&&x[a]===0&&x[b]===d,"pair lift");pred.push(d);R.verifiedLifts++}}
let deficit=4-pred.length;ok(deficit<=allocA.size&&deficit<=allocB.size,"pair deficit");def[ai]+=deficit;def[bi]+=deficit;pair.push({a,b,support:pred,allocated:[allocA.size,allocB.size]});
for(let l=1;l<4;l++){let dot=v=>((v&l)&1)^(((v&l)>>1)&1);if(pred.every(v=>dot(v)===dot(pred[0]))){let row=0;for(let v of [a,b])for(let k=0;k<2;k++)if((l>>k)&1)row^=1<<(2*v+k);equations.push([row,dot(pred[0])])}}
}
for(let i=0;i<T.length;i++)ok(def[i]<=use[i].size&&use[i].size<=D[T[i]],"aggregate");
let basis=new Map;for(;;){R.closureScans++;let changed=false;for(let [row,rhs] of equations){for(let x of models){let v=0;for(let j=0;j<n;j++)v|=x[j]<<(2*j);let t=row&v,p=0;while(t){p^=1;t&=t-1}ok(p===rhs,"forced equation")}while(row){let p=31-Math.clz32(row),q=basis.get(p);if(q){row^=q[0];rhs^=q[1]}else{basis.set(p,[row,rhs]);R.closurePins++;changed=true;break}}if(!row)ok(rhs===0,"closure consistency");if(changed)break}if(!changed)break}
return {name,n,edges:E.length,terminals:T,degree:T.map(v=>D[v]),deficits:def,modelsAtRoot0:models.length,pair,closureRank:basis.size}
}
for(let t=0;t<180;t++){let n=3+rnd(6),E=[],D=Array(n).fill(0);for(let v=1;v<n;v++){let A=Array.from({length:v},(_,i)=>i).filter(i=>D[i]<4),u=A[rnd(A.length)];E.push([u,v,rnd(4)]);D[u]++;D[v]++}for(let j=0;j<n*2;j++){let u=rnd(n),v=rnd(n);if(u!==v&&D[u]<4&&D[v]<4&&D.reduce((a,b)=>a+b,0)<4*n-2){E.push([u,v,rnd(4)]);D[u]++;D[v]++}}analyze(n,E,"random");R.randomGraphs++}
R.sharp.push(analyze(2,[[0,1,1],[0,1,2],[0,1,3]],"full equality two terminals"));
R.sharp.push(analyze(3,[[0,1,2],[0,1,3],[0,2,1]],"parity plus independent exclusion saturates degree3"));
R.sharp.push(analyze(3,[[0,1,2],[0,1,3],[1,2,2],[1,2,3]],"one-bit chain: middle saturated"));
let star=[[0,1,0],[0,1,1],[0,2,0],[0,3,0]];
let res=analyze(4,star,"three-port higher-order relation");ok(res.pair.every(p=>p.support.length===4),"full pair marginals");let w=[-1,0,2,3];ok(brute(4,star,[0],w).length===0,"joint obstruction");R.sharp.push(res);
function rim(ds){let dp=new Map([[0,[]]]);for(let d of ds){let next=new Map;for(let [a,path] of dp)for(let v=0;v<4;v++)if(v!==0&&v!==d&&!next.has(a^v))next.set(a^v,[...path,v]);dp=next}let p=dp.get(0);if(!p)return null;let x=[0];for(let j=0;j<p.length-1;j++)x.push(x[j]^p[j]);let E=[];for(let j=0;j<ds.length;j++)E.push([j,(j+1)%ds.length,0],[j,(j+1)%ds.length,ds[j]]);ok(valid(E,x),"rim lift");return x}
for(let n of [3,5,9,33,129,513]){let ds=Array(n).fill(1);ok(rim(ds)===null,"odd root");ds[0]=2;ok(rim(ds)!==null,"changed direction");R.scaling.push({n,root:"UNSAT",neighbor:"SAT"})}
let K=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)K.push([a,b,0]);for(let [name,E] of [["K5",K],["K5 minus edge",K.slice(1)],["odd doubled triangle",[[0,1,0],[0,1,1],[1,2,0],[1,2,1],[2,0,0],[2,0,1]]],["perturbed doubled triangle",[[0,1,0],[0,1,2],[1,2,0],[1,2,1],[2,0,0],[2,0,1]]]]){let n=name.startsWith("K")?5:3,init=Array(n).fill(-1);init[0]=0;let sat=brute(n,E,Array.from({length:n-1},(_,i)=>i+1),init).length>0;ok(sat===(/minus|perturbed/.test(name)),"closed labels");R.closed.push({name,sat})}
let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],clauses=lines.flatMap(L=>[L.map(v=>[v,1]),L.map(v=>[v,0])]);function solve(C,x){x=x.slice();for(;;){R.closureScans++;let change=false;for(let c of C){if(c.some(([v,b])=>x[v]===b))continue;let u=c.filter(([v])=>x[v]<0);if(!u.length)return null;if(u.length===1){x[u[0][0]]=u[0][1];R.closurePins++;change=true;break}}if(!change)break}let v=x.indexOf(-1);if(v<0)return x;for(let b of [0,1]){let q=x.slice();q[v]=b;let a=solve(C,q);if(a)return a}return null}
for(let del=-1;del<14;del++){let C=clauses.filter((_,j)=>j!==del),count=0;for(let k=0;k<128;k++)if(C.every(c=>c.some(([v,b])=>((k>>v)&1)===b)))count++;let x=solve(C,Array(7).fill(-1));ok(!!x===(count>0)&&count===(del<0?0:5),"Fano decision");if(x)for(let c of C){let ds=[1,1,...c.map(([v,b])=>x[v]===b?2:1)];ok(rim(ds)!==null,"Fano wheel");R.verifiedLifts++}R.fano.push({deleted:del,count,sat:!!x})}
return R
}
console.log(JSON.stringify(run(),null,2));
