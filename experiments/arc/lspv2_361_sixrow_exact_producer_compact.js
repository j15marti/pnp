"use strict";
// LSPV-2 361 compact public exact-producer, no dependencies.
const produce=function produce(){
  const names=["x","y","z","u","v","a","b","c","d"];
  const rows=[[["x","y","z"],1],[["x","u","v"],0],[["y","u","v"],0],[["a","b","c"],0],[["a","b","d"],0],[["c","d","z"],0]];
  const norm=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:0)-(b<0?1:0));
  const source=[];
  for(let ri=0;ri<rows.length;ri++){
    const [vars,rhs]=rows[ri];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
      if((a^b^c)===rhs)continue;
      const ls=norm(vars.map((s,j)=>(names.indexOf(s)+1)*([a,b,c][j]?-1:1)));
      source.push({id:"s"+source.length,row:ri,lits:ls,wrong:[a,b,c]});
    }
  }
  const raw=[
   ["s6","s8",5],["s7","s9",-5],["n0","n1",4],
   ["s4","s10",-5],["s5","s11",5],["n3","n4",4],
   ["s0","n2",1],["s3","n5",-1],["n6","n7",2],
   ["s12","s17",7],["s15","s18",-7],["n9","n10",6],
   ["s13","s16",-7],["s14","s19",7],["n12","n13",6],
   ["s20","n11",8],["s23","n14",-8],["n15","n16",9],["n8","n17",3]
  ];
  const map=new Map(source.map(s=>[s.id,s.lits]));
  const nodes=raw.map(([l,r,p],i)=>{
    const a=map.get(l),b=map.get(r);
    if(!a.includes(p)||!b.includes(-p))throw Error("bad input "+i);
    const ls=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
    if(ls.some(x=>ls.includes(-x)))throw Error("tautology "+i);
    const id="n"+i;map.set(id,ls);
    return {id,rule:"RES",parents:[l,r],pivot:p,lits:ls};
  });
  if(map.get("n18").length!==0)throw Error("not contradiction");
  const clauses=source.map(s=>s.lits);
  const sat=(cs,skip=-1,flip=-1,k=-1)=>{
    for(let a=0;a<512;a++){
      let good=true;
      for(let i=0;i<cs.length;i++){
        if(i===skip)continue;
        if(!cs[i].some((lit,j)=>{
          const v=i===flip&&j===k?-lit:lit;
          return !!((a>>(Math.abs(v)-1))&1)===(v>0);
        })){good=false;break;}
      }
      if(good)return a;
    }
    return null;
  };
  if(sat(clauses)!==null)throw Error("source SAT");
  const deletions=clauses.map((c,i)=>sat(clauses,i));
  const essential=deletions.flatMap((x,i)=>x===null?[]:[i]);
  if(essential.length!==20)throw Error("essentiality");
  const flipped=clauses.map((c,i)=>c.map((x,j)=>sat(clauses,-1,i,j)));
  const core=essential.map(i=>clauses[i]);
  if(sat(core)!==null)throw Error("core SAT");
  const good=source.map(s=>({lits:s.lits})); // regenerate opposite-charge from rows, independently enumerate
  let opposite=0;
  for(let bits=0;bits<512;bits++){
    if(rows.every(([vars,rhs],i)=>vars.reduce((v,x)=>v^((bits>>names.indexOf(x))&1),0)===(rhs^(i===0?1:0))))opposite++;
  }
  if(opposite!==16)throw Error("opposite control");
  const dimacs=(cs)=>"p cnf 9 "+cs.length+"\n"+cs.map(cl=>cl.join(" ")+" 0\n").join("");
  return {id:"LSPV2_SIXROW_RES_CORE_EXACT361",calculus:"Rmix341 (strict RES subsystem only)",
    source:{names,rows:rows.map(([vars,rhs])=>({vars,rhs})),dimacs:dimacs(clauses),core_dimacs:dimacs(core),clauses:source},
    proof:{root:"n18",nodes,cost:19},
    controls:{deletionWitnesses:deletions,flipWitnesses:flipped,essentialIndices:essential,redundantIndices:deletions.flatMap((v,i)=>v===null?[i]:[]),oppositeRhsModels:opposite},
    accounting:{sourceBytes:dimacs(clauses).length,coreBytes:dimacs(core).length,nodes:19,freeChoice:true,searchSeparate:true}};
};
if(typeof module!=="undefined"&&module.exports)module.exports={produce};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(produce()));
