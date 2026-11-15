"use strict";
function run(){
 let checks=0,edges=0,zeroEdges=0,fusionEdges=0;
 function ok(cond,msg){checks++;if(!cond)throw Error(msg)}
 function bits(x){let c=0;for(;x;x&=x-1)c++;return c}
 function first(x){for(let i=0;i<20;i++)if(x&(1<<i))return i;throw Error("empty ancestry")}
 function normalized(a){let map=new Map(),i=0;return a.map(x=>{if(!map.has(x))map.set(x,i++);return map.get(x)})}
 function graph(H){let e=[];if(H===4){for(let i=0;i<H;i++)for(let j=i+1;j<H;j++)e.push([i,j])}else{let n=H/2;for(let i=0;i<n;i++)e.push([i,(i+1)%n],[i+n,(i+1)%n+n],[i,i+n])}return e}
 function state(H,odd=true){let e=graph(H),inc=Array(H).fill(0);e.forEach(([u,v],j)=>{inc[u]^=(1<<j);inc[v]^=(1<<j)});ok(e.length===3*H/2,"noncubic");return {H,inc,rows:[],seen:0,part:Array.from({length:H},(_,i)=>i),halted:false,odd}}
 function join(s,i,j){let a=s.part[i],b=s.part[j];if(a!==b)s.part=normalized(s.part.map(z=>z===b?a:z))}
 function src(s,i){let m=1<<i;s.rows.push({prov:m,anc:m,edge:s.inc[i],rhs:i===0&&s.odd?1:0});s.seen|=m}
 function add(s,j,k){let a=s.rows[j],b=s.rows[k];ok(a!==undefined&&b!==undefined,"operand missing");join(s,first(a.anc),first(b.anc));s.rows.push({prov:a.prov^b.prov,anc:a.anc|b.anc,edge:a.edge^b.edge,rhs:a.rhs^b.rhs})}
 function fuse(s,i,j){let a=s.rows[j];ok(a!==undefined,"fuse operand missing");join(s,first(a.anc),i);let m=1<<i;s.seen|=m;s.rows.push({prov:a.prov^m,anc:a.anc|m,edge:a.edge^s.inc[i],rhs:a.rhs^(i===0&&s.odd?1:0)})}
 function goal(s){return s.rows.some(r=>r.edge===0&&r.rhs===1)}
 function vec(s,mode){let m=bits(s.seen);return [s.H-m,mode==="free"?(m===0?s.H-1:s.H-m):new Set(s.part).size-1,s.halted?0:1]}
 function validate(s){for(let r of s.rows){let e=0,b=0;for(let i=0;i<s.H;i++)if(r.prov&(1<<i)){e^=s.inc[i];b^=(i===0&&s.odd?1:0)}ok(r.edge===e&&r.rhs===b,"bad GF2 provenance");let comps=new Set();for(let i=0;i<s.H;i++)if(r.anc&(1<<i))comps.add(s.part[i]);ok(comps.size===1,"disconnected shared ancestry");if(r.edge===0&&r.rhs===1)ok(r.prov===(1<<s.H)-1,"proper-subset contradiction")}}
 function checkEdge(s,mode,before,cost){let after=vec(s,mode),delta=before.map((x,i)=>x-after[i]);let weight=mode==="base"?[1,1,1]:[1,0,1];let consumed=delta.reduce((z,x,i)=>z+x*weight[i],0);ok(consumed<=cost,JSON.stringify({error:"tariff",mode,delta,cost,consumed}));edges++;if(cost===0)zeroEdges++;return delta}
 let seed=20261114;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
 let counts={};
 for(let H of [4,6,8]){
  let tally={base:0,fused:0,free:0};
  for(let mode of ["base","fused","free"]){
   for(let trial=0;trial<350;trial++){
    let s=state(H);
    for(let t=0;t<24;t++){
     let actions=[];for(let i=0;i<H;i++)actions.push(["S",i]);
     if(s.rows.length){let b=Math.min(s.rows.length,6);for(let j=0;j<b;j++)for(let k=j;k<b;k++)actions.push(["A",j,k]);if(mode==="fused")for(let i=0;i<H;i++)for(let j=0;j<b;j++)actions.push(["F",i,j])}
     if((mode==="free"&&bits(s.seen)===H)||(mode!=="free"&&goal(s)))actions.push(["H"]);
     let ac=actions[rnd(actions.length)],before=vec(s,mode),cost=1;
     if(ac[0]==="S")src(s,ac[1]);
     if(ac[0]==="A"){add(s,ac[1],ac[2]);if(mode==="free")cost=0}
     if(ac[0]==="F"){fuse(s,ac[1],ac[2]);fusionEdges++}
     if(ac[0]==="H"){ok(mode==="free"?bits(s.seen)===H:goal(s),"unsound halt");s.halted=true}
     validate(s);checkEdge(s,mode,before,cost);tally[mode]++;if(s.halted)break;
    }
   }
   let s=state(H),price=0;src(s,0);price++;
   for(let i=1;i<H;i++){if(mode==="fused"){fuse(s,i,s.rows.length-1);price++}else {src(s,i);price++;if(mode==="base"){add(s,s.rows.length-2,s.rows.length-1);price++}}}
   if(mode==="free")ok(bits(s.seen)===H,"full source closure missing");else ok(goal(s),"final XOR absent");
   s.halted=true;price++;validate(s);
   ok(price===(mode==="base"?2*H:H+1),"bad constructive upper bound");
   ok(vec(s,mode).every(v=>v===0),"goal obstruction nonzero");
   tally[mode+"Min"]=price;
  }
  counts[H]=tally;
  let even=state(H,false);for(let i=0;i<H;i++)src(even,i);for(let i=1;i<H;i++)add(even,even.rows.length-2,even.rows.length-1);ok(!goal(even),"even-charge SAT falsely refuted");
 }
 let s=state(4);src(s,0);let b=vec(s,"fused");fuse(s,1,0);let d=b.map((x,i)=>x-vec(s,"fused")[i]);ok(d.join(",")==="1,1,0","fused obstruction witness missing");ok(d[0]+d[1]===2,"fusion overcharge mismatch");
 s=state(4);src(s,0);src(s,1);b=vec(s,"base");add(s,0,1);d=b.map((x,i)=>x-vec(s,"base")[i]);ok(d.join(",")==="0,1,0","raw zero-cost counterexample missing");ok(vec(s,"free")[1]===2,"directed zero closure false");
 let parityControls=[];
 for(let rhs=0;rhs<2;rhs++){let expected=Array.from({length:8},(_,i)=>i).filter(i=>(bits(i)&1)!==rhs),opposite=Array.from({length:8},(_,i)=>i).filter(i=>(bits(i)&1)===rhs);let seven=expected.slice(0,3).concat(opposite);ok(expected.length===4&&opposite.length===4&&seven.length===7,"bad clause count");const authentic=(a)=>a.length===4&&(a.join(",")===expected.join(",")||a.join(",")===opposite.join(","));ok(!authentic(seven),"malformed seven clauses accepted");parityControls.push({rhs,sourceRows:4,invalidSevenAccepted:false})}
 return {status:"PASS",checks,edges,zeroEdges,fusionEdges,counts,parityControls,certificates:{base:"(1,1,1)",fused:"(1,0,1)",free:"(1,0,1)"},counterexampleFused:{delta:[1,1,0],price:1,rawOvercharge:1},counterexampleZero:{rawDelta:[0,1,0],price:0,rawOvercharge:1}};
}
function rationalLP(H,mode){
 const det=(a)=>a[0][0]*(a[1][1]*a[2][2]-a[1][2]*(a[2][1]))-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
 const gcd=(a,b)=>{while(b){let z=a%b;a=b;b=z}return a<0n?-a:a};
 const frac=(a,b)=>{if(b<0n){a=-a;b=-b}let g=gcd(a,b);return {n:a/g,d:b/g}};
 const plus=(a,b)=>frac(a.n*b.d+b.n*a.d,a.d*b.d);
 const times=(a,b)=>frac(a.n*b.n,a.d*b.d);
 const le=(a,b)=>a.n*b.d<=b.n*a.d;const R=x=>frac(BigInt(x),1n);
 const raw=[{a:[-1,0,0],b:0},{a:[0,-1,0],b:0},{a:[0,0,-1],b:0},{a:[1,0,0],b:1},{a:[0,1,0],b:1},{a:[0,0,1],b:1}];
 if(mode!=="base")raw.push({a:[1,1,0],b:1});
 let rows=raw.map(x=>({a:x.a.map(BigInt),b:BigInt(x.b)})),best=null,verts=0;
 for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++)for(let k=j+1;k<rows.length;k++){
  let selected=[rows[i],rows[j],rows[k]],A=selected.map(x=>x.a),d=det(A);if(d===0n)continue;
  let x=[0,1,2].map(c=>frac(det(A.map((row,ri)=>row.map((v,ci)=>ci===c?selected[ri].b:v))),d));
  if(!rows.every(row=>le(row.a.reduce((sum,v,xi)=>plus(sum,times(R(v),x[xi])),R(0)),R(row.b))))continue;
  verts++;let obj=[H,H-1,1].reduce((sum,v,idx)=>plus(sum,times(R(v),x[idx])),R(0));
  if(!best||!le(obj,best.obj))best={x,obj};
 }
 if(!best)throw Error("LP infeasible");
 const str=z=>z.d===1n?z.n.toString():`${z.n}/${z.d}`;
 return {H,mode,verifiedVertices:verts,weights:best.x.map(str),objective:str(best.obj)};
}
const outcome=run();
const lp=[4,6,8,100].flatMap(H=>['base','fused','free'].map(mode=>rationalLP(H,mode)));
if(lp.some(q=>q.objective!==String(q.mode==='base'?2*q.H:q.H+1)))throw Error('LP optimum mismatch');
console.log(JSON.stringify({experiment:outcome,lp,language:'native V8 ECMAScript BigInt exact rational LP'},null,2));
