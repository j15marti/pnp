
function run(m,f){
let stats={assertions:0,ownerChecks:0,closureScans:0,edges:0,nativeChecks:0,cycles:0,cycleArcs:0};
function ck(c){stats.assertions++;if(!c)throw Error("assertion "+stats.assertions)}
const B=i=>1n<<BigInt(i),bit=(w,i)=>Number((w>>BigInt(i))&1n),pop=w=>{let k=0;while(w){w&=w-1n;k++}return k};
function ok(O,w,pin=-1){if(pin>=0&&bit(w,0)!==pin)return false;for(const o of O){stats.ownerChecks++;const a=o.t.reduce((s,i,j)=>s+(bit(w,i)<<j),0);if(o.bad.includes(a))return false}return true}
function closure(O,n,pin){let a=Array(n).fill(-1);if(pin>=0)a[0]=pin;let change=true;while(change){change=false;for(const o of O){stats.closureScans++;let v=[];for(let k=0;k<8;k++)if(!o.bad.includes(k)&&o.t.every((i,j)=>a[i]<0||a[i]===((k>>j)&1)))v.push(k);if(!v.length)return false;for(let j=0;j<3;j++)if(a[o.t[j]]<0&&v.every(k=>((k>>j)&1)===((v[0]>>j)&1))){a[o.t[j]]=(v[0]>>j)&1;change=true}}}return a}
function native(O,n){let nodes=[],edges=[],occ=Array.from({length:n+O.length},()=>[]);
function node(kind,v){nodes.push({kind,v,ports:[]});return nodes.length-1}
function link(a,b,v){edges.push([a,b,v]);nodes[a].ports.push(v);nodes[b].ports.push(v)}
for(let j=0;j<O.length;j++)for(let copy=0;copy<2;copy++){let a=node("B",j);for(const v of [...O[j].t,n+j])occ[v].push(a)}
for(let v=0;v<occ.length;v++){let A=occ[v],t=A.length/2;if(!t)continue;if(t===1){link(A[0],A[1],v);continue}let path=Array.from({length:t-1},()=>node("E",v));for(let i=1;i<path.length;i++)link(path[i-1],path[i],v);let q=0;for(const u of path)while(nodes[u].ports.length<4)link(u,A[q++],v);ck(q===A.length)}
let old=edges;edges=[];for(const x of nodes)x.ports=[];
for(const [a,b,v] of old){let g=Array.from({length:5},()=>node("E",v));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)link(g[i],g[j],v);link(a,g[0],v);link(b,g[1],v)}
ck(nodes.every(x=>x.ports.length===4));ck(edges.every(([a,b])=>a!==b));ck(new Set(edges.map(([a,b])=>Math.min(a,b)+","+Math.max(a,b))).size===edges.length);
return {nodes,edges,check(w){let a=Array.from({length:n},(_,i)=>bit(w,i));for(const o of O){let s=o.t.reduce((q,i)=>q+a[i],0);ck(s===1||s===2);a.push(2-s)}for(const x of nodes){stats.nativeChecks++;let p=x.ports.map(v=>a[v]);ck(x.kind==="B"?p.reduce((s,t)=>s+t,0)===2:p.every(t=>t===p[0]))}for(const [u,v,i] of edges){stats.nativeChecks++;ck(nodes[u].ports.includes(i)&&nodes[v].ports.includes(i))}}}}
function flow(O,n,pair,u,v){let ids=Array.from({length:n},()=>[]);O.forEach((o,i)=>o.t.forEach(j=>ids[j].push(i)));let arcs=[],S=O.length,T=S+1;
function add(a,b,d){for(let i=0;i<Math.abs(d);i++)arcs.push(d>0?[a,b]:[b,a])}
for(let j=0;j<n;j++){ck(ids[j].length===2);let [a,b]=ids[j];if(O[a].p!==pair[0])[a,b]=[b,a];ck(O[a].p===pair[0]);add(a,b,bit(v,j)-bit(u,j))}
for(let i=0;i<O.length;i++){let o=O[i],a=o.t.reduce((q,j)=>q+bit(u,j),0),b=o.t.reduce((q,j)=>q+bit(v,j),0);ck(a>=1&&a<=2&&b>=1&&b<=2);if(o.p===pair[0])add(S,i,b-a);else add(i,T,b-a)}
add(T,S,pop(v)-pop(u));let bal=Array(T+1).fill(0);for(let [a,b] of arcs){bal[a]--;bal[b]++}ck(bal.every(x=>x===0));
let count=0;while(arcs.length){let start=arcs[0][0],at=start;do{let i=arcs.findIndex(e=>e[0]===at);ck(i>=0);at=arcs.splice(i,1)[0][1];stats.cycleArcs++}while(at!==start);count++;stats.cycles++}return count}
function verifyPath(O,n,k,pin,path){let A=O.filter(o=>o.p===0||o.p===k),C=O.filter(o=>o.p!==0&&o.p!==k),pairB=[1,2,3].filter(p=>p!==k),NA=native(A,n),NB=native(C,n);let nc=0;
for(let i=0;i<path.length;i++){let x=BigInt(path[i].x),y=BigInt(path[i].y);ck(ok(A,x,pin)&&ok(C,y,pin));NA.check(x);NB.check(y);ck(pop(x^y)<=1);if(i){let u=BigInt(path[i-1].x),v=BigInt(path[i-1].y);nc+=flow(A,n,[0,k],u,x)+flow(C,n,pairB,v,y)}}let last=path.at(-1);ck(last.x===last.y&&ok(O,BigInt(last.x),pin));native(O,n).check(BigInt(last.x));return nc}
const replay=m.jobs.map(j=>{ck(closure(m.owners,m.n,j.pin)!==false);return {k:j.k,pin:j.pin,cycles:verifyPath(m.owners,m.n,j.k,j.pin,j.both.path)}})
let O=f.O,n=f.n,x=BigInt(f.x),y=BigInt(f.y),z=BigInt(f.z),A=O.filter(o=>o.p<2),C=O.filter(o=>o.p>=2);
ck(pop(x^y)===1&&ok(A,x)&&ok(C,y)&&ok(O,z));ck(closure(O,n,-1).every(x=>x===-1));ck(closure(O,n,1).filter(x=>x>=0).length===1);
let pairs=new Set(),minor=Array(n).fill(0);for(let p=0;p<4;p++){let os=O.filter(o=>o.p===p);ck(os.flatMap(o=>o.t).sort((a,b)=>a-b).every((v,i)=>v===i));for(const o of os){let w=p<2?x:y;let d=o.t.find(i=>o.t.filter(j=>bit(w,j)===bit(w,i)).length===1);minor[d]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=o.t.slice().sort((a,b)=>a-b),s=Math.min(o.t[i],o.t[j])+","+Math.max(o.t[i],o.t[j]);ck(!pairs.has(s));pairs.add(s)}}}ck(minor.every(c=>c>=1)&&minor[0]===4);
native(A,n).check(x);native(C,n).check(y);native(O,n).check(z);
function next(u,v,maxK=1,pin=-1){let out=[],d=pop(u^v);for(let side=0;side<2;side++){let other=side===0?v:u,old=side===0?u:v;for(let j=-1;j<n;j++){let w=other^(j<0?0n:B(j));if(w!==old){stats.edges++;if(ok(side===0?A:C,w,pin))out.push(side===0?[w,v]:[u,w])}}}function visit(start,left,mask){if(!left){stats.edges++;let a=u^mask,b=v^mask;if(ok(A,a,pin)&&ok(C,b,pin))out.push([a,b]);return}for(let j=start;j<n;j++)if(!(B(j)&(u^v)))visit(j+1,left-1,mask|B(j))}for(let i=1;i<=maxK;i++)visit(0,i,0n);return out}
ck(next(x,y,1).length===0);
let pairMoves=next(x,y,2),tripleMoves=next(x,y,3);let path=null,vis=0;
let queue=[[[x,y]]],seen=new Set([x+","+y]);while(queue.length&&vis<n*n){let p=queue.shift(),[a,b]=p.at(-1);vis++;if(a===b){path=p;break}for(let v of next(a,b,2)){let k=v.join(",");if(!seen.has(k)&&seen.size<n*n){seen.add(k);queue.push([...p,v])}}}
let lift=null;if(path){let q=path.map(([a,b])=>({x:String(a),y:String(b)}));lift=verifyPath(O,n,1,-1,q);path=q}
return {replay,frozen:{minor,unilateralAndSingleCommon:0,pairMoves:pairMoves.length,tripleOrSmallerMoves:tripleMoves.length,visited:vis,discovered:seen.size,path,lift,plantedWord:String(z)},stats}
}

const fs=require("fs");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));
