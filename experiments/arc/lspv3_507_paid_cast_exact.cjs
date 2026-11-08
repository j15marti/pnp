#!/usr/bin/env node
"use strict";
/* LSPV-3/507. Distinct fixed typed calculus R_CAST507(w), NOT historical R_mix341.
   Generate original odd-charge cubic Tseitin strict 3-CNF, replace one clause,
   authenticate each RES and paid CAST, then AND3 and GF(2) proof DAG.
   Usage: node experiments/arc/lspv3_507_paid_cast_exact.cjs
*/
const assert=(b,msg)=>{if(!b)throw Error(msg||"assertion failed")};
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const evalClause=(c,a)=>c.some(x=>a[Math.abs(x)-1]===(x>0));
const graphs={
  K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
  K33:[6,Array.from({length:9},(_,k)=>[Math.floor(k/3),3+k%3])],
  cube:[8,Array.from({length:8},(_,i)=>Array.from({length:8},(_,j)=>[i,j])).flat()
    .filter(([i,j])=>i<j && (((i^j)&((i^j)-1))===0))]
};
function make(name,replace=0,odd=true){
  const [h,edges]=graphs[name], n=edges.length; assert(2*n===3*h);
  const origin=[],groups=[];
  for(let v=0;v<h;v++){
    const ids=edges.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
    assert(ids.length===3);let row=[];
    for(let b=0;b<8;b++){
      const bits=[b&1,(b>>1)&1,(b>>2)&1];
      if(((bits[0]+bits[1]+bits[2])&1)!==(odd&&v===0?1:0)){
        row.push(origin.length);
        origin.push(norm(ids.map((x,j)=>bits[j]?-x:x)));
      }
    }
    assert(row.length===4);groups.push(row);
  }
  const C=origin[replace], [a,b,c]=C,u=n+1,z=n+2;
  const A=norm([a,b,u]),B=norm([-u,c,z]),D=norm([-u,c,-z]);
  const source=[],sourceIndex=[];
  for(let j=0;j<origin.length;j++){
    if(j===replace){sourceIndex.push(source.length);source.push(A,B,D)}
    else{sourceIndex.push(source.length);source.push(origin[j])}
  }
  return {name,h,n,origin,groups,source,sourceIndex,C,u,z,A,B,D};
}
function proof(d,w){
  const nodes=d.source.map((clause,id)=>({id,kind:"SOURCE",clause,cost:0}));
  const emit=(kind,parents,fields={})=>{
    const id=nodes.length;nodes.push({id,kind,parents,cost:kind==="CAST"?w:1,...fields});return id;
  };
  const iB=d.source.findIndex(c=>eq(c,d.B)),iD=d.source.findIndex(c=>eq(c,d.D)),
    iA=d.source.findIndex(c=>eq(c,d.A));
  assert(iB>=0 && iD>=0 && iA>=0);
  const r1=emit("RES",[iB,iD],{pivot:d.z,clause:norm([-d.u,d.C[2]])});
  const r2=emit("RES",[iA,r1],{pivot:d.u,clause:d.C});
  const cast=emit("CAST",[r2],{clause:d.C});
  let rows=[];
  for(let v=0;v<d.h;v++){
    const ids=d.groups[v].map(j=>j===d.sourceIndex.length-1?
      d.sourceIndex[j]:j===d.origin.indexOf(d.C)?cast:d.sourceIndex[j]);
    let p=ids[0];
    for(let i=1;i<ids.length;i++)p=emit("AND3",[p,ids[i]]);
    rows.push(p);
  }
  let root=rows[0];
  for(let j=1;j<rows.length;j++)root=emit("XOR",[root,rows[j]]);
  return {nodes,root};
}
function check(d,pr,w){
  const {nodes,root}=pr,m=d.source.length;
  const record=[],depth=[],leafIds=new Set(), costs=[], ancestors=new Set();
  for(let i=0;i<nodes.length;i++){
    const t=nodes[i];assert(t.id===i);
    if(t.kind==="SOURCE"){
      assert(i<m && t.cost===0 && eq(t.clause,d.source[i]));
      record[i]={type:"factor",clause:t.clause,vars:new Set(t.clause.map(x=>Math.abs(x)))};
      depth[i]=0;continue;
    }
    assert(i>=m && t.parents.every(j=>Number.isInteger(j) && j>=0 && j<i));
    const ps=t.parents.map(j=>record[j]),kind=t.kind;
    costs.push(t.cost);depth[i]=t.cost+Math.max(...t.parents.map(j=>depth[j]));
    if(kind==="RES"){
      assert(ps.length===2 && t.cost===1 && t.pivot>0);
      const p=t.pivot,L=ps[0].clause,R=ps[1].clause;
      assert(ps.every((x,j)=>x.type==="clause"||nodes[t.parents[j]].kind==="SOURCE"));
      assert(L.includes(p)&&R.includes(-p)||L.includes(-p)&&R.includes(p));
      const C=norm([...L,...R].filter(x=>Math.abs(x)!==p));
      assert(!C.some(x=>C.includes(-x)) && eq(t.clause,C));
      record[i]={type:"clause",clause:C};
    }else if(kind==="CAST"){
      assert(ps.length===1 && t.cost===w && nodes[t.parents[0]].kind==="RES");
      assert(eq(t.clause,ps[0].clause));
      let vars=new Set(t.clause.map(x=>Math.abs(x)));
      assert(vars.size<=3 && [...vars].every(x=>x>=1&&x<=d.n));
      record[i]={type:"factor",clause:t.clause,vars};
    }else if(kind==="AND3"){
      assert(ps.length===2 && t.cost===1 && ps.every(x=>x.type==="factor"));
      let vars=[...new Set(ps.flatMap(x=>[...x.vars]))].sort((a,b)=>a-b);
      assert(vars.length<=3 && vars.every(x=>x<=d.n));
      let tbl=[];
      for(let mask=0;mask<1<<vars.length;mask++){
        let ass=Array(d.n+2).fill(false);vars.forEach((v,j)=>ass[v-1]=!!(mask&(1<<j)));
        let val=ps.every(x=>x.table?
          x.table.get([...x.vars].sort((a,b)=>a-b).map(v=>+ass[v-1]).join("")):
          evalClause(x.clause,ass));
        tbl.push({ass,val});
      }
      let table=new Map(tbl.map(z=>[vars.map(v=>+z.ass[v-1]).join(""),z.val]));
      let row=null;
      if(vars.length===3){
        for(let b=0;b<=1;b++){
          if(tbl.every(z=>z.val===(vars.reduce((q,v)=>q+(z.ass[v-1]?1:0),0)%2===b)))
            row={mask:vars.reduce((q,v)=>q^(1n<<BigInt(v-1)),0n),rhs:b};
        }
      }
      record[i]={type:"factor",vars:new Set(vars),table,row};
    }else if(kind==="XOR"){
      assert(ps.length===2 && t.cost===1 && ps.every(x=>x.row));
      record[i]={type:"row",row:{mask:ps[0].row.mask^ps[1].row.mask,
        rhs:ps[0].row.rhs^ps[1].row.rhs}};
    }else throw Error("unknown inference "+kind);
  }
  assert(record[root].row && record[root].row.mask===0n && record[root].row.rhs===1);
  let stack=[root];while(stack.length){let j=stack.pop();
    if(ancestors.has(j))continue;ancestors.add(j);
    for(let parent of nodes[j].parents||[])stack.push(parent);
  }
  assert(ancestors.size===nodes.length);
  for(let j=0;j<m;j++)assert(ancestors.has(j));
  const numBin=nodes.filter(t=>["RES","AND3","XOR"].includes(t.kind)).length,
    numCast=nodes.filter(t=>t.kind==="CAST").length,weight=costs.reduce((a,b)=>a+b,0);
  assert(numBin===m-1 && numCast===1 && weight===m-1+w);
  return {graph:d.name,m,weight,binary:numBin,casts:numCast,span:depth[root],
    packet_bytes:Buffer.byteLength(JSON.stringify(nodes))};
}
function models(clauses,n,max=1){
  let got=[];for(let mask=0;mask<(1<<n);mask++){
    let a=Array.from({length:n},(_,j)=>!!(mask&(1<<j)));
    if(clauses.every(c=>evalClause(c,a))){got.push(mask);if(got.length>=max)break}
  }return got;
}
function run(){
  const result={model:"R_CAST507(w) distinct from historical R_mix341",proofs:[],
    corrupt_rejected:0,deletion_controls:0,odd_unsat:0,even_sat:0};
  for(const name of Object.keys(graphs))for(const replace of [0,1,3]){
    let d=make(name,replace,true),even=make(name,replace,false);
    assert(!models(d.source,d.n+2).length);result.odd_unsat++;
    assert(models(even.source,even.n+2).length);result.even_sat++;
    for(let j=0;j<d.source.length;j++)if(name!=="cube" || [0,1,2,d.source.length-1].includes(j)){
      assert(models(d.source.filter((_,k)=>k!==j),d.n+2).length);result.deletion_controls++}
    for(const w of [1,2,4]){
      const pr=proof(d,w);result.proofs.push({...check(d,pr,w),replace,cast_weight:w});
      const bad=JSON.parse(JSON.stringify(pr));
      const k=bad.nodes.findIndex(n=>n.kind==="CAST");
      bad.nodes[k].clause=[123456];
      try{check(d,bad,w);throw Error("CORRUPT ACCEPTED")}
      catch(e){assert(e.message!=="CORRUPT ACCEPTED");result.corrupt_rejected++}
    }
  }
  return result;
}
if(require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
module.exports={make,proof,check,run};