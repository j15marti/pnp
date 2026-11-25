// node supplement.js BS19_results.json BS20_results.json
function supplement(bs,peer){
 const v=l=>Math.abs(l),s=l=>+(l<0),ok=(C,A)=>C.every(c=>c.some(l=>(A[v(l)]^s(l))!==(A[v(c[0])]^s(c[0]))));
 const raw=bs.source.O.map(o=>o.t.map(x=>x+1)),K=bs.common.find(x=>x.K===16).residual,A={...peer.wide.gauge.firstWitness};
 let checks=0;function ck(b){checks++;if(!b)throw Error("supplement")}
 ck(ok(K.C,A));for(let {v:x,bucket} of K.log.slice().reverse()){let needs=new Set();for(let c of bucket){let z=c.map(l=>A[v(l)]^s(l));if(z.every(b=>b===z[0]))needs.add(z[0]^1)}ck(needs.size<=1);A[x]=needs.size?[...needs][0]:0}
 ck(ok(raw,A));let word=Object.entries(A).reduce((r,[x,b])=>r+b*2**(+x-1),0);ck(word===peer.wide.sourceLift);
 let adj=Array.from({length:25},()=>new Set()),edges=new Set();for(let c of raw)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=c[i],b=c[j];adj[a].add(b);adj[b].add(a);edges.add([a,b].sort((a,b)=>a-b).join(","))}
 let Q=[1],seen=new Set(Q);for(let j=0;j<Q.length;j++)for(let x of adj[Q[j]])if(!seen.has(x)){seen.add(x);Q.push(x)}ck(seen.size===24&&edges.size===96&&raw.length===32);
 // Triangle as planar graph, four forbidden complementary sign pairs. Remove one for a SAT control.
 let pair=[];for(let remove of [-1,0,1,2,3]){let C=Array.from({length:4},(_,i)=>[1,i&1?-2:2,i&2?-3:3]).filter((_,i)=>i!==remove);let models=0,min=Infinity;
 for(let w=0;w<8;w++){let a=Object.fromEntries([1,2,3].map(x=>[x,(w>>(x-1))&1]));let bad=C.filter(c=>!ok([c],a)).length;min=Math.min(min,bad);if(!bad)models++}
 let cost=Infinity;for(let z=0;z<8;z++){let b=[z&1,(z>>1)&1,(z>>2)&1];if(b[0]^b[1]^b[2])continue;let t=0;for(let c of C)for(let [k,[i,j]] of [[0,[0,1]],[1,[1,2]],[2,[0,2]]])t+=+(b[k]===(s(c[i])^s(c[j])));cost=Math.min(cost,t)}
 ck(cost===C.length+2*min);ck((remove<0&&models===0)||(remove>=0&&models===2));pair.push({remove,models,minViolation:min,dualCost:cost});
 }return{checks,sourceLift:word,reverseLogs:K.log.length,connected:seen.size,edges:edges.size,pair};
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('fs');console.log(JSON.stringify(supplement(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2))}
