"use strict";
function make(q) {
 if(!Number.isSafeInteger(q)||q<1||q>16)throw Error("bounded test q");
 const p={q,source:[[1],[-1]],res:[{id:"r0",p1:"s0",p2:"s1",pivot:1,out:[]}],ticks:[],seal:{empty:"r0",clock:"t"+(2**q)}};
 for(let i=1;i<=2**q;i++)p.ticks.push({id:"t"+i,from:"t"+(i-1),value:i});
 return p;
}
function checked(p) {
 if(!Number.isInteger(p.q)||p.q<1||p.q>16)throw Error("q invalid");
 if(JSON.stringify(p.source)!=="[[1],[-1]]")throw Error("source unauthenticated");
 const map=new Map([["s0",[1]],["s1",[-1]]]);
 if(!Array.isArray(p.res)||p.res.length!==1)throw Error("resolution count");
 const r=p.res[0],a=map.get(r.p1),b=map.get(r.p2);
 if(!a||!b||r.pivot!==1||!a.includes(r.pivot)||!b.includes(-r.pivot))throw Error("bad pivot/parents");
 const resolvent=[...a.filter(x=>x!==r.pivot),...b.filter(x=>x!==-r.pivot)].sort((x,y)=>x-y);
 if(r.id!=="r0"||JSON.stringify(r.out)!==JSON.stringify(resolvent)||resolvent.length!==0)throw Error("resolution not empty");
 if(!Array.isArray(p.ticks)||p.ticks.length!==2**p.q)throw Error("clock length");
 const seen=new Set();
 for(let j=0;j<p.ticks.length;j++){
  const tick=p.ticks[j],i=j+1;
  if(tick.id!=="t"+i||tick.from!=="t"+j||tick.value!==i||seen.has(tick.id))throw Error("broken clock");
  seen.add(tick.id);
 }
 if(!p.seal||p.seal.empty!=="r0"||p.seal.clock!=="t"+(2**p.q))throw Error("bad seal");
 return {q:p.q,ticks:p.ticks.length,paid_nodes:2**p.q+2,certificate_bytes:JSON.stringify(p).length};
}
function run(){
 const results=[];let checks=0;
 for(let q=1;q<=10;q++){const x=checked(make(q));results.push(x);checks+=x.ticks+5;}
 const z=make(4);
 const mutations=[
 p=>{p.source[0]=[2]},
 p=>{p.res[0].pivot=2},
 p=>{p.res[0].out=[1]},
 p=>{p.ticks.splice(4,1)},
 p=>{p.ticks[3].from="t0"},
 p=>{p.ticks[4].value=4},
 p=>{p.seal.clock="t2"},
 p=>{p.seal.empty="s0"}
 ];
 for(let i=0;i<mutations.length;i++){let p=JSON.parse(JSON.stringify(z));mutations[i](p);let rejects=false;try{checked(p)}catch(e){rejects=true;}if(!rejects)throw Error("mutation accepted "+i);checks++;}
 return {results,assertions:checks,mutation_controls_rejected:mutations.length,scope:"q=1..10 clock horizon controls; symbolic theorem uses q=N=bitlength(F), not empirically tested for large N",status:"COMPUTATIONAL"};
}
if(typeof process!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
