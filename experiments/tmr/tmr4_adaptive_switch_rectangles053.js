"use strict";
// TMR-4/053 self-contained native V8; no random seed, no packages.
const result = (function audit053(){
const revision="tmr4-adaptive-switch-rectangles053.v1",fields=[2,65521];let checks=0;
const A=(test,msg)=>{checks++;if(!test)throw Error(msg)};
function rank(rows,p){let a=rows.map(r=>r.slice()),r=0;const pow=(x,e)=>{let z=1;for(;e;e=Math.floor(e/2),x=x*x%p)if(e%2)z=z*x%p;return z};
for(let c=0;c<a[0].length&&r<a.length;c++){let j=r;while(j<a.length&&!a[j][c])j++;if(j===a.length)continue;[a[j],a[r]]=[a[r],a[j]];let inv=pow(a[r][c],p-2);a[r]=a[r].map(v=>v*inv%p);
for(let i=0;i<a.length;i++)if(i!==r&&a[i][c]){let f=a[i][c];a[i]=a[i].map((v,k)=>(v-f*a[r][k]%p+p)%p)}r++}return r}
class BP{
constructor(){this.nodes=new Map();this.memo=new Map();this.root=0}
node(v,lo,hi){if(lo===hi)return lo;let key=JSON.stringify([v,lo,hi]);if(!this.memo.has(key)){let i=this.nodes.size+2;this.memo.set(key,i);this.nodes.set(i,{v,lo,hi})}return this.memo.get(key)}
build(order,f,fixed={}){let a={...fixed};const rec=i=>{if(i===order.length)return +!!f(a);let v=order[i];a[v]=0;let lo=rec(i+1);a[v]=1;let hi=rec(i+1);delete a[v];return this.node(v,lo,hi)};return rec(0)}
validate(side){let b=0,paths=0,maxTests=0;
const rec=(id,anc,used,prev,sw,d)=>{if(id<2){b=Math.max(b,sw);paths++;maxTests=Math.max(maxTests,d);return}A(this.nodes.has(id)&&!anc.has(id),"malformed cycle");let nd=this.nodes.get(id);A(Object.hasOwn(side,nd.v)&&!used.has(nd.v),"repeated/missing variable");let next=sw+ +(prev!==null&&prev!==side[nd.v]);let na=new Set(anc),nu=new Set(used);na.add(id);nu.add(nd.v);rec(nd.lo,na,nu,side[nd.v],next,d+1);rec(nd.hi,na,nu,side[nd.v],next,d+1)};
rec(this.root,new Set(),new Set(),null,0,0);return {b,paths,maxTests}}
trace(a,side){let id=this.root,prev=null,trans=[],steps=0;while(id>=2){let nd=this.nodes.get(id),s=side[nd.v];if(prev!==null&&prev!==s)trans.push(id);id=a[nd.v]?nd.hi:nd.lo;prev=s;steps++;A(steps<=this.nodes.size,"nontermination")}return {value:id,trans,steps}}
}
const bitstrings=n=>Array.from({length:2**n},(_,t)=>Array.from({length:n},(_,i)=>(t>>i)&1));
function one(name,X,Y,builder,known={}){
let side={};for(let x of X)side[x]="X";for(let y of Y){A(!Object.hasOwn(side,y),"duplicate variable");side[y]="Y"}
let B=new BP();B.root=builder(B);let info=B.validate(side),xs=bitstrings(X.length),ys=bitstrings(Y.length),M=[],groups=new Map(),paid=0,accept=0;
for(let i=0;i<xs.length;i++){let row=[];for(let j=0;j<ys.length;j++){let a={};X.forEach((v,t)=>a[v]=xs[i][t]);Y.forEach((v,t)=>a[v]=ys[j][t]);let tr=B.trace(a,side);row.push(tr.value);paid+=tr.steps;A(tr.trans.length<=info.b,"too many crossings");if(tr.value){accept++;let key=tr.trans.join(",");if(!groups.has(key))groups.set(key,[]);groups.get(key).push([i,j])}}M.push(row)}
let total=0;for(let pairs of groups.values()){let xx=new Set(pairs.map(p=>p[0])),yy=new Set(pairs.map(p=>p[1])),points=new Set(pairs.map(p=>p.join(":")));A(pairs.length===xx.size*yy.size,"nonrectangle");for(let i of xx)for(let j of yy)A(points.has(i+":"+j),"missing rectangle point");total+=pairs.length}A(total===accept,"wrong multiplicity");
let ranks={};for(let p of fields){ranks[p]=rank(M,p);A(ranks[p]<=groups.size,"rank exceeds transcript count");if(Object.hasOwn(known,p))A(ranks[p]===known[p],"known rank mismatch")}
let V=B.nodes.size,coarse=V===0?1n:Array.from({length:info.b+1},(_,i)=>BigInt(V)**BigInt(i)).reduce((a,b)=>a+b,0n);A(BigInt(groups.size)<=coarse,"coarse bound");
return {name,N:X.length+Y.length,X:X.length,Y:Y.length,V,edges:2*V,b:info.b,max_tests:info.maxTests,paths:info.paths,accepted_pairs:accept,accepting_transcripts:groups.size,ranks,coarse_bound:String(coarse),evaluations:xs.length*ys.length,paid_tests:paid}
}
const disj=(a,k)=>Array.from({length:k},(_,i)=>!(a["x"+i]&&a["y"+i])).every(Boolean);
const eq=(a,k)=>Array.from({length:k},(_,i)=>a["x"+i]===a["y"+i]).every(Boolean);
const ip=(a,k)=>Array.from({length:k},(_,i)=>a["x"+i]*a["y"+i]).reduce((s,v)=>s+v,0)%2;
let rows=[];
for(let type of ["DISJ","EQ","IP"])for(let k of [2,3,4]){
let X=Array.from({length:k},(_,i)=>"x"+i),Y=Array.from({length:k},(_,i)=>"y"+i),f=a=>type==="DISJ"?disj(a,k):type==="EQ"?eq(a,k):ip(a,k);
for(let mode of ["grouped","interleaved"]){let order=mode==="grouped"?X.concat(Y):X.flatMap((v,i)=>[v,Y[i]]),known=type==="IP"?{2:k,65521:2**k-1}:{2:2**k,65521:2**k};
rows.push(one(type+k+"_"+mode,X,Y,B=>B.build(order,f),known))}}
for(let type of ["DISJ","IP"]){let k=5,X=Array.from({length:k},(_,i)=>"x"+i),Y=Array.from({length:k},(_,i)=>"y"+i),f=a=>type==="DISJ"?disj(a,k):ip(a,k);
rows.push(one(type+"5_interleaved",X,Y,B=>B.build(X.flatMap((v,i)=>[v,Y[i]]),f),type==="DISJ"?{2:32,65521:32}:{2:5,65521:31}))}
rows.push(one("SELECTOR_ADAPTIVE",["s","x0","x1"],["y0","y1"],B=>{let f=a=>a.s?eq(a,2):disj(a,2);let lo=B.build(["x0","y0","x1","y1"],f,{s:0}),hi=B.build(["x0","x1","y0","y1"],f,{s:1});return B.node("s",lo,hi)}));
rows.push(one("HORN_C6",["v0","v2","v4"],["v1","v3","v5"],B=>B.build(["v0","v1","v2","v3","v4","v5"],a=>{for(let i=0;i<6;i++)if(a["v"+i]&&a["v"+((i+1)%6)])return false;return true})));
rows.push(one("SINGLETON",["x0","x1","x2"],["y0","y1","y2"],B=>B.build(["x0","x1","x2","y0","y1","y2"],a=>["x0","x1","x2","y0","y1","y2"].every(v=>!a[v])),{2:1,65521:1}));
rows.push(one("UNUSED_PAD",["x0","x1","pad"],["y0","y1"],B=>B.build(["x0","x1","pad","y0","y1"],a=>disj(a,2)),{2:4,65521:4}));
rows.push(one("INDEPENDENT_PARITY_PRODUCT",["x0","x1"],["y0","y1"],B=>B.build(["x0","x1","y0","y1"],a=>(a.x0!==a.x1)&&(a.y0!==a.y1)),{2:1,65521:1}));
let malformed=new BP();malformed.root=malformed.node("x0",0,1);malformed.nodes.set(malformed.root,{v:"x0",lo:malformed.root,hi:1});let rejected=false;try{malformed.validate({x0:"X"})}catch(e){rejected=/cycle/.test(String(e))}A(rejected,"malformed cycle accepted");
for(let k of [2,3,4]){let g=rows.find(r=>r.name==="DISJ"+k+"_grouped"),i=rows.find(r=>r.name==="DISJ"+k+"_interleaved");A(g.ranks[2]===2**k&&i.V<=2*k,"DISJ sanity")}
return {revision,seed:null,fields,model:"shared deterministic read-once adaptive branching program",cases:rows.length,assertions:checks,failures:0,malformed:"cycle rejected",rows}
})();
process.stdout.write(JSON.stringify(result,null,2)+"\n");
