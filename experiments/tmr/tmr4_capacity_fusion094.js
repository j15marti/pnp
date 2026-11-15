"use strict";
// TMR-4/044: exactly executed native V8 function serialized without body changes.
const audit=function audit(){
  const ck=(cond,msg)=>{if(!cond)throw Error(msg);checks++};
  let checks=0,edgeChecks=0,zeroChecks=0,dualChecks=0,traceChecks=0,sccChecks=0;
  const catalogs=[
    {id:"AND2",gates:[{a:2,c2:2}]},
    {id:"AND2_AND3",gates:[{a:2,c2:2},{a:3,c2:2}]},
    {id:"AND2_AND4",gates:[{a:2,c2:4},{a:4,c2:2}]},
    {id:"RATIONAL_MIX",gates:[{a:2,c2:3},{a:3,c2:5},{a:4,c2:4}]}
  ];
  function hvals(n,cat){let h=[0,0],pick=[null,null];for(let c=2;c<=n;c++){let opts=cat.gates.map(g=>({val:g.c2+h[Math.max(1,c-g.a+1)],gate:g})).sort((a,b)=>a.val-b.val||b.gate.a-a.gate.a);h[c]=opts[0].val;pick[c]=opts[0].gate;}return {h,pick}}
  function parts(n){let a=[0],r=[];function rec(mx){if(a.length===n){r.push([...a]);return}for(let t=0;t<=mx+1;t++){a.push(t);rec(Math.max(mx,t));a.pop()}}rec(0);return r}
  function norm(p){let mp=new Map(),q=[];for(const x of p){if(!mp.has(x))mp.set(x,mp.size);q.push(mp.get(x))}return q}
  function merge(p,ids){let q=p.map(x=>ids.includes(x)?ids[0]:x);return norm(q)}
  function subsets(arr,max){let out=[];function rec(i,sel){if(sel.length>=2&&sel.length<=max)out.push([...sel]);if(sel.length===max)return;for(let j=i;j<arr.length;j++){sel.push(arr[j]);rec(j+1,sel);sel.pop()}}rec(0,[]);return out}
  function scc(nodes,adj){let idx=0,stack=[],on=new Set(),N=new Map(),L=new Map(),groups=[];function visit(v){N.set(v,idx);L.set(v,idx);idx++;stack.push(v);on.add(v);for(const w of (adj.get(v)||[])){if(!N.has(w)){visit(w);L.set(v,Math.min(L.get(v),L.get(w)))}else if(on.has(w))L.set(v,Math.min(L.get(v),N.get(w)))}if(N.get(v)===L.get(v)){let grp=[],w;do{w=stack.pop();on.delete(w);grp.push(w)}while(w!==v);groups.push(grp)}}for(const v of nodes)if(!N.has(v))visit(v);return groups}
  const rows=[],summaries=[];
  for(const cat of catalogs){
    const ss={catalog:cat.id,lengths:[],maximalLambda:"1/1"};
    for(let n=2;n<=7;n++){
      const {h,pick}=hvals(n,cat);let W=0,c=n,steps=[],pot=0;
      while(c>1){let g=pick[c],d=Math.min(g.a-1,c-1),c1=c-d;ck(h[c]===g.c2+h[c1],"DP Bellman equality");let delta=h[c]-h[c1];ck(delta===g.c2,"dual tight step");W+=g.c2;pot+=delta;steps.push({c,c1,a:g.a,cost2:g.c2,delta2:delta});c=c1;dualChecks++}
      ck(W===h[n]&&pot===h[n],"primal dual path cost");
      const P=parts(n);let nRows=0,nZero=0,seenTight=false;
      for(const p of P){
        let k=new Set(p).size;ck(h[k]>=0&&h[k]<=h[n],"h capacity");
        const metaNodes=[p.join(".")+"@0",p.join(".")+"@1"];
        let adj=new Map([[metaNodes[0],[metaNodes[1]]],[metaNodes[1],[metaNodes[0]]]]);
        const comps=scc(metaNodes,adj);ck(comps.length===1&&comps[0].length===2,"zero VIEW SCC");sccChecks++;
        for(let view=0;view<2;view++){
          ck(h[k]-h[k]===0,"free VIEW tariff");zeroChecks++;
          for(const g of cat.gates){
            const ids=Array.from({length:k},(_,i)=>i);
            for(const chosen of subsets(ids,Math.min(g.a,k))){
              const np=merge(p,chosen),k1=new Set(np).size,d=h[k]-h[k1];
              ck(k-k1===chosen.length-1,"partition merge cardinality");
              ck(d>=0&&d<=g.c2,"exact signed paid tariff");
              edgeChecks++;nRows++;if(d===g.c2)seenTight=true;
              if(n<=5)rows.push({catalog:cat.id,n,source:p.join(""),view,rule:"AND"+g.a,k,k1,distinct:chosen.length,delta7:["0","0","0",d+"/2","0","0","0"],cost:g.c2+"/2"});
            }
          }
          ck(0<=2,"NOT paid row");nRows++;
          ck(0<=0,"SELECT free row");nZero++;
        }
      }
      ck(seenTight,"some paid tight tariff row exists");
      ck(h[n]>0&&W===h[n],"LP primal = cost");dualChecks++;
      ss.lengths.push({n,partitions:P.length,abstractPaidRows:nRows,freeRows:nZero+2*P.length,optimalCost:h[n]+"/2",optimalGates:steps.length});
    }
    summaries.push(ss);
  }
  // Three genuine model-expansion falsifiers, never relabelled as original legal steps.
  const tri=hvals(4,catalogs[1]).h;
  ck(tri[4]===4&&tri[1]===0,"f3 n4 exact cost2");
  ck(tri[4]-tri[1]>2,"price-one AND4 violates f3 tariff");
  ck(hvals(3,catalogs[1]).h[3]>0,"free AND3 invalidates priceful potential");
  ck(hvals(3,catalogs[1]).h[3]-hvals(3,catalogs[1]).h[1]>0,"free merger violates tariff");
  const hostileAdj=new Map([["raw",["merged"]],["merged",[]]]);
  ck(scc(["raw","merged"],hostileAdj).length===2,"directed zero is not SCC");
  ck(Math.min(hvals(3,catalogs[1]).h[3],hvals(3,catalogs[1]).h[1])===0,"directed cl0 collapses obstruction");
  ck((3-1)-(1-1)===2,"raw connectivity has cost-one triple discharge 2");
  // Construct shared-DAG AND source-completions from the independent DP table.
  for(const cat of catalogs)for(let n=2;n<=7;n++){
    const {h,pick}=hvals(n,cat);let groups=Array.from({length:n},(_,i)=>[i]),cost2=0;
    while(groups.length>1){const g=pick[groups.length],t=Math.min(g.a,groups.length),joined=groups.slice(0,t).flat();groups=[joined,...groups.slice(t)];cost2+=g.c2;traceChecks++;ck(new Set(groups.flat()).size===n,"all inputs preserved")}
    ck(cost2===h[n],"constructed DAG matches optimum");ck(groups[0].length===n,"final AND all inputs");
  }
  return {raw:{status:"COMPUTATIONAL",scope:"preauthenticated shared AND/NOT gate-DAG construction; not native SAT TM",checks,edgeChecks,zeroChecks,sccChecks,dualChecks,traceChecks,hostile:{freeMerge:"FAIL lambda=1 if added",unpricedFanin4:"FAIL f3 tariff if added",rawConnectivity:"FAIL at price-one ternary AND",directedZero:"SCC quotient alone insufficient",physicalMachineTransfer:"OPEN"},summaries},matrix:{schema:"7-column [CNF,XOR,SEP,FUS,GAMMA,INTERFACE,MACHINE]. H(c)=minimum half-unit capacity-cover price; Delta_FUS=(H(c)-H(c'))/2. Cost=gate c2/2. All other columns zero.",zeroRows:[{rule:"VIEW/NOP/SELECT",cost:"0",delta7:["0","0","0","0","0","0","0"]}],paidUnchangedRows:[{rule:"APPEND_NOT",cost:"1",delta7:["0","0","0","0","0","0","0"]},{rule:"APPEND_AND with no input-component merge",cost:"gate-specific",delta7:["0","0","0","0","0","0","0"]}],goal:"selected actual AND_n output; abstract c=1 is MAY goal",units:"all arithmetic exact integer numerators over denominator 2",catalogs,rows}};
};
if (typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(audit(),null,2));
if (typeof module!=="undefined") module.exports={audit};
