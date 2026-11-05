#!/usr/bin/env node
"use strict";
/* LSPV-3/429 compact independent structural test. Node >=16, no dependencies.
   Complete full 4-case source/witness fixtures and independent check: local ZIP.
   This reproducer rebuilds K4 and bridged-pair signed original 3-CNFs, checks
   original / unique essential core UNSAT with complete DPLL, and one-deletion SAT. */
const assert=require("assert");
function k4(){return [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];}
function bridgedPair(){
  let edges=[];
  for(let off of [0,5]){
    for(let [u,v] of k4()){
      if(u===0&&v===1){edges.push([u+off,4+off],[4+off,v+off]);}
      else edges.push([u+off,v+off]);
    }
  }
  edges.push([4,9]);return edges;
}
function components(n,edges,removed){
  const adj=Array.from({length:n},()=>[]);
  for(const [a,b] of edges){if(a===removed||b===removed)continue;adj[a].push(b);adj[b].push(a);}
  const seen=new Set([removed]),out=[];
  for(let i=0;i<n;i++)if(!seen.has(i)){
    const st=[i],s=[];seen.add(i);
    while(st.length){let a=st.pop();s.push(a);for(let b of adj[a])if(!seen.has(b)){seen.add(b);st.push(b);}}
    out.push(s);
  }return out;
}
function build(n,edges){
  const adj=Array.from({length:n},()=>[]);
  edges.forEach(([a,b],i)=>{adj[a].push(i);adj[b].push(i);});
  adj.forEach(xs=>assert.strictEqual(xs.length,3));
  const charge=Array(n).fill(0);charge[0]=1;
  const clauses=[],essential=[];
  for(let v=0;v<n;v++){
    const parts=components(n,edges,v);
    for(let a=0;a<8;a++){
      const bits=[0,1,2].map(i=>(a>>i)&1);
      if((bits[0]^bits[1]^bits[2])===charge[v])continue;
      const clause=adj[v].map((e,i)=>bits[i]?-(e+1):e+1);
      const ess=parts.every(H=>{
        let boundary=0;
        for(let i=0;i<3;i++){
          const [p,q]=edges[adj[v][i]];
          if(H.includes(p===v?q:p))boundary^=bits[i];
        }
        const rhs=H.reduce((p,u)=>p^charge[u],0);
        return boundary===rhs;
      });
      clauses.push(clause);if(ess)essential.push(clause);
    }
  }return {clauses,essential};
}
function sat(clauses,assignment,vars){
  let arr=clauses.map(c=>c.slice()),a=assignment.slice();
  function walk(cs,asg){
    while(true){
      let unit=null,rem=[];
      for(const c of cs){
        const free=[];let yes=false;
        for(const lit of c){
          const v=asg[Math.abs(lit)-1];if(v===-1)free.push(lit);
          else if((v===1)===(lit>0)){yes=true;break;}
        }
        if(yes)continue;if(!free.length)return false;
        if(free.length===1){unit=free[0];break;}rem.push(free);
      }
      if(unit!==null){asg[Math.abs(unit)-1]=unit>0?1:0;continue;}
      if(!rem.length)return true;
      const lit=rem[0][0],ix=Math.abs(lit)-1;
      for(const bit of [0,1]){const b=asg.slice();b[ix]=bit;if(walk(rem,b))return true;}
      return false;
    }
  }
  return walk(arr,a);
}
function run(n,edges,expected){
  const {clauses,essential}=build(n,edges),vars=edges.length;
  assert.strictEqual(clauses.length,4*n);assert.strictEqual(essential.length,expected);
  assert.strictEqual(sat(clauses,Array(vars).fill(-1),vars),false);
  assert.strictEqual(sat(essential,Array(vars).fill(-1),vars),false);
  for(let i=0;i<essential.length;i++){
    assert.strictEqual(sat(essential.filter((_,j)=>j!==i),Array(vars).fill(-1),vars),true);
  }
  return {vertices:n,vars,clauses:clauses.length,essential:essential.length,deleted:clauses.length-essential.length};
}
const results=[run(4,k4(),16),run(10,bridgedPair(),36)];
process.stdout.write(JSON.stringify({status:"PASS",scope:"K4 and bridged pair, independent compact reconstruction",results},null,2)+"\n");
