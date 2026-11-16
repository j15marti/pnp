// TMR4 FRONTIER056 v2: self-contained executable audit; Node >=18 or hosted V8.
"use strict";
const SEED=20261115; let rng=SEED>>>0;
const R=n=>(rng=(Math.imul(rng,1664525)+1013904223)>>>0,rng%n);
const report={revision:"tmr4-frontier056.v2",seed:SEED,cases:0,assignments:0,gateSteps:0,bpEdges:0,rankChecks:0,countChecks:0,rejected:0,assertions:0,failures:0,examples:[]};
function ok(b,msg){report.assertions++;if(!b)throw Error(msg)}
function prep(c){
 if(!Number.isInteger(c.n)||c.n<1||!Array.isArray(c.order)||!Array.isArray(c.gates)||c.order.length!==c.n+c.gates.length||c.order[0]!=="x0")throw Error("syntax");
 const gates=new Map(),seen=new Set(["0","1"]);for(const g of c.gates){if(!/^g[0-9]+$/.test(g.id)||gates.has(g.id)||g.op<0||g.op>15||!Number.isInteger(g.op)||g.a===undefined||g.b===undefined)throw Error("gate");gates.set(g.id,g)}
 const inps=new Set(),last=new Map();
 for(const [i,id] of c.order.entries()){if(seen.has(id))throw Error("duplicate");if(/^x[0-9]+$/.test(id)){let j=+id.slice(1);if(j>=c.n)throw Error("input");inps.add(j)}else{let g=gates.get(id);if(!g||!seen.has(g.a)||!seen.has(g.b))throw Error("dependency");}
 seen.add(id);last.set(id,-1);}
 if(inps.size!==c.n||c.gates.length!==c.order.filter(id=>gates.has(id)).length||!seen.has(c.output))throw Error("coverage");
 for(const [i,id] of c.order.entries()){let g=gates.get(id);if(g)for(const a of [g.a,g.b])if(last.has(a))last.set(a,Math.max(i,last.get(a)))}
 if(last.has(c.output))last.set(c.output,c.order.length);
 const live=c.order.map((_,i)=>c.order.slice(0,i+1).filter(j=>last.get(j)>i));
 const stages=[];let previous=[],start=0;
 for(let i=0;i<c.order.length;i++)if(i===c.order.length-1||/^x[0-9]+$/.test(c.order[i+1])){
 const toks=c.order.slice(start,i+1),s={input:toks[0],before:previous,after:live[i],gates:toks.filter(j=>gates.has(j)).map(j=>gates.get(j))};
 const available=new Set(["0","1",...previous,s.input]);for(const g of s.gates){if(!available.has(g.a)||!available.has(g.b))throw Error("unretained input");available.add(g.id)}
 for(const v of s.after)if(!available.has(v))throw Error("unretained output");
 stages.push(s);previous=live[i];start=i+1;}
 const w=Math.max(...live.map(v=>v.length));
 ok(stages.length===c.n,"stage count");
 return {stages,w,live,gateMap:gates,stageBits:8*JSON.stringify(stages).length};
}
function op(g,a,b){return(g.op>>(2*a+b))&1}
function original(c,p,x){const v={"0":0,"1":1};
 for(const id of c.order){const g=p.gateMap.get(id);v[id]=g?op(g,v[g.a],v[g.b]):x[+id.slice(1)]}
 return {v,y:v[c.output]};}
function step(s,vals,bit){let v={"0":0,"1":1};s.before.forEach((j,i)=>v[j]=vals[i]);v[s.input]=bit;
 for(const g of s.gates){v[g.id]=op(g,v[g.a],v[g.b]);report.gateSteps++}
 return {v,vals:s.after.map(j=>v[j])};}
function compile(c,p){
 let states=new Map([["",{v:[],count:1n}]]),layers=[],nodes=0;
 for(const s of p.stages){let next=new Map(),edges=[];
 for(const [key,state]of states){nodes++;for(let z=0;z<2;z++){const v=step(s,state.v,z).vals,key2=v.join("");
 if(!next.has(key2))next.set(key2,{v,count:0n});next.get(key2).count+=state.count;
 edges.push([key,z,key2]);report.bpEdges++;}}
 layers.push({edges,states:next});states=next;}
 ok(nodes<=c.n*2**p.w,"nodes");
 let count=0n;for(const state of states.values()){const s=p.stages.at(-1),i=s.after.indexOf(c.output);let y=c.output==="0"?0:c.output==="1"?1:state.v[i];if(y)count+=state.count;}
 return {layers,nodes,count};
}
function bpEval(c,p,bp,x){let key="";for(let t=0;t<p.stages.length;t++){const z=x[+p.stages[t].input.slice(1)],e=bp.layers[t].edges.find(v=>v[0]===key&&v[1]===z);ok(!!e,"edge");key=e[2]}
 const final=bp.layers.at(-1).states.get(key),i=p.stages.at(-1).after.indexOf(c.output);return c.output==="0"?0:c.output==="1"?1:final.v[i];}
function rank(a,q){a=a.map(r=>r.slice());let i=0;for(let j=0;j<a[0].length&&i<a.length;j++){let k=i;while(k<a.length&&a[k][j]%q===0)k++;if(k===a.length)continue;[a[i],a[k]]=[a[k],a[i]];
 let inv=1;while(inv*a[i][j]%q!==1)inv++;
 for(let h=j;h<a[i].length;h++)a[i][h]=a[i][h]*inv%q;
 for(let t=i+1;t<a.length;t++){let f=a[t][j];for(let h=j;h<a[t].length;h++)a[t][h]=(a[t][h]-f*a[i][h]%q+q)%q;}i++;}return i;}
function inspect(c,name){
 const p=prep(c),bp=compile(c,p),ord=p.stages.map(s=>+s.input.slice(1));let count=0n;
 for(let mask=0;mask<2**c.n;mask++){let x=Array.from({length:c.n},(_,j)=>(mask>>j)&1),o=original(c,p,x),values=[],memory={};
 for(const s of p.stages){let result=step(s,values,x[+s.input.slice(1)]);for(const [id,val]of Object.entries(result.v))if(o.v[id]!==undefined)ok(o.v[id]===val,"step simulation");values=result.vals;for(const id of s.after)ok(o.v[id]===result.v[id],"retained value")}
 const output=c.output==="0"?0:c.output==="1"?1:values[p.stages.at(-1).after.indexOf(c.output)];
 ok(o.y===output&&output===bpEval(c,p,bp,x),"accept/reject");count+=BigInt(o.y);report.assignments++;}
 ok(count===bp.count,"path multiplicity");report.countChecks++;
 for(let t=0;t<=c.n;t++){const a=ord.slice(0,t),b=ord.slice(t),M=[];
 for(let u=0;u<2**t;u++){let row=[];for(let v=0;v<2**(c.n-t);v++){let x=Array(c.n).fill(0);a.forEach((j,i)=>x[j]=(u>>i)&1);b.forEach((j,i)=>x[j]=(v>>i)&1);row.push(original(c,p,x).y)}M.push(row)}
 const width=t?p.stages[t-1].after.length:0;for(const field of [2,101]){ok(rank(M,field)<=2**width,"rank vs live frontier");report.rankChecks++;}}
 report.cases++;
 if(report.examples.length<10)report.examples.push({name,n:c.n,g:c.gates.length,width:p.w,bpNodes:bp.nodes,count:count.toString(),stageBits:p.stageBits});
}
function disj(k,grouped,eq){
 const gates=[],order=[],pair=[];for(let i=0;i<k;i++){pair.push("g"+gates.length);gates.push({id:pair.at(-1),a:"x"+i,b:"x"+(k+i),op:eq?9:7})}
 let last=pair[0];for(let i=1;i<k;i++){const id="g"+gates.length;gates.push({id,a:last,b:pair[i],op:8});last=id}
 if(grouped){for(let i=0;i<k;i++)order.push("x"+i);for(let i=0;i<k;i++){order.push("x"+(k+i),pair[i]);if(i)order.push("g"+(k+i-1))}}
 else{order.push("x0","x"+k,pair[0]);for(let i=1;i<k;i++)order.push("x"+i,"x"+(k+i),pair[i],"g"+(k+i-1))}
 return {n:2*k,order,gates,output:last};
}
for(let k=1;k<=4;k++)for(const grouped of [false,true])for(const eq of [false,true])inspect(disj(k,grouped,eq),(eq?"EQ":"DISJ")+(grouped?"_grouped":"_interleaved")+k);
for(let k=1;k<=6;k++){const gates=[],order=["x0"];let last="x0";for(let i=1;i<k;i++){order.push("x"+i);const id="g"+gates.length;gates.push({id,a:last,b:"x"+i,op:6});order.push(id);last=id;}inspect({n:k,gates,order,output:last},"PARITY"+k)}
for(let test=0;test<90;test++){const n=1+R(5),gates=[],order=["x0"],ready=["x0"];for(let i=0;i<n;i++){if(i){order.push("x"+i);ready.push("x"+i)}
 for(let j=0,k=R(3);j<k;j++){const id="g"+gates.length;gates.push({id,a:ready[R(ready.length)],b:ready[R(ready.length)],op:R(16)});order.push(id);ready.push(id)}}
 inspect({n,gates,order,output:ready[R(ready.length)]},"seeded"+test)}
for(const bad of [{n:1,gates:[],order:["x0","x0"],output:"x0"},{n:1,gates:[{id:"g0",a:"g0",b:"x0",op:8}],order:["x0","g0"],output:"g0"},{n:1,gates:[],order:["x0"],output:"g9"},{n:1,gates:[{id:"g0",a:"x0",b:"x0",op:16}],order:["x0","g0"],output:"g0"}]){let fails=false;try{prep(bad)}catch(e){fails=true}ok(fails,"malformed");report.rejected++}
if(typeof module!=="undefined"&&module.exports)module.exports=report;
else if(typeof print==="function")print(JSON.stringify(report));
return report;
