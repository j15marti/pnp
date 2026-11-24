function experiment(){
const bit=i=>1n<<BigInt(i), dot=(a,b)=>{let x=a&b,p=0;while(x){p^=1;x&=x-1n}return p};
const pivot=x=>x.toString(2).length-1;
function insert(B,x){while(x){let k=pivot(x);if(B.has(k))x^=B.get(k);else{B.set(k,x);return true}}return false}
function deps(rows){let B=new Map(),K=[];rows.forEach((x,i)=>{let y=bit(i);while(x){let k=pivot(x);if(B.has(k)){let [a,b]=B.get(k);x^=a;y^=b}else{B.set(k,[x,y]);return}}K.push(y)});return K}
function linOK(eq){let B=new Map();for(let [x,y] of eq){while(x){let k=pivot(x);if(B.has(k)){let [a,b]=B.get(k);x^=a;y^=b}else{B.set(k,[x,y]);break}}if(!x&&y)return false}return true}
function encode(rows,x){let y=0n;rows.forEach((r,j)=>{if(dot(r,x))y|=bit(j)});return y}
function closure(F){let G=F.map(f=>({u:f.u,s:[...f.s]})),removed=0;for(;;){if(G.some(f=>!f.s.length))return {G,removed,unsat:true};let eq=[];for(let f of G){for(let a=1n;a<bit(f.u.length);a++){let v=dot(a,f.s[0]);if(f.s.every(s=>dot(a,s)===v)){let r=0n;f.u.forEach((x,j)=>{if(a&bit(j))r^=x});eq.push([r,v])}}}if(!linOK(eq))return {G,removed,unsat:true};let change=0;for(let f of G){let s=f.s.filter(y=>linOK(eq.concat(f.u.map((r,j)=>[r,dot(y,bit(j))]))));change+=f.s.length-s.length;f.s=s}removed+=change;if(!change)return {G,removed,unsat:false}}}
function solve(F,features=false,dropResidual=false){
let n=F.length,off=[],A=[];F.forEach(f=>{off.push(A.length);A.push(...f.u)});let L=A.length,K=deps(A),edges=[];
for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let u=F[i].u,v=F[j].u,rr=deps(u.concat(v)),pairs=rr.map(r=>[(r&(bit(u.length)-1n)),r>>BigInt(u.length)]);edges.push({i,j,pairs,w:pairs.length})}
edges.sort((a,b)=>b.w-a.w||a.i-b.i||a.j-b.j);
let parent=Array.from({length:n},(_,i)=>i),find=i=>parent[i]===i?i:(parent[i]=find(parent[i])),adj=Array.from({length:n},()=>[]),B=new Map(),weight=0;
for(let e of edges){let {i,j,pairs,w}=e;if(find(i)===find(j))continue;parent[find(i)]=find(j);weight+=w;for(let [a,b] of pairs){if(!insert(B,(a<<BigInt(off[i]))^(b<<BigInt(off[j]))))throw Error("tree relation dependent")}adj[i].push({j,m:pairs.map(p=>p[0]),other:pairs.map(p=>p[1])});adj[j].push({j:i,m:pairs.map(p=>p[1]),other:pairs.map(p=>p[0])})}
let C=[];for(let k of K)if(insert(B,k))C.push(k);if(C.length!==K.length-weight)throw Error("defect mismatch");let delta=C.length;if(dropResidual)C=[];
const feat=y=>{if(!features)return 1n;let out=1n,k=1;for(let i=0;i<L;i++,k++)if(y&bit(i))out|=bit(k);for(let i=0;i<L;i++)for(let j=i+1;j<L;j++,k++)if((y&bit(i))&&(y&bit(j)))out|=bit(k);return out};
let joins=0,cells=0;
function add(map,k,y){if(!map.has(k))map.set(k,{b:new Map(),ys:[]});let cell=map.get(k);if(insert(cell.b,feat(y)))cell.ys.push(y)}
function visit(i,p){let children=adj[i].filter(e=>e.j!==p).map(e=>({e,m:visit(e.j,i)}));let pe=adj[i].find(e=>e.j===p);let result=new Map();for(let r of F[i].s){let y=r<<BigInt(off[i]),cur=new Map();add(cur,encode(C,y),y);for(let {e,m} of children){let boundary=encode(e.m,r),next=new Map();for(let [t,cell] of cur){for(let [key,c] of m){let [b,z]=key.split(":").map(BigInt);if(b!==boundary)continue;for(let a of cell.ys)for(let d of c.ys){joins++;add(next,t^z,a|d)}}}cur=next}
let b=pe?encode(pe.m,r):0n;for(let [t,cell] of cur)for(let a of cell.ys)add(result,b+":"+t,a)}
cells+=result.size;return result}
let root=visit(0,-1),ys=root.get("0:0")?.ys??[];return {ys,delta,weight,joins,cells,feat,A}
}
let seed=0x2010550;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let out={seed:"0x2010550",random:0,sat:0,unsat:0,referenceAssignments:0,spanComparisons:0,verifiedBasisWitnesses:0,closureRemoved:0,closureContradictions:0,joins:0,scaling:[],hostile:[]};
for(let t=0;t<200;t++){let n=3+rand(6),h=2+rand(6),F=[];for(let i=0;i<h;i++){let u=[],B=new Map(),d=1+rand(Math.min(n,3));while(u.length<d){let r=BigInt(1+rand((1<<n)-1));if(insert(B,r))u.push(r)}let s=[];for(let r=0;r<1<<d;r++)if((rand(101)<(t%2?78:45)))s.push(BigInt(r));if(!s.length)s.push(BigInt(rand(1<<d)));F.push({u,s})}
let full=solve(F,true),cl=closure(F),z=cl.unsat?[]:solve(cl.G,true).ys,ref=new Set();for(let x=0n;x<bit(n);x++){out.referenceAssignments++;if(F.every(f=>f.s.includes(encode(f.u,x))))ref.add(encode(full.A,x))}
let rb=new Map();for(let y of ref)insert(rb,full.feat(y));for(let ys of [full.ys,z]){let b=new Map();for(let y of ys){if(!ref.has(y))throw Error("invalid witness");insert(b,full.feat(y));out.verifiedBasisWitnesses++}let union=new Map(rb);for(let v of b.values())insert(union,v);if(b.size!==rb.size||union.size!==rb.size)throw Error("span mismatch");out.spanComparisons++}
out.random++;out[ref.size?"sat":"unsat"]++;out.closureRemoved+=cl.removed;out.closureContradictions+=Number(cl.unsat);out.joins+=full.joins}
let F=[{u:[1n],s:[1n]},{u:[2n],s:[1n]},{u:[3n],s:[1n]}];let a=solve(F),b=solve(F,false,true);if(a.ys.length||!b.ys.length||a.delta!==1)throw Error("hostile fail");out.hostile.push({name:"three lines",delta:a.delta,exactSAT:!!a.ys.length,treeOnlySAT:!!b.ys.length,closureUnsat:closure(F).unsat});
for(let n of [8,16,32,64,128]){let dense=Array.from({length:n},(_,i)=>(bit(n)-1n)^bit(i));for(let cycle of [false,true])for(let sat of [true,false]){let F=[];for(let i=0;i<(cycle?n:n-1);i++)F.push({u:[dense[i],dense[(i+1)%n]],s:!sat&&cycle&&i===0?[0n,3n]:[1n,2n]});if(!cycle){F.push({u:[dense[0]],s:[0n]});F.push({u:[dense[n-1]],s:[sat?1n:0n]})}
let cl=closure(F),v=solve(F);if(Boolean(v.ys.length)!==sat||cl.unsat===sat)throw Error("scaling label");if(v.ys.length&&deps(v.A).some(k=>dot(k,v.ys[0])))throw Error("lift inconsistency");out.scaling.push({n,cycle,sat,delta:v.delta,joins:v.joins,cells:v.cells,closureUnsat:cl.unsat})}}
return out
}
console.log(JSON.stringify(experiment(),null,2));
