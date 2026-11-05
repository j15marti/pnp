#!/usr/bin/env node
'use strict';
// LSPV-3/433 standalone replay, strict oriented Resolution only.
let checks=0;
function ok(b,m){checks++;if(!b)throw Error(m)}
const C=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const K=a=>a.join(',');
function PHP(p,h){let out=[];for(let i=0;i<p;i++)out.push(C(Array.from({length:h},(_,j)=>i*h+j+1)));for(let j=0;j<h;j++)for(let i=0;i<p;i++)for(let k=i+1;k<p;k++)out.push(C([-(i*h+j+1),-(k*h+j+1)]));return out}
function pad(F,n){let G=[],blocks=[];for(let C0 of F){let k=3-C0.length,aux=Array.from({length:k},()=>++n),ids=[];for(let z=0;z<1<<k;z++){let c=C0.slice();for(let j=0;j<k;j++)c.push((z>>(k-j-1)&1)?aux[j]:-aux[j]);ids.push(G.length);G.push(C(c))}blocks.push({aux,ids,clause:C0})}return {G,blocks,n}}
function res(a,b,v){ok(a.includes(v)&&b.includes(-v),'pivot');let c=C([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);ok(c.every(x=>!c.includes(-x)),'taut');return c}
function proof(F,n){let P=F.map((c,i)=>({c,src:i})),live=new Map(F.map((c,i)=>[K(c),i]));for(let v=1;v<=n;v++){let plus=[],minus=[],N=new Map();for(let i of live.values()){let c=P[i].c;if(c.includes(v))plus.push(i);else if(c.includes(-v))minus.push(i);else N.set(K(c),i)}for(let a of plus)for(let b of minus){let raw=[...P[a].c.filter(x=>x!==v),...P[b].c.filter(x=>x!==-v)];if(raw.some(x=>raw.includes(-x)))continue;let c=C(raw);if(!N.has(K(c))){N.set(K(c),P.length);P.push({c,a,b,v})}}live=N;if(live.has(''))break}ok(live.has(''),'no contradiction');let seen=new Set(),todo=[live.get('')];while(todo.length){let id=todo.pop();if(seen.has(id))continue;seen.add(id);let x=P[id];if(x.src===undefined)todo.push(x.a,x.b)}let ids=[...seen].sort((a,b)=>a-b),remap=new Map(ids.map((a,i)=>[a,i]));return ids.map(i=>{let x={...P[i]};if(x.src===undefined){x.a=remap.get(x.a);x.b=remap.get(x.b)}return x})}
function verify(P,F){for(let i=0;i<P.length;i++){let x=P[i];if(x.src!==undefined){ok(K(x.c)===K(F[x.src]),'wrong original source')}else{ok(x.a<i&&x.b<i,'cycle');ok(K(x.c)===K(res(P[x.a].c,P[x.b].c,x.v)),'false inference')}}ok(P.at(-1).c.length===0,'not UNSAT')}
function lift(P,F,padobj){let {G,blocks}=padobj,Q=G.map((c,i)=>({c,src:i})),root=[];for(let b of blocks){let live=b.ids;for(let v of [...b.aux].reverse()){let nxt=[],idx=new Map(live.map(i=>[K(Q[i].c),i]));for(let i of live){if(!Q[i].c.includes(v))continue;let j=idx.get(K(C([...Q[i].c.filter(x=>x!==v),-v])));ok(j!==undefined,'padding match');let c=res(Q[i].c,Q[j].c,v);nxt.push(Q.length);Q.push({c,a:i,b:j,v})}live=nxt}ok(live.length===1&&K(Q[live[0]].c)===K(b.clause),'source not rebuilt');root.push(live[0])}let map=[];for(let x of P){if(x.src!==undefined)map.push(root[x.src]);else{let a=map[x.a],b=map[x.b];ok(K(res(Q[a].c,Q[b].c,x.v))===K(x.c),'replay');map.push(Q.length);Q.push({c:x.c,a,b,v:x.v})}}verify(Q,G);return Q}
function truth(F,mask){return F.every(c=>c.some(z=>((mask>>(Math.abs(z)-1))&1)===(z>0?1:0)))}
let F=PHP(4,3),P=proof(F,12),B=pad(F,12),Q=lift(P,F,B);verify(P,F);ok(F.length===22&&P.filter(x=>x.src===undefined).length===43,'old bound');ok(B.G.length===40&&B.n===30&&Q.filter(x=>x.src===undefined).length===61,'new bound');ok(B.G.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'not proper 3');
let pruned=B.G.map(c=>{for(let z of c){if(Math.abs(z)<=12)continue;if(z<0)return null}return c.filter(z=>Math.abs(z)<=12)}).filter(c=>c!==null);
ok(K(pruned.map(K))===K(F.map(K)),'wrong restricted source');
let S=PHP(3,3),T=pad(S,9),sat=0;for(let mask=0;mask<(1<<18);mask++){let v=truth(S,mask&511);if(v)sat++;ok(truth(T.G,mask)===v,'SAT control')}ok(sat>0,'SAT disappeared');
let threw=false;try{res([1],[-1],2)}catch(e){threw=true}ok(threw,'bad pivot accepted');
console.log(JSON.stringify({status:'PASS',checks,original_clauses:F.length,original_paid:43,strict3_clauses:B.G.length,strict3_paid:61,SAT_truth_table:1<<18,corrupted_pivot_rejected:true}));
