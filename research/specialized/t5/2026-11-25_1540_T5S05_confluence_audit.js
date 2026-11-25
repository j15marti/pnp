function confluenceAudit(){
const mod=x=>((x%5)+5)%5,add=(a,b,k=1)=>a.map((x,i)=>mod(x+k*b[i])),scale=(a,k)=>a.map(x=>mod(x*k)),key=a=>a.join(""),z=r=>Array(r).fill(0),inv=[0,1,3,2,4],nz=a=>a.some(Boolean);
function basis(vs){let B=[];for(let v of vs){let w=reduce(v,B),p=w.findIndex(Boolean);if(p>=0)B.push([p,scale(w,inv[w[p]])])}return B}
function reduce(v,B){for(let [p,u] of B)v=add(v,u,-v[p]);return v}
let probes=0,transitions=0;
function attainable(cs,r){let s=new Map([[key(z(r)),z(r)]]);for(let c of cs){let t=new Map();for(let v of s.values())for(let a of [1,4]){transitions++;let x=add(v,c,a);t.set(key(x),x)}s=t}return s}
function run(cs,r,reverse){let W=[],steps=[];while(true){let qs=cs.map(c=>reduce(c,W)).filter(nz);let cand=qs.map(c=>[c]);for(let i=0;i<qs.length;i++)for(let j=i+1;j<qs.length;j++)cand.push([qs[i],qs[j]]);if(reverse)cand.reverse();let found=false;for(let v of cand){let B=basis(v);if(B.length!==v.length)continue;let group=qs.filter(c=>!nz(reduce(c,B)));probes++;if(group.length<Math.ceil(Math.log2(5**B.length)))continue;if(attainable(group,r).size!==5**B.length)continue;W=basis(W.map(([p,u])=>u).concat(v));steps.push(B.length);found=true;break}if(!found)break}let members=[];for(let i=0;i<5**r;i++){let a=Array.from({length:r},(_,j)=>Math.floor(i/5**j)%5);if(!nz(reduce(a,W)))members.push(key(a))}return {rank:W.length,members,steps}}
let seed=5051540;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let tests=0,nonzero=0;for(let i=0;i<120;i++){let r=1+rand(3),m=1+rand(12),cs=Array.from({length:m},()=>Array.from({length:r},()=>rand(5)));let a=run(cs,r,false),b=run(cs,r,true);if(JSON.stringify(a.members)!==JSON.stringify(b.members))throw Error("nonconfluent");tests++;nonzero+=+(a.rank>0)}
let cs=[];for(let [v,k] of [[[1,0,0],2],[[0,1,0],3],[[1,1,0],3],[[0,0,1],3],[[1,0,1],3]])for(let j=0;j<k;j++)cs.push(v);
let a=run(cs,3,false),b=run(cs,3,true);if(a.rank!==3||b.rank!==3||attainable(cs,3).size!==125)throw Error("overlap");
return {seed:5051540,tests,nonzero,probes,transitions,overlappingExample:{columns:cs,attainable:125,forward:a.steps,reverse:b.steps,rank:a.rank}}}
console.log(JSON.stringify(confluenceAudit(),null,2));
