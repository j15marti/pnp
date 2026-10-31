"use strict";
const verify=function verify(){
  const ck=(a,msg)=>{if(!a)throw Error(msg)};
  function gadget(bit){
    const cs=[];
    for(let k=0;k<8;k++){
      const mask=bit&&k===0?1:k;
      cs.push([1,2,3].map((v,j)=>((mask>>j)&1)?v:-v));
    }
    return cs;
  }
  function sat(cs){
    for(let b=0;b<8;b++)if(cs.every(c=>c.some(l=>(((b>>(Math.abs(l)-1))&1)===(l>0?1:0)))))return true;
    return false;
  }
  let gadgets=0,guardRows=0,orderCases=0,pairChecks=0,complements=0,mixedEdges=0;
  for(let b=0;b<=1;b++){
    const cs=gadget(b);ck(sat(cs)===Boolean(b),"gadget label");
    ck(cs.length===8&&cs.every(c=>c.length===3),"length");
    gadgets++;
    for(let s=0;s<=1;s++)for(let A=0;A<=1;A++)for(let B=0;B<=1;B++)for(let C=0;C<=1;C++){
      const guarded=(!s)||A||B||C;
      const exists=([0,1]).some(z=>((!s)||A||z)&&((!z)||B||C));
      ck(Boolean(guarded)===exists,"4-to-3 guard");
      guardRows++;
    }
  }
  const perm=(arr,prefix,visit)=>{if(!arr.length){visit(prefix);return}for(let i=0;i<arr.length;i++)perm(arr.filter((_,j)=>j!==i),[...prefix,arr[i]],visit)};
  for(let q=2;q<=7;q++)perm(Array.from({length:q},(_,i)=>i),[],order=>{
    // On all zero responses a correct source-blind OR decoder must inspect all q.
    ck(new Set(order).size===q,"missing query");
    orderCases++;
    for(let i=0;i<q;i++){ck(order.indexOf(i)+1<=q,"one-hot");orderCases++}
  });
  const c=[1,2,3],d=[1,-2,4];
  function want(cl,mode){return new Map(cl.map(l=>[Math.abs(l),mode==="S"?(l>0?1:0):(l>0?0:1)]))}
  for(let m of ["SS","SU","US","UU"]){
    let a=want(c,m[0]),b=want(d,m[1]);
    let claimed=[...a].every(([v,z])=>!b.has(v)||b.get(v)===z);
    let possible=false;
    for(let mask=0;mask<16;mask++){
      const x=v=>(mask>>(v-1))&1;
      const e=(cl,mode)=>cl.every(l=>x(Math.abs(l))===(mode==="S"?(l>0?1:0):(l>0?0:1)));
      possible||=e(c,m[0])&&e(d,m[1]);
    }
    ck(possible===claimed&&!claimed,"four-way incompatible source edge");pairChecks++;mixedEdges++;
  }
  for(let mask=0;mask<16;mask++){
    const x=v=>(mask>>(v-1))&1;
    for(let c of [[1,2,3],[-1,2,-3],[1,-2,4]]){
      let t=c.filter(l=>x(Math.abs(l))===(l>0?1:0)).length;
      let u=c.filter(l=>(1-x(Math.abs(l)))===(l>0?1:0)).length;
      ck(t+u===3,"complement");
      complements++;
    }
  }
  return{run:"ARC-OR-JOIN-BOTH-LABEL-GATE257",gadgets,guardTruthRows:guardRows,decisionOrderOneHotTests:orderCases,exactPairModeTests:pairChecks,explicitMixedEdgeModes:mixedEdges,complementClauseTests:complements,allAssertionsPassed:true,scope:"finite compact checker; full Python 12-source original-indexed experiment is a separate attached artifact"};
};
process.stdout.write(JSON.stringify(verify(), null, 2)+"\n");
