// node checker.js S27_results.json DA22_results.json
const fs=require('fs');
function run(s,d){
let checks=0,splitWords=0,binaryWords=0,closureScans=0,localWords=0;
const assert=(v)=>{checks++;if(!v)throw Error("assertion "+checks)};
const bit=(x,i)=>(x>>>i)&1,par=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
function span(v){let a=[0];for(const x of v)if(!a.includes(x))a=a.concat(a.map(t=>t^x));return a.sort((x,y)=>x-y)}
function hull(v){return v.length?span(v.map(x=>x^v[0])).map(x=>x^v[0]).sort((a,b)=>a-b):[]}
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let seed=20261125;function rand(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
function graphic(n,edges,target,w){
let m=edges.length,q=2*m,cols=edges.map(([a,b])=>(1<<a)^(1<<b)),rhs=target[0]===target[1]?0:cols[0]*0+(1<<target[0])+(1<<target[1]);
let opt=Infinity,sol=[],splitOpt=Infinity,ss=[];
for(let y=0;y<1<<m;y++){binaryWords++;let p=0,c=0;for(let j=0;j<m;j++)if(bit(y,j)){p^=cols[j];c+=w[j]}if(p===rhs){if(c<opt){opt=c;sol=[]}if(c===opt)sol.push(y)}}
let b=Array(n).fill(0);b[target[0]]--;b[target[1]]++;
for(let z=0;z<1<<q;z++){splitWords++;let v=Array(n).fill(0),c=0;for(let j=0;j<m;j++){let [a,t]=edges[j],p=bit(z,j),u=bit(z,j+m);v[a]-=p-u;v[t]+=p-u;c+=w[j]*(p+u)}
if(v.every((x,i)=>x===b[i])){if(c<splitOpt){splitOpt=c;ss=[]}if(c===splitOpt)ss.push(z)}}
assert(opt===splitOpt);
if(!ss.length)return {label:"UNSAT",n,m};
const free=ss.reduce((a,z)=>a|(z^ss[0]),0),project=z=>(z^(z>>>m))&((1<<m)-1),pred=[];
for(let z=free;;z=(z-1)&free){let p=0;for(let j=0;j<q;j++)if(bit(z,j))p^=cols[j%m];if(!p)pred.push(project(z^ss[0]));if(!z)break}
assert(eq([...new Set(ss.map(project))].sort((a,b)=>a-b),sol));assert(eq([...new Set(pred)].sort((a,b)=>a-b),hull(sol)));
return {label:"SAT",n,m,opt,models:sol.length,hull:hull(sol).length,free:par(0)+free.toString(2).replace(/0/g,"").length};
}
let cases=[graphic(4,[[0,1],[1,3],[0,2],[2,3]],[0,3],[1,1,1,1]),graphic(4,[[0,1],[2,3]],[0,3],[1,1])];
for(let i=0;i<80;i++){let n=3+rand(3),edges=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)if(rand(7)<4&&edges.length<7)edges.push([a,b]);if(!edges.length)edges.push([0,1]);cases.push(graphic(n,edges,[rand(n),rand(n)],edges.map(()=>rand(5))))}
const ok=(o,x)=>!o.bad.includes(o.t.reduce((a,v,i)=>a|(bit(x,v)<<i),0));
function closure(n,reg,guard){
let p=Array.from({length:n},(_,i)=>i),z=Array(n).fill(0);
function find(i){if(p[i]===i)return[i,0];let [r,b]=find(p[i]);return[r,b^z[i]]}
function join(a,b,v){let [i,s]=find(a),[j,t]=find(b);if(i===j)return(s^t)===v?0:-1;p[i]=j;z[i]=v^s^t;return 1}
for(let [a,b,v] of guard)if(join(a,b,v)<0)return "UNSAT";
for(;;){let change=false;for(const o of reg){closureScans++;let vs=[...new Set(o.t.map(v=>find(v)[0]))],pos=new Map(vs.map((v,i)=>[v,i])),support=[];
for(let x=0;x<1<<vs.length;x++){localWords++;let q=o.t.reduce((a,v,i)=>{let [j,t]=find(v);return a|((bit(x,pos.get(j))^t)<<i)},0);if(!o.bad.includes(q))support.push(x)}
if(!support.length)return "UNSAT";for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++){let t=bit(support[0],i)^bit(support[0],j);if(support.every(x=>(bit(x,i)^bit(x,j))===t)){let a=join(vs[i],vs[j],t);assert(a>=0);if(a)change=true}}
if(change)break;
}if(!change)return "OPEN"}
}
let peer=[];
for(const x of s.controls.filter(x=>x.neighbor))for(const [label,reg] of [["UNSAT",x.neighbor.root],["SAT",x.neighbor.satRegistry]]){
let cuts=d.results.find(a=>a.id===`S27-${x.n}-${label}`).runs.find(a=>a.mode===2).cuts.map(a=>a.cut);
for(const g of cuts.length?[[],cuts.slice(0,1),cuts]:[[]]){let status=closure(x.n,reg,g),count=0;
for(let v=0;v<1<<x.n;v++){binaryWords++;if(g.every(([a,b,t])=>(bit(v,a)^bit(v,b))===t)&&reg.every(o=>ok(o,v)))count++}
assert(status!=="UNSAT"||count===0);
let edges=new Map(),ob=0;for(const o of reg)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=o.t[i],b=o.t[j],key=[Math.min(a,b),Math.max(a,b)].join(",");edges.set(key,1^bit(o.bad[0],i)^bit(o.bad[0],j))}
function odd(a,b,c){let q=[[a,b],[a,c],[b,c]].map(e=>edges.get(e.join(",")));return q.every(x=>x!==undefined)&&q.reduce((a,b)=>a^b,0)===1}
for(let a=0;a<x.n;a++)for(let b=a+1;b<x.n;b++)for(let c=b+1;c<x.n;c++)for(let e=c+1;e<x.n;e++)if(odd(a,b,c)&&odd(a,b,e)&&odd(a,c,e)&&odd(b,c,e))ob++;
peer.push({n:x.n,label,guard:g,closure:status,count,rawFanoK4:ob});
}}
return {seed:20261125,checks,splitWords,binaryWords,closureScans,localWords,graphicCases:cases,peer};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));
