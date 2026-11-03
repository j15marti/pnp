#!/usr/bin/env node
// LSPV-2 353: compact independently replayable paid exact-clause specialization.
// Source grammar: signed-literal CNF; a gate has three named slots and costs one node.
// This compact self-test is NOT the full 106-certificate archive.
'use strict';
function canon(c){let s=new Set(c);if([...s].some(x=>!Number.isInteger(x)||x===0||s.has(-x)))throw Error('bad clause');return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function res(a,b,p){let x=new Set(a),y=new Set(b);if(x.has(p)&&y.has(-p)){x.delete(p);y.delete(-p)}
else if(x.has(-p)&&y.has(p)){x.delete(-p);y.delete(p)}else throw Error('bad pivot '+p);
return canon([...new Set([...x,...y])])}
function specialize(c,rho){if(c.some(x=>rho.has(Math.abs(x))&&rho.get(Math.abs(x))===Number(x>0)))return null;return c.filter(x=>!rho.has(Math.abs(x)))}
function proof(n,sources,steps){let all=sources.map(canon);
for(let [a,b,p] of steps){if(a>=all.length||b>=all.length||p<1||p>n)throw Error('bad proof');all.push(res(all[a],all[b],p))}
if(!eq(all.at(-1),[]))throw Error('no refutation');return all}
function compile(n,sources,steps,rho){
 let originals=proof(n,sources,steps),m=sources.length,src=sources.map(c=>specialize(canon(c),rho)),next=n,nodes=[],map=[],weaks=0,assigned=0,terminal=null;
 const read=ref=>{if(ref[0]==='s'){if(src[ref[1]]===null)throw Error('true source');return src[ref[1]]}
   let nd=nodes[ref[1]];if(!nd)throw Error('forward ref');
   if(ref[0]==='p'){if(nd.kind!=='RES')throw Error('not clause');return nd.out}
   if(ref[0]==='g'){if(nd.kind!=='DEF')throw Error('not gate');let q=nd.q,a=nd.a,b=nd.b;return canon([[-q,a],[-q,b],[q,-a,-b]][ref[2]])}
   throw Error('ref')};
 const gate=(a,b)=>{if(Math.abs(a)===Math.abs(b))throw Error('bad gate inputs');let q=++next,j=nodes.length;nodes.push({kind:'DEF',q,a,b});return [q,j]};
 const infer=(a,b,p)=>{let out=res(read(a),read(b),p),j=nodes.length;nodes.push({kind:'RES',a,b,p,out});return ['p',j]};
 const weaken=(ref,goal)=>{let C=read(ref),extras=goal.filter(l=>!C.includes(l)),k=C.length,r=extras.length;if(!k||!r)throw Error('degenerate weakening');
   let w,gates={};if(r===1)w=-extras[0];else{let t=gate(-extras[0],-extras[1]);w=t[0];gates[2]=t[1];for(let z=2;z<r;z++){t=gate(w,-extras[z]);w=t[0];gates[z+1]=t[1]}}
   let qs=C.map(l=>gate(-l,w)),before=nodes.length,cur=ref;
   for(let i=0;i<k;i++)cur=infer(cur,['g',qs[i][1],0],Math.abs(C[i]));
   for(let [q,j] of qs)cur=infer(cur,['g',j,2],q);
   for(let z=r;z>1;z--)cur=infer(cur,['g',gates[z],2],nodes[gates[z]].q);
   if(!eq(read(cur),goal))throw Error('weakening value mismatch');weaks++;return cur;};
 for(let j=0;j<m;j++){map.push(src[j]===null?null:['s',j]);if(eq(src[j],[]))terminal=['s',j]}
 if(terminal!==null)return {nodes,terminal,weaks,assigned,sourceImmediate:true};
 for(let i=0;i<steps.length;i++){let [a,b,p]=steps[i],goal=specialize(originals[m+i],rho);
   if(goal===null){map.push(null);continue}
   let ref;
   if(!rho.has(p)){if(!map[a]||!map[b])throw Error('lost active parent');ref=infer(map[a],map[b],p);if(!eq(read(ref),goal))throw Error('restricted RES not exact')}
   else {assigned++;let live=[map[a],map[b]].filter(x=>x!==null);
     if(live.length!==1)throw Error('assigned pivot survival');ref=live[0];
     let C=read(ref);if(!C.every(x=>goal.includes(x)))throw Error('weakening wrong direction');
     if(C.length&&C.length<goal.length)ref=weaken(ref,goal);
   }
   map.push(ref);if(eq(goal,[])){terminal=ref;break}
 }
 if(terminal===null||!eq(read(terminal),[]))throw Error('failed target');
 if(nodes.length>steps.length*Math.max(1,3*n-2))throw Error('cost bound');
 return {nodes,terminal,weaks,assigned,sourceImmediate:false};
}
const cases=[
 {n:3,c:[[1,2],[-1,3],[-2],[-3]],p:[[0,1,1],[4,2,2],[5,3,3]]},
 {n:5,c:[[1,3],[-1,2,4],[-2,5],[-3],[-4],[-5]],p:[[0,1,1],[6,2,2],[7,3,3],[8,4,4],[9,5,5]]},
 {n:4,c:[[1,2],[3,4],[-1,-3],[-2,-4],[1,-2,-3,4],[-1,2,3,-4]],p:[[0,4,2],[2,5,3],[0,7,1],[2,6,1],[3,8,2],[1,9,3],[10,11,4]]}
];
let totals={checks:0,translations:0,paidNodes:0,weakenings:0,assignedPivots:0,immediate:0};
for(let item of cases){proof(item.n,item.c,item.p);let rhoSets=[new Map()];
 for(let i=1;i<=item.n;i++)for(let x of [0,1])rhoSets.push(new Map([[i,x]]));
 if(item.n===4){rhoSets=[];for(let t=0;t<81;t++){let r=new Map(),v=t;for(let i=1;i<=4;i++){let s=v%3;v=Math.floor(v/3);if(s!==2)r.set(i,s)}rhoSets.push(r)}}
 for(let rho of rhoSets){let v=compile(item.n,item.c,item.p,rho);totals.translations++;totals.paidNodes+=v.nodes.length;totals.weakenings+=v.weaks;totals.assignedPivots+=v.assigned;totals.immediate+=Number(v.sourceImmediate);totals.checks++}
}
console.log(JSON.stringify({tag:'LSPV2_LINE_EXACT_RESTRICTION353',status:'PASS',scope:'three fixed original UNSAT proofs, all 81 Peitl-4 partial assignments',totals},null,2));
