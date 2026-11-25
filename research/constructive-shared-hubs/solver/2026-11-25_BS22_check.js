const inputs = [{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];
const run = function run(inputs){
 const bit=i=>1n<<BigInt(i), parity=x=>{let s=0;while(x){s^=1;x&=x-1n}return s}, hi=x=>x.toString(2).length-1;
 let stats={checks:0,gaussianRows:0,closureScans:0,guardTrials:0,leafWords:0,ownerChecks:0,acceptedSplits:0,maxRank:0};
 function ck(v){stats.checks++;if(!v)throw Error("check "+stats.checks)}
 function reduce(v,b,B){while(v){let j=hi(v);if(!B.has(j))break;let p=B.get(j);v^=p[0];b^=p[1]}return [v,b]}
 function red(v,b,B){for(let j of [...B.keys()].sort((a,b)=>b-a))if(v&bit(j)){let p=B.get(j);v^=p[0];b^=p[1]}return [v,b]}
 function add(v,b,B){stats.gaussianRows++;let [a,c]=reduce(v,b,B);if(!a)return c?-1:0;B.set(hi(a),[a,c]);return 1}
 function lift(B){let x=0n;for(let j of [...B.keys()].sort((a,b)=>a-b)){let [a,b]=B.get(j);if(parity(a&x)!==b)x^=bit(j)}return x}
 function valid(O,x){return O.every(o=>{stats.ownerChecks++;return !o.e.every(([a,b])=>parity(a&x)===b)})}
 function close(O,G){let B=new Map();for(let [a,b] of G)if(add(a,b,B)<0)return {no:true};while(true){stats.closureScans++;let R=[],change=false;
 for(let o of O){let C=new Map(),impossible=false;for(let [a,b] of o.e){let [u,v]=red(a,b,B);if(add(u,v,C)<0){impossible=true;break}}if(impossible)continue;if(!C.size)return {no:true};if(C.size===1){let [a,b]=[...C.values()][0];if(add(a,b^1,B)<0)return {no:true};change=true;break}R.push({id:o.id,e:[...C.values()]})}
 if(!change)return {R,B};}}
 function factor(R){
 let B=new Map(),basis=[];for(let o of R)for(let [a] of o.e){stats.gaussianRows++;let [v,c]=reduce(a,0n,B);if(v){let k=basis.length;basis.push(a);B.set(hi(v),[v,c^bit(k)])}}
 let p=basis.map((_,i)=>i);function root(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i}
 function join(a,b){p[root(a)]=root(b)}
 let A=R.map(o=>{let ids=new Set();for(let [a] of o.e){let [v,c]=reduce(a,0n,B);ck(v===0n);for(let i=0;i<basis.length;i++)if(c&bit(i))ids.add(i)}let z=[...ids];ck(z.length>0);for(let j=1;j<z.length;j++)join(z[0],z[j]);return {o,z}});
 let groups=new Map();for(let i=0;i<basis.length;i++){let j=root(i);if(!groups.has(j))groups.set(j,{rows:[],basis:[]});groups.get(j).basis.push(basis[i])}for(let {o,z} of A)groups.get(root(z[0])).rows.push(o);
 return {basis,groups:[...groups.values()],rank:basis.length};}
 function leaf(R,basis,B,cap){if(basis.length>cap)return {label:"OPEN"};for(let w=0;w<2**basis.length;w++){stats.leafWords++;let C=new Map(B);for(let j=0;j<basis.length;j++)ck(add(basis[j],(w>>j)&1,C)>=0);let x=lift(C);if(valid(R,x))return {label:"SAT",x}}return {label:"UNSAT"}}
 function solve(O,G=[],mode="combined",cap=6){
 let cl=close(O,G);if(cl.no)return {label:"UNSAT",rank:0};let {R,B}=cl;let eq=[...B.values()];if(!R.length)return {label:"SAT",x:lift(B),rank:0};
 let f=factor(R),r=f.rank;stats.maxRank=Math.max(stats.maxRank,r);
 if(mode==="direct"||r<=cap)return {...leaf(R,f.basis,B,cap),rank:r};
 function mergeParts(groups,C){let all=[];let unresolved=false;for(let g of groups){let q=solve(g.rows,[...C.values()],mode,cap);if(q.label==="UNSAT")return {label:"UNSAT"};if(q.label==="OPEN"){unresolved=true;continue}for(let a of g.basis)all.push([a,parity(a&q.x)])}if(unresolved)return {label:"OPEN"};let D=new Map(C);for(let [a,b] of all)ck(add(a,b,D)>=0);return {label:"SAT",x:lift(D)}}
 if(f.groups.length>1){ck(f.groups.reduce((s,g)=>s+g.basis.length**2,0)<=r*r-1);let ans=mergeParts(f.groups,B);if(ans.label==="SAT")ck(valid(O,ans.x)&&eq.every(([a,b])=>parity(a&ans.x)===b));return {...ans,rank:r,parts:f.groups.map(g=>g.basis.length)}}
 if(mode==="factor")return {label:"OPEN",rank:r};
 let cand=[...new Set(f.basis.concat(R.flatMap(o=>o.e.map(e=>e[0]))))];for(let a of cand){stats.guardTrials++;let sides=[];for(let b=0;b<2;b++){let q=close(R,eq.concat([[a,b]]));if(q.no){sides.push(q);continue}let z=factor(q.R);sides.push({...q,...z})}
 let credit=sides.reduce((v,s)=>v+(s.no?0:s.groups.reduce((u,g)=>u+g.basis.length**2,0)),0);
 if(credit>r*r-1)continue;stats.acceptedSplits++;
 let pending=false;for(let s of sides){if(s.no)continue;let q=mergeParts(s.groups,s.B);if(q.label==="SAT"){ck(valid(O,q.x)&&eq.every(([a,b])=>parity(a&q.x)===b));return {...q,rank:r,credit,guard:String(a)}}if(q.label==="OPEN")pending=true}return {label:pending?"OPEN":"UNSAT",rank:r,credit,guard:String(a)}}
 return {label:"OPEN",rank:r};}
 function nae(O){return O.map((o,i)=>{let [a,b,c]=o.t,f=o.bad[0];return {id:i,e:[[bit(a)^bit(b),(f^(f>>1))&1],[bit(a)^bit(c),(f^(f>>2))&1]]}})}
 function check(O,G,x){return valid(O,x)&&G.every(([a,b])=>parity(a&x)===b)}
 function exhaustive(O,G,n){for(let x=0n;x<bit(n);x++)if(check(O,G,x))return true;return false}
 function snapshot(){return {...stats}}function diff(a){return Object.fromEntries(Object.keys(a).map(k=>[k,stats[k]-a[k]]))}
 function compare(O,G,truth){let runs=[];for(let mode of ["direct","factor","combined"]){let st=snapshot(),q=solve(O,G,mode);ck(q.label==="OPEN"||(q.label==="SAT")===truth);if(q.label==="SAT")ck(check(O,G,q.x));runs.push({mode,...q,x:q.x?.toString(),cost:diff(st)})}return runs}
 let cases=[];for(let z of inputs)for(let label of ["root","sat"])for(let guarded of [false,true]){if(guarded&&(label!=="root"||!z.guards.length))continue;let O=nae(z[label]),G=guarded?z.guards.map(([a,b,c])=>[bit(a)^bit(b),c]):[];let truth=exhaustive(O,G,z.n);cases.push({n:z.n,label,guarded,truth,runs:compare(O,G,truth)})}
 let seed=20261125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 function product(k,withHub,unsat){let n=2*k+(withHub?1:0),v=Array.from({length:n},(_,i)=>bit(i));for(let i=0;i<8*n;i++){let a=rnd(n),b=rnd(n);if(a!==b)v[a]^=v[b]}let O=[];function put(es){O.push({id:O.length,e:es})}for(let i=0;i<k;i++){let a=v[2*i+(withHub?1:0)],b=v[2*i+(withHub?2:1)];put([[a,0],[b,0]]);if(withHub)put([[v[0],i%2],[a,0]]);if(unsat&&i<2){for(let p=0;p<4;p++)put((withHub?[[v[0],i]]:[]).concat([[a,p&1],[b,p>>1]]))}}return {n,O}}
 for(let k of [2,4,8,16,32,64])for(let hub of [false,true])for(let unsat of [false,true]){let {n,O}=product(k,hub,unsat),truth=!unsat;if(n<=9)ck(exhaustive(O,[],n)===truth);cases.push({k,n,hub,unsat,truth,runs:compare(O,[],truth)})}
 let controls={SAT:0,UNSAT:0,OPEN:0};for(let i=0;i<160;i++){let n=3+rnd(6),O=Array.from({length:2+rnd(15)},(_,j)=>({id:j,e:Array.from({length:1+rnd(3)},()=>[BigInt(rnd(1<<n)),rnd(2)])})),G=Array.from({length:rnd(3)},()=>[BigInt(rnd(1<<n)),rnd(2)]);let t=exhaustive(O,G,n),q=solve(O,G,"combined");ck(q.label==="OPEN"||(q.label==="SAT")===t);if(q.label==="SAT")ck(check(O,G,q.x));controls[q.label]++}
 return {stats,cases,controls};
};
console.log(JSON.stringify(run(inputs),null,2));
